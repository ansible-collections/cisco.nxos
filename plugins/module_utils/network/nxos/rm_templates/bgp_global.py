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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
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
            "result":{
                "confederation": {
                    "identifier": "{{ identifier }}",
                },
            }
        },
        {
            "name": "confederation.peers",
            "getval": re.compile(
                r"""
                \s+confederation\speers\s(?P<peers>\S+)
                $""", re.VERBOSE
            ),
            "setval": _tmplt_confederation_peers,
            "result":{
                "confederation": {
                    "identifier": "{{ identifier }}",
                },
            }
        },
        
    ]
    # fmt: on
