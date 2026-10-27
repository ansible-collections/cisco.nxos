# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos evpn_vnis fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.evpn_vnis.evpn_vnis import (
    Evpn_vnisArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.evpn_vnis import (
    Evpn_vnisTemplate,
)


class Evpn_vnisFacts(object):
    """The nxos evpn_vnis facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Evpn_vnisArgs.argument_spec

    def get_config(self, connection):
        return connection.get("show running-config | section '^evpn'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Evpn_vnis network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        evpn_vnis_parser = Evpn_vnisTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = list(evpn_vnis_parser.parse().values())

        # the parser merges lists as sets, sort them for a stable output
        for obj in objs:
            for key in ("route_target_import", "route_target_export"):
                if key in obj:
                    obj[key] = sorted(obj[key])

        ansible_facts["ansible_network_resources"].pop("evpn_vnis", None)

        params = utils.remove_empties(
            evpn_vnis_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["evpn_vnis"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
