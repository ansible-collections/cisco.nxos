# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_nve_interface config file.
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.nve_interface import (
    Nve_interfaceTemplate,
)


class Nve_interface(ResourceModule):
    """
    The nxos_nve_interface config class
    """

    def __init__(self, module):
        super(Nve_interface, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="nve_interface",
            tmplt=Nve_interfaceTemplate(),
        )
        self.parsers = [
            "description",
            "host_reachability_bgp",
            "advertise_virtual_rmac",
            "source_interface_name",
            "source_interface_hold_time",
            "global_ingress_replication_bgp",
            "global_suppress_arp",
            "multisite_interface",
        ]

    def execute_module(self):
        """Execute the module"""
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self.want
        haved = self.have

        # If state is 'merged', merge want onto have before compare.
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # If state is 'deleted', remove the NVE interface.
        if self.state == "deleted":
            if self.have:
                self.commands.append("no interface nve1")
            return

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Nve_interface network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_vnis(want, have)

        # Handle the 'enabled' state separately
        want_enabled = want.get("enabled")
        have_enabled = have.get("enabled")
        if want_enabled is not None:
            if want_enabled != have_enabled:
                if want_enabled is True:
                    self.addcmd(want, "enabled", True)
                else:
                    self.addcmd(want, "enabled", False)
        # elif not want and self.state in ["overridden", "replaced"]:
        elif (want_enabled is None or not want) and self.state in ["overridden", "replaced"]:
            if have_enabled is not None:
                self.addcmd(have, "enabled", False)

        # Handle the 'global_multicast_group' separately
        want_gmg = want.get("global_multicast_group")
        have_gmg = have.get("global_multicast_group")
        if want_gmg is not None:
            if want_gmg != have_gmg:
                self.addcmd(want, "global_multicast_group")
        # if not want and self.state in ["overridden", "replaced"]:
        if (want_gmg is None or not want) and self.state in ["overridden", "replaced"]:
            if have_gmg is not None:
                self.commands.append(f"no global mcast-group {have_gmg['mode']}")

        if len(self.commands) != begin:
            if "interface nve1" not in self.commands:
                self.commands.insert(begin, "interface nve1")

    def _compare_vnis(self, want, have):
        """Custom handling of VNI option

        :param want: the want vni dictionary
        :param have: the have vni dictionary
        """
        vni_parsers = [
            "vni_id",
            "suppress_arp",
            "suppress_arp_disable",
            "multisite_ingress_replication",
            "ingress_replication_bgp",
        ]

        w_vnis_list = want.get("vnis", [])
        h_vnis_list = have.get("vnis", [])

        w_vnis = {str(v["vni_id"]): v for v in w_vnis_list}
        h_vnis = {str(v["vni_id"]): v for v in h_vnis_list}

        for vni_id, wentry in w_vnis.items():
            begin = len(self.commands)
            have_vni = h_vnis.pop(vni_id, {})

            # Delete vni before recreating if associate_vrf mismatch
            # for state 'overridden' and 'replaced'
            if self.state in ["overridden", "replaced"]:
                want_vrf = wentry.get("associate_vrf")
                have_vrf = have_vni.get("associate_vrf")
                if want_vrf != have_vrf:
                    self.commands.append(f"no member vni {vni_id}")
                    have_vni = {}

            self.compare(parsers=vni_parsers, want=wentry, have=have_vni)

            if len(self.commands) != begin:
                cmd = self._tmplt.render(wentry, "vni_id", False)
                if cmd not in self.commands:
                    self.commands.insert(begin, cmd)

        # Remove remaining items in have for replaced and overridden
        for vni_id, wentry in h_vnis.items():
            cmd = self._tmplt.render(wentry, "vni_id", True)
            if cmd not in self.commands:
                self.commands.append(cmd)
