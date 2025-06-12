# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The L2_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class L2_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(L2_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^interface\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": 'interface {{ name }}',
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                },
            },
            "shared": True,
        },
        {
            "name": "ip_forward",
            "getval": re.compile(
                r"""
                \s+ip\s(?P<ip_forward>forward)
                $""", re.VERBOSE,
            ),
            "setval": "ip forward",
            "result": {
                '{{ name }}': {
                    'ip_forward': "{{ True if ip_forward is defined }}",
                },
            },
        },
        {  # only applicable for switches
            "name": "mode",
            "getval": re.compile(
                r"""
                (?P<negate>\s+no)?
                (?P<switchport>\s+switchport)
                $""", re.VERBOSE,
            ),
            "setval": "switchport",
            "result": {
                '{{ name }}': {
                    'mode': "{{ 'layer2' if switchport is defined and negate is not defined else 'layer3' }}",
                },
            },
        },
    ]
    # fmt: on
