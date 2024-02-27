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
                ^spanning-tree
                \sbridge\s(?P<assurance>assurance)
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree bridge assurance",
            "result": {
                "bridge_assurance": "{{ True if assurance is defined else None }}",
            },
        },
        {
            "name": "mode",
            "getval": re.compile(
                r"""
                ^spanning-tree
                (\smode\s(?P<mode>mst|rapid-pvst))
                $""", re.VERBOSE,
            ),
            "setval": "spanning-tree mode {{ mode }}",
            "result": {
                "mode": "{{ mode }}",
            },
        },
    ]
    # fmt: on
