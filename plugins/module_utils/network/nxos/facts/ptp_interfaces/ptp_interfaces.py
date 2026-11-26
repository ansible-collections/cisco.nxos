# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos ptp_interfaces fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ptp_interfaces.ptp_interfaces import (
    Ptp_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ptp_interfaces import (
    Ptp_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


# the lines with an address that can be repeated
ADDRESS_LISTS = ("master", "slave")


class Ptp_interfacesFacts(object):
    """The nxos ptp_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ptp_interfacesArgs.argument_spec

    def get_config(self, connection):
        # only the interface lines and the ptp lines of the interfaces are returned
        return connection.get('show running-config | include "^interface|^  ptp"')

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Ptp_interfaces network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        # some lines are displayed with trailing spaces
        lines = [line.rstrip() for line in data.splitlines()]
        parser = Ptp_interfacesTemplate(lines=lines, module=self._module)
        objs = []
        for entry in parser.parse().values():
            # an interface without ptp lines is only a header
            if len(entry) == 1:
                continue
            for key in ADDRESS_LISTS:
                if key in entry:
                    entry[key] = sorted(entry[key])
            entry["name"] = normalize_interface(entry["name"])
            objs.append(entry)
        objs.sort(key=lambda item: item["name"])

        ansible_facts["ansible_network_resources"].pop("ptp_interfaces", None)

        params = utils.remove_empties(
            parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["ptp_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
