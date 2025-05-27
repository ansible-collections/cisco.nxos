# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)

class InterfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(InterfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^interface\s(?P<name>\S+)
                $""", re.VERBOSE),
            "setval": 'interface {{ name }}',
            "result": {
                '{{ name }}': {
                    'name': '{{ name }}',
                    'enabled': True,
                },
            },
            "shared": True
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s(?P<description>.+$)
                $""", re.VERBOSE),
            "setval": "description {{ description }}",
            "result": {
                '{{ name }}': {
                    'description': "'{{ description }}'",
                },
            },
        },
        {
            "name": "speed",
            "getval": re.compile(
                r"""
                \s+speed\s(?P<speed>\d+)
                $""", re.VERBOSE),
            "setval": "speed {{ speed|string }}",
            "result": {
                '{{ name }}': {
                    'speed': "{{ speed }}",
                },
            },
        },
    ]
    # fmt: on
