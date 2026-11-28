# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_netflow_interfaces module
"""


class Netflow_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_netflow_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "flow_monitors": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "monitor": {"type": "str", "required": True},
                        "direction": {
                            "type": "str",
                            "required": True,
                            "choices": ["input", "output"],
                        },
                        "protocol": {
                            "type": "str",
                            "default": "ipv4",
                            "choices": ["ipv4", "ipv6", "layer2_switched"],
                        },
                    },
                },
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
