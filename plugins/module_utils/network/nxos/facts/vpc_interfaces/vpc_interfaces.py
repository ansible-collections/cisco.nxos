# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos vpc_interfaces fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.vpc_interfaces.vpc_interfaces import (
    Vpc_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.vpc_interfaces import (
    Vpc_interfacesTemplate,
)


class Vpc_interfacesFacts(object):
    """The nxos vpc_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Vpc_interfacesArgs.argument_spec

    def get_config(self, connection):
        return connection.get("show running-config | section '^interface'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vpc_interfaces network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        vpc_interfaces_parser = Vpc_interfacesTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        parsed = vpc_interfaces_parser.parse()

        # Only include interfaces that have vpc-related configuration
        objs = [
            entry
            for entry in parsed.values()
            if entry.get("vpc") or entry.get("peer_link") or entry.get("orphan_port_suspend")
        ]

        ansible_facts["ansible_network_resources"].pop("vpc_interfaces", None)

        params = utils.remove_empties(
            vpc_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["vpc_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
