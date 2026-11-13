# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_ptp_interfaces config file.
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ptp_interfaces import (
    Ptp_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


# the interval lines: (minimum, maximum) without a profile and for each profile, and the default
# of the plain form, which the device does not display
INTERVALS = {
    "announce_interval": ({None: (0, 4), "aes67": (0, 4), "smpte_2059_2": (-3, 1)}, 1),
    "announce_timeout": ({None: (2, 4), "aes67": (2, 10), "smpte_2059_2": (2, 10)}, 3),
    "sync_interval": ({None: (-3, 1), "aes67": (-4, 1), "smpte_2059_2": (-7, 0)}, -2),
    "delay_request_interval": ({None: (-1, 6), "aes67": (-4, 5), "smpte_2059_2": (-4, 5)}, 0),
}
VLAN_RANGE = (1, 4094)
DELAY_RANGE = (1, 512000000)
# settings with the value the device assumes when the line is not displayed
DEFAULTS = {"role": "dynamic", "transport": "ipv4", "transmission": "multicast"}
# several of these lines can exist on an interface
ADDRESS_LISTS = ("master", "slave")
# everything but `ptp` itself
SETTINGS = (
    "role",
    "transmission",
    "transport",
    "vlan",
    "asymmetric_delay",
    "announce_interval",
    "announce_timeout",
    "sync_interval",
    "delay_request_interval",
    "peer",
    "ucast_source",
) + ADDRESS_LISTS
UCAST_FAMILIES = (("ipv4", 4), ("ipv6", 6))


def _clean_none(value):
    if isinstance(value, dict):
        cleaned = {k: _clean_none(v) for k, v in value.items() if v is not None}
        return {k: v for k, v in cleaned.items() if v not in ({}, [])}
    if isinstance(value, list):
        return [_clean_none(v) for v in value if v is not None]
    return value


class Ptp_interfaces(ResourceModule):
    """
    The nxos_ptp_interfaces config class
    """

    def __init__(self, module):
        super(Ptp_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="ptp_interfaces",
            tmplt=Ptp_interfacesTemplate(),
        )
        self.parsers = [
            "enabled",
            "role",
            "transmission",
            "transport",
            "vlan",
            "asymmetric_delay",
            "delay_request_interval",
            "announce_interval",
            "announce_timeout",
            "sync_interval",
        ]

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
        wantd = {
            normalize_interface(entry["name"]): self._normalize(entry, True) for entry in self.want
        }
        haved = {
            normalize_interface(entry["name"]): self._normalize(entry, False)[0]
            for entry in self.have
        }

        if self.state == "deleted":
            for name in list(wantd) if wantd else list(haved):
                self._interface(name, {}, haved.get(name, {}), prune=True)
            return

        prune = self.state in ["replaced", "overridden"]
        for name, (want, resets) in wantd.items():
            self._interface(name, *self._prepare(name, want, resets, haved.get(name, {})), prune)

        if self.state == "overridden":
            for name, have in haved.items():
                if name not in wantd:
                    self._interface(name, {}, have, prune=True)

    def _prepare(self, name, want, resets, have):
        """Check what the user gave and return (want, have), merged lets the device keep what is not given."""
        merged = self.state == "merged"
        if "enabled" in want:
            enabled = want["enabled"]
        else:
            enabled = have.get("enabled") and merged
        self._check_dependencies(name, want, enabled)
        if merged:
            want = self._merge(have, want, resets)
        self._check_role(name, want)
        return want, have

    # normalisation

    def _fail(self, msg):
        self._module.fail_json(msg=msg)

    def _normalize(self, entry, strict):
        """Return the interface with everything the device does not display removed, and the
        names of the settings the user wants to see removed.

        The values are only validated for what the user gives (strict).
        """
        cfg = _clean_none(deepcopy(entry))
        cfg["name"] = normalize_interface(cfg["name"])
        resets = []
        name = cfg["name"]
        if strict:
            self._validate(name, cfg)

        for key, default in DEFAULTS.items():
            if cfg.get(key) == default:
                del cfg[key]
                resets.append(key)
        for key, (_ranges, default) in INTERVALS.items():
            if cfg.get(key) == {"value": default}:
                del cfg[key]
                resets.append(key)
        self._normalize_addresses(name, cfg, strict)
        if cfg.get("enabled") is False:
            resets.append("enabled")
        return cfg, resets

    def _address(self, name, key, value, strict, version=None):
        """The address as the device displays it, an address that cannot be read is kept as it is."""
        try:
            address = ipaddress.ip_address(value)
        except ValueError:
            if strict:
                self._fail("{0}: {1} must be an IP address, got '{2}'".format(name, key, value))
            return value
        if version and address.version != version and strict:
            self._fail(
                "{0}: {1} must be an IPv{2} address, got '{3}'".format(name, key, version, value),
            )
        return str(address)

    def _normalize_addresses(self, name, cfg, strict):
        for key in ADDRESS_LISTS:
            if key in cfg:
                cfg[key] = sorted({self._address(name, key, item, strict) for item in cfg[key]})
        if "peer" in cfg:
            cfg["peer"] = self._address(name, "peer", cfg["peer"], strict)
        for family, version in UCAST_FAMILIES:
            if family in cfg.get("ucast_source", {}):
                cfg["ucast_source"][family] = self._address(
                    name,
                    "ucast_source " + family,
                    cfg["ucast_source"][family],
                    strict,
                    version,
                )

    def _validate(self, name, cfg):
        if "vlan" in cfg and not VLAN_RANGE[0] <= cfg["vlan"] <= VLAN_RANGE[1]:
            self._fail(
                "{0}: vlan must be in the range {1}-{2}, got '{3}'".format(
                    name,
                    VLAN_RANGE[0],
                    VLAN_RANGE[1],
                    cfg["vlan"],
                ),
            )
        self._validate_intervals(name, cfg)
        self._validate_delay(name, cfg.get("asymmetric_delay", {}))

    def _validate_intervals(self, name, cfg):
        profiles = set()
        for key, (ranges, _default) in INTERVALS.items():
            if key not in cfg:
                continue
            profile = cfg[key].get("profile")
            low, high = ranges[profile]
            value = cfg[key]["value"]
            if not low <= value <= high:
                self._fail(
                    "{0}: {1}{2} must be in the range {3}-{4}, got '{5}'".format(
                        name,
                        key,
                        " with the profile {0}".format(profile) if profile else "",
                        low,
                        high,
                        value,
                    ),
                )
            profiles.add(profile)
        if len(profiles - {None}) > 1:
            self._fail(
                "{0}: the aes67 and smpte_2059_2 profiles cannot be mixed on one interface".format(
                    name,
                ),
            )

    def _validate_delay(self, name, delay):
        if len(delay) > 1:
            self._fail(
                "{0}: asymmetric_delay can only have one of forward_path and reverse_path".format(
                    name,
                ),
            )
        for key, value in delay.items():
            if not DELAY_RANGE[0] <= value <= DELAY_RANGE[1]:
                self._fail(
                    "{0}: asymmetric_delay {1} must be in the range {2}-{3}, got '{4}'".format(
                        name,
                        key,
                        DELAY_RANGE[0],
                        DELAY_RANGE[1],
                        value,
                    ),
                )

    def _check_dependencies(self, name, want, enabled):
        """The device needs `ptp` on the interface before any other ptp command."""
        settings = [key for key in SETTINGS if key in want]
        if settings and enabled is not True:
            self._fail(
                "{0}: {1} can only be configured on an interface with ptp, set enabled to true".format(
                    name,
                    ", ".join(settings),
                ),
            )

    def _check_role(self, name, want):
        if (
            want.get("enabled")
            and want.get("role") == "slave"
            and want.get("transmission", {}).get("mode") != "unicast"
        ):
            self._fail("{0}: the role slave needs the transmission mode unicast".format(name))

    @staticmethod
    def _merge(have, want, resets):
        """Layer want on top of what the device has: a setting that is given with its default
        value, or enabled false, is removed first.
        """
        merged = deepcopy(have)
        for key in resets:
            merged.pop(key, None)
        for key, value in want.items():
            if key in ADDRESS_LISTS:
                merged[key] = sorted(set(merged.get(key, [])) | set(value))
            elif key == "ucast_source":
                merged[key] = {**merged.get(key, {}), **value}
            else:
                merged[key] = value
        return merged

    # commands

    def _interface(self, name, want, have, prune):
        """The commands of one interface, `no ptp` removes all the ptp lines of the interface."""
        begin = len(self.commands)
        if not want.get("enabled"):
            if have.get("enabled"):
                self.addcmd({"enabled": True}, "enabled", True)
        else:
            self._profile_switches(want, have)
            self.compare(parsers=self.parsers, want=want, have=have)
            self._compare_addresses(want, have, prune)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render({"name": name}, "name", False))

    def _profile_switches(self, want, have):
        """Another profile on the port is rejected: the old line goes first."""
        for key in INTERVALS:
            old = have.get(key, {}).get("profile")
            new = want.get(key, {}).get("profile")
            if old and new and old != new:
                self.addcmd(have, key, True)

    def _compare_addresses(self, want, have, prune):
        for key in ADDRESS_LISTS:
            wanted = set(want.get(key, []))
            current = set(have.get(key, []))
            for address in sorted(wanted - current):
                self.addcmd({"address": address}, key)
            if prune:
                for address in sorted(current - wanted):
                    self.addcmd({"address": address}, key, True)
        self._compare_peer(want.get("peer"), have.get("peer"), prune)
        self._compare_sources(want.get("ucast_source", {}), have.get("ucast_source", {}), prune)

    def _compare_peer(self, wanted, current, prune):
        """Only one peer is possible, the old one has to go first."""
        if wanted == current:
            return
        if current and (wanted or prune):
            self.addcmd({"peer": current}, "peer", True)
        if wanted:
            self.addcmd({"peer": wanted}, "peer")

    def _compare_sources(self, wanted, current, prune):
        """One source for each address family, a new address replaces the old one."""
        for family, _version in UCAST_FAMILIES:
            if wanted.get(family):
                if wanted[family] != current.get(family):
                    self.addcmd({"address": wanted[family]}, "ucast_source")
            elif prune and current.get(family):
                self.addcmd({"address": current[family]}, "ucast_source", True)
