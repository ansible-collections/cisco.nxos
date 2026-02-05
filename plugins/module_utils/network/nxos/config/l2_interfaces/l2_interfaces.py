#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_l2_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.l2_interfaces import (
    L2_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    generate_switchport_trunk,
    normalize_interface,
    vlan_list_to_range,
    vlan_range_to_dict,
)


class L2_interfaces(ResourceModule):
    """
    The nxos_l2_interfaces config class
    """

    def __init__(self, module):
        super(L2_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2_interfaces",
            tmplt=L2_interfacesTemplate(),
        )
        self.parsers = [
            "mode",
            "access.vlan",
            "trunk.native_vlan",
            "trunk.allowed_vlans_none",
            "beacon",
            "link_flap.error_disable",
            "cdp_enable",
            "no_cdp_enable",
        ]

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = {entry["name"].lower(): entry for entry in self.want}
        haved = {entry["name"].lower(): entry for entry in self.have}

        for each in wantd, haved:
            self.process_list_attrs(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the L2_interfaces network resource.
        """
        begin = len(self.commands)
        want_without_name = want.copy()
        want_without_name.pop("name", None)
        pre_pop_want = bool(want_without_name)
        want_cdp = want.pop("cdp_enable", None)
        have_cdp = have.pop("cdp_enable", None)
        self.handle_cdp(want_cdp, have_cdp, "cdp_enable", pre_pop_want)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_lists(want, have)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def _compare_lists(self, want, have):
        """Compare list attributes for trunk allowed vlans.

        want_set: VLANs that should be present on the appliance
        have_set: VLANs that are currently on the appliance
        """
        want_set = set(want.get("trunk", {}).get("allowed_vlans", {}))
        have_set = set(have.get("trunk", {}).get("allowed_vlans", {}))

        if self.state == "deleted" and have_set:
            # For deleted state, remove all trunk allowed vlans if any exist
            if have_set:
                self.commands.append("no switchport trunk allowed vlan")
            return

        if self.state in ("merged", "rendered"):
            # Merged/rendered: only ADD vlans, never remove
            # Add vlans that are in want but not in have
            vlans_to_add = want_set - have_set
            if vlans_to_add:
                self.commands.extend(
                    generate_switchport_trunk(
                        "allowed",
                        True,
                        vlan_list_to_range(sorted(vlans_to_add, key=int)),
                    ),
                )
            return

        if self.state in ("replaced", "overridden"):
            # Replaced/overridden: make device match want_set exactly
            # Remove vlans that are in have but not in want
            vlans_to_remove = have_set - want_set
            # Add vlans that are in want but not in have
            vlans_to_add = want_set - have_set

            if not want_set and have_set:
                # Want is empty but have has vlans - remove all
                self.commands.append("no switchport trunk allowed vlan")
            elif vlans_to_remove:
                # Remove excess vlans first
                self.commands.append(
                    f"switchport trunk allowed vlan remove {vlan_list_to_range(sorted(vlans_to_remove, key=int))}",
                )

            if vlans_to_add:
                # Add missing vlans
                self.commands.extend(
                    generate_switchport_trunk(
                        "allowed",
                        True,
                        vlan_list_to_range(sorted(vlans_to_add, key=int)),
                    ),
                )

    def process_list_attrs(self, param):
        if param:
            for _k, val in param.items():
                val["name"] = normalize_interface(val["name"])
                if val.get("trunk"):
                    for vlan in ["allowed_vlans"]:
                        vlanList = val.get("trunk").get(vlan, [])
                        if vlanList and vlanList != "none":
                            val["trunk"][vlan] = vlan_range_to_dict(val.get("trunk").get(vlan))

    def handle_cdp(self, want_cdp, have_cdp, parser, want):
        if want_cdp is None and have_cdp is None:
            if self.state == "replaced" or (self.state == "overridden" and want):
                self.addcmd({parser: True}, parser, True)
        else:
            if want_cdp is True and have_cdp is False:
                self.addcmd({parser: want_cdp}, parser, not want_cdp)
            elif want_cdp is False and have_cdp is None:
                self.addcmd({parser: not want_cdp}, parser, not want_cdp)
            elif want_cdp is None and have_cdp is False:
                if self.state in ["overridden", "deleted"] and not want:
                    self.addcmd({parser: not have_cdp}, parser, have_cdp)
