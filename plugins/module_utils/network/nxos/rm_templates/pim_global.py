# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The Pim_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Pim_globalTemplate(NetworkTemplate):
    """The parser templates class of nxos_pim_global."""

    def __init__(self, lines=None, module=None):
        super(Pim_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                ^ip\spim\s(?P<bfd>bfd)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim bfd",
            "result": {
                "bfd": True,
            },
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                ^ip\spim\s(?P<log_neighbor_changes>log-neighbor-changes)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim log-neighbor-changes",
            "result": {
                "log_neighbor_changes": True,
            },
        },
        {
            "name": "flush_routes",
            "getval": re.compile(
                r"""
                ^ip\spim\s(?P<flush_routes>flush-routes)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim flush-routes",
            "result": {
                "flush_routes": True,
            },
        },
        {
            "name": "register_rate_limit",
            "getval": re.compile(
                r"""
                ^ip\spim\sregister-rate-limit\s(?P<register_rate_limit>\d+)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim register-rate-limit {{ register_rate_limit }}",
            "remval": "ip pim register-rate-limit",
            "result": {
                "register_rate_limit": "{{ register_rate_limit }}",
            },
        },
        {
            "name": "ssm_range",
            "getval": re.compile(
                r"""
                ^ip\spim\sssm\srange\s(?P<ssm_range>\S.*?)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim ssm range {{ ssm_range | join(' ') }}",
            # any 'no ip pim ssm range <range>' resets the whole line to the default (232.0.0.0/8)
            "remval": "ip pim ssm range {{ ssm_range[0] }}",
            "result": {
                "ssm_range": "{{ ssm_range.split() }}",
            },
        },
        {
            "name": "rp_address",
            "getval": re.compile(
                r"""
                ^ip\spim\srp-address\s(?P<rp_address>\S+)
                (\sgroup-list\s(?P<group_list>\S+))?
                (\sprefix-list\s(?P<prefix_list>\S+))?
                (\sroute-map\s(?P<route_map>\S+))?
                (\s(?P<bidir>bidir))?
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim rp-address {{ rp_address }}"
                      "{{ (' group-list ' ~ group_list) if group_list is defined else '' }}"
                      "{{ (' prefix-list ' ~ prefix_list) if prefix_list is defined else '' }}"
                      "{{ (' route-map ' ~ route_map) if route_map is defined else '' }}"
                      "{{ ' bidir' if bidir|d(False) else '' }}",
            "result": {
                "rp_addresses": {
                    "{{ rp_address ~ '_' ~ (group_list|d(prefix_list|d(route_map|d('')))) }}": {
                        "rp_address": "{{ rp_address }}",
                        "group_list": "{{ group_list }}",
                        "prefix_list": "{{ prefix_list }}",
                        "route_map": "{{ route_map }}",
                        "bidir": "{{ True if bidir is defined else None }}",
                    },
                },
            },
        },
        {
            "name": "anycast_rp",
            "getval": re.compile(
                r"""
                ^ip\spim\sanycast-rp\s(?P<anycast_rp>\S+)\s(?P<member>\S+)
                \s*$""", re.VERBOSE,
            ),
            "setval": "ip pim anycast-rp {{ anycast_rp }} {{ member }}",
            "result": {
                "anycast_rps": {
                    "{{ anycast_rp }}": {
                        "anycast_rp": "{{ anycast_rp }}",
                        "members": {
                            "{{ member }}": "{{ member }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
