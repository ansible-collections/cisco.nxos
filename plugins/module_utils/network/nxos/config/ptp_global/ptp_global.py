# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_ptp_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import ipaddress
import re

from copy import deepcopy
from decimal import Decimal, InvalidOperation

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ptp_global import (
    Ptp_globalTemplate,
)


# values the device does not display because they are the default
DEFAULTS = {
    "domain": 0,
    "priority1": 255,
    "priority2": 255,
    "mean_path_delay": 1000000000,
    ("correction_range", "value"): 100000,
    ("ipv6_multicast_scope", "rx"): "0x1-0xE",
    ("ipv6_multicast_scope", "tx"): "0x1",
}
# settings that are on by default: the device displays `no ptp management` when it is off
DEFAULT_ON = ("management",)

# numeric ranges, (minimum, maximum)
RANGES = {
    "domain": (0, 127),
    "priority1": (0, 255),
    "priority2": (0, 255),
    "mean_path_delay": (10, 1000000000),
    ("correction_range", "value"): (10, 1000000000),
    ("clock_periodic_update", "interval"): (0, 3600),
    ("time_distribution_hold", "correction_threshold"): (1, 100000),
    ("time_distribution_hold", "delay_threshold"): (1, 5000),
}
TOLERANCE_RANGE = (Decimal("1.0"), Decimal("100.0"))
HIGH_CORRECTION_INTERVAL = (1, 300)
IMMEDIATE = "immediate"
# the interval of the periodic update that the device does not display
CLOCK_UPDATE_DEFAULT_INTERVAL = 60
SCOPE_RX = re.compile(r"^0x[1-9A-E](?:[-,]0x[1-9A-E])*$")
SCOPE_TX = re.compile(r"^0x[1-9A-E]$")

# on/off settings that have no default, they are only displayed when they are on
FLAGS = (
    "unicast_negotiation",
    ("correction_range", "logging"),
    ("notification", "gm_change"),
    ("notification", "parent_change"),
    ("notification", "port_state_change"),
)
# settings made of one line that is displayed with the values that are set
GROUPS = ("notification.high_correction", "clock_periodic_update", "time_distribution_hold")


def _path(key):
    return key if isinstance(key, tuple) else (key,)


def _get(cfg, key):
    value = cfg
    for part in _path(key):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def _set(cfg, key, value):
    parts = _path(key)
    for part in parts[:-1]:
        cfg = cfg.setdefault(part, {})
    cfg[parts[-1]] = value


def _drop(cfg, key):
    """Remove a value and the dicts that become empty."""
    parts = _path(key)
    chain = [cfg]
    for part in parts[:-1]:
        if part not in chain[-1] or not isinstance(chain[-1][part], dict):
            return
        chain.append(chain[-1][part])
    chain[-1].pop(parts[-1], None)
    for part, parent in zip(reversed(parts[:-1]), reversed(chain[:-1])):
        if not parent[part]:
            del parent[part]


class Ptp_global(ResourceModule):
    """
    The nxos_ptp_global config class
    """

    def __init__(self, module):
        super(Ptp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="ptp_global",
            tmplt=Ptp_globalTemplate(),
        )
        self.parsers = [
            "source.ipv4",
            "source.ipv6",
            "domain",
            "priority1",
            "priority2",
            "mean_path_delay",
            "unicast_negotiation",
            "ipv6_multicast_scope.rx",
            "ipv6_multicast_scope.tx",
            "correction_range.value",
            "correction_range.logging",
            "delay_tolerance.mean_path",
            "delay_tolerance.reverse_path",
            "notification.gm_change",
            "notification.parent_change",
            "notification.port_state_change",
        ] + list(GROUPS)

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
        wantd, resets = self._normalize(self.want, strict=True)
        haved, _unused = self._normalize(self.have, strict=False)

        # a setting that is given with its default value, or switched off, is removed
        # from what the device has, the other settings are kept
        if self.state == "merged":
            for key in resets:
                _drop(haved, key)
            wantd = dict_merge(haved, wantd)
            haved = self._normalize(self.have, strict=False)[0]

        if self.state == "deleted":
            wantd = {}

        self.compare(parsers=self.parsers, want=wantd, have=haved)
        self._compare_management(wantd, haved)

    def _compare_management(self, want, have):
        """management is on by default: only `no ptp management` is displayed, and the
        comparison of the base class skips a False that the device does not have.
        """
        if want.get("management") is False and have.get("management") is not False:
            self.addcmd(want, "management", True)
        elif "management" not in want and have.get("management") is False:
            self.addcmd(have, "management", False)

    # normalisation

    def _normalize(self, cfg, strict):
        """Return the configuration with everything that the device does not display
        removed, and the list of the settings the user wants to see removed.

        The values are only validated for what the user gives (strict).
        """
        cfg = deepcopy(cfg) if cfg else {}
        resets = []
        self._clean_none(cfg)
        self._normalize_source(cfg, strict)
        self._normalize_scope(cfg, strict)

        for key, (low, high) in RANGES.items():
            value = _get(cfg, key)
            if value is not None and strict and not low <= value <= high:
                self._fail(
                    "{0} must be in the range {1}-{2}, got '{3}'".format(
                        ".".join(_path(key)),
                        low,
                        high,
                        value,
                    ),
                )
        for key, default in DEFAULTS.items():
            if _get(cfg, key) == default:
                _drop(cfg, key)
                resets.append(key)

        for key in DEFAULT_ON:
            if cfg.get(key) is True:
                _drop(cfg, key)
                resets.append(key)
        for key in FLAGS:
            if _get(cfg, key) is False:
                _drop(cfg, key)
                resets.append(key)

        self._normalize_tolerance(cfg, strict)
        self._normalize_groups(cfg, resets, strict)
        return cfg, resets

    @staticmethod
    def _clean_none(cfg):
        for key in list(cfg):
            if isinstance(cfg[key], dict):
                Ptp_global._clean_none(cfg[key])
                if not cfg[key]:
                    del cfg[key]
            elif cfg[key] is None:
                del cfg[key]

    def _fail(self, msg):
        self._module.fail_json(msg=msg)

    def _normalize_source(self, cfg, strict):
        for family, version in (("ipv4", 4), ("ipv6", 6)):
            entry = cfg.get("source", {}).get(family)
            if entry is None:
                continue
            if "address" not in entry:
                self._fail("source {0} needs an address".format(family))
            if strict:
                try:
                    address = ipaddress.ip_address(entry["address"])
                except ValueError:
                    self._fail(
                        "source {0} address must be an IP address, got '{1}'".format(
                            family,
                            entry["address"],
                        ),
                    )
                if address.version != version:
                    self._fail(
                        "source {0} address must be an IPv{1} address, got '{2}'".format(
                            family,
                            version,
                            entry["address"],
                        ),
                    )
                entry["address"] = str(address)

    def _normalize_scope(self, cfg, strict):
        """The device displays the hexadecimal digits in upper case: 0xE."""
        for key, pattern in (("rx", SCOPE_RX), ("tx", SCOPE_TX)):
            value = _get(cfg, ("ipv6_multicast_scope", key))
            if value is None:
                continue
            value = re.sub(
                r"0[xX]([0-9a-fA-F]+)",
                lambda found: "0x" + found.group(1).upper(),
                str(value).replace(" ", ""),
            )
            if strict and not pattern.match(value):
                self._fail(
                    "ipv6_multicast_scope {0} must be {1}, got '{2}'".format(
                        key,
                        (
                            "a list of 0x1-0xe values such as 0x2-0x4,0x6"
                            if key == "rx"
                            else "one value from 0x1 to 0xe"
                        ),
                        value,
                    ),
                )
            _set(cfg, ("ipv6_multicast_scope", key), value)

    def _normalize_tolerance(self, cfg, strict):
        """delay tolerance values are shown with two decimals."""
        for key in ("mean_path", "reverse_path"):
            value = _get(cfg, ("delay_tolerance", key))
            if value is None:
                continue
            try:
                number = Decimal(str(value).strip())
                valid = number.is_finite() and TOLERANCE_RANGE[0] <= number <= TOLERANCE_RANGE[1]
            except InvalidOperation:
                valid = False
            if not valid:
                if strict:
                    self._fail(
                        "delay_tolerance {0} must be between 1.0 and 100.0, got '{1}'".format(
                            key,
                            value,
                        ),
                    )
                continue
            _set(cfg, ("delay_tolerance", key), "{0:.2f}".format(number))

    def _normalize_groups(self, cfg, resets, strict):
        """A group is one line: it is on when `enabled` is true or any of its values is given."""
        for name in GROUPS:
            key = tuple(name.split("."))
            group = _get(cfg, key)
            if group is None:
                continue
            enabled = group.pop("enabled", None)
            if enabled is False:
                _drop(cfg, key)
                resets.append(key)
                continue
            group["enabled"] = True
            if (
                name == "clock_periodic_update"
                and group.get("interval") == CLOCK_UPDATE_DEFAULT_INTERVAL
            ):
                del group["interval"]
                resets.append(("clock_periodic_update", "interval"))
            if name == "notification.high_correction" and "interval" in group and strict:
                self._check_high_correction(group)

    def _check_high_correction(self, group):
        value = str(group["interval"]).strip().lower()
        low, high = HIGH_CORRECTION_INTERVAL
        if value != IMMEDIATE and not (value.isdigit() and low <= int(value) <= high):
            self._fail(
                "notification high_correction interval must be '{0}' or a number in the range {1}-{2}, got '{3}'".format(
                    IMMEDIATE,
                    low,
                    high,
                    group["interval"],
                ),
            )
        group["interval"] = value
