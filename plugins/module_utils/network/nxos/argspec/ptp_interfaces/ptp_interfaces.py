# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_ptp_interfaces module
"""

_PROFILE = ["aes67", "smpte_2059_2"]
_INTERVAL = {
    "type": "dict",
    "options": {
        "value": {"type": "int", "required": True},
        "profile": {"type": "str", "choices": _PROFILE},
    },
}


class Ptp_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_ptp_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "enabled": {"type": "bool"},
                "role": {"type": "str", "choices": ["dynamic", "master", "slave"]},
                "transmission": {"type": "str", "choices": ["unicast", "multicast"]},
                "transport": {"type": "str", "choices": ["ipv4", "ipv6"]},
                "vlan": {"type": "int"},
                "announce_interval": _INTERVAL,
                "announce_timeout": _INTERVAL,
                "sync_interval": _INTERVAL,
                "delay_request_interval": _INTERVAL,
                "asymmetric_delay": {
                    "type": "dict",
                    "options": {
                        "forward_path": {"type": "int"},
                        "reverse_path": {"type": "int"},
                    },
                },
                "master": {"type": "list", "elements": "str"},
                "slave": {"type": "list", "elements": "str"},
                "peer": {"type": "str"},
                "ucast_source": {
                    "type": "dict",
                    "options": {
                        "ipv4": {"type": "str"},
                        "ipv6": {"type": "str"},
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
