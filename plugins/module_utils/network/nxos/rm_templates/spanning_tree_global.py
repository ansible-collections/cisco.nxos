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
            "name": "bridge.bridge_assurance",
            "getval": re.compile(
                r"""
                ^Bridge\sAssurance
                \s*(?P<is_enabled>is\senabled|is\sdisabled)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bridge assurance",
            "result": {
                "bridge": {
                    "bridge_assurance": "{{ True if 'enabled' in is_enabled else False }}",
                },
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
    ]
    # fmt: on
