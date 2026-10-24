# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_igmp_snooping module
"""


class Igmp_snoopingArgs(object):  # pylint: disable=R0903
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
                "vlans": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "vlan_id": {"type": "int", "required": True},
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
