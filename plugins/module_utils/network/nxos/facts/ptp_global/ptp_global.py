# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos ptp_global fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ptp_global.ptp_global import (
    Ptp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.ptp_global import (
    PROTECT,
    Ptp_globalTemplate,
)


class Ptp_globalFacts(object):
    """The nxos ptp_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Ptp_globalArgs.argument_spec

    def get_config(self, connection):
        # the pattern is anchored so that the lines of the interfaces are not returned
        return connection.get('show running-config | include "^ptp|^no ptp"')

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Ptp_global network resource.

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
        ptp_global_parser = Ptp_globalTemplate(lines=lines, module=self._module)
        objs = ptp_global_parser.parse()

        # remove the text that protects the scopes from being turned into numbers by the template
        for key, value in objs.get("ipv6_multicast_scope", {}).items():
            objs["ipv6_multicast_scope"][key] = value.replace(PROTECT, "", 1)

        # the template turns 10.50 into the number 10.5, the device shows two decimals
        for key, value in objs.get("delay_tolerance", {}).items():
            objs["delay_tolerance"][key] = "{0:.2f}".format(float(value))

        ansible_facts["ansible_network_resources"].pop("ptp_global", None)

        params = utils.remove_empties(
            ptp_global_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["ptp_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
