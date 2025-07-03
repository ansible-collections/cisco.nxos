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
                r"""\s+mac-address
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
                \s+bandwidth
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
            "name": "dot1q",
            "getval": re.compile(
                r"""
                ^\s*encapsulation\s+dot1q\s+(?P<vlan_id>\d+)\s*$
                """,
                re.VERBOSE,
            ),
            "setval": "encapsulation dot1q"
                      "{{ ' ' + dot1q|string if dot1q is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "dot1q": "{{ vlan_id }}",
                },
            },
        },
        {
            "name": "evpn_multisite_tracking",
            "getval": re.compile(
                r"""
                \s+evpn\s+multisite
                \s+
                (?P<tracking_type>dci-tracking|fabric-tracking)
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "evpn multisite"
                      "{{ ' ' + evpn_multisite_tracking|string "
                      "if evpn_multisite_tracking is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "evpn_multisite_tracking": "{{ tracking_type }}",
                },
            },
        },
        {
            "name": "ipv4.address",
            "getval": re.compile(
                r"""
                \s+ip\s+address
                (?:
                    \s+(?P<address>\S+)
                    (?:\s+(?P<ip_network_mask>(?!secondary\b)\S+))?
                    (?:\s+(?P<secondary>secondary))?
                    (?:\s+route-preference\s+(?P<route_preference>\d+))?
                    (?:\s+tag\s+(?P<tag>\d+))?
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.address.address is defined %}"
                "ip address {{ ipv4.address.address|string }}"
                "{% endif %}"
                "{% if ipv4.address.address is not defined and ipv4.address.ip_network_mask is defined %}"
                "ip address {{ ipv4.address.ip_network_mask|string }}"
                "{% endif %}"
                "{% if ipv4.address.address is defined and ipv4.address.ip_network_mask is defined %}"
                " {{ ipv4.address.ip_network_mask|string }}"
                "{% endif %}"
                "{% if ipv4.address.secondary is defined %}"
                " secondary"
                "{% endif %}"
                "{% if ipv4.address.route_preference is defined %}"
                " route-preference {{ ipv4.address.route_preference|string }}"
                "{% endif %}"
                "{% if ipv4.address.tag is defined %}"
                " tag {{ ipv4.address.tag|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": [{
                        "address": "{{ address }}",
                        "ip_network_mask": "{{ ip_network_mask }}",
                        "route_preference": "{{ route_preference }}",
                        "tag": "{{ tag }}",
                        "secondary": "{{ not not secondary }}",
                    }],
                },
            },
        },
        {
            "name": "redirects",
            "getval": re.compile(
                r"""
                \s+ip\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "ip redirects",
            "result": {
                "{{ name }}": {
                    "redirects": True,
                },
            },
        },
        {
            "name": "no_redirects",
            "getval": re.compile(
                r"""
                \s+no\sip\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "no ip redirects",
            "result": {
                "{{ name }}": {
                    "redirects": False,
                },
            },
        },
        {
            "name": "unreachables",
            "getval": re.compile(
                r"""
                \s+ip\sunreachables
                $""", re.VERBOSE,
            ),
            "setval": "ip unreachables",
            "result": {
                "{{ name }}": {
                    "unreachables": True,
                },
            },
        },
        {
            "name": "proxy_arp",
            "getval": re.compile(
                r"""
                \s+ip\sproxy-arp
                $""", re.VERBOSE,
            ),
            "setval": "ip proxy-arp",
            "result": {
                "{{ name }}": {
                    "proxy_arp": True,
                },
            },
        },
        {
            "name": "port_unreachable",
            "getval": re.compile(
                r"""
                \s+ip\sport-unreachable
                $""", re.VERBOSE,
            ),
            "setval": "ip port-unreachable",
            "result": {
                "{{ name }}": {
                    "port_unreachable": True,
                },
            },
        },
        {
            "name": "verify",
            "getval": re.compile(
                r"""
                \s+ip\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ip verify unicast source reachable-via"
                      "{{ ' ' + verify.unicast.source.reachable_via.mode|string "
                      "if verify.unicast.source.reachable_via.mode else ''}}"
                      "{{ ' allow-default'"
                      " if verify.unicast.source.reachable_via.allow_default|d(False) else ''}}",
            "result": {
                "{{ name }}": {
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
        {
            "name": "dhcp.ipv4",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.smart_relay is defined %}"
                "ip dhcp smart-relay"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "smart_relay": "{{ not not smart_relay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "dhcp.ipv4.option82",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+option82\s+suboption\s+circuit-id\s+(?P<circuit_id>\S+)
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.option82.suboption.circuit_id is defined %}"
                "ip dhcp option82 suboption circuit-id {{ dhcp.ipv4.option82.suboption.circuit_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "option82": {
                                "suboption": {
                                    "circuit_id": "{{ circuit_id }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "dhcp.ipv4.information",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+relay
                    (?:
                        \s+information\s+(?P<trusted>trusted)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.relay.information.trusted is defined %}"
                "ip dhcp relay information trusted"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "relay": {
                                "information": {
                                    "trusted": "{{ not not trusted }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "dhcp.ipv4.subnet_selection",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+relay
                    (?:
                        \s+subnet-selection\s+(?P<subnet_ip>\S+)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.relay.subnet_selection.subnet_ip is defined %}"
                "ip dhcp relay subnet-selection {{ dhcp.ipv4.relay.subnet_selection.subnet_ip }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "relay": {
                                "subnet_selection": {
                                    "subnet_ip": "{{ subnet_ip }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "dhcp.ipv4.source_interface",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+relay
                    (?:
                        \s+source-interface
                            \s+(?P<interface_type>ethernet|vlan|port-channel|loopback)
                            \s+(?P<interface_id>\S+)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.relay.source_interface.interface_type is defined %}"
                "ip dhcp relay source-interface {{ dhcp.ipv4.relay.source_interface.interface_type|string }}"
                " {{ dhcp.ipv4.relay.source_interface.interface_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "relay": {
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
            "name": "dhcp.ipv4.address",
            "getval": re.compile(
                r"""
                \s+ip\s+dhcp
                (?:
                    \s+relay
                    (?:
                        \s+address
                        (?:
                            \s+(?P<relay_ip>\S+)
                            (?:\s+use-vrf\s+(?P<vrf_name>\S+))?
                        )?
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv4.relay_ip is defined %}"
                "ip dhcp relay address {{ dhcp.ipv4.relay_ip|string }}"
                "{% endif %}"
                "{% if dhcp.ipv4.vrf_name is defined %}"
                " use-vrf {{ dhcp.ipv4.vrf_name|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv4": {
                            "relay": {
                                "address": [{
                                    "relay_ip": "{{ relay_ip }}",
                                    "vrf_name": "{{ vrf_name }}",
                                }],
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
                \s+ipv6\s+address
                (?:
                    \s+(?P<address>\S+)
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
            "compval": "ipv6",
            "setval": "{% if ipv6.address.address is defined %}"
                      "ipv6 address {{ ipv6.address.address|string }}"
                      "{% endif %}"
                      "{% if ipv6.address.route_preference is defined %}"
                      " route-preference {{ ipv6.address.route_preference|string }}"
                      "{% endif %}"
                      "{% if ipv6.address.aggregate_prefix_length is defined %}"
                      " aggregate-prefix-length {{ ipv6.address.aggregate_prefix_length|string }}"
                      "{% endif %}"
                      "{% if ipv6.address.tag is defined %}"
                      " tag {{ ipv6.address.tag|string }}"
                      "{% endif %}"
                      "{% if ipv6.address.use_bia is defined %}"
                      " use-bia"
                      "{% endif %}"
                      "{% if ipv6.address.eui64 is defined %}"
                      " eui64"
                      "{% endif %}"
                      "{% if ipv6.address.anycasts is defined %}"
                      " anycast"
                      "{% endif %}",
            "result": {
                "{{ name }}": {
                    "ipv6": [{
                        "address": "{{ address }}",
                        "route_preference": "{{ route_preference }}",
                        "aggregate_prefix_length": "{{ aggregate_prefix_length }}",
                        "tag": "{{ tag }}",
                        "use_bia": "{{ not not use_bia }}",
                        "eui64": "{{ not not eui64 }}",
                        "anycast": "{{ not not anycast }}",
                    }],
                },
            },
        },
        {
            "name": "ipv6_redirects",
            "getval": re.compile(
                r"""
                \s+ipv6\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 redirects",
            "result": {
                "{{ name }}": {
                    "ipv6_redirects": True,
                },
            },
        },
        {
            "name": "ipv6_no_redirects",
            "getval": re.compile(
                r"""
                \s+no\sipv6\sredirects
                $""", re.VERBOSE,
            ),
            "setval": "no ipv6 redirects",
            "result": {
                "{{ name }}": {
                    "ipv6_redirects": False,
                },
            },
        },
        {
            "name": "ipv6_unreachables",
            "getval": re.compile(
                r"""
                \s+ipv6\sunreachables
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 unreachables",
            "result": {
                "{{ name }}": {
                    "ipv6_unreachables": True,
                },
            },
        },
        {
            "name": "ipv6_verify",
            "getval": re.compile(
                r"""
                \s+ipv6\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ipv6 verify unicast source reachable-via "
                      "{{ verify.unicast.source.reachable_via.mode|string + ' '"
                      " if verify.unicast.source.reachable_via.mode else ''}}"
                      "{{ 'allow-default'"
                      " if verify.unicast.source.reachable_via.allow_default|d(False) else ''}}",
            "result": {
                "{{ name }}": {
                    "ipv6_verify": {
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
        {
            "name": "dhcp.ipv6",
            "getval": re.compile(
                r"""
                \s+ipv6\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv6.smart_relay is defined %}"
                "ipv6 dhcp smart-relay"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv6": {
                            "smart_relay": "{{ not not smart_relay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "dhcp.ipv6.source_interface",
            "getval": re.compile(
                r"""
                \s+ipv6\s+dhcp
                (?:
                    \s+relay
                    (?:
                        \s+source-interface
                            \s+(?P<source_interface_type>ethernet|vlan|port-channel|loopback)
                            \s+(?P<source_interface_id>\S+)
                    )
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv6.source_interface_type is defined %}"
                "ipv6 dhcp relay source-interface {{ dhcp.ipv6.source_interface_type|string }} {{ dhcp.ipv6.source_interface_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv6": {
                            "relay": {
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
        {
            "name": "dhcp.ipv6.address",
            "getval": re.compile(
                r"""
                ^\s*ipv6\s+dhcp
                \s+relay
                \s+address
                \s+(?P<relay_ip>\S+)
                (?:\s+interface\s+(?P<interface_type>ethernet|vlan|port-channel)\s+(?P<interface_id>\S+))?
                (?:\s+use-vrf\s+(?P<vrf_name>\S+))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "dhcp",
            "setval": (
                "{% if dhcp.ipv6.relay_ip is defined %}"
                "ipv6 dhcp relay address {{ dhcp.ipv6.relay_ip|string }}"
                "{% endif %}"
                "{% if dhcp.ipv6.interface_type is defined %}"
                " interface {{ dhcp.ipv6.interface_type|string }} {{ dhcp.ipv6.interface_id|string }}"
                "{% endif %}"
                "{% if dhcp.ipv6.vrf_name is defined %}"
                " use-vrf {{ dhcp.ipv6.vrf_name|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "dhcp": {
                        "ipv6": {
                            "relay": {
                                "address": [{
                                    "relay_ip": "{{ relay_ip }}",
                                    "vrf_name": "{{ vrf_name }}",
                                    "interface_type": "{{ interface_type }}",
                                    "interface_id": "{{ interface_id }}",
                                }],
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
