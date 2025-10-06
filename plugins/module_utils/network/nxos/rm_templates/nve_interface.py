# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Nve_interface parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Nve_interfaceTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Nve_interfaceTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "enabled",
            "getval": re.compile(
                r"""
                (?P<negate>\s+no)?
                (?P<shutdown>\s+shutdown)
                $""", re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "enabled": "{{ False if shutdown is defined and negate is not defined else True }}",
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s+(?P<description>.+)
                $""", re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                "description": "{{ description }}",
            },
        },
        {
            "name": "host_reachability_bgp",
            "getval": re.compile(
                r"""
                (?P<host_reachability_bgp>\s+host-reachability\s+protocol\s+bgp\s*)
                $ """, re.VERBOSE,
            ),
            "setval": "host-reachability protocol bgp",
            "result": {
                "host_reachability_bgp": "{{ True if host_reachability_bgp }}",
            },
        },
        {
            "name": "advertise_virtual_rmac",
            "getval": re.compile(
                r"""
                (?P<advertise_virtual_rmac>\s+advertise\svirtual-rmac\s*)
                $""", re.VERBOSE,
            ),
            "setval": "advertise virtual-rmac",
            "result": {
                "advertise_virtual_rmac": "{{ True if advertise_virtual_rmac }}",
            },
        },
        {
            "name": "source_interface_name",
            "getval": re.compile(
                r"""
                \s+source-interface\s+(?P<source_interface_name>loopback\d+)
                $""", re.VERBOSE,
            ),
            "setval": "source-interface {{ source_interface_name }}",
            "result": {
                "source_interface_name": "{{ source_interface_name }}",
            },
        },
        {
            "name": "source_interface_hold_time",
            "getval": re.compile(
                r"""
                \s+source-interface\s+hold-down-time\s+(?P<source_interface_hold_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "source-interface hold-down-time {{ source_interface_hold_time }}",
            "result": {
                "source_interface_hold_time": "{{ source_interface_hold_time }}",
            },
        },
        {
            "name": "global_ingress_replication_bgp",
            "getval": re.compile(
                r"""
                (?P<global_ingress_replication_bgp>\s+global\s+ingress-replication\sprotocol\s+bgp\s*)
                $""", re.VERBOSE,
            ),
            "setval": "global ingress-replication protocol bgp",
            "result": {
                "global_ingress_replication_bgp": "{{ True if global_ingress_replication_bgp }}",
            },
        },
        {
            "name": "global_suppress_arp",
            "getval": re.compile(
                r"""
                (?P<global_suppress_arp>\s+global\s+suppress-arp\s*)
                $""", re.VERBOSE,
            ),
            "setval": "global suppress-arp",
            "result": {
                "global_suppress_arp": "{{ True if global_suppress_arp }}",
            },
        },
        {
            "name": "global_multicast_group",
            "getval": re.compile(
                r"""
                \s+global\s+mcast-group\s+(?P<address>\S+)\s+
                (?P<mode>\S+)
                $""", re.VERBOSE,
            ),
            "setval": (
                "global mcast-group"
                " {{ global_multicast_group.address }}"
                " {{ global_multicast_group.mode }}"
            ),
            "result": {
                "global_multicast_group": {
                    "address": "{{ address }}",
                    "mode": "{{ mode }}",
                },
            },
        },
        {
            "name": "multisite_interface",
            "getval": re.compile(
                r"""
                \s+multisite\s+border-gateway\s+interface\s+(?P<multisite_interface>\s*)
                $""", re.VERBOSE,
            ),
            "setval": "multisite border-gateway interface {{ multisite_interface }}",
            "result": {
                "multisite_interface": "{{ multisite_interface }}",
            },
        },
        # Start vni parsers
        {
            "name": "vni_id",
            "getval": re.compile(
                r"""
                \s+member\s+vni\s+(?P<vni_id>\d+)
                (?P<associate_vrf>\s+associate-vrf\s*)?
                $""", re.VERBOSE,
            ),
            "setval": (
                "member vni {{ vni_id }}"
                "{{ ' associate-vrf' if associate_vrf|d(None) else '' }}"
            ),
            "result": {
                "vnis": {
                    "{{ vni_id }}": {
                        "vni_id": "{{ vni_id }}",
                        "associate_vrf": "{{ True if associate_vrf }}",
                    },
                },
            },
        },
        {
            "name": "suppress_arp",
            "getval": re.compile(
                r"""
                \s+member\s+vni\s+(?P<vni_id>\d+)
                (?P<suppress_arp>\s+suppress-arp\s*)
                $""", re.VERBOSE,
            ),
            "setval": "suppress-arp",
            "result": {
                "vnis": {
                    "{{ vni_id }}": {
                        "suppress_arp": "{{ True if suppress_arp }}",
                    },
                },
            },
        },
        {
            "name": "suppress_arp_disable",
            "getval": re.compile(
                r"""
                \s+member\s+vni\s+(?P<vni_id>\d+)
                (?P<suppress_arp_disable>\s+suppress-arp\s+disable\s*)
                $""", re.VERBOSE,
            ),
            "setval": "suppress-arp disable",
            "result": {
                "vnis": {
                    "{{ vni_id }}": {
                        "suppress_arp_disable": "{{ True if suppress_arp_disable }}",
                    },
                },
            },
        },
        {
            "name": "multisite_ingress_replication",
            "getval": re.compile(
                r"""
                \s*member\s+vni\s+(?P<vni_id>\d+)
                (?P<multisite_ingress_replication>\s+multisite\s+ingress-replication\s*)
                $""", re.VERBOSE,
            ),
            "setval": "multisite ingress-replication",
            "result": {
                "vnis": {
                    "{{ vni_id }}": {
                        "multisite_ingress_replication": "{{ True if multisite_ingress_replication }}",
                    },
                },
            },
        },
        {
            "name": "ingress_replication_bgp",
            "getval": re.compile(
                r"""
                \s*member\s+vni\s+(?P<vni_id>\d+)
                (?P<ingress_replication_bgp>\s+ingress-replication\s+protocol\s+bgp\s*)
                $""", re.VERBOSE,
            ),
            "setval": "ingress-replication protocol bgp",
            "result": {
                "vnis": {
                    "{{ vni_id }}": {
                        "ingress_replication_bgp": "{{ True if ingress_replication_bgp }}",
                    },
                },
            },
        },
        # End vni parsers
    ]
    # fmt: on
