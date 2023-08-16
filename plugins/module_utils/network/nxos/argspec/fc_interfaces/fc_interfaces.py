# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
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
The arg spec for the nxos_fc_interfaces module
"""
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.fc_interfaces import (
    allowed_speed_values,
)


class Fc_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the nxos_fc_interfaces module"""

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "description": {"type": "str"},
                "enabled": {"type": "bool"},
                "speed": {
                    "choices": allowed_speed_values,
                    "type": "str",
                },
                "mode": {
                    "choices": ["auto", "E", "F", "Fx", "NP", "SD"],
                    "type": "str",
                },
                "trunk_mode": {"choices": ["auto", "on", "off"], "type": "str"},
                "analytics": {
                    "choices": ["fc-scsi", "fc-nvme", "fc-all"],
                    "type": "str",
                },
            },
        },
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
                "purged",
            ],
            "default": "merged",
        },
    }  # pylint: disable=C0301
