# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos netflow_interfaces fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.netflow_interfaces.netflow_interfaces import (
    Netflow_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.netflow_interfaces import (
    Netflow_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


PROTOCOLS = ("ipv4", "ipv6", "layer2_switched")
DIRECTIONS = ("input", "output")


class Netflow_interfacesFacts(object):
    """The nxos netflow_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Netflow_interfacesArgs.argument_spec

    def get_config(self, connection):
        # only the interface lines and the flow monitor lines of the interfaces are returned
        return connection.get(
            'show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"',
        )

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Netflow_interfaces network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        lines = [line.rstrip() for line in data.splitlines()]
        parser = Netflow_interfacesTemplate(lines=lines, module=self._module)
        objs = []
        for entry in parser.parse().values():
            # an interface without flow monitors is only a header
            if "flow_monitors" not in entry:
                continue
            entry["name"] = normalize_interface(entry["name"])
            entry["flow_monitors"] = sorted(
                entry["flow_monitors"].values(),
                key=lambda item: (
                    PROTOCOLS.index(item["protocol"]),
                    DIRECTIONS.index(item["direction"]),
                ),
            )
            objs.append(entry)
        objs.sort(key=lambda item: item["name"])

        ansible_facts["ansible_network_resources"].pop("netflow_interfaces", None)

        params = utils.remove_empties(
            parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["netflow_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
