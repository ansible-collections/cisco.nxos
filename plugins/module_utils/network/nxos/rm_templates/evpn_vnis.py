# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Evpn_vnis parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_VNI = "{{ vni }}"
_RT = "{{ rt }}"


class Evpn_vnisTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Evpn_vnisTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            # parent context only, used to render the `evpn` line
            "name": "evpn",
            "getval": re.compile(
                r'''
                ^evpn$
                ''',
                re.VERBOSE,
            ),
            "setval": "evpn",
            "result": {},
        },
        {
            "name": "vni",
            "getval": re.compile(
                r'''
                ^\s+vni\s(?P<vni>\d+)\sl2$
                ''',
                re.VERBOSE,
            ),
            "setval": "vni {{ vni }} l2",
            "result": {
                _VNI: {
                    "vni": _VNI,
                },
            },
            "shared": True,
        },
        {
            "name": "route_distinguisher",
            "getval": re.compile(
                r'''
                ^\s+rd\s(?P<route_distinguisher>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "rd {{ route_distinguisher }}",
            "result": {
                _VNI: {
                    "route_distinguisher": "{{ route_distinguisher }}",
                },
            },
        },
        {
            "name": "route_target_import",
            "getval": re.compile(
                r'''
                ^\s+route-target\simport\s(?P<rt>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "route-target import {{ rt }}",
            "result": {
                _VNI: {
                    "route_target_import": [_RT],
                },
            },
        },
        {
            "name": "route_target_export",
            "getval": re.compile(
                r'''
                ^\s+route-target\sexport\s(?P<rt>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "route-target export {{ rt }}",
            "result": {
                _VNI: {
                    "route_target_export": [_RT],
                },
            },
        },
        {
            # some releases may display the combined form; it is stored
            # as the equivalent import + export pair
            "name": "route_target_both",
            "getval": re.compile(
                r'''
                ^\s+route-target\sboth\s(?P<rt>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "route-target both {{ rt }}",
            "result": {
                _VNI: {
                    "route_target_import": [_RT],
                    "route_target_export": [_RT],
                },
            },
        },
    ]
    # fmt: on
