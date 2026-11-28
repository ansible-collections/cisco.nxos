# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Netflow_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_NAME = "{{ name }}"


class Netflow_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Netflow_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r'''
                ^interface\s(?P<name>\S+)\s*$
                ''',
                re.VERBOSE,
            ),
            "setval": "interface {{ name }}",
            "result": {_NAME: {"name": _NAME}},
            "shared": True,
        },
        {
            # the lines are displayed with trailing spaces, the key keeps the entries apart
            "name": "flow_monitors",
            "getval": re.compile(
                r'''
                ^\s+(?P<cli>ip|ipv6|layer2-switched)\sflow\smonitor
                \s(?P<monitor>\S+)
                \s(?P<direction>input|output)
                \s*$
                ''',
                re.VERBOSE,
            ),
            "setval": "{{ cli }} flow monitor {{ monitor }} {{ direction }}",
            "result": {
                _NAME: {
                    "flow_monitors": {
                        "{{ cli }}_{{ direction }}": {
                            "monitor": "{{ monitor }}",
                            "direction": "{{ direction }}",
                            "protocol": "{{ {'ip': 'ipv4', 'ipv6': 'ipv6', 'layer2-switched': 'layer2_switched'}[cli] }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
