# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.content_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the documentation in the module file and re-run
# ansible.content_builder commenting out
# the path to external 'docstring' in build.yaml.
#
##############################################

"""
The arg spec for the nxos_vrf_global module
"""


class Vrf_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_vrf_global module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "vrfs": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"required": True, "type": "str"},
                        "description": {"type": "str"},
                        "ip": {
                            "type": "dict",
                            "options": {
                                "auto_discard": {"type": "bool"},
                                "domain_list": {"type": "list", "elements": "str"},
                                "domain_name": {"type": "str"},
                                "icmp_err": {
                                    "type": "dict",
                                    "options": {
                                        "source_interface": {
                                            "type": "dict",
                                            "options": {
                                                "interface": {
                                                    "type": "str",
                                                    "choices": [
                                                        "loopback",
                                                        "ethernet",
                                                        "port-channel",
                                                    ],
                                                },
                                                "interface_value": {"type": "str"},
                                            },
                                        }
                                    },
                                },
                                "igmp": {
                                    "type": "dict",
                                    "options": {
                                        "ssm_translate": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "group": {"type": "str"},
                                                "source": {"type": "str"},
                                            },
                                        }
                                    },
                                },
                                "mroutes": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "group": {"type": "str"},
                                        "source": {"type": "str"},
                                        "preference": {"type": "int"},
                                        "vrf": {"type": "str"},
                                    },
                                },
                                "multicast": {
                                    "type": "dict",
                                    "options": {
                                        "group_range_prefix_list": {"type": "str"},
                                        "multipath": {
                                            "type": "dict",
                                            "options": {
                                                "resilient": {"type": "bool"},
                                                "splitting_type": {
                                                    "type": "dict",
                                                    "mutually_exclusive": [
                                                        [
                                                            "legacy",
                                                            "nbm",
                                                            "none",
                                                            "sg_hash",
                                                            "sg_hash_next_hop",
                                                        ]
                                                    ],
                                                    "options": {
                                                        "none": {"type": "bool"},
                                                        "legacy": {"type": "bool"},
                                                        "nbm": {"type": "bool"},
                                                        "sg_hash": {
                                                            "type": "bool"
                                                        },
                                                        "sg_hash_next_hop": {
                                                            "type": "bool"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "rpf": {
                                            "type": "list",
                                            "elements": "dict",
                                            "options": {
                                                "vrf_name": {"type": "str"},
                                                "group_list_range": {
                                                    "type": "str"
                                                },
                                            },
                                        },
                                    },
                                },
                                "name_server": {
                                    "type": "dict",
                                    "options": {
                                        "address_list": {
                                            "type": "list",
                                            "elements": "str",
                                        },
                                        "use_vrf": {
                                            "type": "dict",
                                            "options": {
                                                "vrf": {"type": "str"},
                                                "source_address": {"type": "str"},
                                            },
                                        },
                                    },
                                },
                                "route": {
                                    "type": "list",
                                    "elements": "dict",
                                    "mutually_exclusive": [
                                        ["tags", "vrf", "track"]
                                    ],
                                    "options": {
                                        "source": {"type": "str"},
                                        "destination": {"type": "str"},
                                        "tags": {
                                            "type": "dict",
                                            "options": {
                                                "tag_value": {"type": "int"},
                                                "route_pref": {"type": "int"},
                                            },
                                        },
                                        "vrf": {"type": "str"},
                                        "track": {"type": "str"},
                                    },
                                },
                            },
                        },
                        "vni": {
                            "type": "dict",
                            "options": {
                                "vni_number": {"type": "int"},
                                "layer_3": {"type": "bool"},
                            },
                        },
                        "multicast": {
                            "type": "dict",
                            "options": {
                                "service_reflect": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "service_interface": {
                                            "type": "dict",
                                            "options": {
                                                "interface": {"type": "str"},
                                                "interface_value": {"type": "str"},
                                            },
                                        },
                                        "map_to": {
                                            "type": "dict",
                                            "options": {
                                                "interface": {"type": "str"},
                                                "interface_value": {"type": "str"},
                                            },
                                        },
                                    },
                                }
                            },
                        },
                        "ipv6": {
                            "type": "dict",
                            "options": {
                                "mld_ssm_translate": {
                                    "type": "list",
                                    "elements": "dict",
                                    "options": {
                                        "icmp": {"type": "bool"},
                                        "group": {"type": "str"},
                                        "source": {"type": "str"},
                                    },
                                },
                                "multicast": {
                                    "type": "dict",
                                    "options": {
                                        "group_range_prefix_list": {"type": "str"},
                                        "multipath": {
                                            "type": "dict",
                                            "options": {
                                                "resilient": {"type": "bool"},
                                                "splitting_type": {
                                                    "type": "dict",
                                                    "mutually_exclusive": [
                                                        [
                                                            "none",
                                                            "sg_hash",
                                                            "sg_hash_next_hop",
                                                        ]
                                                    ],
                                                    "options": {
                                                        "none": {"type": "bool"},
                                                        "sg_hash": {
                                                            "type": "bool"
                                                        },
                                                        "sg_hash_next_hop": {
                                                            "type": "bool"
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "parsed",
                "gathered",
                "deleted",
                "merged",
                "replaced",
                "rendered",
                "overridden",
                "purged",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
