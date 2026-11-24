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
import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.igmp_snooping.igmp_snooping import (
    GLOBAL_DEFAULTS,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.igmp_snooping import (
    IgmpSnoopingTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


GROUP_TIMEOUT = "group_timeout"
GROUP_TIMEOUT_NEVER = "never"
GROUP_TIMEOUT_MAX = 10080
VLAN_ID_MAX = 4094
NO_VLAN_CONFIGURATION = "no vlan configuration {0}"
PROXY = "proxy"

# range of the numeric global settings
GLOBAL_RANGES = {
    "max_gq_miss": (3, 5),
    "syslog_threshold": (1, 100),
    "holddown_timer": (1, 300),
}

# on/off settings of a `vlan configuration` block with the value NX-OS assumes
# when the block does not show the line
VLAN_BOOLEANS = {
    "snooping": True,
    "link_local_groups_suppression": True,
    "report_suppression": True,
    "v3_report_suppression": False,
    "explicit_tracking": True,
    "fast_leave": False,
    "proxy_leave_use_group_address": False,
}

# numeric settings of a block: (minimum, maximum, default), no default means
# that the device does not show the setting until it is configured
VLAN_NUMBERS = {
    "querier_timeout": (1, 65535, 255),
    "query_interval": (1, 18000, 125),
    "query_max_response_time": (1, 25, 10),
    "startup_query_count": (1, 10, None),
    "startup_query_interval": (1, 18000, None),
    "robustness_variable": (1, 7, 2),
    "last_member_query_interval": (1, 25, 1),
    "version": (2, 3, 3),
}

MRT_RANGE = (1, 25)
# the device removes the proxy line when mrt has its default value
MRT_DEFAULT = 5
POLICY_KEYWORDS = {"route_map": "route-map", "prefix_list": "prefix-list"}
POLICY_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,63}$")
INTERFACE_NAME_RE = re.compile(
    r"^(?:(?:Eth|Ethernet)[0-9]+(?:/[0-9]+){1,3}(?:\.[0-9]+)?|"
    r"(?:Vl|Vlan)[0-9]+|(?:Lo|loopback)[0-9]+|"
    r"(?:Po|port-channel)[0-9]+(?:\.[0-9]+)?|(?:Nv|Nve)[0-9]+)$",
    re.IGNORECASE | re.ASCII,
)


class IgmpSnooping(ResourceModule):
    """
    The nxos_igmp_snooping config class
    """

    def __init__(self, module):
        super(IgmpSnooping, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="igmp_snooping",
            tmplt=IgmpSnoopingTemplate(),
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

        self._global_commands(targets, have_globals)

        if self.state == "deleted":
            self._deleted_vlans(want_vlans, have_vlans, bool(self.want))
        else:
            self._vlan_commands(want_vlans, have_vlans)

    # normalisation

    def _normalize(self, cfg):
        """Return the global settings and the VLANs as {vlan_id: {"values": {...}, "items": {...}}}."""
        cfg = cfg or {}
        settings = {k: v for k, v in cfg.items() if k not in ("vlans", PROXY) and v is not None}
        self._check_numbers(settings, GLOBAL_RANGES)
        if GROUP_TIMEOUT in settings:
            settings[GROUP_TIMEOUT] = self._group_timeout(settings[GROUP_TIMEOUT])
        self._add_proxy(settings, cfg.get(PROXY))

        vlans = {}
        for vlan in cfg.get("vlans") or []:
            self._check_vlan_id(vlan["vlan_id"])
            known = vlans.setdefault(vlan["vlan_id"], {"values": {}, "items": {}})
            values, items = self._vlan(vlan)
            known["values"].update(values)
            known["items"].update(items)
        return settings, vlans

    def _add_proxy(self, settings, proxy):
        """proxy becomes False when it is switched off, otherwise {"mrt": n or None}."""
        proxy = {k: v for k, v in (proxy or {}).items() if v is not None}
        if not proxy:
            return
        if proxy.get("general_queries") is False:
            if "mrt" in proxy:
                self._module.fail_json(
                    msg="proxy mrt cannot be combined with general_queries false",
                )
            settings[PROXY] = False
        elif proxy.get("general_queries") is None:
            self._module.fail_json(msg="proxy mrt requires general_queries: true")
        else:
            if "mrt" in proxy:
                self._check_range("proxy mrt", proxy["mrt"], MRT_RANGE)
                if proxy["mrt"] == MRT_DEFAULT:
                    self._module.fail_json(
                        msg="proxy mrt {0} is the default and removes the proxy, omit mrt instead".format(
                            MRT_DEFAULT,
                        ),
                    )
            settings[PROXY] = {"mrt": proxy.get("mrt")}

    def _check_range(self, what, value, limits):
        if isinstance(value, bool) or not limits[0] <= value <= limits[1]:
            self._module.fail_json(
                msg="{0} must be in the range {1}-{2}, got '{3}'".format(
                    what,
                    limits[0],
                    limits[1],
                    value,
                ),
            )

    def _check_numbers(self, values, limits):
        for key, limit in limits.items():
            if key in values:
                self._check_range(key, values[key], limit[:2])

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
        if isinstance(vlan_id, bool) or not 1 <= vlan_id <= VLAN_ID_MAX:
            self._module.fail_json(
                msg="vlan_id must be in the range 1-{0}, got '{1}'".format(VLAN_ID_MAX, vlan_id),
            )

    def _policy_name(self, value):
        if not isinstance(value, str) or not POLICY_NAME_RE.fullmatch(value):
            self._module.fail_json(
                msg="policy name must be 1-63 characters using only letters, numbers, '_', '-', or '.'",
            )
        return value

    def _normalize_interface(self, value, what):
        if not isinstance(value, str) or not INTERFACE_NAME_RE.fullmatch(value):
            self._module.fail_json(
                msg="{0} must be a valid NX-OS interface name".format(what),
            )
        normalized = normalize_interface(value)
        if not normalized or not INTERFACE_NAME_RE.fullmatch(normalized):
            self._module.fail_json(
                msg="{0} must be a valid NX-OS interface name".format(what),
            )
        return normalized

    def _address(self, value, what):
        try:
            return ipaddress.IPv4Address(value)
        except ValueError:
            self._module.fail_json(msg="{0} must be an IPv4 address, got '{1}'".format(what, value))

    def _vlan(self, vlan):
        """Split the settings of a VLAN into plain values and the lines it can have several of."""
        values = {}
        for key in list(VLAN_BOOLEANS) + list(VLAN_NUMBERS) + ["querier", GROUP_TIMEOUT]:
            if vlan.get(key) is not None:
                values[key] = vlan[key]
        self._check_numbers(values, VLAN_NUMBERS)
        if GROUP_TIMEOUT in values:
            values[GROUP_TIMEOUT] = self._group_timeout(values[GROUP_TIMEOUT])
        if "querier" in values:
            values["querier"] = str(self._address(values["querier"], "querier"))
        self._add_proxy(values, vlan.get(PROXY))

        items = {}
        self._static_group_items(items, vlan.get("static_groups"))
        for name in vlan.get("mrouter_interfaces") or []:
            name = self._normalize_interface(name, "mrouter interface")
            items[("mrouter", name)] = ("mrouter", {"interface": name})
        self._report_flood_items(items, vlan.get("report_flood"))
        self._policy_items(items, vlan.get("report_policy"), "report_policy")
        self._policy_items(items, vlan.get("access_group"), "access_group")
        self._check_policy_interfaces(items)
        return values, items

    def _check_policy_interfaces(self, items):
        """The device keeps one policy per interface, a second one replaces the first."""
        seen = set()
        for key in items:
            if key[0] in ("report_policy", "access_group_interface"):
                if key[3] in seen:
                    self._module.fail_json(
                        msg="report_policy and access_group can have only one entry per interface, "
                        "'{0}' is used more than once".format(key[3]),
                    )
                seen.add(key[3])

    def _static_group_items(self, items, static_groups):
        for entry in static_groups or []:
            group = self._address(entry["group"], "group")
            if not group.is_multicast:
                self._module.fail_json(
                    msg="group must be a multicast address, got '{0}'".format(entry["group"]),
                )
            source = entry.get("source")
            if source:
                source = str(self._address(source, "source"))
            for name in entry["interfaces"]:
                name = self._normalize_interface(name, "static group interface")
                data = {"group": str(group), "interface": name}
                parser = "static_group"
                if source:
                    data["source"] = source
                    parser = "static_group_source"
                items[(parser, str(group), source or "", name)] = (parser, data)

    def _report_flood_items(self, items, report_flood):
        report_flood = report_flood or {}
        if report_flood.get("all"):
            items[("report_flood_all",)] = ("report_flood_all", {})
        for name in report_flood.get("interfaces") or []:
            name = self._normalize_interface(name, "report flood interface")
            items[("report_flood_interface", name)] = (
                "report_flood_interface",
                {"interface": name},
            )

    def _policy_items(self, items, policies, kind):
        for entry in policies or []:
            policy_type = POLICY_KEYWORDS[entry["policy_type"]]
            name = self._policy_name(entry["name"])
            interface = entry.get("interface")
            if interface:
                interface = self._normalize_interface(interface, "policy interface")
                data = {"policy_type": policy_type, "name": name, "interface": interface}
                parser = kind if kind == "report_policy" else "access_group_interface"
            elif kind == "access_group" and policy_type == "route-map":
                data = {"name": name}
                parser = "access_group"
            else:
                self._module.fail_json(
                    msg="{0} {1} requires an interface".format(kind, entry["policy_type"]),
                )
            items[(parser, policy_type, name, interface or "")] = (parser, data)

    # globals

    def _targets(self, want):
        """The value each global setting must end up with.

        merged and rendered only act on what was given, replaced and
        overridden reset everything else to the NX-OS default.
        """
        if self.state in ["replaced", "overridden"]:
            targets = dict(GLOBAL_DEFAULTS)
            targets.update({GROUP_TIMEOUT: None, PROXY: False})
            targets.update(want)
            return targets
        return dict(want)

    @staticmethod
    def _deleted_targets(want, has_config):
        """Without config every setting is reset, otherwise the listed ones."""
        scope = want if has_config else dict(GLOBAL_DEFAULTS, **{GROUP_TIMEOUT: None, PROXY: False})
        defaults = dict(GLOBAL_DEFAULTS, **{GROUP_TIMEOUT: None, PROXY: False})
        return {key: defaults.get(key) for key in scope}

    def _global_commands(self, targets, have):
        """group-timeout is sent after the other settings, except when snooping ends up
        disabled, then it goes first.
        """
        for key, default in GLOBAL_DEFAULTS.items():
            if key in targets:
                self._value_command(key, key, targets[key], have.get(key), default)
        if PROXY in targets:
            self._proxy_command("", targets[PROXY], have.get(PROXY, False), self.commands)
        if GROUP_TIMEOUT in targets:
            timeout = []
            self._value_command(
                GROUP_TIMEOUT,
                GROUP_TIMEOUT,
                targets[GROUP_TIMEOUT],
                have.get(GROUP_TIMEOUT),
                None,
                timeout,
            )
            snooping = targets.get("snooping", have.get("snooping", GLOBAL_DEFAULTS["snooping"]))
            if snooping:
                self.commands.extend(timeout)
            else:
                self.commands[:0] = timeout

    def _value_command(self, key, parser, target, current, default, commands=None):
        """Set key to target; target equal to the default removes the line the device shows."""
        commands = self.commands if commands is None else commands
        if target is None:
            target = default
        if target == current:
            return
        if isinstance(target, bool):
            commands.append(self._tmplt.render({key: target}, parser, not target))
        elif target == default and current is not None:
            commands.append(self._tmplt.render({key: current}, parser, True))
        else:
            commands.append(self._tmplt.render({key: target}, parser, False))

    def _proxy_command(self, prefix, target, current, commands):
        if target == current:
            return
        if target is False:
            commands.append(self._tmplt.render({}, prefix + PROXY, True))
        elif target.get("mrt") is None:
            commands.append(self._tmplt.render({}, prefix + PROXY, False))
        else:
            commands.append(self._tmplt.render({PROXY: target}, prefix + "proxy_mrt", False))

    # VLANs

    def _vlan_commands(self, want, have):
        """merged and rendered add, replaced and overridden make the listed
        VLANs identical to want, overridden also drops the unlisted ones.
        """
        prune = self.state in ["replaced", "overridden"]
        for vlan_id, wanted in want.items():
            if prune and not wanted["values"] and not wanted["items"]:
                # an empty want means no block at all
                self._remove_block(vlan_id, have)
            else:
                self._vlan_block(vlan_id, wanted, have.get(vlan_id), prune)

        if self.state == "overridden":
            for vlan_id in [v for v in have if v not in want]:
                self._remove_block(vlan_id, have)

    def _remove_block(self, vlan_id, have):
        if vlan_id in have:
            self.commands.append(NO_VLAN_CONFIGURATION.format(vlan_id))

    def _vlan_block(self, vlan_id, want, have, prune):
        """The block is only entered when it has something to change."""
        have = have or {"values": {}, "items": {}}
        lines = []
        if prune:
            lines.extend(self._item_lines(have["items"], want["items"], True))
        lines.extend(self._item_lines(want["items"], have["items"], False))
        self._value_lines(lines, want["values"], have["values"], prune)
        self._enter(vlan_id, lines)

    def _enter(self, vlan_id, lines):
        if lines:
            self.commands.append(self._tmplt.render({"vlan_id": vlan_id}, "vlan", False))
            self.commands.extend(lines)

    def _item_lines(self, source, other, negate):
        """Commands for the lines of source that other does not have."""
        return [
            self._tmplt.render(data, parser, negate)
            for key, (parser, data) in source.items()
            if key not in other
        ]

    def _value_lines(self, lines, want, have, prune):
        """Build VLAN value commands for the requested state."""
        defaults = dict(VLAN_BOOLEANS)
        defaults.update({key: limits[2] for key, limits in VLAN_NUMBERS.items()})
        defaults.update({"querier": None, GROUP_TIMEOUT: None})
        if prune:
            self._prune_value_lines(lines, want, have, defaults)
            return
        self._merge_value_lines(lines, want, have, defaults)

    def _prune_value_lines(self, lines, want, have, defaults):
        """Reset omitted values to defaults and apply requested values."""
        for key, default in defaults.items():
            if key not in want:
                current = have.get(key, default)
                self._value_command(key, "vlan_" + key, default, current, default, lines)
        proxy = want.get(PROXY, False)
        self._proxy_command("vlan_", proxy, have.get(PROXY, False), lines)
        for key, target in want.items():
            if key in defaults:
                default = defaults[key]
                current = have.get(key, default)
                self._value_command(key, "vlan_" + key, target, current, default, lines)

    def _merge_value_lines(self, lines, want, have, defaults):
        """Apply only VLAN values explicitly present in the request."""
        for key, default in defaults.items():
            if key not in want:
                continue
            current = have.get(key) if self.state == "rendered" else have.get(key, default)
            self._value_command(key, "vlan_" + key, want[key], current, default, lines)
        if PROXY in want:
            self._proxy_command("vlan_", want[PROXY], have.get(PROXY, False), lines)

    def _deleted_vlans(self, want, have, has_config):
        """A listed VLAN without settings is removed as a whole, one with
        settings only loses those. Without config all of them go.
        """
        if not has_config:
            want = {vlan_id: {"values": {}, "items": {}} for vlan_id in have}
        for vlan_id, wanted in want.items():
            if vlan_id not in have:
                continue
            if not wanted["values"] and not wanted["items"]:
                self.commands.append(NO_VLAN_CONFIGURATION.format(vlan_id))
                continue
            existing = have[vlan_id]
            remaining_values = set(existing["values"]) - set(wanted["values"])
            remaining_items = set(existing["items"]) - set(wanted["items"])
            if not remaining_values and not remaining_items:
                self.commands.append(NO_VLAN_CONFIGURATION.format(vlan_id))
                continue
            present = {
                key: item for key, item in wanted["items"].items() if key in have[vlan_id]["items"]
            }
            lines = self._item_lines(present, {}, True)
            targets = {key: self._vlan_default(key) for key in wanted["values"]}
            self._value_lines(lines, targets, have[vlan_id]["values"], False)
            self._enter(vlan_id, lines)

    @staticmethod
    def _vlan_default(key):
        """The value of a plain setting after its line is removed."""
        if key in VLAN_BOOLEANS:
            return VLAN_BOOLEANS[key]
        if key in VLAN_NUMBERS:
            return VLAN_NUMBERS[key][2]
        return False if key == PROXY else None
