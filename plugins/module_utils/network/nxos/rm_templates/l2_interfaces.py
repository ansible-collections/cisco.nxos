# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The L2_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


STORM_TYPES = ("broadcast", "multicast", "unicast")
STP_PREFIX = r"^\s+spanning-tree\s"
STP_SECTIONS = {"mst": "instances", "vlans": "vlans"}
STP_KEYWORDS = {"mst": "mst", "vlans": "vlan"}
STP_ATTRS = {"cost": "cost", "port_priority": "port-priority"}


def _stp_parser(name, pattern, setval, result, remval=None):
    parser = {
        "name": name,
        "getval": re.compile(STP_PREFIX + pattern),
        "setval": setval,
        "result": {"{{ name }}": {"spanning_tree": result}},
    }
    if remval:
        parser["remval"] = remval
    return parser


def _storm_parser(traffic):
    return {
        "name": "storm_control.%s.level" % traffic,
        "getval": re.compile(
            r"^\s+storm-control\s" + traffic + r"\slevel\s(?P<level>\d+(?:\.\d+)?)$",
        ),
        "setval": "storm-control " + traffic + " level {{ storm_control." + traffic + ".level }}",
        "result": {
            "{{ name }}": {"storm_control": {traffic: {"level": "'{{ level }}'"}}},
        },
    }


def _keyed_parser(section, attr):
    """One cost or port-priority line of a `spanning-tree mst|vlan <list>` entry."""
    keyword, word = STP_KEYWORDS[section], STP_ATTRS[attr]
    return _stp_parser(
        section + "_" + attr,
        keyword + r"\s(?P<key>\S+)\s" + word + r"\s(?P<value>\d+)$",
        "spanning-tree " + keyword + " {{ key }} " + word + " {{ value }}",
        {section: {"{{ key }}": {STP_SECTIONS[section]: "{{ key }}", attr: "{{ value }}"}}},
        remval="spanning-tree " + keyword + " {{ key }} " + word,
    )


def _stp_storm_parsers():
    parsers = [
        _stp_parser(
            "spanning_tree.port_type",
            r"port\stype\s(?P<port_type>edge\strunk|edge|network|normal)$",
            "spanning-tree port type {{ spanning_tree.port_type|replace('_', ' ') }}",
            {"port_type": "{{ port_type|replace(' ', '_') }}"},
        ),
        _stp_parser(
            "spanning_tree.link_type",
            r"link-type\s(?P<link_type>auto|point-to-point|shared)$",
            "spanning-tree link-type {{ spanning_tree.link_type|replace('_', '-') }}",
            {"link_type": "{{ link_type|replace('-', '_') }}"},
            remval="spanning-tree link-type",
        ),
        _stp_parser(
            "spanning_tree.guard",
            r"guard\s(?P<guard>loop|root|none)$",
            "spanning-tree guard {{ spanning_tree.guard }}",
            {"guard": "{{ guard }}"},
            remval="spanning-tree guard",
        ),
    ]
    # bpduguard / bpdufilter are tri-state: the config class feeds "enable"/"disable" here
    for word in ("bpduguard", "bpdufilter"):
        parsers.append(
            _stp_parser(
                "spanning_tree." + word,
                word + r"\s(?P<state>enable|disable)$",
                "spanning-tree " + word + " {{ spanning_tree." + word + " }}",
                {word: "{{ state == 'enable' }}"},
                remval="spanning-tree " + word,
            ),
        )
    for attr, word in STP_ATTRS.items():
        parsers.append(
            _stp_parser(
                "spanning_tree." + attr,
                word + r"\s(?P<value>\d+)$",
                "spanning-tree " + word + " {{ spanning_tree." + attr + " }}",
                {attr: "{{ value }}"},
                remval="spanning-tree " + word,
            ),
        )
    parsers.extend(_keyed_parser(section, attr) for section in STP_SECTIONS for attr in STP_ATTRS)
    parsers.extend(_storm_parser(traffic) for traffic in STORM_TYPES)
    parsers.append(
        {
            "name": "storm_control.action",
            "getval": re.compile(r"^\s+storm-control\saction\s(?P<action>shutdown|trap)$"),
            "setval": "storm-control action {{ storm_control.action }}",
            "result": {"{{ name }}": {"storm_control": {"action": "{{ action }}"}}},
        },
    )
    return parsers


class L2_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^interface\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": 'interface {{ name }}',
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                },
            },
            "shared": True,
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                \s+switchport\smode
                \s+(?P<mode>access|trunk|dot1q-tunnel|fex-fabric|fabricpath)
                $""", re.VERBOSE,
            ),
            "setval": "switchport mode {{ mode }}",
            "result": {
                '{{ name }}': {
                    'mode': "{{ mode }}",
                },
            },
        },
        {
            "name": "access.vlan",
            "getval": re.compile(
                r"""
                \s+switchport\saccess\svlan
                \s+(?P<vlan>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport access vlan {{ access.vlan }}",
            "result": {
                '{{ name }}': {
                    'access': {
                        'vlan': "{{ vlan }}",
                    },
                },
            },
        },
        {
            "name": "trunk.native_vlan",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\snative\svlan
                \s+(?P<vlan>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport trunk native vlan {{ trunk.native_vlan|string }}",
            "result": {
                '{{ name }}': {
                    'trunk': {
                        'native_vlan': "{{ vlan }}",
                    },
                },
            },
        },
        {
            "name": "trunk.allowed_vlans_none",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\sallowed\svlan
                \s+(?P<isnone>none)
                $""", re.VERBOSE,
            ),
            "setval": "switchport trunk allowed vlan",
            "result": {
                '{{ name }}': {
                    'trunk': {
                        'allowed_vlans_none': "{{ not not isnone }}",
                    },
                },
            },
        },
        {
            "name": "trunk.allowed_vlans",
            "getval": re.compile(
                r"""
                \s+switchport\strunk\sallowed\svlan
                \s+(?!none$)(?P<allowed_vlans>.+)
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                '{{ name }}': {
                    'trunk': {
                        'allowed_vlans': "'{{ allowed_vlans }}'",
                    },
                },
            },
        },
        {
            "name": "beacon",
            "getval": re.compile(
                r"""
                \s+(?P<beacon>beacon)
                $""", re.VERBOSE,
            ),
            "setval": "beacon",
            "result": {
                '{{ name }}': {
                    'beacon': "{{ True if beacon }}",
                },
            },
        },
        {
            "name": "link_flap.error_disable",
            "getval": re.compile(
                r"""
                \s+link-flap\serror-disable
                (\s+count\s(?P<count>\d+))?
                (\s+interval\s(?P<interval>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "link-flap error-disable"
            "{{ ' count ' + count|string if count is defined else '' }}"
            "{{ ' interval ' + interval|string if interval is defined else '' }}",
            "result": {
                '{{ name }}': {
                    'link_flap': {
                        'error_disable': {
                            'count': "{{ count }}",
                            'interval': "{{ interval }}",
                        },
                    },
                },
            },
        },
        {
            "name": "cdp_enable",
            "getval": re.compile(
                r"""
                \s+cdp\senable
                $""", re.VERBOSE,
            ),
            "setval": "cdp enable",
            "result": {
                '{{ name }}': {
                    'cdp_enable': True,
                },
            },
        },
        {
            "name": "no_cdp_enable",
            "getval": re.compile(
                r"""
                \s+no\scdp\senable
                $""", re.VERBOSE,
            ),
            "setval": "no cdp enable",
            "result": {
                '{{ name }}': {
                    'cdp_enable': False,
                },
            },
        },
    ] + _stp_storm_parsers()
    # fmt: on
