# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Vpc parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class VpcTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(VpcTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "domain",
            "getval": re.compile(
                r'''
                ^vpc\sdomain\s(?P<domain>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "vpc domain {{ domain }}",
            "result": {
                "{{ domain }}": {
                    "domain": "{{ domain }}",
                },
            },
            "shared": True,
        },
        {
            "name": "role_priority",
            "getval": re.compile(
                r'''
                ^\s+role\spriority\s(?P<role_priority>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "role priority {{ role_priority }}",
            "result": {
                "{{ domain }}": {
                    "role_priority": "{{ role_priority }}",
                },
            },
        },
        {
            "name": "system_priority",
            "getval": re.compile(
                r'''
                ^\s+system-priority\s(?P<system_priority>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "system-priority {{ system_priority }}",
            "result": {
                "{{ domain }}": {
                    "system_priority": "{{ system_priority }}",
                },
            },
        },
        {
            "name": "delay_restore",
            "getval": re.compile(
                r'''
                ^\s+delay\srestore\s(?P<delay_restore>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "delay restore {{ delay_restore }}",
            "result": {
                "{{ domain }}": {
                    "delay_restore": "{{ delay_restore }}",
                },
            },
        },
        {
            "name": "delay_restore_interface_vlan",
            "getval": re.compile(
                r'''
                ^\s+delay\srestore\sinterface-vlan\s(?P<delay_restore_interface_vlan>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "delay restore interface-vlan {{ delay_restore_interface_vlan }}",
            "result": {
                "{{ domain }}": {
                    "delay_restore_interface_vlan": "{{ delay_restore_interface_vlan }}",
                },
            },
        },
        {
            "name": "delay_restore_orphan_port",
            "getval": re.compile(
                r'''
                ^\s+delay\srestore\sorphan-port\s(?P<delay_restore_orphan_port>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "delay restore orphan-port {{ delay_restore_orphan_port }}",
            "result": {
                "{{ domain }}": {
                    "delay_restore_orphan_port": "{{ delay_restore_orphan_port }}",
                },
            },
        },
        {
            "name": "auto_recovery_reload_delay",
            "getval": re.compile(
                r'''
                ^\s+auto-recovery\sreload-delay\s(?P<auto_recovery_reload_delay>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "auto-recovery reload-delay {{ auto_recovery_reload_delay }}",
            "result": {
                "{{ domain }}": {
                    "auto_recovery_reload_delay": "{{ auto_recovery_reload_delay }}",
                },
            },
        },
        {
            "name": "auto_recovery",
            "getval": re.compile(
                r'''
                ^\s+(?P<negate>no\s+)?auto-recovery$
                ''',
                re.VERBOSE,
            ),
            "setval": "auto-recovery",
            "result": {
                "{{ domain }}": {
                    "auto_recovery": "{{ False if negate is defined and negate else True }}",
                },
            },
        },
        {
            "name": "peer_gw",
            "getval": re.compile(
                r'''
                ^\s+(?P<negate>no\s+)?peer-gateway$
                ''',
                re.VERBOSE,
            ),
            "setval": "peer-gateway",
            "result": {
                "{{ domain }}": {
                    "peer_gw": "{{ False if negate is defined and negate else True }}",
                },
            },
        },
        {
            "name": "peer_sw",
            "getval": re.compile(
                r'''
                ^\s+(?P<negate>no\s+)?peer-switch$
                ''',
                re.VERBOSE,
            ),
            "setval": "peer-switch",
            "result": {
                "{{ domain }}": {
                    "peer_sw": "{{ False if negate is defined and negate else True }}",
                },
            },
        },
        {
            "name": "peer_keepalive",
            "getval": re.compile(
                r'''
                ^\s+peer-keepalive\sdestination\s(?P<pkl_dest>[\d.]+)
                (?:\ssource\s(?P<pkl_src>[\d.]+))?
                (?:\svrf\s(?P<pkl_vrf>\S+))?$
                ''',
                re.VERBOSE,
            ),
            "setval": "peer-keepalive destination {{ pkl_dest }}"
                      "{% if pkl_src is defined and pkl_src %} source {{ pkl_src }}{% endif %}"
                      "{% if pkl_vrf is defined and pkl_vrf %} vrf {{ pkl_vrf }}{% endif %}",
            "result": {
                "{{ domain }}": {
                    "pkl_dest": "{{ pkl_dest }}",
                    "pkl_src": "{{ pkl_src }}",
                    "pkl_vrf": "{{ pkl_vrf }}",
                },
            },
        },
    ]
    # fmt: on
