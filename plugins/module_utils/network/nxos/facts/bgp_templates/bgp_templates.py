# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos bgp_templates fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_templates.bgp_templates import (
    Bgp_templatesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.bgp_templates import (
    Bgp_templatesTemplate,
)


class Bgp_templatesFacts(object):
    """The nxos bgp_templates facts class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Bgp_templatesArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config bgp | section 'template'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bgp_templates network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        data = self._flatten_config(data)

        # parse native config using the Bgp_templates template
        bgp_templates_parser = Bgp_templatesTemplate(lines=data, module=self._module)
        parsed = bgp_templates_parser.parse()

        objs = {}
        # pop top-level keys and assign values to them
        for k, v in iteritems(parsed):
            objs[k] = list(v.values())

        ansible_facts["ansible_network_resources"].pop("bgp_templates", None)

        params = utils.remove_empties(
            bgp_templates_parser.validate_config(self.argument_spec, {"config": objs}, redact=True),
        )

        facts["bgp_templates"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _flatten_config(self, data):
        flattened_data = []
        cur_peer = ""
        data = data.split("\n")

        for x in data:
            x = x.strip()
            if x.startswith("template peer"):
                cur_peer = x + " "
            elif x.startswith("address-family"):
                # a template peer <> line has to preceed AF line
                x = cur_peer + x
            flattened_data.append(x)

        return flattened_data
