# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vpc_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Vpc_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Vpc_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "interface",
            "getval": re.compile(
                r'''
                ^interface\s(?P<name>\S+)$
                ''',
                re.VERBOSE,
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
            "name": "vpc",
            "getval": re.compile(
                r'''
                ^\s+vpc\s(?P<vpc>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "vpc {{ vpc }}",
            "result": {
                "{{ name }}": {
                    "vpc": "{{ vpc }}",
                },
            },
        },
        {
            "name": "peer_link",
            "getval": re.compile(
                r'''
                ^\s+vpc\speer-link$
                ''',
                re.VERBOSE,
            ),
            "setval": "vpc peer-link",
            "result": {
                "{{ name }}": {
                    "peer_link": True,
                },
            },
        },
        {
            "name": "orphan_port_suspend",
            "getval": re.compile(
                r'''
                ^\s+vpc\sorphan-port\ssuspend$
                ''',
                re.VERBOSE,
            ),
            "setval": "vpc orphan-port suspend",
            "result": {
                "{{ name }}": {
                    "orphan_port_suspend": True,
                },
            },
        },
    ]
    # fmt: on
