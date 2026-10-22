# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_evpn_vnis config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.evpn_vnis import (
    Evpn_vnisTemplate,
)


def _unique(items):
    """Drop duplicates while keeping the order the user gave."""
    return list(dict.fromkeys(items))


class Evpn_vnis(ResourceModule):
    """
    The nxos_evpn_vnis config class
    """

    def __init__(self, module):
        super(Evpn_vnis, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="evpn_vnis",
            tmplt=Evpn_vnisTemplate(),
        )
        self.parsers = []

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
        wantd = {entry["vni"]: self._normalize(entry) for entry in self.want}
        haved = {entry["vni"]: self._normalize(entry) for entry in self.have}

        if self.state == "merged":
            wantd = self._merge_with_have(wantd, haved)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self.addcmd(have, "vni", True)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, None))

        # every VNI line lives under the `evpn` context
        if self.commands:
            self.commands.insert(0, self._tmplt.render({}, "evpn", False))

    @staticmethod
    def _normalize(entry):
        """`route-target both X` is the same as an import plus an export of X,
        so fold it into those two lists. Device output and playbook input are
        then compared in a single form whichever way NX-OS displays it.
        """
        both = entry.get("route_target_both") or []
        norm = {k: v for k, v in entry.items() if k != "route_target_both" and v is not None}
        for key in ("route_target_import", "route_target_export"):
            targets = _unique((entry.get(key) or []) + both)
            if targets:
                norm[key] = targets
        return norm

    @staticmethod
    def _merge_with_have(wantd, haved):
        """Layer want on top of have so that a single compare path can be used
        for every state: the route distinguisher is overridden when given and
        the route-target lists are extended, so merged never removes anything.
        """
        merged = {}
        for vni, want in wantd.items():
            entry = dict(haved.get(vni, {}))
            entry.update({k: v for k, v in want.items() if not k.startswith("route_target")})
            for key in ("route_target_import", "route_target_export"):
                targets = _unique(entry.get(key, []) + want.get(key, []))
                if targets:
                    entry[key] = targets
            merged[vni] = entry
        return merged

    def _compare(self, want, have):
        """Generate set/delete commands for a single VNI."""
        begin = len(self.commands)
        have = have or {}

        self.compare(parsers=["route_distinguisher"], want=want, have=have)

        for key in ("route_target_import", "route_target_export"):
            w_rts = want.get(key, [])
            h_rts = have.get(key, [])
            for rt in h_rts:
                if rt not in w_rts:
                    self.addcmd({"rt": rt}, key, True)
            for rt in w_rts:
                if rt not in h_rts:
                    self.addcmd({"rt": rt}, key, False)

        # a VNI with nothing in it is still created by its own line
        if len(self.commands) != begin or not have:
            self.commands.insert(begin, self._tmplt.render(want, "vni", False))
