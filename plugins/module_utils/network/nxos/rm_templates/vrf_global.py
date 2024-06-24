# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vrf_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


def name_server_addr_list(lines, tmplt):
    pass


class Vrf_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vrf_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^vrf\scontext\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "vrf context {{ name }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s(?P<description>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        'description': '{{ description }}',
                    },
                },
            },
        },
        {
            "name": "ip.auto_discard",
            "getval": re.compile(
                r"""
                \s+ip\s(?P<auto_disc>auto-discard)
                $""", re.VERBOSE,
            ),
            "setval": "ip auto-discard",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "auto_discard": "{{ true if auto_disc is defined }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ip.domain_list",
            "getval": re.compile(
                r"""
                \s+ip\sdomain-list\s(?P<domain_list>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip domain-list {{ domain_list }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "domain_list": [
                                "{{ domain_list }}",
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "ip.domain_name",
            "getval": re.compile(
                r"""
                \s+ip\sdomain-name\s(?P<domain_name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip domain-name {{ ip.domain_name }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "domain_name": "{{ domain_name }}",
                        },
                    },
                },
            },
        },
        {
            "name": "ip.icmp_err.source_interface",
            "getval": re.compile(
                r"""
                \s+ip\sicmp-errors
                \ssource-interface\s(?P<interface>eth|po|lo)
                (?P<interface_val>(\d+\S*))
                $""", re.VERBOSE,
            ),
            "setval": "ip icmp-errors source-interface {{ interface }} {{ interface_value }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "icmp_err": {
                                "source_interface": {
                                    "interface": "{{ 'ethernet' if 'eth' in interface }}"
                                    "{{ 'port-channel' if 'po' in interface }}"
                                    "{{ 'loopback' if 'lo' in interface }}",
                                    "interface_value": "{{ interface_val }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.igmp.ssm_translate",
            "getval": re.compile(
                r"""
                \s+ip\sigmp
                \sssm-translate
                \s(?P<group_val>\S+)
                \s(?P<source_val>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip igmp ssm-translate {{ group }} {{ source }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "igmp": {
                                "ssm_translate": {
                                    "group": "{{ group_val }}",
                                    "source": "{{ source_val }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.mroutes",
            "getval": re.compile(
                r"""
                \s+ip\smroute
                \s(?P<group_val>\S+)
                \s(?P<source_val>\S+)
                (\s(?P<pref_val>\d+))?
                (\svrf\s(?P<vrf_val>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "ip mroute {{ group }} {{ source }}"
            "{{ ' ' + preference if preference is defined }}"
            "{{ ' vrf ' + vrf if vrf is defined }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "mroutes": [
                                {
                                    "group": "{{ group_val }}",
                                    "source": "{{ source_val }}",
                                    "preference": "{{ pref_val if pref_val is defined }}",
                                    "vrf": "{{ vrf_val if vrf_val is defined }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.group_range_prefix_list",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \sprefix-list\s(?P<prefix_lst>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast group-range prefix-list {{ group_range_prefix_list }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "group_range_prefix_list": "{{ prefix_lst }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.resilient",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath\s(?P<res>resilient)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath resilient",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "resilient": "{{ true if res is defined }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.splitting_type.none",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath\s(?P<noneval>none)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath none",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "splitting_type": {
                                        "none": "{{ true if noneval is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.splitting_type.legacy",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath\s(?P<legacy_val>legacy)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath legacy",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "splitting_type": {
                                        "legacy": "{{ true if legacy_val is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.splitting_type.nbm",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath\s(?P<nbm_val>nbm)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath nbm",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "splitting_type": {
                                        "nbm": "{{ true if nbm_val is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.splitting_type.sg_hash",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath\s(?P<sg_hash_val>s-g-hash)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath s-g-hash",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "splitting_type": {
                                        "sg_hash": "{{ true if sg_hash_val is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.multipath.splitting_type.sg_hash_next_hop",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \smultipath
                \s(?P<sg_hash_nxt_val>s-g-hash\snext-hop-based)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast multipath s-g-hash next-hop-based",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "multipath": {
                                    "splitting_type": {
                                        "sg_hash_next_hop": "{{ true if sg_hash_nxt_val is defined }}",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.multicast.rpf",
            "getval": re.compile(
                r"""
                \s+ip\smulticast
                \srpf\sselect
                \svrf\s(?P<vrf_val>\S+)
                \sgroup-list\s(?P<group_list>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip multicast rpf select vrf {{ vrf_name }} group-list {{ group_list_range }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "multicast": {
                                "rpf": [
                                    {
                                        "vrf_name": "{{ vrf_val }}",
                                        "group_list_range": "{{ group_list }}",
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.name_server.address_list",
            "getval": re.compile(
                r"""
                \s+ip\sname-server
                \s(?P<addr_list>.+$)
                $""", re.VERBOSE,
            ),
            "setval": name_server_addr_list,
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "name_server": {
                                "address_list": "{{ addr_list }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.name_server.use_vrf",
            "getval": re.compile(
                r"""
                \s+ip\sname-server
                \s(?P<source_addr>\S+)
                \suse-vrf\s(?P<vrf_name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip name-server {{ source_address }} use-vrf {{ vrf }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "name_server": {
                                "use_vrf": {
                                    "source_address": "{{ source_addr }}",
                                    "vrf": "{{ vrf_name }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ip.route",
            "getval": re.compile(
                r"""
                \s+ip\sroute
                \s(?P<src_val>\S+)
                \s(?P<dest_val>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip route {{ ip.route.source }} {{ ip.route.destination }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "route": [
                                {
                                    "source": "{{ src_val }}",
                                    "destination": "{{ dest_val }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "ip.route.tags",
            "getval": re.compile(
                r"""
                \s+ip\sroute
                \s(?P<src_val>\S+)
                \s(?P<dest_val>\S+)
                \stag\s(?P<tag_val>\d+)
                (\s(?P<route_pref_val>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "ip route {{ ip.route.source }} {{ ip.route.destination }} tag {{ tag }}"
            "{{ ' ' + route_pref if route_pref is defined }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "route": [
                                {
                                    "source": "{{ src_val }}",
                                    "destination": "{{ dest_val }}",
                                    "tags": {
                                        "tag_value": "{{ tag_val }}",
                                        "route_pref": "{{ route_pref_val if route_pref_val is defined }}",
                                    }
                                    
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "ip.route.vrf",
            "getval": re.compile(
                r"""
                \s+ip\sroute
                \s(?P<src_val>\S+)
                \s(?P<dest_val>\S+)
                \svrf\s(?P<vrf_val>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip route {{ ip.route.source }} {{ ip.route.destination }} vrf {{ vrf }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "route": [
                                {
                                    "source": "{{ src_val }}",
                                    "destination": "{{ dest_val }}",
                                    "vrf": "{{ vrf_val }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "ip.route.track",
            "getval": re.compile(
                r"""
                \s+ip\sroute
                \s(?P<src_val>\S+)
                \s(?P<dest_val>\S+)
                \strack\s(?P<track_val>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "ip route {{ ip.route.source }} {{ ip.route.destination }} vrf {{ vrf }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "ip" : {
                            "route": [
                                {
                                    "source": "{{ src_val }}",
                                    "destination": "{{ dest_val }}",
                                    "track": "{{ track_val }}",
                                },
                            ],
                        },
                    },
                },
            },
        },
        {
            "name": "vni",
            "getval": re.compile(
                r"""
                \s+vni\s(?P<vni_val>\d+)
                (\s(?P<l3_val>l3))?
                $""", re.VERBOSE,
            ),
            "setval": "vni {{ vni }} {{ 'l3' if l3 is defined }}",
            "result": {
                "vrfs": {
                    '{{ name }}': {
                        'name': '{{ name }}',
                        "vni": {
                            "vni_number": "{{ vni_val }}",
                            "l3": "{{ true if l3_val is defined }}",
                        },
                    },
                },
            },
        }
    ]
    # fmt: on
