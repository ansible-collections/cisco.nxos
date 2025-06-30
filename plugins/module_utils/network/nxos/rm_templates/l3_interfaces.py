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
            "name": "dotiq",
            "getval": re.compile(
                r"""
                \s+encapsulation
                \s+dot1Q         
                \s+(?P<vlan_id>\d+)   
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "encapsulation dot1Q"
                      "{{ ' ' + dotiq.vlan_id|string if dotiq.vlan_id is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "dotiq": "{{ vlan_id }}",
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
                re.VERBOSE | re.IGNORECASE
            ),
            "setval": "even multisite"
                      "{{ ' ' + evpn_multisite_tracking.tracking_type|string "
                      "if evpn_multisite_tracking.tracking_type is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "evpn_multisite_tracking": "{{ tracking_type }}",
                },
            },
        },
        {
            "name": "ipv4.addresses",
            "getval": re.compile(
                r"""
                \s+ip\s+address
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.addresses.dhcp is defined %}"
                "ip address dhcp"
                "{% endif %}"
                "{% if ipv4.addresses.ip_address is defined %}"
                "ip address {{ ipv4.addresses.ip_address|string }}"
                "{% endif %}"
                "{% if ipv4.addresses.ip_address is not defined and ipv4.addresses.ip_network_mask is defined %}"
                "ip address {{ ipv4.addresses.ip_network_mask|string }}"
                "{% endif %}"
                "{% if ipv4.addresses.ip_address is defined and ipv4.addresses.ip_network_mask is defined %}"
                " {{ ipv4.addresses.ip_network_mask|string }}"
                "{% endif %}"
                "{% if ipv4.addresses.route_preference is defined %}"
                " route-preference {{ ipv4.addresses.route_preference|string }}"
                "{% endif %}"
                "{% if ipv4.addresses.tag is defined %}"
                " tag {{ ipv4.addresses.tag|string }}"
                "{% endif %}"
                "{% if ipv4.addresses.secondary is defined %}"
                " secondary"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "addresses": [{
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
                \s+ip\sport-unreachable
                $""", re.VERBOSE,
            ),
            "setval": "ip port-unreachable",
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
                \s+ip\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ip verify unicast source reachable-via"
                      "{{ ' ' + ipv4.verify.unicast.source.reachable_via.mode|string "
                      "if ipv4.verify.unicast.source.reachable_via.mode else ''}}"
                      "{{ ' allow-default'"
                      " if ipv4.verify.unicast.source.reachable_via.allow_default|d(False) else ''}}",
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
                \s+ip\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.smart_relay is defined %}"
                "ip dhcp smart-relay"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
                            "smart_relay": "{{ not not smart_relay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ipv4.dhcp.option82",
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.option82.suboption.circuit_id is defined %}"
                "ip dhcp option82 suboption circuit-id {{ ipv4.dhcp.option82.suboption.circuit_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
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
            "name": "ipv4.dhcp.information",
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.relay.information.trusted is defined %}"
                "ip dhcp relay information trusted"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
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
            "name": "ipv4.dhcp.subnet_selection",
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.relay.subnet_selection.subnet_ip is defined %}"
                "ip dhcp relay subnet-selection {{ ipv4.dhcp.relay.subnet_selection.subnet_ip }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
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
            "name": "ipv4.dhcp.source_interface",
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.relay.source_interface.interface_type is defined %}"
                "ip dhcp relay source-interface {{ ipv4.dhcp.relay.source_interface.interface_type|string }}"
                " {{ ipv4.dhcp.relay.source_interface.interface_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
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
            "name": "ipv4.dhcp.address",
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
            "compval": "ipv4",
            "setval": (
                "{% if ipv4.dhcp.relay_ip is defined %}"
                "ip dhcp relay address {{ ipv4.dhcp.relay_ip|string }} use-vrf {{ ipv4.dhcp.vrf_name|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv4": {
                        "dhcp": {
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
            "name": "ipv6.addresses",
            "getval": re.compile(
                r"""
                \s+ipv6\s+address
                (?:
                    \s+(?P<dhcp>dhcp)
                    |
                    \s+(?P<autoconfig>autoconfig)(?:\s+(?P<autoconfig_default>default))?
                    |
                    \s+(?P<use_link_local>use-link-local-only)
                    |
                    \s+(?P<ipv6_address>\S+)
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
            "setval": "{% if ipv6.addresses.ipv6_address is defined %}"
                      "ipv6 address {{ ipv6.addresses.ipv6_address|string }}"
                      "{% endif %}"
                      "{% if ipv6.addresses.dhcp is defined %}"
                      "ipv6 address dhcp"
                      "{% endif %}"
                      "{% if ipv6.addresses.use_link_local_only is defined %}"
                      "ipv6 address use-link-local-only"
                      "{% endif %}"
                      "{% if ipv6.addresses.autoconfig is defined %}"
                      "ipv6 address autoconfig"
                      "{% endif %}"
                      "{% if ipv6.addresses.default is defined %}"
                      " default"
                      "{% endif %}"
                      "{% if ipv6.addresses.route_preference is defined %}"
                      " route-preference {{ ipv6.addresses.route_preference|string }}"
                      "{% endif %}"
                      "{% if ipv6.addresses.aggregate_prefix_length is defined %}"
                      " aggregate-prefix-length {{ ipv6.addresses.aggregate_prefix_length|string }}"
                      "{% endif %}"
                      "{% if ipv6.addresses.tag is defined %}"
                      " tag {{ ipv6.addresses.tag|string }}"
                      "{% endif %}"
                      "{% if ipv6.addresses.use_bia is defined %}"
                      " use-bia"
                      "{% endif %}"
                      "{% if ipv6.addresses.eui64 is defined %}"
                      " eui64"
                      "{% endif %}"
                      "{% if ipv6.addresses.anycasts is defined %}"
                      " anycast"
                      "{% endif %}",
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "addresses": [{
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
                \s+ipv6\s+verify\s+unicast\s+source\s+reachable-via
                \s+(?P<mode>\S+)
                (?:\s+(?P<allow_default>allow-default))?
                \s*$
                """,
                re.VERBOSE,
            ),
            "setval": "ipv6 verify unicast source reachable-via "
                      "{{ ipv6.verify.unicast.source.reachable_via.mode|string + ' '"
                      " if ipv6.verify.unicast.source.reachable_via.mode else ''}}"
                      "{{ 'allow-default'"
                      " if ipv6.verify.unicast.source.reachable_via.allow_default|d(False) else ''}}",
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
                \s+ipv6\s+dhcp
                (?:
                    \s+(?P<smart_relay>smart-relay)
                )
                \s*$
                """,
                re.VERBOSE,
            ),
            "compval": "ipv6",
            "setval": (
                "{% if ipv6.dhcp.smart_relay is defined %}"
                "ipv6 dhcp smart-relay"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "dhcp": {
                            "smart_relay": "{{ not not smart_relay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ipv6.dhcp.source_interface",
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
            "compval": "ipv6",
            "setval": (
                "{% if ipv6.dhcp.source_interface_type is defined %}"
                "ipv6 dhcp relay source-interface {{ ipv6.dhcp.source_interface_type|string }} {{ ipv6.dhcp.source_interface_id|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "dhcp": {
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
            "name": "ipv6.dhcp.address",
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
            "compval": "ipv6",
            "setval": (
                "{% if ipv6.dhcp.relay_ip is defined %}"
                "ipv6 dhcp relay address {{ ipv6.dhcp.relay_ip|string }}"
                "{% endif %}"
                "{% if ipv6.dhcp.interface_type is defined %}"
                " interface {{ ipv6.dhcp.interface_type|string }} {{ ipv6.dhcp.interface_id|string }}"
                "{% endif %}"
                "{% if ipv6.dhcp.vrf_name is defined %}"
                " use-vrf {{ ipv6.dhcp.vrf_name|string }}"
                "{% endif %}"
            ),
            "result": {
                "{{ name }}": {
                    "ipv6": {
                        "dhcp": {
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
