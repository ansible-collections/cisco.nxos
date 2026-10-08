# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.interfaces import (
    InterfacesTemplate,
)


class InterfacesFacts(object):
    """The nxos interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = InterfacesArgs.argument_spec

    def _get_interface_config(self, connection):
        return connection.get("show running-config | section ^interface")

    def _add_default_svi_shutdown(self, data):
        """
        Add shutdown to Vlan interfaces that don't mention an admin state,
        as NX-OS only writes 'no shutdown' for SVIs explicitly brought up
        :param obj: data
        :returns: running-config with the default SVI admin state made explicit
        """
        regex_svi_block = re.compile(r"(?m)^(interface Vlan\S+\n)((?:[ \t]+.*\n?)*)")
        regex_admin_state = re.compile(r"(?m)^[ \t]+(?:no[ \t]+)?shutdown[ \t]*$")

        def add_shutdown(match):
            interface, config = match.group(1), match.group(2)
            if regex_admin_state.search(config):
                return interface + config
            return interface + "  shutdown\n" + config

        return regex_svi_block.sub(add_shutdown, data)

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Interfaces network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self._get_interface_config(connection)

        data = self._add_default_svi_shutdown(data)

        # parse native config using the Interfaces template
        interfaces_parser = InterfacesTemplate(lines=data.splitlines(), module=self._module)
        objs = list(interfaces_parser.parse().values())
        ansible_facts["ansible_network_resources"].pop("interfaces", None)
        facts = {"interfaces": []}
        params = utils.remove_empties(
            interfaces_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["interfaces"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
