# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The nxos_pim_global config file.
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.pim_global import (
    Pim_globalTemplate,
)

# A static RP without a group-list, prefix-list or route-map covers all groups and
# NX-OS stores it with this group-list.
RP_ALL_GROUPS = "224.0.0.0/4"

# options that are a flag in the running-config
FLAGS = ("bfd", "log_neighbor_changes", "flush_routes")


class Pim_global(ResourceModule):
    """The nxos_pim_global config class."""

    def __init__(self, module):
        super().__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="pim_global",
            tmplt=Pim_globalTemplate(),
        )

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
        wantd = self._normalize(self.want)
        haved = self._normalize(self.have)

        # If state is 'merged', merge want onto have before compare.
        if self.state == "merged":
            wantd = self._merge(haved, wantd)

        # If state is 'deleted', everything is removed, or only what is listed in config.
        if self.state == "deleted":
            wantd = self._remaining(haved, wantd) if self.want else self._normalize({})

        self._compare(want=wantd, have=haved)

    @staticmethod
    def _normalize(config):
        """
        Convert the facts or argspec data to the shape that is compared.

        Static RPs and anycast RP members become dictionaries with one entry per
        configuration line.
        """
        config = config or {}
        data = {
            "ssm_range": list(config.get("ssm_range") or []),
            "register_rate_limit": config.get("register_rate_limit"),
            "rps": {},
            "anycast": {},
        }
        for flag in FLAGS:
            data[flag] = config.get(flag)

        for rp in config.get("rp_addresses") or []:
            entry = {"rp_address": rp["rp_address"]}
            if rp.get("prefix_list"):
                entry["prefix_list"] = rp["prefix_list"]
            elif rp.get("route_map"):
                entry["route_map"] = rp["route_map"]
            else:
                entry["group_list"] = rp.get("group_list") or RP_ALL_GROUPS
            if rp.get("bidir"):
                entry["bidir"] = True
            data["rps"][
                (
                    entry["rp_address"],
                    entry.get("group_list") or entry.get("prefix_list") or entry.get("route_map"),
                )
            ] = entry

        for anycast in config.get("anycast_rps") or []:
            for member in anycast.get("members") or []:
                data["anycast"][(anycast["anycast_rp"], member)] = {
                    "anycast_rp": anycast["anycast_rp"],
                    "member": member,
                }
        return data

    @staticmethod
    def _merge(have, want):
        """
        Add what is given in want to have.

        The SSM range is one list in NX-OS, so the ranges of want are added to the
        configured ranges. The keyword none stands alone.
        """
        merged = {}
        merged["rps"] = dict(have["rps"])
        merged["rps"].update(want["rps"])
        merged["anycast"] = dict(have["anycast"])
        merged["anycast"].update(want["anycast"])
        for key in ("register_rate_limit",) + FLAGS:
            merged[key] = want[key] if want[key] is not None else have[key]

        if want["ssm_range"]:
            if "none" in want["ssm_range"]:
                merged["ssm_range"] = ["none"]
            else:
                merged["ssm_range"] = [r for r in have["ssm_range"] if r != "none"] + [
                    r for r in want["ssm_range"] if r not in have["ssm_range"]
                ]
        else:
            merged["ssm_range"] = have["ssm_range"]
        return merged

    @staticmethod
    def _remaining(have, want):
        """
        Build the configuration that is left after state deleted.

        Everything in have stays except what is listed in want, so that comparing
        against it only negates what is listed.
        """
        remaining = {
            "rps": {k: v for k, v in have["rps"].items() if k not in want["rps"]},
            "anycast": {k: v for k, v in have["anycast"].items() if k not in want["anycast"]},
            "ssm_range": [] if want["ssm_range"] else have["ssm_range"],
        }
        for key in ("register_rate_limit",) + FLAGS:
            remaining[key] = None if want[key] is not None else have[key]
        return remaining

    def _compare(self, want, have):
        """
        Compare want and have and add the commands.

        The commands that remove configuration come first so that a changed line
        (for example a static RP that changes to bidir) is replaced.
        """
        remove_all = self.state in ["replaced", "overridden", "deleted"]
        additions = []

        # static RPs
        for key, entry in have["rps"].items():
            wanted = want["rps"].get(key)
            if (wanted is None and remove_all) or (wanted is not None and wanted != entry):
                self.addcmd(entry, "rp_address", True)
        for key, entry in want["rps"].items():
            if entry != have["rps"].get(key):
                additions.append(("rp_address", entry))

        # anycast RP members
        for key, entry in have["anycast"].items():
            if key not in want["anycast"] and remove_all:
                self.addcmd(entry, "anycast_rp", True)
        for key, entry in want["anycast"].items():
            if key not in have["anycast"]:
                additions.append(("anycast_rp", entry))

        # flags
        for flag in FLAGS:
            if want[flag] is True and not have[flag]:
                additions.append((flag, {flag: True}))
            elif have[flag] and (want[flag] is False or (want[flag] is None and remove_all)):
                self.addcmd({flag: True}, flag, True)

        # register rate limit
        want_limit = want["register_rate_limit"]
        have_limit = have["register_rate_limit"]
        if want_limit is not None and want_limit != have_limit:
            additions.append(("register_rate_limit", {"register_rate_limit": want_limit}))
        elif want_limit is None and have_limit is not None and remove_all:
            self.addcmd({"register_rate_limit": have_limit}, "register_rate_limit", True)

        # SSM range, one line that replaces the previous one. Removing any range
        # resets the line to the default 232.0.0.0/8, which is not displayed.
        want_ssm = want["ssm_range"]
        have_ssm = have["ssm_range"]
        if want_ssm:
            if set(want_ssm) != set(have_ssm):
                if set(want_ssm) == {"232.0.0.0/8"}:
                    if have_ssm:
                        self.addcmd({"ssm_range": have_ssm}, "ssm_range", True)
                else:
                    additions.append(("ssm_range", {"ssm_range": want_ssm}))
        elif have_ssm and remove_all:
            self.addcmd({"ssm_range": have_ssm}, "ssm_range", True)

        for parser, data in additions:
            self.addcmd(data, parser, False)
