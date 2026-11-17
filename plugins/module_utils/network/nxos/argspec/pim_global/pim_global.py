# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The arg spec for the nxos_pim_global module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class Pim_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_pim_global module."""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "dict",
            "options": {
                "bfd": {"type": "bool"},
                "log_neighbor_changes": {"type": "bool"},
                "flush_routes": {"type": "bool"},
                "register_rate_limit": {"type": "int"},
                "ssm_range": {"type": "list", "elements": "str"},
                "rp_addresses": {
                    "type": "list",
                    "elements": "dict",
                    "mutually_exclusive": [["group_list", "prefix_list", "route_map"]],
                    "options": {
                        "rp_address": {"type": "str", "required": True},
                        "group_list": {"type": "str"},
                        "prefix_list": {"type": "str"},
                        "route_map": {"type": "str"},
                        "bidir": {"type": "bool"},
                    },
                },
                "anycast_rps": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "anycast_rp": {"type": "str", "required": True},
                        "members": {"type": "list", "elements": "str"},
                    },
                },
            },
        },
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
        },
    }
