# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_igmp_snooping module
"""


class IgmpSnoopingArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_igmp_snooping module"""

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "snooping": {"type": "bool"},
                "group_timeout": {"type": "str"},
                "link_local_groups_suppression": {"type": "bool"},
                "report_suppression": {"type": "bool"},
                "v3_report_suppression": {"type": "bool"},
                "vxlan": {"type": "bool"},
                "disable_nve_static_router_port": {"type": "bool"},
                "max_gq_miss": {"type": "int"},
                "syslog_threshold": {"type": "int"},
                "holddown_timer": {"type": "int"},
                "proxy": {
                    "type": "dict",
                    "options": {
                        "general_queries": {"type": "bool"},
                        "mrt": {"type": "int"},
                    },
                },
                "vlans": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "vlan_id": {"type": "int", "required": True},
                        "snooping": {"type": "bool"},
                        "group_timeout": {"type": "str"},
                        "link_local_groups_suppression": {"type": "bool"},
                        "report_suppression": {"type": "bool"},
                        "v3_report_suppression": {"type": "bool"},
                        "explicit_tracking": {"type": "bool"},
                        "fast_leave": {"type": "bool"},
                        "proxy": {
                            "type": "dict",
                            "options": {
                                "general_queries": {"type": "bool"},
                                "mrt": {"type": "int"},
                            },
                        },
                        "proxy_leave_use_group_address": {"type": "bool"},
                        "querier": {"type": "str"},
                        "querier_timeout": {"type": "int"},
                        "query_interval": {"type": "int"},
                        "query_max_response_time": {"type": "int"},
                        "startup_query_count": {"type": "int"},
                        "startup_query_interval": {"type": "int"},
                        "robustness_variable": {"type": "int"},
                        "last_member_query_interval": {"type": "int"},
                        "version": {"type": "int"},
                        "mrouter_interfaces": {"type": "list", "elements": "str"},
                        "report_flood": {
                            "type": "dict",
                            "options": {
                                "all": {"type": "bool"},
                                "interfaces": {"type": "list", "elements": "str"},
                            },
                        },
                        "report_policy": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "policy_type": {
                                    "type": "str",
                                    "required": True,
                                    "choices": ["route_map", "prefix_list"],
                                },
                                "name": {"type": "str", "required": True},
                                "interface": {"type": "str", "required": True},
                            },
                        },
                        "access_group": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "policy_type": {
                                    "type": "str",
                                    "required": True,
                                    "choices": ["route_map", "prefix_list"],
                                },
                                "name": {"type": "str", "required": True},
                                "interface": {"type": "str"},
                            },
                        },
                        "static_groups": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "group": {"type": "str", "required": True},
                                "source": {"type": "str"},
                                "interfaces": {
                                    "type": "list",
                                    "elements": "str",
                                    "required": True,
                                },
                            },
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
