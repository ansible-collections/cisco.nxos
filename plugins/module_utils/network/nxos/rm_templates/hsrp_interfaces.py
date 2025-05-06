# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Hsrp_interfaces parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Hsrp_interfacesTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Hsrp_interfacesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""^interface
                    (\s(?P<name>\S+))
                    $""",
                re.VERBOSE,
            ),
            "compval": "name",
            "setval": "interface {{ name }}",
            "result": {"{{ name }}": {"name": "{{ name }}"}},
            "shared": True,
        },
        {
            "name": "standby.version",
            "getval": re.compile(
                r"""
                \s*hsrp\sversion\s(?P<version>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "hsrp version {{ version|string }}",
            "result": {
                "{{ name }}": {
                    "standby": {
                        "version": "{{ version }}",
                    },
                },
            },
        },
        {
            "name": "standby.bfd",
            "getval": re.compile(
                r"""
                \s*hsrp\sbfd
                $""", re.VERBOSE,
            ),
            "setval": "hsrp bfd",
            "result": {
                "{{ name }}": {
                    "standby": {
                        "bfd": True,
                    },
                },
            },
        },
        {
            "name": "standby.delay",
            "getval": re.compile(
                r"""
                \s*hsrp\sdelay
                (\sminimum\s(?P<minimum>\d+))?
                (\sreload\s(?P<reload>\d+))?
                $""", re.VERBOSE,
            ),
            "setval": "hsrp delay"
                      "{{ ' ' + delay.minimum|string if delay.minimum is defined else ''}}"
                      "{{ ' ' + delay.reload|string if delay.reload is defined else ''}}",
            "result": {
                "{{ name }}": {
                    "standby": {
                        "delay": {
                            "minimum": "{{ minimum }}",
                            "reload": "{{ reload }}",
                        },
                    },
                },
            },
        },
        {
            "name": "standby.mac_refresh",
            "getval": re.compile(
                r"""
                \s*hsrp\smac-refresh\s(?P<mac_refresh_number>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "hsrp mac-refresh {{ mac_refresh|string }}",
            "result": {
                "{{ name }}": {
                    "standby": {
                        "mac_refresh": "{{ mac_refresh_number }}",
                    },
                },
            },
        },
        {
            "name": "standby.use_bia",
            "getval": re.compile(
                r"""
                \s*hsrp\suse-bia\sscope\sinterface
                $""", re.VERBOSE,
            ),
            "setval": "hsrp use-bia scope interface",
            "result": {
                "{{ name }}": {
                    "standby": {
                        "use_bia": {
                            "set": True,
                            "scope": True,
                        },
                    },
                },
            },
        },
        {
            "name": "group_no",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                $""", re.VERBOSE,
            ),
            "setval": "hsrp {{ grp_no|string }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "group_no": "{{ grp_no }}",
                    },
                },
            },
        },
        {
            "name": "follow",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*follow\s(?P<description>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "follow {{ follow }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "follow": "{{ description }}",
                    },
                },
            },
        },
        {
            "name": "mac_address",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*mac-address\s(?P<address>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "mac-address {{ mac_address }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "mac_address": "{{ address }}",
                    },
                },
            },
        },
        {
            "name": "group_name",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*name\s(?P<group_name>.+$)
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "group_name": "{{ group_name }}",
                    },
                },
            },
        },
    ]
    # fmt: on
