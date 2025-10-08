# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The arg spec for the nxos_nve_interface module.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class Nve_interfaceArgs(object):
    """
    The arg spec for the nxos_nve_interface module.
    """

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "dict",
            "options": {
                "enabled": {"type": "bool"},
                "description": {"type": "str"},
                "host_reachability_bgp": {"type": "bool"},
                "advertise_virtual_rmac": {"type": "bool"},
                "source_interface_name": {"type": "str"},
                "source_interface_hold_time": {"type": "int"},
                "global_suppress_arp": {"type": "bool"},
                "global_ingress_replication_bgp": {"type": "bool"},
                "global_multicast_group": {
                    "type": "dict",
                    "options": {
                        "address": {"type": "str"},
                        "mode": {
                            "type": "str",
                            "choices": [
                                "L2",
                                "L3",
                            ],
                            "required": True,
                        },
                    },
                },
                "multisite_interface": {"type": "str"},
                "vnis": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "vni_id": {
                            "type": "int",
                            "required": True,
                        },
                        "associate_vrf": {"type": "bool"},
                        "suppress_arp": {"type": "bool"},
                        "suppress_arp_disable": {"type": "bool"},
                        "multisite_ingress_replication": {"type": "bool"},
                        "ingress_replication_bgp": {"type": "bool"},
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
