# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_netflow_global module
"""

_BOOL = {"type": "bool"}


class Netflow_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_netflow_global module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "timeout": {"type": "int"},
                "exporters": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "required": True},
                        "description": {"type": "str"},
                        "destination": {
                            "type": "dict",
                            "options": {
                                "address": {"type": "str", "required": True},
                                "vrf": {"type": "str"},
                            },
                        },
                        "source": {"type": "str"},
                        "transport_udp": {"type": "int"},
                        "dscp": {"type": "int"},
                        "template_data_timeout": {"type": "int"},
                        "option_exporter_stats_timeout": {"type": "int"},
                        "option_interface_table_timeout": {"type": "int"},
                    },
                },
                "records": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "required": True},
                        "description": {"type": "str"},
                        "match": {
                            "type": "dict",
                            "options": {
                                "datalink": {
                                    "type": "dict",
                                    "options": {
                                        "mac_source_address": _BOOL,
                                        "mac_destination_address": _BOOL,
                                        "vlan": _BOOL,
                                        "ethertype": _BOOL,
                                    },
                                },
                                "ip": {
                                    "type": "dict",
                                    "options": {"protocol": _BOOL, "tos": _BOOL},
                                },
                                "ipv4": {
                                    "type": "dict",
                                    "options": {
                                        "source_address": _BOOL,
                                        "destination_address": _BOOL,
                                    },
                                },
                                "ipv6": {
                                    "type": "dict",
                                    "options": {
                                        "source_address": _BOOL,
                                        "destination_address": _BOOL,
                                        "flow_label": _BOOL,
                                        "options": _BOOL,
                                    },
                                },
                                "transport": {
                                    "type": "dict",
                                    "options": {"source_port": _BOOL, "destination_port": _BOOL},
                                },
                            },
                        },
                        "collect": {
                            "type": "dict",
                            "options": {
                                "counter": {
                                    "type": "dict",
                                    "options": {"bytes": _BOOL, "packets": _BOOL},
                                },
                                "timestamp_sys_uptime": {
                                    "type": "dict",
                                    "options": {"first": _BOOL, "last": _BOOL},
                                },
                                "transport_tcp_flags": _BOOL,
                                "ip_version": _BOOL,
                            },
                        },
                    },
                },
                "monitors": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "required": True},
                        "description": {"type": "str"},
                        "record": {"type": "str"},
                        "exporters": {"type": "list", "elements": "str"},
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
