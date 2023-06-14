# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Static_routes parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Static_routesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Static_routesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            'name': 'vrf',
            'getval': re.compile(
                r'''
                ^vrf\scontext\s(?P<namevrf>\S+)$
                ''', re.VERBOSE,
            ),
            'setval': 'vrf context {{ namevrf }}',
            'result': {
                # '{{ namevrf }}': {
                #     'namevrf': '{{ namevrf }}',
                # },
            },
            'shared': True,
        },
        {
            "name": "ipv4",
            "getval": re.compile(
                r"""
                (^|\s+)ip\sroute
                (\s(?P<dest>\S+))
                (\s(?P<interface>(Ethernet|loopback|mgmt|Null|port-channel)\S+))?
                (\s(?P<forward_router_address>\S+))?
                (\svrf\s(?P<dest_vrf>\S+))?
                (\sname\s(?P<route_name>\S+))?
                (\stag\s(?P<tag>\d+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<admin_distance>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "ip route"
            "{{ (' ' + ip.dest) if ip.dest is defined else '' }}"
            "{{ (' ' + ip.interface) if ip.interface is defined else '' }}"
            "{{ (' ' + ip.forward_router_address) if ip.forward_router_address is defined else '' }}"
            "{{ (' vrf ' + ip.dest_vrf) if ip.dest_vrf is defined else '' }}"
            "{{ (' name ' + ip.route_name) if ip.route_name is defined else '' }}"
            "{{ (' tag ' + ip.tag|string) if ip.tag is defined else '' }}"
            "{{ (' track ' + ip.track|string) if ip.track is defined else '' }}"
            "{{ (' ' + ip.admin_distance|string) if ip.admin_distance is defined else '' }}",
            "result": {
                "{{ dest }}_{{ interface|d() }}_{{ namevrf|d() }}_ipv4": [
                    {
                        "_vrf": "{{ namevrf }}",
                        "_afi": "ipv4",
                        "_dest": "{{ dest }}",
                        "interface": "{{ interface }}",
                        "forward_router_address": "{{ forward_router_address }}",
                        "admin_distance": "{{ admin_distance }}",
                        "dest_vrf": "{{ dest_vrf }}",
                        "tag": "{{ tag }}",
                        "route_name": "{{ route_name }}",
                        "track": "{{ track }}",
                    },
                ],
            },
        },
        {
            "name": "ipv6",
            "getval": re.compile(
                r"""
                (^|\s+)ipv6\sroute
                (\s(?P<dest>\S+))
                (\s(?P<interface>(Ethernet|loopback|mgmt|Null|port-channel)\S+))?
                (\s(?P<forward_router_address>\S+))?
                (\svrf\s(?P<dest_vrf>\S+))?
                (\sname\s(?P<route_name>\S+))?
                (\stag\s(?P<tag>\d+))?
                (\strack\s(?P<track>\d+))?
                (\s(?P<admin_distance>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "ipv6 route"
            "{{ (' ' + ipv6.dest) if ipv6.dest is defined else '' }}"
            "{{ (' ' + ipv6.interface) if ipv6.interface is defined else '' }}"
            "{{ (' ' + ipv6.forward_router_address) if ipv6.forward_router_address is defined else '' }}"
            "{{ (' vrf ' + ipv6.dest_vrf) if ipv6.dest_vrf is defined else '' }}"
            "{{ (' name ' + ipv6.route_name) if ipv6.route_name is defined else '' }}"
            "{{ (' tag ' + ipv6.tag|string) if ipv6.tag is defined else '' }}"
            "{{ (' track ' + ipv6.track|string) if ipv6.track is defined else '' }}"
            "{{ (' ' + ipv6.admin_distance|string) if ipv6.admin_distance is defined else '' }}",
            "result": {
                "{{ dest }}_{{ interface|d() }}_{{ namevrf|d() }}_ipv6": [
                    {
                        "_vrf": "{{ namevrf }}",
                        "_afi": "ipv4",
                        "_dest": "{{ dest }}",
                        "interface": "{{ interface }}",
                        "forward_router_address": "{{ forward_router_address }}",
                        "admin_distance": "{{ admin_distance }}",
                        "dest_vrf": "{{ dest_vrf }}",
                        "tag": "{{ tag }}",
                        "route_name": "{{ route_name }}",
                        "track": "{{ track }}",
                    },
                ],
            },
        },
    ]
    # fmt: on
