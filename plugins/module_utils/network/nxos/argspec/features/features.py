# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The arg spec for the nxos_features module."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class FeaturesArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_features module."""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "enabled": {"type": "bool", "default": True},
            },
        },
        "state": {
            "type": "str",
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
        },
    }
