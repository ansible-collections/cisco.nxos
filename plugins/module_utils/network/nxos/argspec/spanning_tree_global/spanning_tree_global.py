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
The arg spec for the nxos_spanning_tree_global module
"""


class Spanning_tree_globalArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_spanning_tree_global module
    """

    argument_spec = {
        "config": {
            "type": "dict",
            "options": {
                "bridge_assurance": {"type": "bool"},
                "bridge_domain": {"type": "str"},
                "fcoe": {"type": "bool"},
                "lc_issu": {
                    "type": "str",
                    "choices": ["auto", "disruptive", "non-disruptive"],
                },
                "loopguard_default": {"type": "bool"},
                "mode": {"type": "str", "choices": ["mst", "rapid-pvst"]},
                "pathcost_method": {"type": "str", "choices": ["long", "short"]},
                "port_type": {
                    "type": "dict",
                    "mutually_exclusive": [["edge", "network", "default"]],
                    "options": {
                        "edge": {
                            "type": "str",
                            "choices": ["bpdufilter", "bpduguard", "default"],
                        },
                        "network": {"type": "bool"},
                        "default": {"type": "bool"},
                    },
                },
                "vlan": {"type": "str"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "purged",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301