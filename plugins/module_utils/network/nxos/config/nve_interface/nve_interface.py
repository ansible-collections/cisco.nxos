# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The nxos_nve_interface config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.nve_interface import (
    Nve_interfaceTemplate,
)


# pairs of VNI options that NX-OS treats as alternatives
VNI_EXCLUSIVE = (
    ("suppress_arp", "suppress_arp_disable"),
    ("mcast_group", "ingress_replication_bgp"),
)


class Nve_interface(ResourceModule):
    """The nxos_nve_interface config class."""

    def __init__(self, module):
        super().__init__(
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
        """Execute the module."""

        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """
        Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self.want
        haved = self.have

        self._validate_vnis(wantd.get("vnis", []))

        # If state is 'merged', merge want onto have before compare.
        if self.state == "merged":
            wantd = self._merge(haved, wantd)

        # If state is 'deleted', remove only what is listed in config,
        # or the whole NVE interface when no config is given.
        if self.state == "deleted":
            if not wantd:
                if haved:
                    self.commands.append("no interface nve1")
                return
            wantd = self._remaining(haved, wantd)
            if not haved:
                return

        self._compare(want=wantd, have=haved)

    def _validate_vnis(self, vnis):
        """
        Reject VNI options that NX-OS treats as alternatives.

        `suppress-arp` and `suppress-arp disable` replace each other, as do
        `mcast-group` and `ingress-replication protocol bgp`.
        """
        for vni in vnis:
            for first, second in VNI_EXCLUSIVE:
                if vni.get(first) and vni.get(second):
                    self._module.fail_json(
                        msg="vni {0}: '{1}' and '{2}' are mutually exclusive".format(
                            vni["vni_id"],
                            first,
                            second,
                        ),
                    )

    @staticmethod
    def _remaining(have, want):
        """
        Build the configuration that is left after state deleted.

        Everything in have stays except the attributes and VNIs listed in
        want, so that comparing against it only negates the listed ones.
        """
        listed_vnis = {str(v["vni_id"]) for v in want.get("vnis", [])}
        remaining = {k: v for k, v in have.items() if k not in want}
        if "enabled" in want and have.get("enabled") is not None:
            remaining["enabled"] = False
        vnis = [v for v in have.get("vnis", []) if str(v["vni_id"]) not in listed_vnis]
        if vnis:
            remaining["vnis"] = vnis
        else:
            remaining.pop("vnis", None)
        return remaining

    def _merge(self, have, want):
        """
        Merge want onto have for state merged.

        VNIs are merged by `vni_id`. Setting one option of a mutually
        exclusive pair removes the other one if it is configured.
        """
        merged = dict_merge(have, {k: v for k, v in want.items() if k != "vnis"})
        have_vnis = {v["vni_id"]: v for v in have.get("vnis", [])}
        vnis = dict(have_vnis)
        for wvni in want.get("vnis", []):
            vni = dict(have_vnis.get(wvni["vni_id"], {}))
            vni.update(wvni)
            for first, second in VNI_EXCLUSIVE:
                for set_key, drop_key in ((first, second), (second, first)):
                    if wvni.get(set_key) and drop_key not in wvni:
                        vni.pop(drop_key, None)
            vnis[wvni["vni_id"]] = vni
        if vnis:
            merged["vnis"] = [vnis[k] for k in sorted(vnis)]
        return merged

    def _compare(self, want, have):
        """
        Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Nve_interface network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_vnis(want, have)

        # 'enabled' is a bool where 'no shutdown' is the set form
        want_enabled = want.get("enabled")
        have_enabled = have.get("enabled")
        if have_enabled is None and have:
            # shutdown is the default of nve1 and may not be shown by the device
            have_enabled = False
        if want_enabled is not None:
            if want_enabled != have_enabled:
                self.addcmd(want, "enabled", want_enabled)
        elif have_enabled and self.state in ["overridden", "replaced"]:
            # an interface that is not requested to be enabled is shut
            self.addcmd(have, "enabled", False)

        # 'global_multicast_group' needs the mode, so it is handled here
        want_gmg = want.get("global_multicast_group")
        have_gmg = have.get("global_multicast_group")
        if want_gmg is not None:
            if want_gmg != have_gmg:
                if (
                    have_gmg
                    and have_gmg["mode"] != want_gmg["mode"]
                    and self.state in ["overridden", "replaced"]
                ):
                    self.commands.append(self._gmg_negate(have_gmg))
                self.addcmd(want, "global_multicast_group")
        elif have_gmg is not None and self.state in ["overridden", "replaced", "deleted"]:
            self.commands.append(self._gmg_negate(have_gmg))

        if len(self.commands) != begin:
            if "interface nve1" not in self.commands:
                self.commands.insert(begin, "interface nve1")

    @staticmethod
    def _gmg_negate(gmg):
        return "no global mcast-group {mode}".format(**gmg)

    def _compare_vnis(self, want, have):
        """
        Custom handling of VNI option

        :param want: the want vni dictionary
        :param have: the have vni dictionary
        """
        vni_parsers = [
            "vni_id",
            "suppress_arp",
            "suppress_arp_disable",
            "multisite_ingress_replication",
            "ingress_replication_bgp",
            "mcast_group",
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
            if have_vni and self.state in ["overridden", "replaced"]:
                if bool(wentry.get("associate_vrf")) != bool(have_vni.get("associate_vrf")):
                    self.commands.append(self._tmplt.render(have_vni, "vni_id", True))
                    have_vni = {}

            self.compare(parsers=vni_parsers, want=wentry, have=have_vni)

            if len(self.commands) != begin:
                # remove first so an alternative option can take its place
                new = self.commands[begin:]
                new.sort(key=lambda c: not c.startswith("no "))
                self.commands[begin:] = new
                cmd = self._tmplt.render(wentry, "vni_id", False)
                if cmd not in self.commands:
                    self.commands.insert(begin, cmd)

        # Remove remaining items in have for replaced and overridden
        for vni_id, wentry in h_vnis.items():
            cmd = self._tmplt.render(wentry, "vni_id", True)
            if cmd not in self.commands:
                self.commands.append(cmd)
