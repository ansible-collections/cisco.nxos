# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_ptp_global module
"""


class Ptp_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_ptp_global module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "source": {
                    "type": "dict",
                    "options": {
                        "ipv4": {
                            "type": "dict",
                            "options": {
                                "address": {"type": "str"},
                                "vrf": {"type": "str"},
                            },
                        },
                        "ipv6": {
                            "type": "dict",
                            "options": {
                                "address": {"type": "str"},
                                "vrf": {"type": "str"},
                            },
                        },
                    },
                },
                "domain": {"type": "int"},
                "priority1": {"type": "int"},
                "priority2": {"type": "int"},
                "management": {"type": "bool"},
                "unicast_negotiation": {"type": "bool"},
                "mean_path_delay": {"type": "int"},
                "correction_range": {
                    "type": "dict",
                    "options": {
                        "value": {"type": "int"},
                        "logging": {"type": "bool"},
                    },
                },
                "ipv6_multicast_scope": {
                    "type": "dict",
                    "options": {
                        "rx": {"type": "str"},
                        "tx": {"type": "str"},
                    },
                },
                "delay_tolerance": {
                    "type": "dict",
                    "options": {
                        "mean_path": {"type": "str"},
                        "reverse_path": {"type": "str"},
                    },
                },
                "notification": {
                    "type": "dict",
                    "options": {
                        "gm_change": {"type": "bool"},
                        "parent_change": {"type": "bool"},
                        "port_state_change": {"type": "bool"},
                        "high_correction": {
                            "type": "dict",
                            "options": {
                                "enabled": {"type": "bool"},
                                "interval": {"type": "str"},
                            },
                        },
                    },
                },
                "clock_periodic_update": {
                    "type": "dict",
                    "options": {
                        "enabled": {"type": "bool"},
                        "interval": {"type": "int"},
                    },
                },
                "time_distribution_hold": {
                    "type": "dict",
                    "options": {
                        "enabled": {"type": "bool"},
                        "correction_threshold": {"type": "int"},
                        "delay_threshold": {"type": "int"},
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
