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

    # Numeric sub-commands. NX-OS rejects the bare no-form of some of these
    # (``no system-priority`` returns "% Incomplete command" on 10.4(2)), so
    # removal is expressed by re-applying the platform default instead.
    SCALARS = (
        ("role_priority", "role priority {0}", "32667"),
        ("system_priority", "system-priority {0}", "32667"),
        ("delay_restore", "delay restore {0}", "60"),
        ("delay_restore_interface_vlan", "delay restore interface-vlan {0}", "10"),
        ("delay_restore_orphan_port", "delay restore orphan-port {0}", "0"),
        ("auto_recovery_reload_delay", "auto-recovery reload-delay {0}", "240"),
    )

    # Boolean sub-commands. An absent line means the feature is disabled.
    BOOLEANS = (
        ("auto_recovery", "auto-recovery", "no auto-recovery"),
        ("peer_gw", "peer-gateway", "no peer-gateway"),
        ("peer_sw", "peer-switch", "no peer-switch"),
    )

    # Sub-commands that make NX-OS prompt for confirmation.
    NEEDS_DONT_ASK = ("peer_gw", "peer_sw")

    PKL_KEYS = ("pkl_dest", "pkl_src", "pkl_vrf")

    # NX-OS does not nvgen the peer-keepalive VRF when it is the default one,
    # so an absent VRF has to be treated as ``management`` for comparison.
    DEFAULT_PKL_VRF = "management"

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
        want = self.want or {}
        have = self.have or {}

        # if state is deleted, remove the vpc domain entirely
        if self.state == "deleted":
            if have:
                self.commands.append("terminal dont-ask")
                self.commands.append("no vpc domain {0}".format(have.get("domain")))
            return

        # only one vpc domain can exist at a time, so changing the domain ID
        # means tearing down the existing one first
        if (
            have
            and want.get("domain")
            and want["domain"] != have.get("domain")
            and self.state in ["replaced", "overridden"]
        ):
            self.commands.append("terminal dont-ask")
            self.commands.append("no vpc domain {0}".format(have["domain"]))
            have = {}

        self._compare(want, have)

    def _compare(self, want, have):
        """Generate set/delete commands for VPC global domain configuration."""
        begin = len(self.commands)
        needs_dont_ask = False
        domain = want.get("domain") or have.get("domain")
        prune = self.state not in ["merged", "rendered"]

        for key, set_tmpl, default in self.SCALARS:
            w_val = want.get(key)
            h_val = have.get(key)
            if w_val is not None:
                if w_val != h_val:
                    self.commands.append(set_tmpl.format(w_val))
            elif prune and h_val is not None and h_val != default:
                # replaced / overridden: reset to the platform default
                self.commands.append(set_tmpl.format(default))

        for key, set_cmd, unset_cmd in self.BOOLEANS:
            w_val = want.get(key)
            if w_val is None and not prune:
                continue
            # an absent line, on either side, means the feature is disabled
            w_val = bool(w_val)
            h_val = bool(have.get(key))
            if w_val != h_val:
                if key in self.NEEDS_DONT_ASK:
                    needs_dont_ask = True
                self.commands.append(set_cmd if w_val else unset_cmd)

        self._compare_peer_keepalive(want, have)

        if len(self.commands) != begin:
            self.commands.insert(begin, "vpc domain {0}".format(domain))
            if needs_dont_ask:
                self.commands.insert(begin, "terminal dont-ask")

    def _compare_peer_keepalive(self, want, have):
        """peer-keepalive is a single composite command, so it is compared
        as a unit rather than key by key.

        For ``merged`` and ``rendered`` the keys supplied in want are layered
        on top of what the device already has, otherwise omitting an optional
        key would silently drop it from the rebuilt command. For ``replaced``
        and ``overridden`` want is authoritative and anything omitted is
        dropped, which is what those states promise.
        """
        w_pkl = self._pkl_effective(want)
        h_pkl = self._pkl_effective(have)

        if w_pkl and self.state in ["merged", "rendered"]:
            merged = dict(h_pkl)
            merged.update(w_pkl)
            w_pkl = merged

        if w_pkl:
            if w_pkl != h_pkl:
                self.commands.append(self._pkl_cmd(w_pkl))
        elif h_pkl and self.state not in ["merged", "rendered"]:
            # negate the full line; NX-OS rejects a bare `no peer-keepalive`
            self.commands.append("no " + self._pkl_cmd(h_pkl))

    def _pkl_effective(self, cfg):
        """Collect the peer-keepalive keys, filling in the VRF that NX-OS
        leaves out of running-config when it is the default one.
        """
        pkl = {k: cfg.get(k) for k in self.PKL_KEYS if cfg.get(k)}
        if pkl.get("pkl_dest") and not pkl.get("pkl_vrf"):
            pkl["pkl_vrf"] = self.DEFAULT_PKL_VRF
        return pkl

    def _pkl_cmd(self, pkl):
        cmd = "peer-keepalive destination {0}".format(pkl["pkl_dest"])
        if pkl.get("pkl_src"):
            cmd += " source {0}".format(pkl["pkl_src"])
        if pkl.get("pkl_vrf"):
            cmd += " vrf {0}".format(pkl["pkl_vrf"])
        return cmd
