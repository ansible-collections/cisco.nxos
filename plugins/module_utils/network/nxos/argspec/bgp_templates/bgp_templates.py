# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.plugin_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the nxos_bgp_templates module
"""


class Bgp_templatesArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_bgp_templates module"""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "dict",
            "options": {
                "peers": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str"},
                        "address_family": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "afi": {
                                    "type": "str",
                                    "choices": [
                                        "ipv4",
                                        "ipv6",
                                        "link-state",
                                        "l2vpn",
                                    ],
                                    "required": True,
                                },
                                "safi": {
                                    "type": "str",
                                    "choices": ["unicast", "multicast", "mvpn"],
                                },
                                "advertise_map": {
                                    "type": "dict",
                                    "options": {
                                        "route_map": {
                                            "type": "str",
                                            "required": True,
                                        },
                                        "exist_map": {"type": "str"},
                                        "non_exist_map": {"type": "str"},
                                    },
                                },
                                "advertisement_interval": {"type": "int"},
                                "allowas_in": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "max_occurences": {"type": "int"},
                                    },
                                },
                                "as_override": {"type": "bool"},
                                "capability": {
                                    "type": "dict",
                                    "options": {
                                        "additional_paths": {
                                            "type": "dict",
                                            "options": {
                                                "receive": {
                                                    "type": "str",
                                                    "choices": [
                                                        "enable",
                                                        "disable",
                                                    ],
                                                },
                                                "send": {
                                                    "type": "str",
                                                    "choices": [
                                                        "enable",
                                                        "disable",
                                                    ],
                                                },
                                            },
                                        },
                                    },
                                },
                                "default_originate": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                                "disable_peer_as_check": {"type": "bool"},
                                "filter_list": {
                                    "type": "dict",
                                    "options": {
                                        "inbound": {"type": "str"},
                                        "outbound": {"type": "str"},
                                    },
                                },
                                "inherit": {
                                    "type": "dict",
                                    "options": {"peer_session": {"type": "str"}},
                                },
                                "maximum_prefix": {
                                    "type": "dict",
                                    "options": {
                                        "max_prefix_limit": {"type": "int"},
                                        "generate_warning_threshold": {
                                            "type": "int",
                                        },
                                        "restart_interval": {"type": "int"},
                                        "warning_only": {"type": "bool"},
                                    },
                                },
                                "next_hop_self": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "all_routes": {"type": "bool"},
                                    },
                                },
                                "next_hop_third_party": {"type": "bool"},
                                "prefix_list": {
                                    "type": "dict",
                                    "options": {
                                        "inbound": {"type": "str"},
                                        "outbound": {"type": "str"},
                                    },
                                },
                                "route_map": {
                                    "type": "dict",
                                    "options": {
                                        "inbound": {"type": "str"},
                                        "outbound": {"type": "str"},
                                    },
                                },
                                "route_reflector_client": {"type": "bool"},
                                "send_community": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "extended": {"type": "bool"},
                                        "standard": {"type": "bool"},
                                        "both": {"type": "bool"},
                                    },
                                },
                                "soft_reconfiguration_inbound": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "always": {"type": "bool"},
                                    },
                                },
                                "soo": {"type": "str"},
                                "suppress_inactive": {"type": "bool"},
                                "unsuppress_map": {"type": "str"},
                                "weight": {"type": "int"},
                            },
                        },
                        "bfd": {
                            "type": "dict",
                            "options": {
                                "set": {"type": "bool"},
                                "singlehop": {"type": "bool"},
                                "multihop": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "interval": {
                                            "type": "dict",
                                            "options": {
                                                "tx_interval": {"type": "int"},
                                                "min_rx_interval": {"type": "int"},
                                                "multiplier": {"type": "int"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "bmp_activate_server": {"type": "int"},
                        "capability": {
                            "type": "dict",
                            "options": {"suppress_4_byte_as": {"type": "bool"}},
                        },
                        "description": {"type": "str"},
                        "disable_connected_check": {"type": "bool"},
                        "dont_capability_negotiate": {"type": "bool"},
                        "dscp": {"type": "str"},
                        "dynamic_capability": {"type": "bool"},
                        "ebgp_multihop": {"type": "int"},
                        "graceful_shutdown": {
                            "type": "dict",
                            "options": {
                                "activate": {
                                    "type": "dict",
                                    "options": {
                                        "set": {"type": "bool"},
                                        "route_map": {"type": "str"},
                                    },
                                },
                            },
                        },
                        "inherit": {
                            "type": "dict",
                            "options": {"peer_session": {"type": "str"}},
                        },
                        "local_as": {"type": "str"},
                        "log_neighbor_changes": {
                            "type": "dict",
                            "options": {
                                "set": {"type": "bool"},
                                "disable": {"type": "bool"},
                            },
                        },
                        "low_memory": {
                            "type": "dict",
                            "options": {"exempt": {"type": "bool"}},
                        },
                        "password": {
                            "type": "dict",
                            "options": {
                                "encryption": {"type": "int"},
                                "key": {"type": "str"},
                            },
                        },
                        "path_attribute": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "action": {
                                    "type": "str",
                                    "choices": ["discard", "treat-as-withdraw"],
                                },
                                "type": {"type": "int"},
                                "range": {
                                    "type": "dict",
                                    "options": {
                                        "start": {"type": "int"},
                                        "end": {"type": "int"},
                                    },
                                },
                            },
                        },
                        "remote_as": {"type": "str"},
                        "remove_private_as": {
                            "type": "dict",
                            "options": {
                                "set": {"type": "bool"},
                                "replace_as": {"type": "bool"},
                                "all": {"type": "bool"},
                            },
                        },
                        "shutdown": {"type": "bool"},
                        "timers": {
                            "type": "dict",
                            "options": {
                                "keepalive": {"type": "int"},
                                "holdtime": {"type": "int"},
                            },
                        },
                        "transport": {
                            "type": "dict",
                            "options": {
                                "connection_mode": {
                                    "type": "dict",
                                    "options": {"passive": {"type": "bool"}},
                                },
                            },
                        },
                        "ttl_security": {
                            "type": "dict",
                            "options": {"hops": {"type": "int"}},
                        },
                        "update_source": {"type": "str"},
                    },
                },
            },
        },
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "deleted",
                "purged",
                "parsed",
                "gathered",
                "rendered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
