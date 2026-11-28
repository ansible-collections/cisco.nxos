# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Netflow_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


# the template turns a result such as 10 or 1,2 into a number or a tuple, a value that starts with
# this text stays a string, the facts remove it
PROTECT = "text:"

# the lines of the running configuration are split in these sections, each one has its own parsers
SECTIONS = ("exporter", "record", "monitor")


def _header(section):
    plural = section + "s"
    return {
        "name": section,
        "section": section,
        "getval": re.compile(r"^flow\s" + section + r"\s(?P<name>\S+)\s*$"),
        "setval": "flow " + section + " {{ name }}",
        "result": {
            plural: {
                "{{ name }}": {"name": PROTECT + "{{ name }}"},
            },
        },
        "shared": True,
    }


def _text(section, name, keyword, indent=r"\s+"):
    """A line with a free text, the description or the name of the record of a monitor."""
    plural = section + "s"
    return {
        "name": section + "." + name,
        "section": section,
        "getval": re.compile("^" + indent + keyword + r"\s(?P<value>.+?)\s*$"),
        "setval": keyword + " {{ " + name + " }}",
        "remval": keyword,
        "result": {plural: {"{{ name }}": {name: PROTECT + "{{ value }}"}}},
    }


def _number(section, name, keyword, indent=r"\s+"):
    """A line with a number."""
    plural = section + "s"
    return {
        "name": section + "." + name,
        "section": section,
        "getval": re.compile("^" + indent + re.escape(keyword) + r"\s(?P<value>\d+)\s*$"),
        "setval": keyword + " {{ " + name + " }}",
        "remval": keyword,
        "result": {plural: {"{{ name }}": {name: "{{ value }}"}}},
    }


def _nested(path):
    result = "{{ True }}"
    for part in reversed(path.split(".")):
        result = {part: result}
    return result


def _flag(name, keyword):
    """A line of a record without argument, it is only displayed when it is set."""
    return {
        "name": "record." + name,
        "section": "record",
        "getval": re.compile(r"^\s+" + keyword.replace(" ", r"\s") + r"\s*$"),
        "setval": keyword,
        "result": {"records": {"{{ name }}": _nested(name)}},
    }


# the settings of a record that are lines without argument: name and keyword
RECORD_FLAGS = (
    ("match.datalink.mac_source_address", "match datalink mac source-address"),
    ("match.datalink.mac_destination_address", "match datalink mac destination-address"),
    ("match.datalink.vlan", "match datalink vlan"),
    ("match.datalink.ethertype", "match datalink ethertype"),
    ("match.ip.protocol", "match ip protocol"),
    ("match.ip.tos", "match ip tos"),
    ("match.ipv4.source_address", "match ipv4 source address"),
    ("match.ipv4.destination_address", "match ipv4 destination address"),
    ("match.ipv6.source_address", "match ipv6 source address"),
    ("match.ipv6.destination_address", "match ipv6 destination address"),
    ("match.ipv6.flow_label", "match ipv6 flow-label"),
    ("match.ipv6.options", "match ipv6 options"),
    ("match.transport.source_port", "match transport source-port"),
    ("match.transport.destination_port", "match transport destination-port"),
    ("collect.counter.bytes", "collect counter bytes"),
    ("collect.counter.packets", "collect counter packets"),
    ("collect.timestamp_sys_uptime.first", "collect timestamp sys-uptime first"),
    ("collect.timestamp_sys_uptime.last", "collect timestamp sys-uptime last"),
    ("collect.transport_tcp_flags", "collect transport tcp flags"),
    ("collect.ip_version", "collect ip version"),
)


class Netflow_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None, section=None):
        super(Netflow_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)
        if section:
            # the parsers of one section, a line such as the description exists in all of them
            self.PARSERS = [
                parser for parser in self.PARSERS if parser.get("section") in (section, None)
            ]

    # fmt: off
    PARSERS = [
        {
            "name": "timeout",
            "getval": re.compile(r"^flow\stimeout\s(?P<timeout>\d+)\s*$"),
            "setval": "flow timeout {{ timeout }}",
            "result": {"timeout": "{{ timeout }}"},
        },
        _header("exporter"),
        _text("exporter", "description", "description"),
        {
            "name": "exporter.destination",
            "section": "exporter",
            "getval": re.compile(
                r"""
                ^\s+destination\s(?P<address>\S+)(\suse-vrf\s(?P<vrf>\S+))?\s*$
                """,
                re.VERBOSE,
            ),
            "setval": "destination {{ destination.address }}"
                      "{{ ' use-vrf ' ~ destination.vrf if destination.vrf is defined else '' }}",
            "result": {
                "exporters": {
                    "{{ name }}": {
                        "destination": {"address": "{{ address }}", "vrf": "{{ vrf }}"},
                    },
                },
            },
        },
        _number("exporter", "transport_udp", "transport udp"),
        {
            "name": "exporter.source",
            "section": "exporter",
            "getval": re.compile(r"^\s+source\s(?P<value>\S+)\s*$"),
            "setval": "source {{ source }}",
            "remval": "source",
            "result": {"exporters": {"{{ name }}": {"source": PROTECT + "{{ value }}"}}},
        },
        _number("exporter", "dscp", "dscp"),
        _number("exporter", "template_data_timeout", "template data timeout"),
        _number("exporter", "option_exporter_stats_timeout", "option exporter-stats timeout"),
        _number("exporter", "option_interface_table_timeout", "option interface-table timeout"),
        _header("record"),
        _text("record", "description", "description"),
    ] + [
        _flag(name, keyword) for name, keyword in RECORD_FLAGS
    ] + [
        _header("monitor"),
        _text("monitor", "description", "description"),
        _text("monitor", "record", "record"),
        {
            "name": "monitor.exporters",
            "section": "monitor",
            "getval": re.compile(r"^\s+exporter\s(?P<value>\S+)\s*$"),
            "setval": "exporter {{ exporter }}",
            # the template does not keep the order of a list, a dict does: the facts turn it into a list
            "result": {"monitors": {"{{ name }}": {"exporter_names": {PROTECT + "{{ value }}": "{{ True }}"}}}},
        },
    ]
    # fmt: on


# lines that the device displays and that carry nothing to manage: the version of the exporter, which is always 9,
# and the matches that the device adds to every record
IGNORED = re.compile(
    r"^\s+(version\s9|match\s(input\sinterface|output\sinterface|flow\sdirection))\s*$",
)
