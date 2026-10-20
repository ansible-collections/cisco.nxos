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

import time

from ansible.module_utils.connection import ConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)


# NX-OS tears a domain down asynchronously after 'no vpc domain'.  On a
# reused persistent connection the next 'vpc domain <id>' is answered with
# 'Domain delete in progress'.  Sleep this many seconds after sending the
# delete before sending the recreate.
_DOMAIN_DELETE_SLEEP = 8
_MAX_RETRY = 5
_RETRY_INTERVAL = 4
_TERMINAL_DONT_ASK = "terminal dont-ask"
_NO_VPC_DOMAIN_FMT = "no vpc domain {0}"

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
        ("layer3_peer_router", "layer3 peer-router", "no layer3 peer-router"),
        ("arp_synchronize", "ip arp synchronize", "no ip arp synchronize"),
        ("nd_synchronize", "ipv6 nd synchronize", "no ipv6 nd synchronize"),
    )

    # Sub-commands that make NX-OS prompt for confirmation.
    NEEDS_DONT_ASK = ("peer_gw", "peer_sw", "layer3_peer_router")

    PKL_KEYS = ("pkl_dest", "pkl_src", "pkl_vrf")

    VPL_KEYS = ("virtual_peer_link_dest", "virtual_peer_link_src", "virtual_peer_link_dscp")

    # NX-OS silently appends dscp 56 to running-config when virtual peer-link
    # is configured without an explicit dscp value.  Treat an absent dscp as
    # DEFAULT_VPL_DSCP so the comparison does not falsely report a change.
    DEFAULT_VPL_DSCP = "56"

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
            self._run_with_domain_wait()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        want = self.want or {}
        have = self.have or {}

        domain = want.get("domain")
        if domain is not None:
            try:
                d = int(domain)
                if not (1 <= d <= 1000):
                    raise ValueError
            except (ValueError, TypeError):
                self._module.fail_json(
                    msg="vpc domain must be in the range 1-1000, got '{0}'".format(domain),
                )

        # if state is deleted, remove the vpc domain entirely
        if self.state == "deleted":
            if have:
                self.commands.append(_TERMINAL_DONT_ASK)
                self.commands.append(_NO_VPC_DOMAIN_FMT.format(have.get("domain")))
            self._restore_dont_ask()
            return

        # only one vpc domain can exist at a time, so changing the domain ID
        # means tearing down the existing one first
        domain_recreate = False
        if (
            have
            and want.get("domain")
            and want["domain"] != have.get("domain")
            and self.state in ["replaced", "overridden"]
        ):
            self.commands.append(_TERMINAL_DONT_ASK)
            self.commands.append(_NO_VPC_DOMAIN_FMT.format(have["domain"]))
            have = {}
            domain_recreate = True

        self._compare(want, have)

        # When the domain ID changed and _compare emitted no sub-commands
        # (want has only the bare domain with no attributes), _compare never
        # inserts the new 'vpc domain X' line.  Ensure it is always present.
        new_domain = "vpc domain {0}".format(want.get("domain"))
        if domain_recreate and new_domain not in self.commands:
            no_idx = next(i for i, c in enumerate(self.commands) if c.startswith("no vpc domain"))
            self.commands.insert(no_idx + 1, new_domain)

        # NX-OS 10.4(x): every 'no peer-keepalive' form is rejected in
        # (config-vpc-domain)#.  The only reliable way to remove a keepalive
        # is to delete and recreate the domain — the freshly created domain
        # starts without one.  This is disruptive (flaps the peer relationship)
        # but is the only approach that works on this platform.
        if any(c.startswith("no peer-keepalive") for c in self.commands):
            self.commands = self._rewrite_as_domain_recreate(want)
            return

        self._restore_dont_ask()

    def _restore_dont_ask(self):
        """Undo ``terminal dont-ask`` so the module does not leave the session
        suppressing confirmation prompts for everything that runs after it.

        This brackets the setting the same way ``nxos_vsan`` and
        ``nxos_devicealias`` do. Without it a connection that has torn down a
        vpc domain stays in that state, and later tasks reusing the same
        connection do not behave as they would on a fresh one.
        """
        if _TERMINAL_DONT_ASK in self.commands:
            self.commands.append("no terminal dont-ask")

    def _positive_cmds_from_want(self, want):
        """Return positive (non-default) commands from want for a fresh domain.

        A freshly created domain already has platform defaults, so re-setting
        them wastes CLI round trips.
        """
        cmds = []
        for key, set_tmpl, default in self.SCALARS:
            w_val = want.get(key)
            if w_val is not None and w_val != default:
                cmds.append(set_tmpl.format(w_val))
        for key, set_cmd, _unset in self.BOOLEANS:
            if want.get(key):
                cmds.append(set_cmd)
        w_pkl = self._pkl_effective(want)
        if w_pkl:
            cmds.append(self._pkl_cmd(w_pkl))
        w_vpl = self._vpl_effective(want)
        if w_vpl:
            cmds.append(self._vpl_cmd(w_vpl))
        return cmds

    def _rewrite_as_domain_recreate(self, want):
        """Return a command list that deletes the current domain and recreates it.

        Used when a keepalive removal is needed — NX-OS rejects every
        'no peer-keepalive' form in (config-vpc-domain)#, so the domain must
        be torn down and rebuilt with only the wanted (non-default) commands.
        The freshly created domain starts with all platform defaults, so
        explicit default-value commands are omitted.
        """
        domain = want.get("domain") or (self.have or {}).get("domain")
        positive = self._positive_cmds_from_want(want)
        cmds = [
            _TERMINAL_DONT_ASK,
            _NO_VPC_DOMAIN_FMT.format(domain),
            "vpc domain {0}".format(domain),
        ]
        cmds.extend(positive)
        cmds.append("no terminal dont-ask")
        return cmds

    def _edit_config_until_ready(self, candidate):
        """Send candidate commands, retrying when NX-OS reports that an async
        domain delete is still in progress.

        Over CLI the signal is text in the edit_config return value; over
        NX-API it is a ConnectionError whose message contains
        'Domain delete in progress'.
        """
        _DOMAIN_DELETE_MSG = "Domain delete in progress"
        for attempt in range(1, _MAX_RETRY + 1):
            try:
                output = self._connection.edit_config(candidate=candidate)
                if _DOMAIN_DELETE_MSG not in str(output or ""):
                    return
                if attempt == _MAX_RETRY:
                    raise RuntimeError(
                        "VPC: domain delete still in progress"
                        " after {0} attempts".format(attempt),
                    )
            except ConnectionError as exc:
                if _DOMAIN_DELETE_MSG not in str(exc) or attempt == _MAX_RETRY:
                    raise
            time.sleep(_RETRY_INTERVAL)

    def _probe_domain_ready(self, probe_cmd):
        """Poll until NX-OS confirms the async domain delete has finished."""
        self._edit_config_until_ready([probe_cmd])

    def _run_with_domain_wait(self):
        """Run commands, splitting at 'no vpc domain' to give NX-OS time to
        finish tearing down the domain before 'vpc domain' is sent on the same
        persistent connection.

        NX-OS tears the domain down asynchronously after replying to
        'no vpc domain'.  On a reused connection the next 'vpc domain <id>'
        is answered with 'Domain delete in progress', and subsequent
        sub-commands land at global config where NX-OS rejects them as
        '% Invalid command'.  A fresh connection avoids this only because the
        reconnect time outlasts the delete window.

        Fix: send everything up to and including 'no vpc domain', sleep
        _DOMAIN_DELETE_SLEEP seconds, then probe with just 'vpc domain <id>'
        until NX-OS confirms the delete is complete before sending the rest.
        """
        split_idx = next(
            (i for i, cmd in enumerate(self.commands) if cmd.startswith("no vpc domain")),
            None,
        )

        if split_idx is None or self._module.check_mode:
            self.run_commands()
            return

        boundary = split_idx + 1
        first = self.commands[:boundary]
        rest = self.commands[boundary:]

        self._connection.edit_config(candidate=first)
        time.sleep(_DOMAIN_DELETE_SLEEP)

        # Probe the first 'vpc domain X' command in rest — it may not be
        # rest[0] when terminal dont-ask was already set before the split.
        probe_cmd = next((c for c in rest if c.startswith("vpc domain")), None)
        if probe_cmd:
            self._probe_domain_ready(probe_cmd)

        if rest:
            self._edit_config_until_ready(rest)
        self.changed = True

    def _compare_scalars(self, want, have, prune):
        for key, set_tmpl, default in self.SCALARS:
            w_val = want.get(key)
            h_val = have.get(key)
            if w_val is not None:
                if w_val != h_val:
                    self.commands.append(set_tmpl.format(w_val))
            elif prune and h_val is not None and h_val != default:
                # replaced / overridden: reset to the platform default
                self.commands.append(set_tmpl.format(default))

    def _compare_booleans(self, want, have, prune):
        needs_dont_ask = False
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
        return needs_dont_ask

    def _compare(self, want, have):
        """Generate set/delete commands for VPC global domain configuration."""
        begin = len(self.commands)
        domain = want.get("domain") or have.get("domain")
        prune = self.state not in ["merged", "rendered"]

        self._compare_scalars(want, have, prune)
        needs_dont_ask = self._compare_booleans(want, have, prune)
        self._compare_peer_keepalive(want, have)
        self._compare_virtual_peer_link(want, have)

        if len(self.commands) != begin:
            self.commands.insert(begin, "vpc domain {0}".format(domain))
            # Only add terminal dont-ask when it isn't already present before
            # the block we're about to insert (e.g. domain-change path already
            # set it up — inserting a second copy pushes 'vpc domain X' out of
            # rest[0], breaking the domain-ready probe in _run_with_domain_wait)
            if needs_dont_ask and _TERMINAL_DONT_ASK not in self.commands[:begin]:
                self.commands.insert(begin, _TERMINAL_DONT_ASK)

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

    def _compare_virtual_peer_link(self, want, have):
        """virtual peer-link is a single composite command compared as a unit.

        NX-OS silently appends ``dscp 56`` to running-config when no dscp is
        configured.  _vpl_effective() injects the default so that omitting dscp
        in want does not cause a spurious change every run.
        """
        w_vpl = self._vpl_effective(want)
        h_vpl = self._vpl_effective(have)

        if w_vpl and self.state in ["merged", "rendered"]:
            merged = dict(h_vpl)
            merged.update(w_vpl)
            w_vpl = merged

        if w_vpl:
            if w_vpl != h_vpl:
                self.commands.append(self._vpl_cmd(w_vpl))
        elif h_vpl and self.state not in ["merged", "rendered"]:
            self.commands.append("no " + self._vpl_cmd(h_vpl))

    def _vpl_effective(self, cfg):
        """Collect virtual-peer-link keys, injecting the default dscp that
        NX-OS appends silently to running-config.
        """
        vpl = {k: cfg.get(k) for k in self.VPL_KEYS if cfg.get(k)}
        if vpl.get("virtual_peer_link_dest") and not vpl.get("virtual_peer_link_dscp"):
            vpl["virtual_peer_link_dscp"] = self.DEFAULT_VPL_DSCP
        return vpl

    def _vpl_cmd(self, vpl):
        cmd = "virtual peer-link destination {0}".format(vpl["virtual_peer_link_dest"])
        if vpl.get("virtual_peer_link_src"):
            cmd += " source {0}".format(vpl["virtual_peer_link_src"])
        if vpl.get("virtual_peer_link_dscp"):
            cmd += " dscp {0}".format(vpl["virtual_peer_link_dscp"])
        return cmd
