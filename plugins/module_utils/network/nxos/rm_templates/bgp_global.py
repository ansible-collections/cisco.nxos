# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Bgp_global parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def _tmplt_confederation_peers(proc):
    pass

def _tmplt_graceful_shutdown_activate(proc):
    pass

class Bgp_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Bgp_globalTemplate, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "asn",
            "getval": re.compile(
                r"""
                ^router\sbgp\s(?P<asn>\S+)
                $""", re.VERBOSE
            ),
            "setval": "router bgp {{ asn }}",
            "result": {
                "asn": "{{ asn }}",
            },
            "shared": True
        },
        {
            "name": "bestpath.always_compare_med",
            "getval": re.compile(
                r"""
                \s+bestpath\s(?P<always_compare_med>always-compare-med)
                $""", re.VERBOSE
            ),
            "setval": "bestpath always-compare-med",
            "result": {
                "bestpath": {
                    "always_compare_med": "{{ not not always_compare_med }}",
                }
            }
        },
        {
            "name": "bestpath.as_path.ignore",
            "getval": re.compile(
                r"""
                \s+bestpath\sas-path\s(?P<ignore>ignore)
                $""", re.VERBOSE
            ),
            "setval": "bestpath as-path ignore",
            "result": {
                "bestpath": {
                    "as_path": {
                        "ignore": "{{ not not ignore }}",
                    }
                }
            }
        },
        {
            "name": "bestpath.as_path.multipath_relax",
            "getval": re.compile(
                r"""
                \s+bestpath\sas-path\s(?P<multipath_relax>multipath-relax)
                $""", re.VERBOSE
            ),
            "setval": " bestpath as-path multipath-relax",
            "result": {
                "bestpath": {
                    "as_path": {
                        "multipath_relax": "{{ not not multipath_relax }}",
                    }
                }
            }
        },
        {
            "name": "bestpath.compare_neighborid",
            "getval": re.compile(
                r"""
                \s+bestpath\s(?P<compare_neighborid>compare-neighborid)
                $""", re.VERBOSE
            ),
            "setval": "bestpath compare-neighborid",
            "result": {
                "bestpath": {
                    "compare_neighborid": "{{ not not compare_neighborid }}",
                }
            }
        },
        {
            "name": "bestpath.compare_routerid",
            "getval": re.compile(
                r"""
                \s+bestpath\s(?P<compare_routerid>compare-routerid)
                $""", re.VERBOSE
            ),
            "setval": "bestpath compare-routerid",
            "result": {
                "bestpath": {
                    "compare_routerid": "{{ not not compare_routerid }}",
                }
            }
        },
        {
            "name": "bestpath.cost_community_ignore",
            "getval": re.compile(
                r"""
                \s+bestpath\scost-community\s(?P<cost_community_ignore>ignore)
                $""", re.VERBOSE
            ),
            "setval": "bestpath cost-community ignore",
            "result": {
                "bestpath": {
                    "cost_community_ignore": "{{ not not cost_community_ignore }}",
                }
            }
        },
        {
            "name": "bestpath.igp_metric_ignore",
            "getval": re.compile(
                r"""
                \s+bestpath\sigp-metric\s(?P<igp_metric_ignore>ignore)
                $""", re.VERBOSE
            ),
            "setval": "bestpath igp-metric ignore",
            "result": {
                "bestpath": {
                    "igp_metric_ignore": "{{ not not igp_metric_ignore }}",
                }
            }
        },
        {
            "name": "bestpath.med.confed",
            "getval": re.compile(
                r"""
                \s+bestpath\smed\s(?P<confed>confed)
                $""", re.VERBOSE
            ),
            "setval": "bestpath med confed",
            "result": {
                "bestpath": {
                    "med": {
                        "confed": "{{ not not confed }}",
                    }
                }
            }
        },
        {
            "name": "bestpath.med.missing_as_worst",
            "getval": re.compile(
                r"""
                \s+bestpath\smed\s(?P<missing_as_worst>missing-as-worst)
                $""", re.VERBOSE
            ),
            "setval": "bestpath med missing-as-worst",
            "result": {
                "bestpath": {
                    "med": {
                        "missing_as_worst": "{{ not not missing_as_worst }}",
                    }
                }
            }
        },
        {
            "name": "bestpath.med.non_deterministic",
            "getval": re.compile(
                r"""
                \s+bestpath\smed\s(?P<non_deterministic>non-deterministic)
                $""", re.VERBOSE
            ),
            "setval": "bestpath med non-deterministic",
            "result": {
                "bestpath": {
                    "med": {
                        "non_deterministic": "{{ not not non_deterministic }}",
                    }
                }
            }
        },
        {
            "name": "cluster_id",
            "getval": re.compile(
                r"""
                \s+cluster-id\s(?P<cluster_id>\S+)
                $""", re.VERBOSE
            ),
            "setval": "cluster-id {{ cluster_id }}",
            "result": {
                "cluster_id": "{{ cluster_id }}",
            }
        },
        {
            "name": "confederation.identifier",
            "getval": re.compile(
                r"""
                \s+confederation\sidentifier\s(?P<identifier>\S+)
                $""", re.VERBOSE
            ),
            "setval": "confederation identifier {{ confederation.identifier }}",
            "result": {
                "confederation": {
                    "identifier": "{{ identifier }}",
                },
            },
        },
        {
            "name": "confederation.peers",
            "getval": re.compile(
                r"""
                \s+confederation\speers\s(?P<peers>.*)
                $""", re.VERBOSE
            ),
            "setval": _tmplt_confederation_peers,
            "result": {
                "confederation": {
                    "peers": "{{ peers }}",
                },
            }
        },
        {
            "name": "disable_policy_batching",
            "getval": re.compile(
                r"""
                \s+(?P<disable_policy_batching>disable-policy-batching)
                $""", re.VERBOSE
            ),
            "setval": "disable-policy-batching",
            "result": {
                "disable_policy_batching": {
                    "set": "{{ not not disable_policy_batching }}",
                },
            }
        },
        {
            "name": "disable_policy_batching",
            "getval": re.compile(
                r"""
                \s+(?P<disable_policy_batching>disable-policy-batching)
                $""", re.VERBOSE
            ),
            "setval": "disable-policy-batching",
            "result": {
                "disable_policy_batching": {
                    "set": "{{ not not disable_policy_batching }}",
                },
            }
        },
        {
            "name": "disable_policy_batching.ipv4.prefix_list",
            "getval": re.compile(
                r"""
                \s+disable-policy-batching\sipv4
                \sprefix-list\s(?P<ipv4_prefix_list>\S+)
                $""", re.VERBOSE
            ),
            "setval": "disable-policy-batching ipv4 prefix-list {{ disable_policy_batching.ipv4.prefix_list }}",
            "result": {
                "disable_policy_batching": {
                    "ipv4": {
                        "prefix_list": "{{ ipv4_prefix_list }}",
                    }
                },
            }
        },
        {
            "name": "disable_policy_batching.ipv6.prefix_list",
            "getval": re.compile(
                r"""
                \s+disable-policy-batching\sipv6
                \sprefix-list\s(?P<ipv6_prefix_list>\S+)
                $""", re.VERBOSE
            ),
            "setval": "disable-policy-batching ipv6 prefix-list {{ disable_policy_batching.ipv6.prefix_list }}",
            "result": {
                "disable_policy_batching": {
                    "ipv6": {
                        "prefix_list": "{{ ipv6_prefix_list }}",
                    }
                },
            }
        },
        {
            "name": "disable_policy_batching.nexthop",
            "getval": re.compile(
                r"""
                \s+disable-policy-batching\s(?P<nexthop>nexthop)
                $""", re.VERBOSE
            ),
            "setval": "disable-policy-batching nexthop",
            "result": {
                "disable_policy_batching": {
                    "nexthop": "{{ not not nexthop }}",
                },
            }
        },
        {
            "name": "dynamic_med_interval",
            "getval": re.compile(
                r"""
                \s+dynamic-med-interval\s(?P<dynamic_med_interval>\d+)
                $""", re.VERBOSE
            ),
            "setval": "dynamic-med-interval {{ dynamic_med_interval }}",
            "result": {
                "dynamic_med_interval": "{{ dynamic_med_interval }}",
            }
        },
        {
            "name": "enforce_first_as",
            "getval": re.compile(
                r"""
                \s+no\s(?P<enforce_first_as>enforce-first-as)
                $""", re.VERBOSE
            ),
            "setval": "enforce-first-as",
            "result": {
                "enforce_first_as": "{{ not enforce_first_as }}",
            }
        },
        {
            "name": "enhanced_error",
            "getval": re.compile(
                r"""
                \s+no\s(?P<enhanced_error>enhanced-error)
                $""", re.VERBOSE
            ),
            "setval": "enhanced-error",
            "result": {
                "enhanced_error": "{{ not enhanced_error }}",
            }
        },
        {
            "name": "fast_external_fallover",
            "getval": re.compile(
                r"""
                \s+no\s(?P<fast_external_fallover>fast-external-fallover)
                $""", re.VERBOSE
            ),
            "setval": "fast-external-fallover",
            "result": {
                "fast_external_fallover": "{{ not fast_external_fallover }}",
            }
        },
        {
            "name": "flush_routes",
            "getval": re.compile(
                r"""
                \s+(?P<flush_routes>flush-routes)
                $""", re.VERBOSE
            ),
            "setval": "flush-routes",
            "result": {
                "flush_routes": "{{ not not flush_routes }}",
            }
        },
        {
            "name": "graceful_restart",
            "getval": re.compile(
                r"""
                \s+no\s(?P<graceful_restart>graceful-restart)
                $""", re.VERBOSE
            ),
            "setval": "graceful-restart",
            "result": {
                "graceful_restart": {
                    "set": "{{ not graceful_restart }}",
                },
            }
        },
        {
            "name": "graceful_restart.restart_time",
            "getval": re.compile(
                r"""
                \s+graceful-restart\srestart-time\s(?P<restart_time>\d+)
                $""", re.VERBOSE
            ),
            "setval": "graceful-restart restart-time {{ graceful_restart.restart_time }}",
            "result": {
                "graceful_restart": {
                    "restart_time": "{{ restart_time }}",
                },
            }
        },
        {
            "name": "graceful_restart.stalepath_time",
            "getval": re.compile(
                r"""
                \s+graceful-restart\sstalepath-time\s(?P<stalepath_time>\d+)
                $""", re.VERBOSE
            ),
            "setval": "graceful-restart stalepath-time {{ graceful_restart.stalepath_time }}",
            "result": {
                "graceful_restart": {
                    "stalepath_time": "{{ stalepath_time }}",
                },
            }
        },
        {
            "name": "graceful_restart.helper",
            "getval": re.compile(
                r"""
                \s+(?P<helper>graceful-restart-helper)
                $""", re.VERBOSE
            ),
            "setval": "graceful-restart-helper",
            "result": {
                "graceful_restart": {
                    "helper": "{{ not not helper }}",
                },
            }
        },
        {
            "name": "graceful_shutdown.activate",
            "getval": re.compile(
                r"""
                \s+graceful-shutdown
                \s(?P<activate>activate)
                (\sroute-map
                \s(?P<route_map>\S+))?
                $""", re.VERBOSE
            ),
            "setval": _tmplt_graceful_shutdown_activate,
            "result": {
                "graceful_shutdown": {
                    "activate": {
                        "set": "{{ True if activate is defined and route_map is undefined else None }}",
                        "route_map": "{{ route_map }}",
                    }
                },
            }
        },
        {
            "name": "graceful_shutdown.aware",
            "getval": re.compile(
                r"""
                \s+no\sgraceful-shutdown
                \s(?P<aware>aware)
                $""", re.VERBOSE
            ),
            "setval": "graceful-shutdown aware",
            "result": {
                "graceful_shutdown": {
                    "aware": "{{ not aware }}"
                },
            }
        },
        {
            "name": "isolate",
            "getval": re.compile(
                r"""
                \s+(?P<isolate>isolate)
                (\s(?P<include_local>include-local))?
                $""", re.VERBOSE
            ),
            "setval": "isolate{{ ' include-local' if isolate.include_local|d(False) is True }}",
            "result": {
                "isolate": {
                    "set": "{{ True if isolate is defined and include_local is not defined else None }}",
                    "include_local": "{{ not not include_local }}",
                },
            }
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                \s+(?P<log_neighbor_changes>log-neighbor-changes)
                $""", re.VERBOSE
            ),
            "setval": "log-neighbor-changes",
            "result": {
                "log_neighbor_changes": "{{ not not log_neighbor_changes }}",
            }
        },
        {
            "name": "maxas_limit",
            "getval": re.compile(
                r"""
                \s+maxas-limit\s(?P<maxas_limit>\d+)
                $""", re.VERBOSE
            ),
            "setval": "maxas-limit {{ maxas_limit }}",
            "result": {
                "maxas_limit": "{{ maxas_limit }}",
            }
        },
        {
            "name": "neighbor.neighbor_address",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                $""", re.VERBOSE
            ),
            "setval": "neighbor {{ neighbor_address }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "neighbor_address": "{{ neighbor_address }}",
                    }
                }
            }
        },
        {
            "name": "neighbor.remote_as",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sremote-as\s(?P<remote_as>\S+)
                $""", re.VERBOSE
            ),
            "setval": "remote-as {{ remote_as }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "remote_as": "{{ remote_as }}",
                    }
                }
            }
        },
        {
            "name": "neighbor.bmp_activate_server",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sbmp-activate-server\s(?P<bmp_activate_server>\d+)
                $""", re.VERBOSE
            ),
            "setval": "bmp-activate-server {{ bmp_activate_server }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "bmp_activate_server": "{{ bmp_activate_server }}",
                    }
                }
            }
        },
        {
            "name": "neighbor.capability",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \scapability\ssuppress\s(?P<suppress_4_byte_as>4-byte-as)
                $""", re.VERBOSE
            ),
            "setval": "capability suppress 4-byte-as",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "capability": {
                            "suppress_4_byte_as": "{{ not not suppress_4_byte_as }}",
                        }
                    }
                }
            }
        },
        {
            "name": "neighbor.description",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sdescription\s(?P<description>\S+)
                $""", re.VERBOSE
            ),
            "setval": "description {{ description }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "description": "{{ description }}",
                    }
                }
            }
        },
        {
            "name": "neighbor.disable_connected_check",
            "getval": re.compile(
                r"""
                \s+neighbor\s(?P<neighbor_address>\S+)
                \sdescription\s(?P<description>\S+)
                $""", re.VERBOSE
            ),
            "setval": "description {{ description }}",
            "result": {
                "neighbors": {
                    "{{ neighbor_address }}": {
                        "description": "{{ description }}",
                    }
                }
            }
        },
    ]
    # fmt: on
