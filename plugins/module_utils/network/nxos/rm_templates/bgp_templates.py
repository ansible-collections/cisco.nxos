# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Bgp_templates parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Bgp_templatesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Bgp_templatesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "peer.name",
            "getval": re.compile(
                r"""
                template\speer\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "template peer {{ name }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "name": "{{ name }}",
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "bfd",
            "getval": re.compile(
                r"""
                (?P<bfd>bfd)
                (\s(?P<singlehop>singlehop))?
                (\s(?P<multihop>multihop))?
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "bfd": {
                            "set": "{{ True if bfd is defined and singlehop is undefined and multihop is undefined else None }}",
                            "singlehop": "{{ not not singlehop }}",
                            "multihop": {
                                "set": "{{ not not multihop }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bfd.multihop.interval",
            "getval": re.compile(
                r"""
                bfd\smultihop\sinterval
                \s(?P<tx_interval>\d+)
                \smin_rx\s(?P<min_rx_interval>\d+)
                \smultiplier\s(?P<multiplier>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "bfd multihop interval"
                      " {{ bfd.multihop.interval.tx_interval }}"
                      " min_rx {{ bfd.multihop.interval.min_rx_interval }}"
                      " multiplier {{ bfd.multihop.interval.multiplier }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "bfd": {
                            "multihop": {
                                "interval": {
                                    "tx_interval": "{{ tx_interval }}",
                                    "min_rx_interval": "{{ min_rx_interval }}",
                                    "multiplier": "{{ multiplier }}",
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "bmp_activate_server",
            "getval": re.compile(
                r"""
                bmp-activate-server\s(?P<bmp_activate_server>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "bmp-activate-server {{ bmp_activate_server }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                       "bmp_activate_server": "{{ bmp_activate_server }}",
                    },
                },
            },
        },
        {
            "name": "capability",
            "getval": re.compile(
                r"""
                capability\ssuppress\s(?P<suppress_4_byte_as>4-byte-as)
                $""", re.VERBOSE,
            ),
            "setval": "capability suppress 4-byte-as",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "capability": {
                            "suppress_4_byte_as": "{{ not not suppress_4_byte_as }}",
                        },
                    },
                },
            },
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                description\s(?P<description>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "description {{ description }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "description": "{{ description }}",
                    },
                },
            },
        },
        {
            "name": "disable_connected_check",
            "getval": re.compile(
                r"""
                (?P<disable_connected_check>disable-connected-check)
                $""", re.VERBOSE,
            ),
            "setval": "disable-connected-check",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "disable_connected_check": "{{ not not disable_connected_check }}",
                    },
                },
            },
        },
        {
            "name": "dont_capability_negotiate",
            "getval": re.compile(
                r"""
                (?P<dont_capability_negotiate>dont-capability-negotiate)
                $""", re.VERBOSE,
            ),
            "setval": "dont-capability-negotiate",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "dont_capability_negotiate": "{{ not not dont_capability_negotiate }}",
                    },
                },
            },
        },
        {
            "name": "dscp",
            "getval": re.compile(
                r"""
                dscp\s(?P<dscp>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "dscp {{ dscp }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "dscp": "{{ dscp }}",
                    },
                },
            },
        },
        {
            "name": "dynamic_capability",
            "getval": re.compile(
                r"""
                (?P<dynamic_capability>dynamic-capability)
                $""", re.VERBOSE,
            ),
            "setval": "dynamic-capability",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "dynamic_capability": "{{ not not dynamic_capability }}",
                    },
                },
            },
        },
        {
            "name": "ebgp_multihop",
            "getval": re.compile(
                r"""
                ebgp-multihop\s(?P<ebgp_multihop>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ebgp-multihop {{ ebgp_multihop }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "ebgp_multihop": "{{ ebgp_multihop }}",
                    },
                },
            },
        },
        {
            "name": "graceful_shutdown",
            "getval": re.compile(
                r"""
                graceful-shutdown
                \s(?P<activate>activate)
                (\sroute-map\s(?P<route_map>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "graceful-shutdown{{ (' route-map ' + graceful_shutdown.route_map) if graceful_shutdown.route_map is defined }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "graceful_shutdown": {
                            "activate": {
                                "set": "{{ True if activate is defined and route_map is undefined else None }}",
                                "route_map": "{{ route_map }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "inherit.peer_session",
            "getval": re.compile(
                r"""
                inherit
                \speer-session\s(?P<peer_session>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "inherit peer-session {{ inherit.peer_session }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "inherit": {
                            "peer_session": "{{ peer_session }}",
                        },
                    },
                },
            },
        },
        {
            "name": "local_as",
            "getval": re.compile(
                r"""
                local-as\s(?P<local_as>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "local-as {{ local_as }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "local_as": "{{ local_as }}",
                    },
                },
            },
        },
        {
            "name": "log_neighbor_changes",
            "getval": re.compile(
                r"""
                (?P<log_neighbor_changes>log-neighbor-changes)
                (\s(?P<disable>disable))?
                $""", re.VERBOSE,
            ),
            "setval": "log-neighbor-changes{{ ' disable' if log_neighbor_changes.disable is defined }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "log_neighbor_changes": {
                            "set": "{{ True if log_neighbor_changes is defined and disable is undefined }}",
                            "disable": "{{ not not disable }}",
                        },
                    },
                },
            },
        },
        {
            "name": "low_memory",
            "getval": re.compile(
                r"""
                low-memory\s(?P<exempt>exempt)
                $""", re.VERBOSE,
            ),
            "setval": "low-memory exempt",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "low_memory": {
                            "exempt": "{{ not not exempt }}",
                        },
                    },
                },
            },
        },
        {
            "name": "password",
            "getval": re.compile(
                r"""
                password\s(?P<encryption>\d+)\s(?P<key>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "password{{ (' ' + password.encryption|string) if password.encryption is defined }} {{ password.key }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "password": {
                            "encryption": "{{ encryption }}",
                            "key": "{{ key }}",
                        },
                    },
                },
            },
        },
        {
            "name": "path_attribute",
            "getval": re.compile(
                r"""
                path-attribute\s(?P<action>\S+)\s
                (?P<type>\d+)?
                (range\s(?P<start>\d+)\s(?P<end>\d+))?
                \sin
                $""", re.VERBOSE,
            ),
            "setval": "",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "path_attribute": [
                            {
                                "action": "{{ action }}",
                                "type": "{{ type if type is defined else None }}",
                                "range": {
                                    "start": "{{ start if start is defined }}",
                                    "end": "{{ end if end is defined }}",
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "remote_as",
            "getval": re.compile(
                r"""
                \sremote-as\s(?P<remote_as>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "remote-as {{ remote_as }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "remote_as": "{{ remote_as }}",
                    },
                },
            },
        },
        {
            "name": "remove_private_as",
            "getval": re.compile(
                r"""
                (?P<remove_private_as>remove-private-as)
                (\s(?P<all>all))?
                (\s(?P<replace_as>replace-as))?
                $""", re.VERBOSE,
            ),
            "setval": "remove-private-as",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "remove_private_as": {
                            "set": "{{ True if remove_private_as is defined and replace_as is undefined and all is undefined else None }}",
                            "replace_as": "{{ not not replace_as }}",
                            "all": "{{ not not all }}",
                        },
                    },
                },
            },
        },
        {
            "name": "shutdown",
            "getval": re.compile(
                r"""
                (?P<shutdown>shutdown)
                $""", re.VERBOSE,
            ),
            "setval": "shutdown",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "shutdown": "{{ not not shutdown }}",
                    },
                },
            },
        },
        {
            "name": "timers",
            "getval": re.compile(
                r"""
                timers\s(?P<keepalive>\d+)\s(?P<holdtime>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "timers {{ timers.keepalive }} {{ timers.holdtime }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "timers": {
                            "keepalive": "{{ keepalive }}",
                            "holdtime": "{{ holdtime }}",
                        },
                    },
                },
            },
        },
        {
            "name": "transport",
            "getval": re.compile(
                r"""
                transport\sconnection-mode
                \s(?P<passive>passive)
                $""", re.VERBOSE,
            ),
            "setval": "transport connection-mode passive",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "transport": {
                            "connection_mode": {
                                "passive": "{{ not not passive }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "ttl_security",
            "getval": re.compile(
                r"""
                ttl-security\shops\s(?P<hops>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "ttl-security hops {{ ttl_security.hops }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "ttl_security": {
                            "hops": "{{ hops }}",
                        },
                    },
                },
            },
        },
        {
            "name": "update_source",
            "getval": re.compile(
                r"""
                update-source\s(?P<update_source>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "update-source {{ update_source }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "update_source": "{{ update_source }}",
                    },
                },
            },
        },
        # start template AF parsers
        {
            "name": "address_family",
            "getval": re.compile(
                r"""
                template\speer\s(?P<name>\S+)
                \saddress-family\s(?P<afi>\S+)\s(?P<safi>\S+)
                $""",
                re.VERBOSE,
            ),
            "setval": "address-family {{ afi }}{{ (' ' + safi) if safi is defined else '' }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "address_family": {
                            "{{ afi + '_' + safi|d() }}": {
                                "afi": "{{ afi }}",
                                "safi": "{{ safi }}",
                            },
                        },
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "allowas_in",
            "getval": re.compile(
                r"""
                (?P<allowas_in>allowas-in)\s(?P<max_occurences>\d+)
                $""",
                re.VERBOSE,
            ),
            "setval": "allowas-in{{ ' ' + allowas_in.max_occurences|string if allowas_in.max_occurences is defined else '' }}",
            "result": {
                "peers": {
                    "{{ name }}": {
                        "address_family": {
                            "{{ afi + '_' + safi|d() }}": {
                                "allowas_in": {
                                    "set": "{{ True if allowas_in is defined and max_occurences is undefined }}",
                                    "max_occurences": "{{ max_occurences }}",
                                },
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
