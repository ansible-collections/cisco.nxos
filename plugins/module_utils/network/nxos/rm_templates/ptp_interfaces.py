# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Ptp_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_NAME = "{{ name }}"
_ADDRESS = "{{ address }}"
# the interval lines can carry a profile word between the keyword and the value
_PROFILES = "aes67|smpte-2059-2"
_INTERVALS = {
    "announce_interval": "announce interval",
    "announce_timeout": "announce timeout",
    "sync_interval": "sync interval",
    "delay_request_interval": "delay-request minimum interval",
}
_ADDRESS_RE = "[0-9a-fA-F:.]+"


def _interval(name, keyword):
    """Two parsers for a line that has a value and an optional profile."""
    prefix = "^\\s+ptp\\s" + keyword.replace(" ", "\\s")
    setval = (
        "ptp "
        + keyword
        + "{{ ' ' ~ "
        + name
        + ".profile | replace('_', '-') if "
        + name
        + ".profile is defined else '' }} {{ "
        + name
        + ".value }}"
    )
    return [
        {
            "name": name + "_profile",
            "getval": re.compile(prefix + "\\s(?P<profile>" + _PROFILES + ")\\s(?P<value>-?\\d+)$"),
            "setval": setval,
            "result": {
                _NAME: {
                    name: {
                        "value": "{{ value }}",
                        "profile": "{{ profile | replace('-', '_') }}",
                    },
                },
            },
        },
        {
            "name": name,
            "getval": re.compile(prefix + "\\s(?P<value>-?\\d+)$"),
            "setval": setval,
            "result": {_NAME: {name: {"value": "{{ value }}"}}},
        },
    ]


def _address_list(name, keyword):
    """A `ptp master|slave <address>` line, several can exist. A negotiation schema is parsed away."""
    return {
        "name": name,
        "getval": re.compile(
            "^\\s+ptp\\s"
            + keyword
            + "\\s(?P<address>"
            + _ADDRESS_RE
            + ")(?:\\snegotiation-schema\\s\\S+)?$",
        ),
        "setval": "ptp " + keyword + " {{ address }}",
        "result": {_NAME: {name: ["{{ address }}"]}},
    }


class Ptp_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Ptp_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r'''
                ^interface\s(?P<name>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {_NAME: {"name": _NAME}},
            "shared": True,
        },
        {
            "name": "enabled",
            "getval": re.compile(r"^\s+ptp$"),
            "setval": "ptp",
            "result": {_NAME: {"enabled": True}},
        },
        {
            "name": "role",
            "getval": re.compile(r"^\s+ptp\srole\s(?P<role>dynamic|master|slave)$"),
            "setval": "ptp role {{ role }}",
            "result": {_NAME: {"role": "{{ role }}"}},
        },
        {
            # a negotiation schema cannot be created from the CLI, it is parsed away
            "name": "transmission",
            "getval": re.compile(
                r"^\s+ptp\stransmission\s(?P<transmission>unicast|multicast)(?:\snegotiation-schema\s\S+)?$",
            ),
            "setval": "ptp transmission {{ transmission }}",
            "result": {_NAME: {"transmission": "{{ transmission }}"}},
        },
        {
            "name": "transport",
            "getval": re.compile(r"^\s+ptp\stransport\s(?P<transport>ipv4|ipv6)$"),
            "setval": "ptp transport {{ transport }}",
            "result": {_NAME: {"transport": "{{ transport }}"}},
        },
        {
            "name": "vlan",
            "getval": re.compile(r"^\s+ptp\svlan\s(?P<vlan>\d+)$"),
            "setval": "ptp vlan {{ vlan }}",
            "result": {_NAME: {"vlan": "{{ vlan }}"}},
        },
        {
            # forward and reverse path exclude each other, the last one configured wins
            "name": "asymmetric_delay",
            "getval": re.compile(r"(?!)"),  # render only
            "setval": "ptp asymmetric-delay"
                      "{{ ' forward-path ' ~ asymmetric_delay.forward_path"
                      " if asymmetric_delay.forward_path is defined"
                      " else ' reverse-path ' ~ asymmetric_delay.reverse_path }}",
            "result": {},
        },
        {
            "name": "asymmetric_delay_forward",
            "getval": re.compile(r"^\s+ptp\sasymmetric-delay\sforward-path\s(?P<forward_path>\d+)$"),
            "setval": "",
            "result": {_NAME: {"asymmetric_delay": {"forward_path": "{{ forward_path }}"}}},
        },
        {
            "name": "asymmetric_delay_reverse",
            "getval": re.compile(r"^\s+ptp\sasymmetric-delay\sreverse-path\s(?P<reverse_path>\d+)$"),
            "setval": "",
            "result": {_NAME: {"asymmetric_delay": {"reverse_path": "{{ reverse_path }}"}}},
        },
    ] + [
        parser
        for name, keyword in _INTERVALS.items()
        for parser in _interval(name, keyword)
    ] + [
        _address_list("master", "master"),
        _address_list("slave", "slave"),
        {
            "name": "peer",
            "getval": re.compile("^\\s+ptp\\speer\\s(?P<peer>" + _ADDRESS_RE + ")$"),
            "setval": "ptp peer {{ peer }}",
            "result": {_NAME: {"peer": "{{ peer }}"}},
        },
        {
            # parse only, one source per address family
            "name": "ucast_source_ipv4",
            "getval": re.compile(r"^\s+ptp\sucast-source\s(?P<address>\d+\.\d+\.\d+\.\d+)$"),
            "setval": "",
            "result": {_NAME: {"ucast_source": {"ipv4": "{{ address }}"}}},
        },
        {
            "name": "ucast_source_ipv6",
            "getval": re.compile(r"^\s+ptp\sucast-source\s(?P<address>[0-9a-fA-F:]*:[0-9a-fA-F:.]*)$"),
            "setval": "",
            "result": {_NAME: {"ucast_source": {"ipv6": "{{ address }}"}}},
        },
        {
            "name": "ucast_source",
            "getval": re.compile(r"(?!)"),  # render only
            "setval": "ptp ucast-source {{ address }}",
            "result": {},
        },
    ]
    # fmt: on
