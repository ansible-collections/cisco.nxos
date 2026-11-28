# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_netflow_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import ipaddress

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.netflow_global import (
    RECORD_FLAGS,
    Netflow_globalTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


KINDS = ("exporters", "records", "monitors")
SINGULAR = {"exporters": "exporter", "records": "record", "monitors": "monitor"}
# the default of the device for a global setting
DEFAULT_TIMEOUT = 10
# the settings of an exporter that the device does not display with their default value. The device
# removes them with a `no` command that must carry the value, so they are set to the default instead
EXPORTER_DEFAULTS = {
    "transport_udp": 9995,
    "dscp": 0,
    "template_data_timeout": 15,
    "option_exporter_stats_timeout": 0,
    "option_interface_table_timeout": 0,
}
# these are configured below `version 9`
VERSION_9_KEYS = (
    "template_data_timeout",
    "option_exporter_stats_timeout",
    "option_interface_table_timeout",
)
VERSION_9_COMMANDS = {
    "template_data_timeout": "template data timeout",
    "option_exporter_stats_timeout": "option exporter-stats timeout",
    "option_interface_table_timeout": "option interface-table timeout",
}
# numeric ranges, (minimum, maximum)
RANGES = {
    "timeout": (5, 60),
    "transport_udp": (1, 65535),
    "dscp": (0, 63),
    "template_data_timeout": (1, 86400),
    "option_exporter_stats_timeout": (0, 86400),
    "option_interface_table_timeout": (0, 86400),
}
# the order of the commands, the same as the device displays them
ORDER = {
    "exporters": [
        "description",
        "destination",
        "transport_udp",
        "source",
        "dscp",
    ]
    + list(VERSION_9_KEYS),
    "records": ["description"] + [name for name, _keyword in RECORD_FLAGS],
    "monitors": ["description", "record", "exporters"],
}
# the matches and collects that a Layer 2 record does not accept
LAYER_2_CONFLICTS = (
    "match.ip.",
    "match.ipv4.",
    "match.ipv6.",
    "match.transport.",
    "collect.transport_tcp_flags",
    "collect.ip_version",
)
# the records the device has, the name of a record that starts like this is not checked
PREDEFINED_RECORD_PREFIX = "netflow"
MAX_MONITOR_EXPORTERS = 2
# the default VRF is not displayed
DEFAULT_VRF = "default"


def _flatten(entity, prefix=""):
    """`{"match": {"ipv4": {"source_address": True}}}` becomes `{"match.ipv4.source_address": True}`.

    The destination of an exporter is one setting.
    """
    flat = {}
    for key, value in entity.items():
        if key == "name":
            continue
        if isinstance(value, dict) and key != "destination":
            flat.update(_flatten(value, prefix + key + "."))
        else:
            flat[prefix + key] = value
    return flat


def _interface(name):
    """The name as the device displays it: Ethernet1/1, loopback1, mgmt0, port-channel10, Vlan10."""
    name = normalize_interface(name)
    lowered = name.lower()
    for prefix in ("ethernet", "vlan"):
        if lowered.startswith(prefix):
            return prefix.capitalize() + lowered.replace(prefix, "", 1)
    return lowered if lowered.startswith(("loopback", "mgmt", "port-channel")) else name


def _nest(key, value):
    """The opposite of _flatten for one setting, what the templates are rendered from."""
    for part in reversed(key.split(".")):
        value = {part: value}
    return value


class Netflow_global(ResourceModule):
    """
    The nxos_netflow_global config class
    """

    def __init__(self, module):
        super(Netflow_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="netflow_global",
            tmplt=Netflow_globalTemplate(),
        )

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

        The order of the commands matters: the monitors are changed first when they lose a
        reference, then the entities that are not wanted are removed, then the exporters and
        the records are created or changed and last the monitors that use them.
        """
        want = self._normalize(self.want, strict=True)
        have = self._normalize(self.have, strict=False)

        if self.state in ("merged", "replaced", "overridden"):
            self._check_references(want, have)

        monitors_first = []
        deletes = {"monitors": [], "records": [], "exporters": []}
        changes = {"exporters": [], "records": [], "monitors": []}

        for kind in KINDS:
            for name in self._doomed(kind, want[kind], have[kind]):
                deletes[kind].append("no flow {0} {1}".format(SINGULAR[kind], name))
            if self.state == "deleted":
                continue
            for name, (entity, resets) in want[kind].items():
                current = have[kind].get(name)
                removes, adds, version_9 = self._diff(
                    kind,
                    name,
                    entity,
                    resets,
                    current[0] if current else {},
                )
                header = "flow {0} {1}".format(SINGULAR[kind], name)
                if kind == "monitors":
                    if removes:
                        monitors_first.extend([header] + removes)
                    commands = adds
                else:
                    commands = removes + adds
                    if version_9:
                        commands += ["version 9"] + version_9
                if commands or current is None:
                    changes[kind].extend([header] + commands)

        global_removals, global_changes = self._compare_timeout(want, have)

        self.commands = (
            monitors_first
            + deletes["monitors"]
            + deletes["records"]
            + deletes["exporters"]
            + global_removals
            + global_changes
            + changes["exporters"]
            + changes["records"]
            + changes["monitors"]
        )

    def _doomed(self, kind, wanted, existing):
        """The names of the entities that are removed."""
        if self.state == "overridden":
            return [name for name in existing if name not in wanted]
        if self.state != "deleted":
            return []
        if not self.want:
            return list(existing)
        missing = [name for name in wanted if name not in existing]
        if missing:
            self._module.warn(
                "the {0} {1} are not configured on the device, nothing is deleted for them".format(
                    kind,
                    ", ".join(missing),
                ),
            )
        return [name for name in wanted if name in existing]

    def _compare_timeout(self, want, have):
        wanted, reset = want["timeout"]
        current = have["timeout"][0]
        remove = ["no flow timeout"]
        change = ["flow timeout {0}".format(wanted)]
        if self.state == "deleted":
            if current is not None and (not self.want or "timeout" in self.want):
                return remove, []
        elif self.state == "merged":
            if wanted is not None and wanted != current:
                return [], change
            if reset and current is not None:
                return remove, []
        elif wanted is None and current is not None:
            return remove, []
        elif wanted is not None and wanted != current:
            return [], change
        return [], []

    # comparison of an entity

    def _diff(self, kind, name, wanted, resets, current):
        """Return the commands to remove, to add and to add below `version 9`."""
        desired = self._desired(kind, wanted, resets, current)
        if kind == "monitors" and len(desired.get("exporters", [])) > MAX_MONITOR_EXPORTERS:
            self._module.fail_json(
                msg="a monitor can have {0} exporters at most, got {1}".format(
                    MAX_MONITOR_EXPORTERS,
                    ", ".join(desired["exporters"]),
                ),
            )
        if kind == "records":
            self._check_record_type(dict(desired, name=name))

        removes, adds, version_9 = [], [], []
        self._removals(kind, desired, current, removes, version_9)
        self._additions(kind, desired, current, removes, adds, version_9)
        return removes, adds, version_9

    def _removals(self, kind, desired, current, removes, version_9):
        """The settings the device has and that are not wanted."""
        for key, value in self._ordered(kind, current).items():
            if key in desired or (kind == "monitors" and key == "record"):
                # the device has no command to remove the record of a monitor
                continue
            if key == "exporters":
                removes.extend(self._render(kind, key, item, True) for item in value)
            elif kind == "exporters" and key in VERSION_9_KEYS:
                version_9.append(self._default_command(key))
            else:
                removes.append(self._render(kind, key, value, True))

    def _additions(self, kind, desired, current, removes, adds, version_9):
        """The settings that are wanted and that the device does not have."""
        for key, value in self._ordered(kind, desired).items():
            if current.get(key) == value:
                continue
            if key == "exporters":
                old = current.get(key, [])
                adds.extend(
                    self._render(kind, key, item, False) for item in value if item not in old
                )
                removes.extend(
                    self._render(kind, key, item, True) for item in old if item not in value
                )
            elif kind == "exporters" and key in VERSION_9_KEYS:
                version_9.append("{0} {1}".format(VERSION_9_COMMANDS[key], value))
            else:
                if key == "destination" and "vrf" not in value and "vrf" in current.get(key, {}):
                    # the device keeps the VRF of the current destination unless it is given
                    value = dict(value, vrf=DEFAULT_VRF)
                adds.append(self._render(kind, key, value, False))

    def _desired(self, kind, wanted, resets, current):
        """The settings the entity has once the commands are applied."""
        if self.state != "merged":
            return dict(wanted)
        desired = dict(current)
        for key in resets:
            desired.pop(key, None)
        desired.update(wanted)
        if kind == "monitors" and "exporters" in wanted:
            old = current.get("exporters", [])
            desired["exporters"] = old + [item for item in wanted["exporters"] if item not in old]
        return desired

    def _check_record_type(self, settings):
        """A record is of one type, the device refuses the fields of another one."""
        name = settings.get("name", "")
        if any(key.startswith("match.datalink.") for key in settings) and any(
            key.startswith(LAYER_2_CONFLICTS) for key in settings
        ):
            self._module.fail_json(
                msg="record {0}: the datalink (Layer 2) matches cannot be mixed with the ip, ipv4, ipv6 or "
                "transport matches, or with collecting the TCP flags or the IP version".format(
                    name,
                ),
            )
        if any(key.startswith("match.ipv4.") for key in settings) and any(
            key.startswith("match.ipv6.") for key in settings
        ):
            self._module.fail_json(
                msg="record {0}: the ipv4 and ipv6 matches cannot be mixed".format(name),
            )

    def _check_references(self, want, have):
        """The monitors can only use the exporters and records that exist once the
        commands are applied, the device would stop in the middle of the configuration.
        """
        for kind in ("exporters", "records"):
            if self.state == "overridden":
                known = set(want[kind])
            else:
                known = set(want[kind]) | set(have[kind])
            for name, (monitor, _resets) in want["monitors"].items():
                used = (
                    monitor.get("exporters", []) if kind == "exporters" else [monitor.get("record")]
                )
                for item in used:
                    if item is None or item in known:
                        continue
                    if kind == "records" and item.startswith(PREDEFINED_RECORD_PREFIX):
                        continue
                    self._module.fail_json(
                        msg="monitor {0} uses the {1} '{2}' that does not exist".format(
                            name,
                            SINGULAR[kind],
                            item,
                        ),
                    )

    @staticmethod
    def _ordered(kind, settings):
        order = ORDER[kind]
        return dict((key, settings[key]) for key in order if key in settings)

    @staticmethod
    def _default_command(key):
        return "{0} {1}".format(VERSION_9_COMMANDS[key], EXPORTER_DEFAULTS[key])

    def _render(self, kind, key, value, negate):
        parser = "{0}.{1}".format(SINGULAR[kind], key)
        data = {"exporter": value} if key == "exporters" else _nest(key, value)
        return self._tmplt.render(data, parser, negate)

    # normalisation

    def _normalize(self, cfg, strict):
        """Return the configuration as {kind: {name: (settings, resets)}}, the settings are flat
        dicts without what the device does not display. `resets` are the settings that the user
        gives with their default value or switched off, they are removed from the device.

        The values are only validated for what the user gives (strict).
        """
        cfg = deepcopy(cfg) if cfg else {}
        result = {}
        timeout = cfg.get("timeout")
        reset = False
        if timeout is not None:
            self._check_range("timeout", timeout, strict)
            if timeout == DEFAULT_TIMEOUT:
                timeout, reset = None, True
        result["timeout"] = (timeout, reset)

        for kind in KINDS:
            entities = {}
            for entity in cfg.get(kind) or []:
                name = entity["name"]
                if name in entities:
                    self._module.fail_json(
                        msg="{0} '{1}' is given more than once".format(SINGULAR[kind], name),
                    )
                entities[name] = self._normalize_entity(kind, entity, strict)
            result[kind] = entities
        return result

    def _check_range(self, key, value, strict):
        low, high = RANGES[key]
        if strict and not low <= value <= high:
            self._module.fail_json(
                msg="{0} must be in the range {1}-{2}, got '{3}'".format(key, low, high, value),
            )

    def _normalize_entity(self, kind, entity, strict):
        flat = _flatten(entity)
        resets = set()
        for key in list(flat):
            value = flat[key]
            if value is None:
                del flat[key]
            elif value is False:
                del flat[key]
                resets.add(key)
            elif key in RANGES:
                self._check_range(key, value, strict)
        if kind == "exporters":
            self._normalize_exporter(flat, resets, strict)
        if kind == "monitors" and "exporters" in flat:
            flat["exporters"] = list(dict.fromkeys(flat["exporters"]))
        return flat, resets

    def _normalize_exporter(self, flat, resets, strict):
        for key, default in EXPORTER_DEFAULTS.items():
            if flat.get(key) == default:
                del flat[key]
                resets.add(key)
        if "source" in flat:
            flat["source"] = _interface(flat["source"])
        destination = flat.get("destination")
        if not destination:
            return
        if strict:
            try:
                ipaddress.ip_address(destination["address"])
            except ValueError:
                self._module.fail_json(
                    msg="destination address must be an IPv4 or IPv6 address, got '{0}'".format(
                        destination["address"],
                    ),
                )
        destination = dict(destination)
        if destination.get("vrf") in (None, DEFAULT_VRF):
            destination.pop("vrf", None)
        flat["destination"] = destination
