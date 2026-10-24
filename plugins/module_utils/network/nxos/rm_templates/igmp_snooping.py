# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Igmp_snooping parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_VLAN_ID = "{{ vlan_id }}"
_GROUP = "{{ group }}"
_IF = "{{ interface }}"
_ENABLED = "{{ False if negate is defined else True }}"
_PREFIX = "ip igmp snooping"
_POLICY_TYPE = "{{ policy_type | replace('-', '_') }}"


def _line(scope, body):
    """Pattern of one line, global lines start in column one and the lines of a
    `vlan configuration` block are indented.
    """
    start = "^" if scope == "global" else "^\\s+"
    return re.compile(start + "(?P<negate>no\\s)?ip\\sigmp\\ssnooping" + body + "$")


def _result(scope, data):
    """Place a result below the VLAN when it belongs to a `vlan configuration` block."""
    if scope == "global":
        return data
    return {"vlans": {_VLAN_ID: data}}


def _boolean(scope, name, keyword):
    """Parser of an on/off line; the device shows the no-form for a default-on
    setting and the plain form for a default-off one.
    """
    suffix = "\\s" + re.escape(keyword) if keyword else ""
    return {
        "name": name if scope == "global" else "vlan_" + name,
        "getval": _line(scope, suffix),
        "setval": _PREFIX + (" " + keyword if keyword else ""),
        "result": _result(scope, {name: _ENABLED}),
    }


def _value(scope, name, keyword, pattern="\\d+"):
    """Parser of a line with one argument."""
    return {
        "name": name if scope == "global" else "vlan_" + name,
        "getval": _line(scope, "\\s" + re.escape(keyword) + "\\s(?P<value>" + pattern + ")"),
        "setval": _PREFIX + " " + keyword + " {{ " + name + " }}",
        "result": _result(scope, {name: "{{ value }}"}),
    }


def _proxy(scope):
    """The two forms of `proxy general-queries`, with and without the mrt."""
    prefix = "" if scope == "global" else "vlan_"
    return [
        {
            "name": prefix + "proxy_mrt",
            "getval": _line(scope, "\\sproxy\\sgeneral-queries\\smrt\\s(?P<mrt>\\d+)"),
            "setval": _PREFIX + " proxy general-queries mrt {{ proxy.mrt }}",
            "result": _result(scope, {"proxy": {"general_queries": True, "mrt": "{{ mrt }}"}}),
        },
        {
            "name": prefix + "proxy",
            "getval": _line(scope, "\\sproxy\\sgeneral-queries"),
            "setval": _PREFIX + " proxy general-queries",
            "result": _result(scope, {"proxy": {"general_queries": True}}),
        },
    ]


def _scope_parsers(scope):
    """The settings that exist globally and in a `vlan configuration` block."""
    return [
        _boolean(scope, "snooping", ""),
        _boolean(scope, "link_local_groups_suppression", "link-local-groups-suppression"),
        _boolean(scope, "report_suppression", "report-suppression"),
        _boolean(scope, "v3_report_suppression", "v3-report-suppression"),
        {
            "name": "group_timeout" if scope == "global" else "vlan_group_timeout",
            "getval": _line(scope, "\\sgroup-timeout\\s(?P<group_timeout>\\d+|never)"),
            "setval": _PREFIX + " group-timeout {{ group_timeout }}",
            "result": _result(scope, {"group_timeout": "{{ group_timeout }}"}),
        },
    ] + _proxy(scope)


class Igmp_snoopingTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Igmp_snoopingTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = _scope_parsers("global") + [
        _boolean("global", "vxlan", "vxlan"),
        _boolean("global", "disable_nve_static_router_port", "disable-nve-static-router-port"),
        _value("global", "max_gq_miss", "max-gq-miss"),
        _value("global", "syslog_threshold", "syslog-threshold"),
        _value("global", "holddown_timer", "holddown-timer"),
        {
            "name": "vlan",
            "getval": re.compile(
                r'''
                ^vlan\sconfiguration\s(?P<vlan_id>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "vlan configuration {{ vlan_id }}",
            "result": {
                "vlans": {
                    _VLAN_ID: {
                        "vlan_id": _VLAN_ID,
                    },
                },
            },
            "shared": True,
        },
    ] + _scope_parsers("vlan") + [
        _boolean("vlan", "explicit_tracking", "explicit-tracking"),
        _boolean("vlan", "fast_leave", "fast-leave"),
        _boolean("vlan", "proxy_leave_use_group_address", "proxy-leave use-group-address"),
        _value("vlan", "querier", "querier", "\\d+\\.\\d+\\.\\d+\\.\\d+"),
        _value("vlan", "querier_timeout", "querier-timeout"),
        _value("vlan", "query_interval", "query-interval"),
        _value("vlan", "query_max_response_time", "query-max-response-time"),
        _value("vlan", "startup_query_count", "startup-query-count"),
        _value("vlan", "startup_query_interval", "startup-query-interval"),
        _value("vlan", "robustness_variable", "robustness-variable"),
        _value("vlan", "last_member_query_interval", "last-member-query-interval"),
        _value("vlan", "version", "version"),
        {
            "name": "mrouter",
            "getval": _line("vlan", "\\smrouter\\sinterface\\s(?P<interface>\\S+)"),
            "setval": _PREFIX + " mrouter interface {{ interface }}",
            "result": _result("vlan", {"mrouter_interfaces": [_IF]}),
        },
        {
            "name": "report_flood_all",
            "getval": _line("vlan", "\\sreport-flood\\sall"),
            "setval": _PREFIX + " report-flood all",
            "result": _result("vlan", {"report_flood": {"all": True}}),
        },
        {
            "name": "report_flood_interface",
            "getval": _line("vlan", "\\sreport-flood\\sinterface\\s(?P<interface>\\S+)"),
            "setval": _PREFIX + " report-flood interface {{ interface }}",
            "result": _result("vlan", {"report_flood": {"interfaces": [_IF]}}),
        },
        {
            "name": "report_policy",
            "getval": _line(
                "vlan",
                "\\sreport-policy\\s(?P<policy_type>route-map|prefix-list)\\s(?P<name>\\S+)\\sinterface\\s(?P<interface>\\S+)",
            ),
            "setval": _PREFIX + " report-policy {{ policy_type }} {{ name }} interface {{ interface }}",
            "result": _result("vlan", {
                "report_policy": {
                    "{{ policy_type }}|{{ name }}|{{ interface }}": {
                        "policy_type": _POLICY_TYPE,
                        "name": "{{ name }}",
                        "interface": _IF,
                    },
                },
            }),
        },
        {
            "name": "access_group_interface",
            "getval": _line(
                "vlan",
                "\\saccess-group\\s(?P<policy_type>route-map|prefix-list)\\s(?P<name>\\S+)\\sinterface\\s(?P<interface>\\S+)",
            ),
            "setval": _PREFIX + " access-group {{ policy_type }} {{ name }} interface {{ interface }}",
            "result": _result("vlan", {
                "access_group": {
                    "{{ policy_type }}|{{ name }}|{{ interface }}": {
                        "policy_type": _POLICY_TYPE,
                        "name": "{{ name }}",
                        "interface": _IF,
                    },
                },
            }),
        },
        {
            "name": "access_group",
            "getval": _line("vlan", "\\saccess-group\\s(?P<name>[^\\s]+)"),
            "setval": _PREFIX + " access-group {{ name }}",
            "result": _result("vlan", {
                "access_group": {
                    "route-map|{{ name }}|": {
                        "policy_type": "route_map",
                        "name": "{{ name }}",
                    },
                },
            }),
        },
        {
            "name": "static_group_source",
            "getval": _line(
                "vlan",
                "\\sstatic-group\\s(?P<group>\\S+)\\ssource\\s(?P<source>\\S+)\\sinterface\\s(?P<interface>\\S+)",
            ),
            "setval": _PREFIX + " static-group {{ group }} source {{ source }} interface {{ interface }}",
            "result": _result("vlan", {
                "static_groups": {
                    _GROUP + "|{{ source }}": {
                        "group": _GROUP,
                        "source": "{{ source }}",
                        "interfaces": [_IF],
                    },
                },
            }),
        },
        {
            "name": "static_group",
            "getval": _line("vlan", "\\sstatic-group\\s(?P<group>\\S+)\\sinterface\\s(?P<interface>\\S+)"),
            "setval": _PREFIX + " static-group {{ group }} interface {{ interface }}",
            "result": _result("vlan", {
                "static_groups": {
                    _GROUP: {
                        "group": _GROUP,
                        "interfaces": [_IF],
                    },
                },
            }),
        },
    ]
    # fmt: on
