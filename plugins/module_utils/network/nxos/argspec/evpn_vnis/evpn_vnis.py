# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The arg spec for the nxos_evpn_vnis module
"""


class Evpn_vnisArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_evpn_vnis module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "vni": {"type": "int", "required": True},
                "route_distinguisher": {"type": "str"},
                "route_target_import": {"type": "list", "elements": "str"},
                "route_target_export": {"type": "list", "elements": "str"},
                "route_target_both": {"type": "list", "elements": "str"},
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
