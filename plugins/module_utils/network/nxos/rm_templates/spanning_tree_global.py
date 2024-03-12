# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Spanning_tree_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Spanning_tree_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Spanning_tree_globalTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "bridge_assurance",
            "getval": re.compile(
                r"""
                ^Bridge\sAssurance
                \s*(?P<is_enabled>is\senabled|is\sdisabled)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bridge assurance",
            "result": {
                "bridge_assurance": "{{ True if 'enabled' in is_enabled else False }}",
            },
        },
        {
            "name": "domain.identifier",
            "getval": re.compile(
                r"""
                ^spanning-tree\domain
                \s(?P<identifier>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree domain {{ identifier }}",
            "result": {
                "domain": {
                    "identifier": "{{ identifier }}",
                },
            },
        },
        {
            "name": "domain.disable",
            "getval": re.compile(
                r"""
                ^spanning-tree\domain
                \s(?P<disable>disable)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree domain disable",
            "result": {
                "domain": {
                    "disable": "{{ True if disable is defined else False }}",
                },
            },
        },
        {
            "name": "domain.enable",
            "getval": re.compile(
                r"""
                ^spanning-tree\domain
                \s(?P<enable>enable)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree domain enable",
            "result": {
                "domain": {
                    "enable": "{{ True if enable is defined else False }}",
                },
            },
        },
        {
            "name": "domain.clear_stats",
            "getval": re.compile(
                r"""
                ^spanning-tree\domain
                \s(?P<clear>clear\sstatistics)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree domain enable",
            "result": {
                "domain": {
                    "clear_stats": "{{ True if clear is defined else False }}",
                },
            },
        },
        {
            "name": "fcoe",
            "getval": re.compile(
                r"""
                ^no\sspanning-tree
                \s(?P<fcoe>fcoe)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree fcoe",
            "result": {
                "fcoe": "{{ False if fcoe is defined else True }}",
            },
        },
        {
            "name": "lc_issu",
            "getval": re.compile(
                r"""
                ^spanning-tree\slc-issu
                \s(?P<lc_issu>auto|disruptive|non-disruptive)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree lc-issu {{ lc_issu }}",
            "result": {
                "lc_issu": "{{ lc_issu }}",
            },
        },
        {
            "name": "loopguard_default",
            "getval": re.compile(
                r"""
                ^Loopguard\sDefault
                \s*(?P<is_enabled>is\senabled|is\sdisabled)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree loopguard default",
            "result": {
                "loopguard_default": "{{ True if 'enabled' in is_enabled else False }}",
            },
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                ^Switch\sis\sin
                \s(?P<mode_val>mst|rapid-pvst)
                \smode
                (\s\(IEEE\sStandard\))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mode {{ mode }}",
            "result": {
                "mode": "{{ mode_val }}",
            },
        },
        {
            "name": "mst.forward_time",
            "getval": re.compile(
                r"""
                ^spanning-tree\smst
                \sforward-time\s(?P<forward_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst forward-time {{ forward_time }}",
            "result": {
                "mst": {
                    "forward_time": "{{ forward_time }}",
                },
            },
        },
        {
            "name": "mst.hello_time",
            "getval": re.compile(
                r"""
                ^spanning-tree\smst
                \shello-time\s(?P<hello_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst hello-time {{ hello_time }}",
            "result": {
                "mst": {
                    "hello_time": "{{ hello_time }}",
                },
            },
        },
        {
            "name": "mst.max_age",
            "getval": re.compile(
                r"""
                ^spanning-tree\smst
                \smax-age\s(?P<max_age>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst max-age {{ max_age }}",
            "result": {
                "mst": {
                    "max_age": "{{ max_age }}",
                },
            },
        },
        {
            "name": "mst.max_hops",
            "getval": re.compile(
                r"""
                ^spanning-tree\smst
                \smax-hops\s(?P<max_hops>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst max-hops {{ max_hops }}",
            "result": {
                "mst": {
                    "max_hops": "{{ max_hops }}",
                },
            },
        },
        {
            "name": "mst.simulate_pvst_global",
            "getval": re.compile(
                r"""
                ^PVST\sSimulation
                \s+is\s(?P<simulate_pvst_global>enabled|disabled)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mst simulate pvst global",
            "result": {
                "mst": {
                    "simulate_pvst_global": "{{ True if 'enabled' in simulate_pvst_global else False }}",
                },
            },
        },
        {
            "name": "mst.configure_mst.name",
            "getval": re.compile(
                r"""
                ^\s+name\s(?P<name>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "name {{ configure_mst.name }}",
            "result": {
                "mst": {
                    "configure_mst": {
                        "name": "{{ name }}",
                    },
                },
            },
        },
        {
            "name": "mst.configure_mst.revision",
            "getval": re.compile(
                r"""
                ^\s+revision\s(?P<revision>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "revision {{ configure_mst.revision }}",
            "result": {
                "mst": {
                    "configure_mst": {
                        "revision": "{{ revision }}",
                    },
                },
            },
        },
        {
            "name": "mst.configure_mst.private_vlan_sync",
            "getval": re.compile(
                r"""
                ^\s+private-vlan\s(?P<synchronize>synchronize)
                $""", re.VERBOSE,
            ),
            "setval": "private-vlan synchronize",
            "result": {
                "mst": {
                    "configure_mst": {
                        "private_vlan_sync": "{{ True if synchronize is defined else False }}",
                    },
                },
            },
        },
        {
            "name": "mst.configure_mst.instance_vlan",
            "getval": re.compile(
                r"""
                ^\s+instance
                \s(?P<instance_id>\d+)
                \svlan\s(?P<vlan_range>\S+)
                $""", re.VERBOSE,
            ),
            "setval": "instance {{ instance_id }} vlan {{ vlan_range }}",
            "result": {
                "mst": {
                    "configure_mst": {
                        "instance_vlan": {
                            "{{ instance_id }}": {
                                "instance_id": "{{ instance_id }}",
                                "vlan_range": "{{ vlan_range | string }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "pathcost_method",
            "getval": re.compile(
                r"""
                ^Pathcost\smethod\sused
                \s*is\s(?P<pc_method>long|short)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree pathcost method {{ pathcost_method }}",
            "result": {
                "pathcost_method": "{{ pc_method }}",
            },
        },
        {
            "name": "port_type.edge.bpdufilter",
            "getval": re.compile(
                r"""
                ^spanning-tree
                \sport\stype\sedge
                \sbpdufilter\s(?P<bpdufilter>default)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree port type edge bpdufilter default",
            "result": {
                "port_type": {
                    "edge": {
                        "bpdufilter": "{{ True if bpdufilter is defined else False }}",
                    },
                },
            },
        },
        {
            "name": "port_type.edge.bpduguard",
            "getval": re.compile(
                r"""
                ^spanning-tree
                \sport\stype\sedge
                \sbpduguard\s(?P<bpduguard>default)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree port type edge bpduguard default",
            "result": {
                "port_type": {
                    "edge": {
                        "bpduguard": "{{ True if bpduguard is defined else False }}",
                    },
                },
            },
        },
        {
            "name": "port_type.default_type",
            "getval": re.compile(
                r"""
                ^spanning-tree
                \sport\stype
                \s(?P<default_type>edge|network)
                \sdefault
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree port type {{ default_type }} default",
            "result": {
                "port_type": {
                    "default_type": "{{ default_type }}",
                },
            },
        },
        {
            "name": "pseudo_info.mst_info.designated_priority",
            "getval": re.compile(
                r"""
                ^\s+mst\s(?P<range>\S+)
                \sdesignated\spriority
                \s(?P<designated_priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "mst {{ mst_info.range }} designated priority {{ mst_info.designated_priority }}",
            "result": {
                "pseudo_info": {
                    "mst_info": {
                        "{{ range }}": {
                            "range": "{{ range }}",
                            "designated_priority": "{{ designated_priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "pseudo_info.mst_info.root_priority",
            "getval": re.compile(
                r"""
                ^\s+mst\s(?P<range>\S+)
                \sroot\spriority
                \s(?P<root_priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "mst {{ mst_info.range }} root priority {{ mst_info.root_priority }}",
            "result": {
                "pseudo_info": {
                    "mst_info": {
                        "{{ range }}": {
                            "range": "{{ range }}",
                            "root_priority": "{{ root_priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "pseudo_info.vlan_info.designated_priority",
            "getval": re.compile(
                r"""
                ^\s+vlan\s(?P<range>\S+)
                \sdesignated\spriority
                \s(?P<designated_priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "vlan {{ vlan_info.range }} designated priority {{ vlan_info.designated_priority }}",
            "result": {
                "pseudo_info": {
                    "vlan_info": {
                        "{{ range }}": {
                            "range": "{{ range }}",
                            "designated_priority": "{{ designated_priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "pseudo_info.vlan_info.root_priority",
            "getval": re.compile(
                r"""
                ^\s+vlan\s(?P<range>\S+)
                \sroot\spriority
                \s(?P<root_priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "vlan {{ vlan_info.range }} root priority {{ vlan_info.root_priority }}",
            "result": {
                "pseudo_info": {
                    "vlan_info": {
                        "{{ range }}": {
                            "range": "{{ range }}",
                            "root_priority": "{{ root_priority }}",
                        },
                    },
                },
            },
        },
        {
            "name": "vlan.forward_time",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \sforward-time\s(?P<forward_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }} forward-time {{ forward_time }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "forward_time": "{{ forward_time }}",
                    },
                },
            },
        },
        {
            "name": "vlan.hello_time",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \shello-time\s(?P<hello_time>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }} hello-time {{ hello_time }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "hello_time": "{{ hello_time }}",
                    },
                },
            },
        },
        {
            "name": "vlan.max_age",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \smax-age\s(?P<max_age>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }} max-age {{ max_age }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "max_age": "{{ max_age }}",
                    },
                },
            },
        },
        {
            "name": "vlan.priority",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \spriority\s(?P<priority>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }} priority {{ priority }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "priority": "{{ priority }}",
                    },
                },
            },
        },
        {
            "name": "vlan.root.primary",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \sroot\sprimary
                (\sdiameter\s(?P<diameter>\d+))?
                (\shello-time\s(?P<hello_time>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }}"
                      " root primary"
                      "{{ (' diameter ' + root.primary.diameter|string) if root.primary.diameter is defined else '' }}"
                      "{{ (' hello-time ' + root.primary.hello_time|string) if root.primary.hello_time is defined else '' }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "root": {
                            "primary": {
                                "diameter": "{{ diameter }}",
                                "hello_time": "{{ hello_time }}",
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "vlan.root.secondary",
            "getval": re.compile(
                r"""
                ^spanning-tree\svlan
                \s(?P<vlan_range>\S+)
                \sroot\ssecondary
                (\sdiameter\s(?P<diameter>\d+))?
                (\shello-time\s(?P<hello_time>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree vlan {{ vlan_range }}"
                      " root secondary"
                      "{{ (' diameter ' + root.secondary.diameter|string) if root.secondary.diameter is defined else '' }}"
                      "{{ (' hello-time ' + root.secondary.hello_time|string) if root.secondary.hello_time is defined else '' }}",
            "result": {
                "vlan": {
                    "{{ vlan_range | string }}": {
                        "vlan_range": "{{ vlan_range | string }}",
                        "root": {
                            "secondary": {
                                "diameter": "{{ diameter }}",
                                "hello_time": "{{ hello_time }}",
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
