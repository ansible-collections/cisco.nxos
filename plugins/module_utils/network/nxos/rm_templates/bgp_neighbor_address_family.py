# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Bgp_neighbor_address_family parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


class Bgp_neighbor_address_familyTemplate(NetworkTemplate):
    def __init__(self, lines=None):
        super(Bgp_neighbor_address_familyTemplate, self).__init__(
            lines=lines, tmplt=self
        )

    # fmt: off
    PARSERS = [
        {
            "name": "as_number",
            "getval": re.compile(
                r"""
                ^router\sbgp\s(?P<as_number>\S+)
                $""", re.VERBOSE
            ),
            "setval": "router bgp {{ as_number }}",
            "result": {
                "as_number": "{{ as_number }}",
            },
            "shared": True
        },
        {
            "name": "address_family",
            "getval": re.compile(
                r"""
                (vrf\s(?P<vrf>\S+))?
                \s*neighbor\s(?P<neighbor>\S+)
                \saddress-family
                \s(?P<afi>\S+)
                (\s(?P<safi>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "address-family {{ afi }}{{ (' ' + safi) if safi is defined }}",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "neighbors": {
                            "{{ neighbor }}": {
                                "neighbor": "{{ neighbor }}",
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "afi": "{{ afi }}",
                                        "safi": "{{ safi }}",
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "shared": True,
        },
        {
            "name": "no_advertise_local_labeled_route",
            "getval": re.compile(
                r"""
                no\sadvertise
                \s(?P<local_labeled_route>local-labeled-route)
                $""",
                re.VERBOSE,
            ),
            "setval": "advertise local-labeled-route",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "vrf": "{{ vrf }}",
                        "neighbors": {
                            "{{ neighbor }}": {
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "no_advertise_local_labeled_route": "{{ not not local_labeled_route }}"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "advertise_map",
            "getval": re.compile(
                r"""
                advertise-map
                \s(?P<route_map>\S+)
                (\sexist-map\s(?P<exist_map>\S+))?
                (\snon-exist-map\s(?P<non_exist_map>\S+))?
                $""",
                re.VERBOSE,
            ),
            "setval": "advertise-map {{ advertise_map.route_map }}{{ ' ' + advertise_map.exist_map if advertise_map.exist_map is defined else ' ' + advertise_map.non_exist_map}}",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "vrf": "{{ vrf }}",
                        "neighbors": {
                            "{{ neighbor }}": {
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "advertise_map": {
                                            "route_map": "{{ route_map }}",
                                            "exist_map": "{{ exist_map }}",
                                            "non_exist_map": "{{ non_exist_map }}",
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "advertisement_interval",
            "getval": re.compile(
                r"""
                advertisement-interval
                \s(?P<advertisement_interval>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "advertisement_interval {{ advertisement_interval }}",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "vrf": "{{ vrf }}",
                        "neighbors": {
                            "{{ neighbor }}": {
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "advertisement_interval": "{{ advertisement_interval }}",
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "allowas_in",
            "getval": re.compile(
                r"""
                (?P<allowas_in>allowas-in)
                \s(?P<max_occurences>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "allowas-in{{ ' ' + allowas_in.max_occurences if allowas_in.max_occurences is defined }}",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "vrf": "{{ vrf }}",
                        "neighbors": {
                            "{{ neighbor }}": {
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "allowas_in": {
                                            "set": "{{ True if allowas_in is defined and max_occurences is undefined }}",
                                            "max_occurences": "{{ max_occurences }}",
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "advertise_gw_ip",
            "getval": re.compile(
                r"""
                no\s(?P<no_advertise_gw_ip>advertise-gw-ip)
                $""",
                re.VERBOSE,
            ),
            "setval": "advertise-gw-ip",
            "result": {
                "vrfs": {
                    "{{ 'vrf_' + vrf|d() }}": {
                        "vrf": "{{ vrf }}",
                        "neighbors": {
                            "{{ neighbor }}": {
                                "address_family": {
                                    '{{ afi + "_" + safi|d() }}': {
                                        "no_advertise_gw_ip": "{{ not not no_advertise_gw_ip }}",
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
    ]
    # fmt: on
