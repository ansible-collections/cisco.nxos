# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The nxos_pim_global fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.pim_global.pim_global import (
    Pim_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.pim_global import (
    Pim_globalTemplate,
)


class Pim_globalFacts(object):
    """The nxos_pim_global fact class."""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Pim_globalArgs.argument_spec

    def get_pim_global_data(self, connection):
        """Get the global PIM configuration."""

        return connection.get("show running-config | include '^ip pim '")

    def populate_facts(self, connection, ansible_facts, data=None):
        """
        Populate the facts for the pim_global network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_pim_global_data(connection)

        pim_global_parser = Pim_globalTemplate(lines=data.splitlines(), module=self._module)
        obj = pim_global_parser.parse()

        self._post_parse(obj)
        obj = utils.remove_empties(obj)

        ansible_facts["ansible_network_resources"].pop("pim_global", None)
        params = utils.remove_empties(
            pim_global_parser.validate_config(self.argument_spec, {"config": obj}, redact=True),
        )

        facts["pim_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    @staticmethod
    def _post_parse(obj):
        """
        Converts the intermediate data structure
        to valid format as per argspec.

        :param obj: dict
        """
        rps = obj.get("rp_addresses")
        if rps:
            obj["rp_addresses"] = sorted(
                rps.values(),
                key=lambda k: (
                    k["rp_address"],
                    k.get("group_list") or k.get("prefix_list") or k.get("route_map") or "",
                ),
            )
        anycast = obj.get("anycast_rps")
        if anycast:
            for entry in anycast.values():
                entry["members"] = sorted(entry["members"])
            obj["anycast_rps"] = sorted(anycast.values(), key=lambda k: k["anycast_rp"])
