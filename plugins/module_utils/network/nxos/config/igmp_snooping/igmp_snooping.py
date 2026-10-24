# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_igmp_snooping config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import ipaddress

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.igmp_snooping.igmp_snooping import (
    GLOBAL_DEFAULTS,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.igmp_snooping import (
    Igmp_snoopingTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


GROUP_TIMEOUT = "group_timeout"
GROUP_TIMEOUT_NEVER = "never"
GROUP_TIMEOUT_MAX = 10080
VLAN_ID_MAX = 4094
NO_VLAN_CONFIGURATION = "no vlan configuration {0}"


class Igmp_snooping(ResourceModule):
    """
    The nxos_igmp_snooping config class
    """

    def __init__(self, module):
        super(Igmp_snooping, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="igmp_snooping",
            tmplt=Igmp_snoopingTemplate(),
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

        The global commands are sent first: once a `vlan configuration`
        context is entered, the same keywords would be read as per-VLAN ones.
        """
        want_globals, want_vlans = self._normalize(self.want)
        have_globals, have_vlans = self._normalize(self.have)

        if self.state == "deleted":
            targets = self._deleted_targets(want_globals, bool(self.want))
        else:
            targets = self._targets(want_globals)

        self._check_group_timeout(targets, have_globals)
        self._global_commands(targets, have_globals)

        if self.state == "deleted":
            self._deleted_vlans(want_vlans, have_vlans, bool(self.want))
        else:
            self._vlan_commands(want_vlans, have_vlans)

    # normalisation

    def _normalize(self, cfg):
        """Return the global settings and the VLANs as {vlan_id: {(group, source): [interfaces]}}."""
        cfg = cfg or {}
        settings = {k: v for k, v in cfg.items() if k != "vlans" and v is not None}
        if GROUP_TIMEOUT in settings:
            settings[GROUP_TIMEOUT] = self._group_timeout(settings[GROUP_TIMEOUT])

        vlans = {}
        for vlan in cfg.get("vlans") or []:
            self._check_vlan_id(vlan["vlan_id"])
            groups = vlans.setdefault(vlan["vlan_id"], {})
            for key, interfaces in self._groups(vlan.get("static_groups")).items():
                known = groups.setdefault(key, [])
                known.extend(i for i in interfaces if i not in known)
        return settings, vlans

    def _group_timeout(self, value):
        text = str(value).strip().lower()
        if text == GROUP_TIMEOUT_NEVER:
            return text
        if not text.isdigit() or not 1 <= int(text) <= GROUP_TIMEOUT_MAX:
            self._module.fail_json(
                msg="group_timeout must be 'never' or a number in the range 1-{0}, got '{1}'".format(
                    GROUP_TIMEOUT_MAX,
                    value,
                ),
            )
        return str(int(text))

    def _check_vlan_id(self, vlan_id):
        if not 1 <= vlan_id <= VLAN_ID_MAX:
            self._module.fail_json(
                msg="vlan_id must be in the range 1-{0}, got '{1}'".format(VLAN_ID_MAX, vlan_id),
            )

    def _address(self, value, what):
        try:
            return ipaddress.IPv4Address(value)
        except ValueError:
            self._module.fail_json(msg="{0} must be an IPv4 address, got '{1}'".format(what, value))

    def _groups(self, static_groups):
        """Map the static groups of a VLAN to {(group, source): [interfaces]}."""
        result = {}
        for entry in static_groups or []:
            group = self._address(entry["group"], "group")
            if not group.is_multicast:
                self._module.fail_json(
                    msg="group must be a multicast address, got '{0}'".format(entry["group"]),
                )
            source = entry.get("source")
            if source:
                source = str(self._address(source, "source"))
            interfaces = result.setdefault((str(group), source or ""), [])
            for name in entry["interfaces"]:
                name = normalize_interface(name)
                if name not in interfaces:
                    interfaces.append(name)
        return result

    # globals

    def _targets(self, want):
        """The value each global setting must end up with.

        merged and rendered only act on what was given, replaced and
        overridden reset everything else to the NX-OS default.
        """
        if self.state in ["replaced", "overridden"]:
            targets = dict(GLOBAL_DEFAULTS)
            targets[GROUP_TIMEOUT] = None
            targets.update(want)
            return targets
        return dict(want)

    @staticmethod
    def _deleted_targets(want, has_config):
        """Without config every setting is reset, otherwise the listed ones."""
        scope = want if has_config else dict(GLOBAL_DEFAULTS, **{GROUP_TIMEOUT: None})
        return {key: GLOBAL_DEFAULTS.get(key) for key in scope}

    def _check_group_timeout(self, targets, have):
        """The device rejects group-timeout while snooping is disabled."""
        if targets.get(GROUP_TIMEOUT) is None:
            return
        if not self._final_snooping(targets, have):
            self._module.fail_json(
                msg="group_timeout cannot be set while snooping is, or is being set to, false",
            )

    @staticmethod
    def _final_snooping(targets, have):
        return targets.get("snooping", have.get("snooping", GLOBAL_DEFAULTS["snooping"]))

    def _global_commands(self, targets, have):
        """Booleans first, group-timeout last (it is rejected while snooping is
        disabled), except when it is removed because snooping is being turned off.
        """
        for key in GLOBAL_DEFAULTS:
            if key in targets and targets[key] != have.get(key):
                self.addcmd({}, key, not targets[key])

        if GROUP_TIMEOUT not in targets:
            return
        commands = self._group_timeout_commands(targets[GROUP_TIMEOUT], have.get(GROUP_TIMEOUT))
        if self._final_snooping(targets, have):
            self.commands.extend(commands)
        else:
            self.commands[:0] = commands

    def _group_timeout_commands(self, target, current):
        if target == current:
            return []
        if target is None:
            return [self._tmplt.render({GROUP_TIMEOUT: current}, GROUP_TIMEOUT, True)]
        return [self._tmplt.render({GROUP_TIMEOUT: target}, GROUP_TIMEOUT, False)]

    # VLANs

    def _vlan_commands(self, want, have):
        """merged and rendered add, replaced and overridden make the listed
        VLANs identical to want, overridden also drops the unlisted ones.
        """
        prune = self.state in ["replaced", "overridden"]
        for vlan_id, groups in want.items():
            if prune and not groups:
                # an empty want means no block at all
                self._remove_block(vlan_id, have)
            else:
                self._vlan_block(vlan_id, groups, have.get(vlan_id, {}), prune)

        if self.state == "overridden":
            for vlan_id in [v for v in have if v not in want]:
                self._remove_block(vlan_id, have)

    def _remove_block(self, vlan_id, have):
        if vlan_id in have:
            self.commands.append(NO_VLAN_CONFIGURATION.format(vlan_id))

    def _vlan_block(self, vlan_id, want, have, prune):
        """The block is only entered when it has something to change."""
        lines = []
        if prune:
            lines.extend(self._group_lines(have, want, True))
        lines.extend(self._group_lines(want, have, False))
        if lines:
            self.commands.append(self._tmplt.render({"vlan_id": vlan_id}, "vlan", False))
            self.commands.extend(lines)

    def _group_lines(self, source, other, negate):
        """Commands for the (group, source, interface) triplets of source missing in other."""
        lines = []
        for (group, src), interfaces in source.items():
            for interface in interfaces:
                if interface not in other.get((group, src), []):
                    data = {"group": group, "interface": interface}
                    parser = "static_group"
                    if src:
                        data["source"] = src
                        parser = "static_group_source"
                    lines.append(self._tmplt.render(data, parser, negate))
        return lines

    def _deleted_vlans(self, want, have, has_config):
        """A listed VLAN without static groups is removed as a whole, one with
        static groups only loses those groups. Without config all of them go.
        """
        if not has_config:
            want = {vlan_id: {} for vlan_id in have}
        for vlan_id, groups in want.items():
            if vlan_id not in have:
                continue
            if not groups:
                self.commands.append(NO_VLAN_CONFIGURATION.format(vlan_id))
                continue
            lines = self._group_lines(self._common(groups, have[vlan_id]), {}, True)
            if lines:
                self.commands.append(self._tmplt.render({"vlan_id": vlan_id}, "vlan", False))
                self.commands.extend(lines)

    @staticmethod
    def _common(want, have):
        """The (group, source, interface) triplets of want that exist in have."""
        common = {}
        for key, interfaces in want.items():
            present = [i for i in interfaces if i in have.get(key, [])]
            if present:
                common[key] = present
        return common
