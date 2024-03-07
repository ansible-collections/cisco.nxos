# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos hostname fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.hostname.hostname import (
    HostnameArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.hostname import (
    HostnameTemplate,
)


class HostnameFacts(object):
    """The nxos hostname facts class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = HostnameArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section ^hostname")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Hostname network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = self.get_config(connection)

        # parse native config using the Hostname template
        hostname_parser = HostnameTemplate(lines=data.splitlines(), module=self._module)
        objs = hostname_parser.parse()

        ansible_facts["ansible_network_resources"].pop("hostname", None)

        params = utils.remove_empties(
            hostname_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["hostname"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
