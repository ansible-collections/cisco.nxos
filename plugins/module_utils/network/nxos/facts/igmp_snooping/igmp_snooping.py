# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos igmp_snooping fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.igmp_snooping.igmp_snooping import (
    Igmp_snoopingArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.igmp_snooping import (
    Igmp_snoopingTemplate,
)


# Settings that NX-OS leaves out of the running-config while they have this
# value, the facts report them anyway so that gathered returns what is in effect.
GLOBAL_DEFAULTS = {
    "snooping": True,
    "link_local_groups_suppression": True,
    "report_suppression": True,
    "v3_report_suppression": False,
    "vxlan": False,
    "disable_nve_static_router_port": False,
}

_VLAN_HEADER = re.compile(r"^vlan\sconfiguration\s\d+$")


def _ip_key(address):
    """Sort key for a dotted address, ordering numerically."""
    return tuple(int(octet) if octet.isdigit() else -1 for octet in address.split("."))


def _relevant_lines(data):
    """Keep what the parser can attribute safely: top-level lines and the
    lines of a `vlan configuration <id>` block.

    The global `include` output carries the indented lines of the VLAN blocks
    without their header, and a block with a header that is not a single VLAN
    id is not managed, so both are dropped instead of being credited to the
    wrong VLAN.
    """
    keep = []
    in_block = False
    for line in data.splitlines():
        if line and not line[0].isspace():
            in_block = bool(_VLAN_HEADER.match(line))
            if not line.startswith("vlan configuration") or in_block:
                keep.append(line)
        elif in_block:
            keep.append(line)
    return keep


class Igmp_snoopingFacts(object):
    """The nxos igmp_snooping facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Igmp_snoopingArgs.argument_spec

    def get_config(self, connection):
        vlans = connection.get('show running-config | section "^vlan configuration"')
        global_cfg = connection.get('show running-config | include "ip igmp snooping"')
        return "\n".join([global_cfg or "", vlans or ""])

    @staticmethod
    def _vlan_list(vlans):
        """Turn the parsed mappings into the argspec lists, in a stable order."""
        result = []
        for vlan_id in sorted(vlans):
            vlan = vlans[vlan_id]
            groups = sorted(
                vlan.get("static_groups", {}).values(),
                key=lambda grp: (_ip_key(grp["group"]), _ip_key(grp.get("source", ""))),
            )
            for group in groups:
                group["interfaces"] = sorted(group["interfaces"])
            if groups:
                vlan["static_groups"] = groups
            result.append(vlan)
        return result

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Igmp_snooping network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        parser = Igmp_snoopingTemplate(lines=_relevant_lines(data), module=self._module)
        objs = parser.parse()

        config = dict(GLOBAL_DEFAULTS)
        config.update(objs)
        vlans = self._vlan_list(config.pop("vlans", {}))
        if vlans:
            config["vlans"] = vlans

        ansible_facts["ansible_network_resources"].pop("igmp_snooping", None)

        params = utils.remove_empties(
            parser.validate_config(self.argument_spec, {"config": config}, redact=True),
        )

        facts["igmp_snooping"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
