# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Fc_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

allowed_speed_values = [
    "auto",
    "1000",
    "2000",
    "4000",
    "8000",
    "10000",
    "16000",
    "32000",
    "64000",
    "auto max 2000",
    "auto max 4000",
    "auto max 8000",
    "auto max 16000",
    "auto max 32000",
    "auto max 64000",
]
allowed_values_pattern = "|".join(re.escape(val) for val in allowed_speed_values)


class Fc_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Fc_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "interface",
            "getval": re.compile(
                r"""
              ^interface\s
              (?P<name>\S+)$""", re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                },
            },
            "shared": True,
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+switchport\s+description\s+(?P<description>.*)
                $""", re.VERBOSE,
            ),
            "setval": "switchport description {{ description }}",
            "result": {
                "{{ name }}": {
                    "description": "{{ description }}",
                },
            },
        },
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
                "{{ name }}": {
                    "enabled": "{{ False if shutdown is defined and negate is not defined else True }}",
                },
            },
        },
        {
            "name": "speed",
            "getval": re.compile(
                rf"""\s+switchport\s+speed\s+(?P<speed>{allowed_values_pattern})$""", re.VERBOSE,),
            "setval": "switchport speed {{ speed|string }}",
            "result": {
                "{{ name }}": {
                    "speed": "{{ speed|string }}",
                },
            },
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                \s+switchport\s+mode\s+(?P<mode>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport mode {{ mode|string }}",
            "result": {
                "{{ name }}": {
                    "mode": "{{ mode }}",
                },
            },
        },
        {
            "name": "trunk_mode",
            "getval": re.compile(
                r"""
                (?P<negate>\s+no)?
                \s+switchport\s+trunk\s+mode\s+(?P<trunk_mode>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "switchport trunk mode {{ trunk_mode|string }}",
            "result": {
                "{{ name }}": {
                    "trunk_mode": "{{ trunk_mode }}",
                },
            },
        },

        {
            "name": "analytics_scsi",
            "getval": re.compile(
                r"""
                (?P<negate>\s+no)?
                \s+analytics\s+type\s+(?P<analytics_scsi>fc-scsi)
                $""", re.VERBOSE,
            ),
            "setval": "analytics type {{ analytics_scsi|string }}",
            "result": {
                "{{ name }}": {
                    "analytics_scsi": "{{ analytics_scsi }}",  # list
                },
            },
        },
        {
            "name": "analytics_nvme",
            "getval": re.compile(
                r"""
                \s+analytics\s+type\s+(?P<analytics_nvme>fc-nvme)
                $""", re.VERBOSE,
            ),
            "setval": "analytics type {{ analytics_nvme|string }}",
            "result": {
                "{{ name }}": {
                    "analytics_nvme": "{{ analytics_nvme }}",  # list
                },
            },
        },


        # {
        #     "name": "analytics_scsi",
        #     "getval": re.compile(
        #         r"""
        #         (?P<negate>\sno)?
        #         \s+analytics\s+type\s+(?P<analytics>fc-scsi)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "analytics type fc-scsi",
        #     "result": {
        #         "{{ name }}": {
        #             "analytics_scsi": "{{ 'scsi' if analytics_scsi is defined and negate is not defined }}",
        #         },
        #     },
        # },
        # {
        #     "name": "analytics_nvme",
        #     "getval": re.compile(
        #         r"""
        #         (?P<negate>\sno)?
        #         \s+analytics\s+type\s+(?P<analytics>fc-nvme)
        #         $""", re.VERBOSE,
        #     ),
        #     "setval": "analytics type fc-nvme",
        #     "result": {
        #         "{{ name }}": {
        #             "analytics_nvme": "{{ True if fc-nvme is defined and negate is not defined else False }}",
        #         },
        #     },
        # },

        {
            "name": "analytics",
            "getval": re.compile(
                r"""
                \s+analytics\s+type\s+(?P<analytics>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "analytics type {{ analytics|string }}",
            "result": {
                "{{ name }}": {
                    "analytics": "{{ analytics }}",
                },
            },
        },
    ]
    # fmt: on
