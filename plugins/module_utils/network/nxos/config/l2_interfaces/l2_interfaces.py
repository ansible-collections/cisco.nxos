#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_l2_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

import re

from copy import deepcopy
from decimal import Decimal, InvalidOperation

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.l2_interfaces import (
    STORM_TYPES,
    L2_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    generate_switchport_trunk,
    normalize_interface,
    vlan_list_to_range,
    vlan_range_to_dict,
)


MAX_PRIORITY = 224
PRIORITY_STEP = 32
DEFAULT_LEVEL = "100.00"
DEFAULT_PRIORITY = 128
DEFAULT_LINK_TYPE = "auto"
SWITCHPORT_DEFAULT = "show running-config all | incl 'system default switchport'"
SWITCHPORT_TYPES = ("ethernet", "port-channel")
MAX_LEVEL = Decimal(100)
LEVEL_STEP = Decimal("0.01")
MAX_ID = 4094
BOOL_TO_STATE = {True: "enable", False: "disable"}
# attribute of an `mst` / `vlans` entry that holds the (instance or vlan) range
RANGE_KEYS = {"mst": ("instances", 0), "vlans": ("vlans", 1)}


class L2StpStormError(ValueError):
    """Raised for invalid spanning_tree / storm_control input."""


def normalize_level(value):
    """Return a storm-control level as a string with two decimals so that 1.0 equals 1.00."""
    try:
        level = Decimal(str(value).strip())
        valid = (
            level.is_finite() and 0 <= level <= MAX_LEVEL and level == level.quantize(LEVEL_STEP)
        )
    except InvalidOperation:
        valid = False
    if not valid:
        raise L2StpStormError(
            "storm_control level '{0}' must be a decimal between 0 and 100 with at most two decimals".format(
                value,
            ),
        )
    return "{0:.2f}".format(level)


def normalize_range(value, lowest):
    """Return an instance / vlan list such as '3, 1,2,5-6' in its canonical form '1-3,5-6'."""
    numbers = set()
    for part in str(value).replace(" ", "").split(","):
        first, _sep, last = part.partition("-")
        if not first.isdigit() or (last and not last.isdigit()):
            raise L2StpStormError("'{0}' is not a valid list of ids such as 1,3-5".format(value))
        low, high = int(first), int(last or first)
        if not lowest <= low <= high <= MAX_ID:
            raise L2StpStormError(
                "'{0}' is outside the range {1}-{2}".format(value, lowest, MAX_ID),
            )
        numbers.update(range(low, high + 1))
    return vlan_list_to_range(sorted(numbers))


def normalize_storm(storm):
    """Validate the storm_control levels of an interface and canonicalise them in place."""
    for traffic in STORM_TYPES:
        if "level" in storm.get(traffic, {}):
            storm[traffic]["level"] = normalize_level(storm[traffic]["level"])


def check_priority(value, label):
    """The device only accepts multiples of 32 from 0 to 224 as port priority."""
    if not 0 <= value <= MAX_PRIORITY or value % PRIORITY_STEP:
        raise L2StpStormError(
            "{0}: port_priority {1} is invalid, it must be a multiple of {2} from 0 to {3}".format(
                label,
                value,
                PRIORITY_STEP,
                MAX_PRIORITY,
            ),
        )


def check_entry(section, entry):
    """Validate the cost and port_priority of one mst / vlans entry."""
    label = "spanning_tree {0} {1}".format(section, entry[RANGE_KEYS[section][0]])
    if "port_priority" in entry:
        check_priority(entry["port_priority"], label)
    if section == "mst" and entry.get("cost", 1) < 1:
        raise L2StpStormError("{0}: cost must be at least 1".format(label))


def normalize_spanning_tree(stp):
    """Turn bools into enable/disable and the mst / vlans lists into dicts keyed by their canonical range."""
    if "port_priority" in stp:
        check_priority(stp["port_priority"], "spanning_tree")
    for attr in ("bpduguard", "bpdufilter"):
        if attr in stp:
            stp[attr] = BOOL_TO_STATE[stp[attr]]
    for section, (key, lowest) in RANGE_KEYS.items():
        entries = {}
        for entry in stp.get(section, []):
            entry[key] = normalize_range(entry[key], lowest)
            check_entry(section, entry)
            entries[entry[key]] = entry
        if entries:
            stp[section] = entries


def strip_defaults(entry):
    """Remove the values the device does not display because they are the default.

    Returns the removed (section, key) pairs so that merged can still reset them.
    """
    removed = []
    stp = entry.get("spanning_tree", {})
    for key, default in (("port_priority", DEFAULT_PRIORITY), ("link_type", DEFAULT_LINK_TYPE)):
        if stp.get(key) == default:
            del stp[key]
            removed.append(("spanning_tree", key))
    storm = entry.get("storm_control", {})
    for traffic in STORM_TYPES:
        if storm.get(traffic, {}).get("level") == DEFAULT_LEVEL:
            del storm[traffic]
            removed.append(("storm_control", traffic))
    return removed


class L2_interfaces(ResourceModule):
    """
    The nxos_l2_interfaces config class
    """

    def __init__(self, module):
        super(L2_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="l2_interfaces",
            tmplt=L2_interfacesTemplate(),
        )
        self.parsers = (
            [
                "mode",
                "access.vlan",
                "trunk.native_vlan",
                "trunk.allowed_vlans_none",
                "beacon",
                "link_flap.error_disable",
                "cdp_enable",
                "no_cdp_enable",
                "spanning_tree.port_type",
                "spanning_tree.bpduguard",
                "spanning_tree.bpdufilter",
                "spanning_tree.guard",
                "spanning_tree.cost",
                "spanning_tree.port_priority",
                "spanning_tree.link_type",
            ]
            + ["storm_control.%s.level" % traffic for traffic in STORM_TYPES]
            + ["storm_control.action"]
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
        """
        wantd = {entry["name"].lower(): entry for entry in self.want}
        haved = {entry["name"].lower(): entry for entry in self.have}

        try:
            for each in wantd, haved:
                self.process_list_attrs(each)
        except L2StpStormError as err:
            self._module.fail_json(msg=str(err))

        # Rebuild dicts with normalized interface name keys
        wantd = {val["name"]: val for val in wantd.values()}
        haved = {val["name"]: val for val in haved.values()}

        # Get port-channel members detected during facts gathering
        pc_members = getattr(self._module, "_l2_pc_members", set())

        resets = self._prepare_stp_storm(wantd, haved)
        user_provided_config = bool(wantd)

        for intf_name in list(wantd.keys()):
            if intf_name in pc_members:
                self._module.fail_json(
                    msg="Interface {0} is a port-channel member. "
                    "L2 configuration cannot be applied directly on port-channel "
                    "member interfaces. Apply the configuration on the "
                    "port-channel interface instead.".format(intf_name),
                )

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            # Strip synthesized allowed_vlans before merge so implicit
            # 1-4094 is not treated as an explicit configured set.
            for k, have in haved.items():
                if have.get("trunk", {}).get("allowed_vlans_implicit"):
                    if k in wantd and wantd[k].get("trunk", {}).get("allowed_vlans"):
                        have.get("trunk", {}).pop("allowed_vlans", None)
            wantd = dict_merge(self._without_reset(haved, resets), wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not user_provided_config}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the L2_interfaces network resource.
        """
        begin = len(self.commands)
        want_without_name = want.copy()
        want_without_name.pop("name", None)
        pre_pop_want = bool(want_without_name)
        want_cdp = want.pop("cdp_enable", None)
        have_cdp = have.pop("cdp_enable", None)
        self.handle_cdp(want_cdp, have_cdp, "cdp_enable", pre_pop_want)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_lists(want, have)
        self._compare_keyed(want.get("spanning_tree", {}), have.get("spanning_tree", {}))
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def _prepare_stp_storm(self, wantd, haved):
        """Drop the displayed-as-absent defaults, return what want resets and check the ports."""
        resets = {name: strip_defaults(want) for name, want in wantd.items()}
        for have in haved.values():
            strip_defaults(have)
        self._check_switchports(wantd)
        return resets

    def get_switchport_defaults(self):
        """Wrapper method for `_connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return self._connection.get(SWITCHPORT_DEFAULT)

    def _default_is_layer2(self):
        """Whether ports are switchports unless configured otherwise; unknown counts as layer 3."""
        found = re.search(
            r"^(no )?system default switchport$",
            self.get_switchport_defaults(),
            re.M,
        )
        return bool(found) and not found.group(1)

    def _check_switchports(self, wantd):
        """Fail before any command is sent when spanning_tree / storm_control target a port
        that is not a confirmed switchport: the interface commands do not exist on a routed port.
        """
        if self.state not in ("merged", "replaced", "overridden"):
            return
        names = [
            n for n, want in wantd.items() if want.get("spanning_tree") or want.get("storm_control")
        ]
        if not names:
            return
        routed = getattr(self._module, "_l2_routed", set())
        switchports = getattr(self._module, "_l2_switchports", set())
        default_layer2 = self._default_is_layer2()
        for name in names:
            confirmed = name in switchports or (default_layer2 and name not in routed)
            if not confirmed or not name.lower().startswith(SWITCHPORT_TYPES):
                self._module.fail_json(
                    msg="Interface {0} is not a switchport or port-channel in switchport mode. "
                    "spanning_tree and storm_control can only be configured on layer-2 interfaces, "
                    "configure 'switchport' on the interface first.".format(name),
                )

    @staticmethod
    def _without_reset(haved, resets):
        """Copy of have without the values that want sets to their default, so merged resets them."""
        base = deepcopy(haved)
        for name, paths in resets.items():
            for section, key in paths:
                base.get(name, {}).get(section, {}).pop(key, None)
        return base

    def _compare_keyed(self, want, have):
        """Compare the cost / port_priority of the mst and vlans entries."""
        for section in RANGE_KEYS:
            wanted, current = want.get(section, {}), have.get(section, {})
            for rng in sorted(set(wanted) | set(current)):
                for attr in ("cost", "port_priority"):
                    self._compare_keyed_attr(
                        section + "_" + attr,
                        rng,
                        wanted.get(rng, {}).get(attr),
                        current.get(rng, {}).get(attr),
                    )

    def _compare_keyed_attr(self, parser, rng, inw, inh):
        if inw is not None and inw != inh:
            self.addcmd({"key": rng, "value": inw}, parser)
        elif inw is None and inh is not None:
            self.addcmd({"key": rng, "value": inh}, parser, True)

    def _compare_lists(self, want, have):
        """Compare list attributes for trunk allowed vlans.

        want_set: VLANs that should be present on the appliance
        have_set: VLANs that are currently on the appliance
        """
        want_set = set(want.get("trunk", {}).get("allowed_vlans", {}))
        have_set = set(have.get("trunk", {}).get("allowed_vlans", {}))

        if self.state == "deleted" and have_set:
            # For deleted state, remove all trunk allowed vlans if any exist
            if have_set:
                self.commands.append("no switchport trunk allowed vlan")
            return

        if self.state in ("merged", "rendered"):
            if not have_set and want_set:
                self.commands.extend(
                    generate_switchport_trunk(
                        "allowed",
                        False,
                        vlan_list_to_range(sorted(want_set, key=int)),
                    ),
                )
            else:
                vlans_to_add = want_set - have_set
                if vlans_to_add:
                    self.commands.extend(
                        generate_switchport_trunk(
                            "allowed",
                            True,
                            vlan_list_to_range(sorted(vlans_to_add, key=int)),
                        ),
                    )
            return

        if self.state in ("replaced", "overridden"):
            if not want_set and have_set:
                self.commands.append("no switchport trunk allowed vlan")
            elif want_set and want_set != have_set:
                self.commands.extend(
                    generate_switchport_trunk(
                        "allowed",
                        False,
                        vlan_list_to_range(sorted(want_set, key=int)),
                    ),
                )

    def process_list_attrs(self, param):
        if param:
            for _k, val in param.items():
                val["name"] = normalize_interface(val["name"])
                normalize_spanning_tree(val.get("spanning_tree", {}))
                normalize_storm(val.get("storm_control", {}))
                if val.get("trunk"):
                    for vlan in ["allowed_vlans"]:
                        vlanList = val.get("trunk").get(vlan, [])
                        if vlanList and vlanList != "none":
                            val["trunk"][vlan] = vlan_range_to_dict(val.get("trunk").get(vlan))

    def handle_cdp(self, want_cdp, have_cdp, parser, want):
        if want_cdp is None and have_cdp is None:
            if self.state == "replaced" or (self.state == "overridden" and want):
                self.addcmd({parser: True}, parser, True)
        else:
            if want_cdp is True and have_cdp is False:
                self.addcmd({parser: want_cdp}, parser, not want_cdp)
            elif want_cdp is False and have_cdp is None:
                self.addcmd({parser: not want_cdp}, parser, not want_cdp)
            elif want_cdp is None and have_cdp is False:
                if self.state in ["overridden", "deleted"] and not want:
                    self.addcmd({parser: not have_cdp}, parser, have_cdp)
