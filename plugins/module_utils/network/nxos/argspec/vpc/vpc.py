# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_vpc module
"""


class VpcArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_vpc module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "domain": {"type": "str", "required": True},
                "role_priority": {"type": "str"},
                "system_priority": {"type": "str"},
                "pkl_src": {"type": "str"},
                "pkl_dest": {"type": "str"},
                "pkl_vrf": {"type": "str"},
                "peer_gw": {"type": "bool"},
                "peer_sw": {"type": "bool"},
                "auto_recovery": {"type": "bool"},
                "auto_recovery_reload_delay": {"type": "str"},
                "delay_restore": {"type": "str"},
                "delay_restore_interface_vlan": {"type": "str"},
                "delay_restore_orphan_port": {"type": "str"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
