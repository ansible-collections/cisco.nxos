# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ptp_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_ENABLED = "{{ False if negate is defined else True }}"
_PREFIX = "^(?P<negate>no\\s)?ptp\\s"


def _value(name, keyword, pattern="\\d+"):
    """Parser of a global line with one argument."""
    return {
        "name": name,
        "getval": re.compile("^ptp\\s" + re.escape(keyword) + "\\s(?P<value>" + pattern + ")$"),
        "setval": "ptp " + keyword + " {{ " + name + " }}",
        "result": {name: "{{ value }}"},
    }


def _flag(name, keyword):
    """Parser of a flag, a line without argument that is only displayed when it is set
    (or, for a setting that is on by default, when it is switched off).
    """
    parts = name.split(".")
    result = _ENABLED
    for part in reversed(parts):
        result = {part: result}
    return {
        "name": name,
        "getval": re.compile(_PREFIX + re.escape(keyword) + "$"),
        "setval": "ptp " + keyword,
        "result": result,
    }


# the template turns a result such as 0x2-0x4 into a number or 0x2,0x5 into a tuple, a value that
# starts with this text stays a string, the facts remove it
PROTECT = "text:"


def _nested(name, keyword, pattern="\\S+", prefix=""):
    """Parser of a line with one argument whose value is part of a dict (a.b)."""
    top, sub = name.split(".")
    return {
        "name": name,
        "getval": re.compile("^ptp\\s" + re.escape(keyword) + "\\s(?P<value>" + pattern + ")$"),
        "setval": "ptp " + keyword + " {{ " + name + " }}",
        "result": {top: {sub: prefix + "{{ value }}"}},
    }


class Ptp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ptp_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "source.ipv4_vrf",
            "getval": re.compile(
                r'''
                ^ptp\ssource\s(?P<address>\d+\.\d+\.\d+\.\d+)\svrf\s(?P<vrf>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "ptp source {{ source.ipv4.address }} vrf {{ source.ipv4.vrf }}",
            "result": {"source": {"ipv4": {"address": "{{ address }}", "vrf": "{{ vrf }}"}}},
        },
        {
            "name": "source.ipv4",
            "getval": re.compile(
                r'''
                ^ptp\ssource\s(?P<address>\d+\.\d+\.\d+\.\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "ptp source {{ source.ipv4.address }}"
                      "{{ ' vrf ' ~ source.ipv4.vrf if source.ipv4.vrf is defined else '' }}",
            "result": {"source": {"ipv4": {"address": "{{ address }}"}}},
        },
        {
            "name": "source.ipv6_vrf",
            "getval": re.compile(
                r'''
                ^ptp\ssource\s(?P<address>[0-9a-fA-F:]*:[0-9a-fA-F:.]*)\svrf\s(?P<vrf>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "ptp source {{ source.ipv6.address }} vrf {{ source.ipv6.vrf }}",
            "result": {"source": {"ipv6": {"address": "{{ address }}", "vrf": "{{ vrf }}"}}},
        },
        {
            "name": "source.ipv6",
            "getval": re.compile(
                r'''
                ^ptp\ssource\s(?P<address>[0-9a-fA-F:]*:[0-9a-fA-F:.]*)$
                ''',
                re.VERBOSE,
            ),
            "setval": "ptp source {{ source.ipv6.address }}"
                      "{{ ' vrf ' ~ source.ipv6.vrf if source.ipv6.vrf is defined else '' }}",
            "result": {"source": {"ipv6": {"address": "{{ address }}"}}},
        },
        _value("domain", "domain"),
        _value("priority1", "priority1"),
        _value("priority2", "priority2"),
        _value("mean_path_delay", "mean-path-delay"),
        _flag("management", "management"),
        _flag("unicast_negotiation", "unicast-negotiation"),
        _nested("correction_range.value", "correction-range", "\\d+"),
        _flag("correction_range.logging", "correction-range logging"),
        _nested("ipv6_multicast_scope.rx", "ipv6 multicast scope rx", "0x[0-9a-fA-F]+(?:[-,]0x[0-9a-fA-F]+)*", PROTECT),
        _nested("ipv6_multicast_scope.tx", "ipv6 multicast scope tx", "0x[0-9a-fA-F]+", PROTECT),
        _nested("delay_tolerance.mean_path", "delay tolerance mean-path", "\\d+(?:\\.\\d+)?"),
        _nested("delay_tolerance.reverse_path", "delay tolerance reverse-path", "\\d+(?:\\.\\d+)?"),
        {
            "name": "notification.gm_change",
            "getval": re.compile(_PREFIX + "notification\\stype\\sgm-change$"),
            "setval": "ptp notification type gm-change",
            "result": {"notification": {"gm_change": _ENABLED}},
        },
        {
            "name": "notification.parent_change",
            "getval": re.compile(_PREFIX + "notification\\stype\\sparent-change$"),
            "setval": "ptp notification type parent-change",
            "result": {"notification": {"parent_change": _ENABLED}},
        },
        {
            "name": "notification.port_state_change",
            "getval": re.compile(_PREFIX + "notification\\stype\\sport-state-change$"),
            "setval": "ptp notification type port-state-change",
            "result": {"notification": {"port_state_change": _ENABLED}},
        },
        {
            "name": "notification.high_correction",
            "getval": re.compile(
                _PREFIX + "notification\\stype\\shigh-correction(?:\\sinterval\\s(?P<interval>\\S+))?$",
            ),
            "setval": "ptp notification type high-correction"
                      "{{ ' interval ' ~ notification.high_correction.interval"
                      " if notification.high_correction.interval is defined else '' }}",
            "remval": "ptp notification type high-correction",
            "result": {
                "notification": {
                    "high_correction": {
                        "enabled": _ENABLED,
                        "interval": "{{ interval }}",
                    },
                },
            },
        },
        {
            "name": "clock_periodic_update",
            "getval": re.compile(
                _PREFIX + "clock\\speriodic-update(?:\\sinterval\\s(?P<interval>\\d+))?$",
            ),
            "setval": "ptp clock periodic-update"
                      "{{ ' interval ' ~ clock_periodic_update.interval"
                      " if clock_periodic_update.interval is defined else '' }}",
            "remval": "ptp clock periodic-update",
            "result": {
                "clock_periodic_update": {
                    "enabled": _ENABLED,
                    "interval": "{{ interval }}",
                },
            },
        },
        {
            "name": "time_distribution_hold",
            "getval": re.compile(
                _PREFIX + "time\\sdistribution-hold"
                "(?:\\scorrection-threshold\\s(?P<correction_threshold>\\d+))?"
                "(?:\\sdelay-threshold\\s(?P<delay_threshold>\\d+))?$",
            ),
            "setval": "ptp time distribution-hold"
                      "{{ ' correction-threshold ' ~ time_distribution_hold.correction_threshold"
                      " if time_distribution_hold.correction_threshold is defined else '' }}"
                      "{{ ' delay-threshold ' ~ time_distribution_hold.delay_threshold"
                      " if time_distribution_hold.delay_threshold is defined else '' }}",
            "remval": "ptp time distribution-hold",
            "result": {
                "time_distribution_hold": {
                    "enabled": _ENABLED,
                    "correction_threshold": "{{ correction_threshold }}",
                    "delay_threshold": "{{ delay_threshold }}",
                },
            },
        },
    ]
    # fmt: on
