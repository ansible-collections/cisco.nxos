# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Route_maps parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class Route_mapsTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Route_mapsTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "route_map",
            "getval": re.compile(
                r"""
                ^route-map\s(?P<route_map>\S+)\s(?P<action>\S+)\s(?P<sequence>\d+)
                $""", re.VERBOSE),
            "setval": "route-map {{ route_map }} {{ action }}{{ ' ' + sequence|string if sequence is defined else '' }}",
            "result": {
                "{{ route_map }}": {
                    "route_map": "{{ route_map }}",
                    "entries": {
                        "{{ sequence }}": {
                            "sequence": "{{ sequence }}",
                            "action": "{{ action }}",
                        }
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "continue",
            "getval": re.compile(
                r"""
                \s+continue\s(?P<continue>\d+)
                $""", re.VERBOSE),
            "setval": "continue {{ continue }}",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "continue": "{{ continue }}",
                        }
                    }
                }
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \s+description\s(?P<description>\S+)
                $""", re.VERBOSE),
            "setval": "description {{ description }}",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "description": "{{ description }}",
                        }
                    }
                }
            },
        },
        {
            "name": "match.as_number.asn",
            "getval": re.compile(
                r"""
                \s+match\sas-number
                \s(?P<asn>\S+)\s*
                $""", re.VERBOSE),
            "setval": "match as-number {{ asn }}",
            "result": {
                "{{ route_map }}": {
                    "route_map": "{{ route_map }}",
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                                "as_number": {
                                    "asn": "{{ asn }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.as_number.as_path_list",
            "getval": re.compile(
                r"""
                \s+match\sas-number
                \sas-path-list\s(?P<as_path_list>\S+)\s*
                $""", re.VERBOSE),
            "setval": "match as-number as-path-list {{ as_path_list }}",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                                "as_number": {
                                    "as_path_list": "{{ as_path_list }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.as_number.as_path",
            "getval": re.compile(
                r"""
                \s+match\sas-path\s(?P<as_path>\S+)\s*
                $""", re.VERBOSE),
            "setval": "match as-path {{ as_path }}",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "as_path": "{{ as_path }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.community",
            "getval": re.compile(
                r"""
                \s+match\scommunity
                \s(?P<community_list>.+)
                \s(?P<exact_match>exact-match)?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "community": {
                                   "community_list": "{{ community_list.split() }}",
                                   "exact_match": "{{ not not exact_match }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.evpn.route_type",
            "getval": re.compile(
                r"""
                \s+match\sevpn
                \sroute-type
                \s(?P<route_type>.+)\s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "evpn": {
                                   "route_type": "{{ route_type.split() }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.extcommunity",
            "getval": re.compile(
                r"""
                \s+match\sextcommunity
                \s(?P<extcommunity_list>.+)
                \s(?P<exact_match>exact-match)?
                \s*
                $""", re.VERBOSE),
            "setval": "match as-path {{ as_path }}",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "extcommunity": {
                                   "extcommunity_list": "{{ extcommunity_list.split() }}",
                                   "exact_match": "{{ not not exact_match }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.interfaces",
            "getval": re.compile(
                r"""
                \s+match\sinterface
                \s(?P<interfaces>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "interfaces": "{{ interfaces.split() }}"
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip.address.access_list",
            "getval": re.compile(
                r"""
                \s+match\sip\saddress
                \s(?P<access_list>\S+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ip": {
                                   "address": {
                                       "access_list": "{{ access_list }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip.address.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sip\saddress
                \sprefix-list
                \s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ip": {
                                   "address": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                    }
                               }
                            }
                        }
                    }
                }
            },
        },
        # match ip multicast source 192.1.2.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 209.165.201.0/27 rp-type Bidir
        {
            "name": "match.ip.multicast.group",
            "getval": re.compile(
                r"""
                \s+match\sip\smulticast
                (\ssource\s(?P<source>\S+))?
                \sgroup
                \s(?P<prefix>\S+)
                (\srp\s(?P<rp>\S+))?
                (\srp-type\s(?P<rp_type>\S+))?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ip": {
                                   "multicast": {
                                       "group": {
                                           "prefix": "{{ prefix }}",
                                           "rp": {
                                              "prefix": "{{ rp }}",
                                              "rp_type": "{{ rp_type }}",
                                           },
                                           "source": "{{ source }}",
                                       }
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip.multicast.group_range",
            "getval": re.compile(
                r"""
                \s+match\sip\smulticast
                (\ssource\s(?P<source>\S+))?
                \sgroup-range
                \s(?P<first>\S+)
                \sto
                \s(?P<last>\S+)
                (\srp\s(?P<rp>\S+))?
                (\srp-type\s(?P<rp_type>\S+))?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ip": {
                                   "multicast": {
                                       "group_range": {
                                           "first": "{{ first }}",
                                           "last": "{{ last }}",
                                           "rp": {
                                              "prefix": "{{ rp }}",
                                              "rp_type": "{{ rp_type }}",
                                           },
                                           "source": "{{ source }}",
                                       },
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip.next_hop.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sip\snext-hop
                \sprefix-list\s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ip": {
                                   "next_hop": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ip.route_source.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sipv6\sroute-source
                \sprefix-list\s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "route_source": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.address.access_list",
            "getval": re.compile(
                r"""
                \s+match\sipv6\saddress
                \s(?P<access_list>\S+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "address": {
                                       "access_list": "{{ access_list }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.address.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sipv6\saddress
                \sprefix-list
                \s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "address": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                    }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.multicast.group",
            "getval": re.compile(
                r"""
                \s+match\sipv6\smulticast
                (\ssource\s(?P<source>\S+))?
                \sgroup
                \s(?P<prefix>\S+)
                (\srp\s(?P<rp>\S+))?
                (\srp-type\s(?P<rp_type>\S+))?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "multicast": {
                                       "group": {
                                           "prefix": "{{ prefix }}",
                                           "rp": {
                                              "prefix": "{{ rp }}",
                                              "rp_type": "{{ rp_type }}",
                                           },
                                           "source": "{{ source }}",
                                       }
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.multicast.group_range",
            "getval": re.compile(
                r"""
                \s+match\sipv6\smulticast
                (\ssource\s(?P<source>\S+))?
                \sgroup-range
                \s(?P<first>\S+)
                \sto
                \s(?P<last>\S+)
                (\srp\s(?P<rp>\S+))?
                (\srp-type\s(?P<rp_type>\S+))?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "multicast": {
                                       "group_range": {
                                           "first": "{{ first }}",
                                           "last": "{{ last }}",
                                           "rp": {
                                              "prefix": "{{ rp }}",
                                              "rp_type": "{{ rp_type }}",
                                           },
                                           "source": "{{ source }}",
                                       },
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.next_hop.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sipv6\snext-hop
                \sprefix-list\s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "next_hop": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ipv6.route_source.prefix_lists",
            "getval": re.compile(
                r"""
                \s+match\sipv6\sroute-source
                \sprefix-list\s(?P<prefix_lists>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ipv6": {
                                   "route_source": {
                                       "prefix_lists": "{{ prefix_lists.split() }}",
                                   }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.mac_list",
            "getval": re.compile(
                r"""
                \s+match\smac-list
                \s(?P<mac_list>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "mac_list": "{{ mac_list.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.metric",
            "getval": re.compile(
                r"""
                \s+match\smetric
                \s(?P<metric>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "metric": "{{ metric.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.ospf_area",
            "getval": re.compile(
                r"""
                \s+match\sospf-area
                \s(?P<ospf_area>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "ospf_area": "{{ ospf_area.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.route_type",
            "getval": re.compile(
                r"""
                \s+match\sroute-type
                \s(?P<route_type>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "route_type": "{{ route_type.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.source_protocol",
            "getval": re.compile(
                r"""
                \s+match\ssource-protocol
                \s(?P<route_type>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "source_protocol": "{{ source_protocol.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "match.tags",
            "getval": re.compile(
                r"""
                \s+match\stag
                \s(?P<tags>.+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "match": {
                               "tags": "{{ tags.split() }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.as_path.prepend.as_number",
            "getval": re.compile(
                r"""
                \s+set\sas-path\sprepend
                \s(?P<as_number>(?!last-as).+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "as_path": {
                                   "prepend": {
                                       "as_number": "{{ as_number.split() }}",
                                    }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.as_path.prepend.last_as",
            "getval": re.compile(
                r"""
                \s+set\sas-path\sprepend
                \slast-as\s(?P<last_as>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "as_path": {
                                   "prepend": {
                                       "last_as": "{{ last_as }}",
                                    }
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.as_path.tag",
            "getval": re.compile(
                r"""
                \s+set\sas-path
                \s(?P<tag>tag)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "as_path": {
                                   "tag": "{{ not not tag }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.comm_list",
            "getval": re.compile(
                r"""
                \s+set\scomm-list
                \s(?P<comm_list>\S+)
                \s*delete
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "comm_list": "{{ comm_list }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.community",
            "getval": re.compile(
                r"""
                \s+set\scommunity
                (\s(?P<internet>internet))?
                (?P<number>(\s\d+:\d+)*)
                (\s(?P<no_export>no-export))?
                (\s(?P<no_advertise>no-advertise))?
                (\s(?P<local_as>local-AS))?
                (\s(?P<graceful_shutdown>graceful-shutdown))?
                (\s(?P<additive>additive))?\s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "community": {
                                   "internet": "{{ not not internet }}",
                                   "number": "{{ number.split() }}",
                                   "no_export": "{{ not not no_export }}",
                                   "no_advertise": "{{ not not no_advertise }}",
                                   "local_as": "{{ not not local_as }}",
                                   "graceful_shutdown": "{{ not not graceful_shutdown }}",
                                   "additive": "{{ not not additive }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.dampening",
            "getval": re.compile(
                r"""
                \s+set\sdampening
                \s(?P<half_life>\d+)
                \s(?P<start_reuse_route>\d+)
                \s(?P<start_suppress_route>\d+)
                \s(?P<max_suppress_time>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                                "dampening": {
                                        "half_life": "{{ half_life }}",
                                        "start_reuse_route": "{{ start_reuse_route }}",
                                        "start_suppress_route": "{{ start_suppress_route }}",
                                        "max_suppress_time": "{{ max_suppress_time }}",
                                    }
                                }
                        }
                    }
                }
            },
        },
        {
            "name": "set.distance",
            "getval": re.compile(
                r"""
                \s+set\sdistance
                \s(?P<igp_ebgp_routes>\d+)
                \s(?P<internal_routes>\d+)
                \s(?P<local_routes>\d+)
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                                "distance": {
                                    "igp_ebgp_routes": "{{ igp_ebgp_routes }}",
                                    "internal_routes": "{{ internal_routes }}",
                                    "local_routes": "{{ local_routes }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.evpn.gateway_ip",
            "getval": re.compile(
                r"""
                \s+set\sevpn
                \sgateway-ip
                (\s(?P<ip>(?!use-nexthop)\S+))?
                (\s(?P<use_nexthop>use-nexthop))?
                \s*
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                                "evpn": {
                                    "gateway_ip": {
                                        "ip": "{{ ip }}",
                                        "use_nexthop": "{{ not not use_nexthop }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.extcomm_list",
            "getval": re.compile(
                r"""
                \s+set\sextcomm-list
                \s(?P<extcomm_list>\S+)
                \s*delete
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "extcomm_list": "{{ extcomm_list }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.forwarding_address",
            "getval": re.compile(
                r"""
                \s+set
                \s(?P<forwarding_address>forwarding-address)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "forwarding_address": "{{ not not forwarding_address }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.null_interface",
            "getval": re.compile(
                r"""
                \s+set\sinterface
                \s(?P<interface>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "null_interface": "{{ interface }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ip.address.prefix_list",
            "getval": re.compile(
                r"""
                \s+set\sip\saddress
                \sprefix-list\s(?P<prefix_list>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "ip": {
                                   "address": {
                                       "prefix_list": "{{ prefix_list }}",
                                   }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ip.precedence",
            "getval": re.compile(
                r"""
                \s+set\sip
                \sprecedence\s(?P<precedence>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "ip": {
                                   "precedence": "{{ precedence }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ipv6.address.prefix_list",
            "getval": re.compile(
                r"""
                \s+set\sipv6\saddress
                \sprefix-list\s(?P<prefix_list>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "ipv6": {
                                   "address": {
                                       "prefix_list": "{{ prefix_list }}",
                                   }
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.ipv6.precedence",
            "getval": re.compile(
                r"""
                \s+set\sipv6
                \sprecedence\s(?P<precedence>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "ipv6": {
                                   "precedence": "{{ precedence }}",
                                }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.label_index",
            "getval": re.compile(
                r"""
                \s+set\slabel-index
                \s(?P<label_index>\d+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "label_index": "{{ label_index }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.level",
            "getval": re.compile(
                r"""
                \s+set\slevel
                \s(?P<level>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "level": "{{ level }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.local_preference",
            "getval": re.compile(
                r"""
                \s+set\slocal-preference
                \s(?P<local_preference>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "local_preference": "{{ local_preference }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.metric",
            "getval": re.compile(
                r"""
                \s+set\smetric
                \s(?P<bandwidth>\d+)
                \s(?P<igrp_delay_metric>\d+)
                \s(?P<igrp_reliability_metric>\d+)
                \s(?P<igrp_effective_bandwidth_metric>\d+)
                \s(?P<igrp_mtu>\d+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "metric": {
                                   "bandwidth": "{{ bandwidth }}",
                                   "igrp_delay_metric": "{{ igrp_delay_metric }}",
                                   "igrp_reliability_metric": "{{ igrp_reliability_metric }}",
                                   "igrp_effective_bandwidth_metric": "{{ igrp_effective_bandwidth_metric }}",
                                   "igrp_mtu": "{{ igrp_mtu }}",
                               }
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.metric_type",
            "getval": re.compile(
                r"""
                \s+set\smetric-type
                \s(?P<metric_type>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "metric_type": "{{ metric_type }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.nssa_only",
            "getval": re.compile(
                r"""
                \s+set
                \s(?P<nssa_only>nssa-only)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "nssa_only": "{{ not not nssa_only }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.origin",
            "getval": re.compile(
                r"""
                \s+set\sorigin
                \s(?P<origin>\S+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "origin": "{{ origin }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.path_selection",
            "getval": re.compile(
                r"""
                \s+set\spath-selection
                \s(?P<path_selection>\S+)
                \sadvertise
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "path_selection": "{{ path_selection }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.tag",
            "getval": re.compile(
                r"""
                \s+set\stag
                \s(?P<tag>\d+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "tag": "{{ tag }}",
                            }
                        }
                    }
                }
            },
        },
        {
            "name": "set.weight",
            "getval": re.compile(
                r"""
                \s+set\sweight
                \s(?P<weight>\d+)
                \s*$""", re.VERBOSE),
            "setval": "",
            "result": {
                "{{ route_map }}": {
                    "entries": {
                        "{{ sequence }}": {
                            "set": {
                               "weight": "{{ weight }}",
                            }
                        }
                    }
                }
            },
        },
    ]
    # fmt: on
