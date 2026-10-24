# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The Igmp_snooping parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


_VLAN_ID = "{{ vlan_id }}"
_GROUP = "{{ group }}"
_IF = "{{ interface }}"
_ENABLED = "{{ False if negate is defined else True }}"
_STATIC_GROUP = "ip igmp snooping static-group"


def _global_boolean(name, keyword):
    """Parser of a global on/off line; the device shows the no-form for a
    default-on setting and the plain form for a default-off one.
    """
    suffix = "\\s" + re.escape(keyword) if keyword else ""
    return {
        "name": name,
        "getval": re.compile("^(?P<negate>no\\s)?ip\\sigmp\\ssnooping" + suffix + "$"),
        "setval": "ip igmp snooping" + (" " + keyword if keyword else ""),
        "result": {name: _ENABLED},
    }


class Igmp_snoopingTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Igmp_snoopingTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        _global_boolean("snooping", ""),
        _global_boolean("link_local_groups_suppression", "link-local-groups-suppression"),
        _global_boolean("report_suppression", "report-suppression"),
        _global_boolean("v3_report_suppression", "v3-report-suppression"),
        _global_boolean("vxlan", "vxlan"),
        _global_boolean("disable_nve_static_router_port", "disable-nve-static-router-port"),
        {
            "name": "group_timeout",
            "getval": re.compile(
                r'''
                ^ip\sigmp\ssnooping\sgroup-timeout\s(?P<group_timeout>\d+|never)$
                ''',
                re.VERBOSE,
            ),
            "setval": "ip igmp snooping group-timeout {{ group_timeout }}",
            "result": {
                "group_timeout": "{{ group_timeout }}",
            },
        },
        {
            "name": "vlan",
            "getval": re.compile(
                r'''
                ^vlan\sconfiguration\s(?P<vlan_id>\d+)$
                ''',
                re.VERBOSE,
            ),
            "setval": "vlan configuration {{ vlan_id }}",
            "result": {
                "vlans": {
                    _VLAN_ID: {
                        "vlan_id": _VLAN_ID,
                    },
                },
            },
            "shared": True,
        },
        {
            "name": "static_group_source",
            "getval": re.compile(
                r'''
                ^\s+ip\sigmp\ssnooping\sstatic-group\s(?P<group>\S+)
                \ssource\s(?P<source>\S+)
                \sinterface\s(?P<interface>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": _STATIC_GROUP + " {{ group }} source {{ source }} interface {{ interface }}",
            "result": {
                "vlans": {
                    _VLAN_ID: {
                        "static_groups": {
                            _GROUP + "|{{ source }}": {
                                "group": _GROUP,
                                "source": "{{ source }}",
                                "interfaces": [_IF],
                            },
                        },
                    },
                },
            },
        },
        {
            "name": "static_group",
            "getval": re.compile(
                r'''
                ^\s+ip\sigmp\ssnooping\sstatic-group\s(?P<group>\S+)
                \sinterface\s(?P<interface>\S+)$
                ''',
                re.VERBOSE,
            ),
            "setval": _STATIC_GROUP + " {{ group }} interface {{ interface }}",
            "result": {
                "vlans": {
                    _VLAN_ID: {
                        "static_groups": {
                            _GROUP: {
                                "group": _GROUP,
                                "interfaces": [_IF],
                            },
                        },
                    },
                },
            },
        },
    ]
    # fmt: on
