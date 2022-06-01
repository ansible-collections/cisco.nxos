# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# cli_rm_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the module docstring and re-run
# cli_rm_builder.
#
#############################################

"""
The arg spec for the nxos_snmp_server module
"""


class Snmp_serverArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_snmp_server module"""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "dict",
            "options": {
                "aaa_user": {
                    "type": "dict",
                    "options": {"cache_timeout": {"type": "int"}},
                },
                "communities": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "name": {"type": "str", "aliases": ["community"]},
                        "group": {"type": "str"},
                        "ro": {"type": "bool"},
                        "rw": {"type": "bool"},
                        "use_ipv4acl": {"type": "str"},
                        "use_ipv6acl": {"type": "str"},
                    },
                },
                "contact": {"type": "str"},
                "context": {
                    "type": "dict",
                    "options": {
                        "name": {"type": "str"},
                        "instance": {"type": "str"},
                        "topology": {"type": "str"},
                        "vrf": {"type": "str"},
                    },
                },
                "counter": {
                    "type": "dict",
                    "options": {
                        "cache": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "timeout": {"type": "int"},
                            },
                        }
                    },
                },
                "drop": {
                    "type": "dict",
                    "options": {
                        "unknown_engine_id": {"type": "bool"},
                        "unknown_user": {"type": "bool"},
                    },
                },
                "traps": {
                    "type": "dict",
                    "options": {
                        "aaa": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "server_state_change": {"type": "bool"},
                            },
                        },
                        "bgp": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                            },
                        },
                        "bridge": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "newroot": {"type": "bool"},
                                "topologychange": {"type": "bool"},
                            },
                        },
                        "callhome": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "event_notify": {"type": "bool"},
                                "smtp_send_fail": {"type": "bool"},
                            },
                        },
                        "cfs": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "merge_failure": {"type": "bool"},
                                "state_change_notif": {"type": "bool"},
                            },
                        },
                        "config": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "ccmCLIRunningConfigChanged": {"type": "bool"},
                            },
                        },
                        "entity": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "cefcMIBEnableStatusNotification": {
                                    "type": "bool"
                                },
                                "entity_fan_status_change": {"type": "bool"},
                                "entity_mib_change": {"type": "bool"},
                                "entity_module_inserted": {"type": "bool"},
                                "entity_module_removed": {"type": "bool"},
                                "entity_module_status_change": {
                                    "type": "bool"
                                },
                                "entity_power_out_change": {"type": "bool"},
                                "entity_power_status_change": {"type": "bool"},
                                "entity_sensor": {"type": "bool"},
                                "entity_unrecognised_module": {"type": "bool"},
                            },
                        },
                        "feature_control": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "featureOpStatusChange": {"type": "bool"},
                                "ciscoFeatOpStatusChange": {"type": "bool"},
                            },
                        },
                        "generic": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "coldStart": {"type": "bool"},
                                "warmStart": {"type": "bool"},
                            },
                        },
                        "license": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "notify_license_expiry": {"type": "bool"},
                                "notify_license_expiry_warning": {
                                    "type": "bool"
                                },
                                "notify_licensefile_missing": {"type": "bool"},
                                "notify_no_license_for_feature": {
                                    "type": "bool"
                                },
                            },
                        },
                        "link": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "cErrDisableInterfaceEventRev1": {
                                    "type": "bool"
                                },
                                "cieLinkDown": {"type": "bool"},
                                "cieLinkUp": {"type": "bool"},
                                "cisco_xcvr_mon_status_chg": {"type": "bool"},
                                "cmn_mac_move_notification": {"type": "bool"},
                                "delayed_link_state_change": {"type": "bool"},
                                "extended_linkDown": {"type": "bool"},
                                "extended_linkUp": {"type": "bool"},
                                "linkDown": {"type": "bool"},
                                "linkUp": {"type": "bool"},
                            },
                        },
                        "mmode": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "cseMaintModeChangeNotify": {"type": "bool"},
                                "cseNormalModeChangeNotify": {"type": "bool"},
                            },
                        },
                        "ospf": {
                            "type": "dict",
                            "options": {"enable": {"type": "bool"}},
                        },
                        "ospfv3": {
                            "type": "dict",
                            "options": {"enable": {"type": "bool"}},
                        },
                        "rf": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "redundancy_framework": {"type": "bool"},
                            },
                        },
                        "rmon": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "fallingAlarm": {"type": "bool"},
                                "hcFallingAlarm": {"type": "bool"},
                                "hcRisingAlarm": {"type": "bool"},
                                "risingAlarm": {"type": "bool"},
                            },
                        },
                        "snmp": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "authentication": {"type": "bool"},
                            },
                        },
                        "storm_control": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "cpscEventRev1": {"type": "bool"},
                                "trap_rate": {"type": "bool"},
                            },
                        },
                        "stpx": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "inconsistency": {"type": "bool"},
                                "loop_inconsistency": {"type": "bool"},
                                "root_inconsistency": {"type": "bool"},
                            },
                        },
                        "syslog": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "message_generated": {"type": "bool"},
                            },
                        },
                        "sysmgr": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "cseFailSwCoreNotifyExtended": {
                                    "type": "bool"
                                },
                            },
                        },
                        "system": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "clock_change_notification": {"type": "bool"},
                            },
                        },
                        "upgrade": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "upgradeJobStatusNotify": {"type": "bool"},
                                "upgradeOpNotifyOnCompletion": {
                                    "type": "bool"
                                },
                            },
                        },
                        "vtp": {
                            "type": "dict",
                            "options": {
                                "enable": {"type": "bool"},
                                "notifs": {"type": "bool"},
                                "vlancreate": {"type": "bool"},
                                "vlandelete": {"type": "bool"},
                            },
                        },
                    },
                },
                "engine_id": {
                    "type": "dict",
                    "options": {"local": {"type": "str"}},
                },
                "global_enforce_priv": {"type": "bool"},
                "hosts": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "host": {"type": "str"},
                        "community": {"type": "str"},
                        "filter_vrf": {"type": "str"},
                        "informs": {"type": "bool"},
                        "source_interface": {"type": "str"},
                        "traps": {"type": "bool"},
                        "use_vrf": {"type": "str"},
                        "version": {
                            "type": "str",
                            "choices": ["1", "2c", "3"],
                        },
                        "auth": {"type": "str"},
                        "priv": {"type": "str"},
                        "udp_port": {"type": "int"},
                    },
                },
                "location": {"type": "str"},
                "mib": {
                    "type": "dict",
                    "options": {
                        "community_map": {
                            "type": "dict",
                            "options": {
                                "community": {"type": "str"},
                                "context": {"type": "str"},
                            },
                        }
                    },
                },
                "packetsize": {"type": "int"},
                "protocol": {
                    "type": "dict",
                    "options": {"enable": {"type": "bool"}},
                },
                "source_interface": {
                    "type": "dict",
                    "options": {
                        "informs": {"type": "str"},
                        "traps": {"type": "str"},
                    },
                },
                "system_shutdown": {"type": "bool"},
                "tcp_session": {
                    "type": "dict",
                    "options": {
                        "enable": {"type": "bool"},
                        "auth": {"type": "bool"},
                    },
                },
                "users": {
                    "type": "dict",
                    "options": {
                        "auth": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "user": {"type": "str"},
                                "group": {"type": "str"},
                                "authentication": {
                                    "type": "dict",
                                    "options": {
                                        "algorithm": {
                                            "type": "str",
                                            "choices": [
                                                "md5",
                                                "sha",
                                                "sha-256",
                                            ],
                                        },
                                        "password": {
                                            "type": "str",
                                            "no_log": False,
                                        },
                                        "engine_id": {"type": "str"},
                                        "localized_key": {"type": "bool"},
                                        "localizedv2_key": {"type": "bool"},
                                        "priv": {
                                            "type": "dict",
                                            "options": {
                                                "privacy_password": {
                                                    "type": "str",
                                                    "no_log": False,
                                                },
                                                "aes_128": {"type": "bool"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "use_acls": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "user": {"type": "str"},
                                "ipv4": {"type": "str"},
                                "ipv6": {"type": "str"},
                            },
                        },
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
                "parsed",
                "gathered",
                "rendered",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
