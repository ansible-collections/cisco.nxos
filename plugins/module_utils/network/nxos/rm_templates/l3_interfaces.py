# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The L3_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class L3_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L3_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""^mac-address
                    (\s(?P<mac_address>\S+))
                    $""",
                re.VERBOSE,
            ),
            "setval": "mac-address {{ mac_address }}",
            "result": {"{{ name }}": {"mac_address": "{{ mac_address }}"}},
        },
        {
            "name": "bandwidth",
            "getval": re.compile(
                r"""
                ^\s*bandwidth
                (?:\s+(?P<inherit>inherit))?
                \s+(?P<kilobits>\d+)
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "bandwidth"
                      "{{ ' inherit' if bandwidth.inherit|d(False) else ''}}"
                      "{{ ' ' + bandwidth.kilobits|string if bandwidth.kilobits is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "bandwidth": {
                        "inherit": "{{ not not inherit }}",
                        "kilobits": "{{ kilobits }}",
                    },
                },
            },
        },
        {
            "name": "ipv4.address",
            "getval": re.compile(
                r"""
                ^ip\s+address
                (?:
                    \s+(?P<dhcp>dhcp)
                    |
                    \s+(?P<ip_address>\S+)
                    (?:\s+(?P<ip_network_mask>\S+))?
                    (?:\s+route-preference\s+(?P<route_preference>\d+))?
                    (?:\s+tag\s+(?P<tag>\d+))?
                    (?:\s+(?P<secondary>secondary))?
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv4_address",
            "setval": "ip address"
                      "{{ ' dhcp' if ipv4_address.dhcp|d(False) else ''}}"
                      "{{ ' ' + ipv4_address.ip_address|string if ipv4_address.ip_address is defined else ''}}"
                      "{{ ' ' + ipv4_address.ip_network_mask|string if ipv4_address.ip_network_mask is defined else ''}}"
                      "{{ ' ' + 'route-preference ' + ipv4_address.route_preference|string if ipv4_address.route_preference is defined else ''}}"
                      "{{ ' tag ' + ipv4_address.tag|string if ipv4_address.tag is defined else ''}}"
                      "{{ ' secondary' if ipv4_address.secondary|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "address": [{
                            "dhcp": "{{ not not dhcp }}",
                            "ip_address": "{{ ip_address }}",
                            "ip_network_mask": "{{ ip_network_mask }}",
                            "route_preference": "{{ route_preference }}",
                            "tag": "{{ tag }}",
                            "secondary": "{{ not not secondary }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "ipv4.redirects",
            "getval": re.compile(
                r"""
                \s+ip\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "ip redirects",
            "result": {
                "{{ name }}": {
                    "ipv4":
                        {
                            "redirects": True,
                        },
                },
            },
        },
        {
            "name": "ipv4.unreachables",
            "getval": re.compile(
                r"""
                \s+ip\sunreachables
                $""", re.VERBOSE,
            ),
            "setval": "ip unreachables",
            "result": {
                "{{ name }}": {
                    "ipv4":
                    {
                        "unreachables": True,
                    },
                },
            },
        },
        {
            "name": "ipv4.proxy_arp",
            "getval": re.compile(
                r"""
                \s+ip\sproxy-arp
                $""", re.VERBOSE,
            ),
            "setval": "ip proxy-arp",
            "result": {
                "{{ name }}": {
                    "ipv4":
                    {
                        "proxy_arp": True,
                    },
                },
            },
        },
        {
            "name": "ipv4.port_unreachable",
            "getval": re.compile(
                r"""
                \s+ip\sport_unreachable
                $""", re.VERBOSE,
            ),
            "setval": "ip port_unreachable",
            "result": {
                "{{ name }}": {
                    "ipv4":
                    {
                        "port_unreachable": True,
                    },
                },
            },
        },
        {
            "name": "ipv4.verify",
            "getval": re.compile(
                r"""
                ^ip\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ip verify unicast source reachable-via"
                      "{{ ' ' + ipv4.verify.mode|string if ipv4.verify.mode else ''}}"
                      "{{ ' allow-default' if ipv4.verify.allow_default|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "verify": {
                            "unicast": {
                                "source": {
                                    "reachable_via": {
                                        "mode": "{{ mode }}",
                                        "allow_default": "{{ not not allow_default }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv4.dhcp",
            "getval": re.compile(
                r"""
                ^ip\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                    |
                    \s+option82\s+suboption\s+circuit-id\s+(?P<circuit_id>\S+)
                    |
                    \s+relay
                    (?:
                        \s+address
                        (?:
                            \s+(?P<relay_ip>\S+)
                            (?:\s+use-vrf\s+(?P<vrf_name>\S+))?
                        )?
                        |
                        \s+information\s+(?P<trusted>trusted)
                        |
                        \s+subnet-selection\s+(?P<subnet_ip>\S+)
                        |
                        \s+source-interface
                            \s+(?P<interface_type>ethernet|vlan|port-channel|loopback)
                            \s+(?P<interface_id>\S+)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv4_dhcp",
            "setval": "ip dhcp"
                      "{{ ' ' + 'smart-relay' if ipv4_dhcp.smart_relay|d(False) else ''}}"
                      "{{ ' option82 suboption circuit-id ' + ipv4_dhcp.circuit_id|string if ipv4_dhcp.circuit_id else ''}}"
                      "{{ ' relay address ' + ipv4_dhcp.relay_ip|string if ipv4_dhcp.relay_ip else ''}}"
                      "{{ ' use-vrf ' + ipv4_dhcp.vrf_name|string if ipv4_dhcp.vrf_name else ''}}"
                      "{{ ' relay information trusted' if ipv4_dhcp.trusted|d(False) else ''}}"
                      "{{ ' relay subnet-selection ' +  ipv4_dhcp.subnet_ip if ipv4_dhcp.subnet_ip else ''}}"
                      "{{ ' relay source-interface ' + ipv4_dhcp.interface_type|string if ipv4_dhcp.interface_type else ''}}"
                      "{{ ' ' + ipv4_dhcp.interface_id|string if ipv4_dhcp.interface_id else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
                            "option82": {
                                "suboption": {
                                    "circuit_id": "{{ circuit_id }}",
                                },
                            },
                            "smart_relay": "{{ not not smart_relay }}",
                            "relay": {
                                "address": [{
                                    "relay_ip": "{{ relay_ip }}",
                                    "vrf_name": "{{ vrf_name }}",
                                }],
                                "information": {
                                    "trusted": "{{ not not trusted }}",
                                },
                                "subnet_selection": {
                                    "subnet_ip": "{{ subnet_ip }}",
                                },
                                "source_interface": {
                                    "interface_type": "{{ interface_type }}",
                                    "interface_id": "{{ interface_id }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.address",
            "getval": re.compile(
                r"""
                ^ipv6\s+address
                (?:
                    \s+(?P<dhcp>dhcp)
                    |
                    \s+(?P<autoconfig>autoconfig)(?:\s+(?P<autoconfig_default>default))?
                    |
                    \s+(?P<use_link_local>use-link-local-only)
                    |
                    \s+(?P<ipv6_prefix>\S+)
                        (?:
                            \s+aggregate-prefix-length\s+(?P<aggregate_prefix_length>\S+)
                        )?
                        (?:
                            \s+(?P<anycast>anycast)
                        )?
                        (?:
                            \s+(?P<eui64>eui64)
                        )?
                        (?:
                            \s+route-preference\s+(?P<route_preference>\S+)
                        )?
                        (?:
                            \s+tag\s+(?P<tag>\S+)
                        )?
                        (?:
                            \s+(?P<use_bia>use-bia)
                        )?
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv6_address",
            "setval": "ipv6 address"
                      "{{ ' dhcp' if ipv6_address.dhcp|d(False) else ''}}"
                      "{{ ' use-link-local-only' if ipv6_address.use_link_local_only|d(False) else ''}}"
                      "{{ ' autoconfig' if ipv6_address.autoconfig|d(False) else ''}}"
                      "{{ ' default' if ipv6_address.default|d(False) else ''}}"
                      "{{ ' ' + ipv6_address.ipv6_address|string if ipv6_address.ipv6_address is defined else ''}}"
                      "{{ ' route-preference ' + ipv6_address.route_preference|string if ipv6_address.route_preference is defined else ''}}"
                      "{{ ' aggregate-prefix-length ' + ipv6_address.aggregate_prefix_length|string "
                      "if ipv6_address.aggregate_prefix_length is defined else ''}}"
                      "{{ ' tag ' + ipv6_address.tag|string if ipv6_address.tag is defined else ''}}"
                      "{{ ' use-bia' if ipv6_address.use_bia|d(False) else ''}}"
                      "{{ ' eui64' if ipv6_address.eui64|d(False) else ''}}"
                      "{{ ' anycast' if ipv6_address.anycast|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "address": [{
                            "dhcp": "{{ not not dhcp }}",
                            "use_link_local_only": "{{ not not use_link_local_only }}",
                            "autoconfig": "{{ not not autoconfig }}",
                            "default": "{{ not not default }}",
                            "ipv6_address": "{{ ipv6_address }}",
                            "route_preference": "{{ route_preference }}",
                            "tag": "{{ tag }}",
                            "use_bia": "{{ not not use_bia }}",
                            "eui64": "{{ not not eui64 }}",
                            "anycast": "{{ not not anycast }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "ipv6.redirects",
            "getval": re.compile(
                r"""
                \s+ipv6\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 redirects",
            "result": {
                "{{ name }}": {
                    "ipv6":
                    {
                        "redirects": True,
                    },
                },
            },
        },
        {
            "name": "ipv6.unreachables",
            "getval": re.compile(
                r"""
                \s+ipv6\sunreachables
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 unreachables",
            "result": {
                "{{ name }}": {
                    "ipv6":
                    {
                        "unreachables": True,
                    },
                },
            },
        },
        {
            "name": "ipv6.verify",
            "getval": re.compile(
                r"""
                ^ipv6\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ipv6 verify unicast source reachable-via "
                      "{{ ipv6.verify.mode|string + ' ' if ipv6.verify.mode else ''}}"
                      "{{ 'allow-default' if ipv6.verify.allow_default|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "verify": {
                            "unicast": {
                                "source": {
                                    "reachable_via": {
                                        "mode": "{{ mode }}",
                                        "allow_default": "{{ not not allow_default }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.dhcp",
            "getval": re.compile(
                r"""
                ^ipv6\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                    |
                    \s+relay
                    (?:
                        \s+address
                        (?:
                            \s+(?P<relay_ip>\S+)
                            (?:\s+use-vrf\s+(?P<vrf_name>\S+))?
                            (?:\s+interface\s+(?P<interface_type>ethernet|vlan|port-channel|loopback)\s+(?P<interface_id>\S+))?
                        )?
                        |
                        \s+source-interface
                            \s+(?P<source_interface_type>ethernet|vlan|port-channel|loopback)
                            \s+(?P<source_interface_id>\S+)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv6_dhcp",
            "setval": "ipv6 dhcp"
                      "{{ ' smart-relay' if ipv6_dhcp.smart_relay|d(False) else ''}}"
                      "{{ ' relay address ' + ipv6_dhcp.relay_ip|string if ipv6_dhcp.relay_ip else ''}}"
                      "{{ ' interface ' + ipv6_dhcp.interface_type|string + ' ' + ipv6_dhcp.interface_id|string if ipv6_dhcp.interface_type else ''}}"
                      "{{ ' use-vrf ' + ipv6_dhcp.vrf_name|string if ipv6_dhcp.vrf_name else ''}}"
                      "{{ ' relay source-interface ' + ipv6_dhcp.source_interface_type|string if ipv6_dhcp.source_interface_type else ''}}"
                      "{{ ' ' + ipv6_dhcp.source_interface_id|string if ipv6_dhcp.source_interface_id else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "dhcp": {
                            "smart_relay": "{{ not not smart_relay }}",
                            "relay": {
                                "address": [{
                                    "relay_ip": "{{ relay_ip }}",
                                    "vrf_name": "{{ vrf_name }}",
                                    "interface_type": "{{ interface_type }}",
                                    "interface_id": "{{ interface_id }}",
                                }],
                                "source_interface": {
                                    "interface_type": "{{ source_interface_type }}",
                                    "interface_id": "{{ source_interface_id }}",
                                },
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
