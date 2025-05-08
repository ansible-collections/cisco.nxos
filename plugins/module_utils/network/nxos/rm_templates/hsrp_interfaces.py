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
        {
            "name": "ip",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*ip\s(?P<ipv4>\S+)
                (\s(?P<secondary>secondary))?
                $""", re.VERBOSE,
            ),
            "setval": "ip {{ virtual_ip }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "ip": [
                            {
                                "virtual_ip": "{{ ipv4 }}",
                                "secondary": "{{ not not secondary }}",
                            },
                        ],
                    },
                },
            },
        },
        {
            "name": "preempt",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*preempt\sdelay
                (\sminimum\s(?P<minimum>\d+))
                (\sreload\s(?P<reload>\d+))
                (\ssync\s(?P<sync>\d+))
                (\s(?P<delay>delay))?
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "preempt": {
                            "set": True,
                            "minimum": "{{ minimum }}",
                            "reload": "{{ reload }}",
                            "sync": "{{ sync }}",
                            "delay": "{{ not not delay }}",
                        },
                    },
                },
            },
        },
        {
            "name": "priority",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*priority\s(?P<priority>\d+)
                (\sforwarding-threshold\slower\s(?P<lower>\d+))
                (\supper\s(?P<upper>\d+))
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "priority": {
                            "level": "{{ priority }}",
                            "upper": "{{ upper }}",
                            "lower": "{{ lower }}",
                        },
                    },
                },
            },
        },
        {
            "name": "timer",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*timers
                (\s*(?P<msec>msec))?
                (\s*(?P<hello_interval>\d+))
                (\s*(?P<hold_time>\d+))
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "timer": {
                            "msec": "{{ not not msec }}",
                            "hello_interval": "{{ hello_interval }}",
                            "hold_time": "{{ hold_time }}",
                        },
                    },
                },
            },
        },
        {
            "name": "track",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*track
                (\s*(?P<object_no>\d+))
                (\s*decrement\s(?P<decrement>\d+))
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "track": [{
                            "object_no": "{{ object_no }}",
                            "decrement": "{{ decrement }}",
                        }],
                    },
                },
            },
        },
        {
            "name": "authentication",
            "getval": re.compile(
                r"""
                \s*hsrp\s(?P<grp_no>\d+)
                \s*authentication
                (\stext\s(?P<password_text>\S+))?
                (\smd5\skey-chain\s(?P<key_chain>\S+))?
                (\smd5\skey-string\s(?P<key_string>\S+))?
                $""", re.VERBOSE,
            ),
            "setval": "name {{ group_name }}",
            "result": {
                "{{ name }}": {
                    "group_{{ grp_no|string }}": {
                        "authentication": {
                            "key_chain": "{{ key_chain }}",
                            "key_string": "{{ key_string }}",
                            "password_text": "{{ password_text }}",
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
