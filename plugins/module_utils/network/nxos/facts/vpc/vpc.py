# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos vpc fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.vpc.vpc import (
    VpcArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.vpc import (
    VpcTemplate,
)


class VpcFacts(object):
    """The nxos vpc facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = VpcArgs.argument_spec

    def get_config(self, connection):
        return connection.get("show running-config | section '^vpc domain'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Vpc network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        vpc_parser = VpcTemplate(lines=data.splitlines(), module=self._module)
        parsed = vpc_parser.parse()

        # single-instance resource: take the first (and only) domain entry
        objs = list(parsed.values())[0] if parsed else {}

        # remove any unmatched optional regex groups rendered as the string "None"
        objs = {k: v for k, v in objs.items() if v not in (None, "", "None")}

        ansible_facts["ansible_network_resources"].pop("vpc", None)

        params = utils.remove_empties(
            vpc_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["vpc"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
