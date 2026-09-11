#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_vpc config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.vpc import (
    VpcTemplate,
)


class Vpc(ResourceModule):
    """
    The nxos_vpc config class
    """

    def __init__(self, module):
        super(Vpc, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="vpc",
            tmplt=VpcTemplate(),
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
        want = self.want
        have = self.have

        # if state is deleted, remove the vpc domain entirely
        if self.state == "deleted":
            if have:
                self.commands.append("terminal dont-ask")
                self.commands.append("no vpc domain {0}".format(have.get("domain")))
            return

        self._compare(want, have)

    def _compare(self, want, have):
        """Generate set/delete commands for VPC global domain configuration."""
        begin = len(self.commands)
        needs_terminal = False
        domain = want.get("domain") or have.get("domain")

        # scalar sub-commands: field → (set template, no-form command)
        scalar_cmds = [
            ("role_priority", "role priority {0}", "no role priority"),
            ("system_priority", "system-priority {0}", "no system-priority"),
            ("delay_restore", "delay restore {0}", "no delay restore"),
            (
                "delay_restore_interface_vlan",
                "delay restore interface-vlan {0}",
                "no delay restore interface-vlan",
            ),
            (
                "delay_restore_orphan_port",
                "delay restore orphan-port {0}",
                "no delay restore orphan-port",
            ),
            (
                "auto_recovery_reload_delay",
                "auto-recovery reload-delay {0}",
                "no auto-recovery reload-delay",
            ),
        ]

        for key, set_tmpl, unset_cmd in scalar_cmds:
            w_val = want.get(key)
            h_val = have.get(key)
            if w_val is not None and w_val != h_val:
                self.commands.append(set_tmpl.format(w_val))
            elif w_val is None and h_val is not None and self.state not in ["merged", "rendered"]:
                # replaced / overridden: remove config not present in want
                self.commands.append(unset_cmd)

        # boolean sub-commands
        bool_cmds = [
            ("auto_recovery", "auto-recovery", "no auto-recovery"),
            ("peer_gw", "peer-gateway", "no peer-gateway"),
            ("peer_sw", "peer-switch", "no peer-switch"),
        ]

        for key, set_cmd, unset_cmd in bool_cmds:
            w_val = want.get(key)
            h_val = have.get(key)
            if w_val is not None and w_val != h_val:
                if key in ("peer_gw", "peer_sw"):
                    needs_terminal = True
                self.commands.append(set_cmd if w_val else unset_cmd)
            elif w_val is None and h_val is not None and self.state not in ["merged", "rendered"]:
                # replaced / overridden: remove config not present in want
                if key in ("peer_gw", "peer_sw"):
                    needs_terminal = True
                self.commands.append(unset_cmd)

        # peer-keepalive: composite command — merge want pkl fields onto have
        pkl_keys = ["pkl_dest", "pkl_src", "pkl_vrf"]
        w_pkl = {k: want.get(k) for k in pkl_keys if want.get(k)}
        h_pkl = {k: have.get(k) for k in pkl_keys if have.get(k)}

        if w_pkl:
            # retain existing pkl values not overridden by want
            merged_pkl = dict(h_pkl)
            merged_pkl.update(w_pkl)
            if merged_pkl != h_pkl:
                self.commands.append(self._pkl_cmd(merged_pkl))
        elif h_pkl and self.state not in ["merged", "rendered"]:
            # replaced / overridden: remove peer-keepalive entirely
            self.commands.append("no peer-keepalive")

        if len(self.commands) != begin:
            self.commands.insert(begin, "vpc domain {0}".format(domain))
            if needs_terminal:
                self.commands.insert(begin, "terminal dont-ask")

    def _pkl_cmd(self, pkl):
        cmd = "peer-keepalive destination {0}".format(pkl["pkl_dest"])
        if pkl.get("pkl_src"):
            cmd += " source {0}".format(pkl["pkl_src"])
        if pkl.get("pkl_vrf"):
            cmd += " vrf {0}".format(pkl["pkl_vrf"])
        return cmd
