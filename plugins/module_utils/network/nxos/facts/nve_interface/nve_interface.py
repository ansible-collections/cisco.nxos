# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos nve_interface fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.nve_interface.nve_interface import (
    Nve_interfaceArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.nve_interface import (
    Nve_interfaceTemplate,
)


class Nve_interfaceFacts(object):
    """The nxos_nve_interface fact class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Nve_interfaceArgs.argument_spec

    def get_nve_interface_data(self, connection):
        """Wrapper method for `connection.get()`
        This exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section '^interface nve1'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for nve_interface network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_nve_interface_data(connection)

        data = self._flatten_config(data)

        # Parse native config using the Nve_interface template
        nve_interface_parser = Nve_interfaceTemplate(lines=data.splitlines(), module=self._module)
        obj = nve_interface_parser.parse()

        self._post_parse(obj)
        obj = utils.remove_empties(obj)

        ansible_facts["ansible_network_resources"].pop("nve_interface", None)
        params = utils.remove_empties(
            nve_interface_parser.validate_config(self.argument_spec, {"config": obj}, redact=True),
        )

        facts["nve_interface"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _flatten_config(self, data):
        """Flatten vni contexts
        in the running-config for easier parsing.
        :param obj: dict
        :returns: flattended running config
        """
        data = data.split("\n")
        in_vni_cxt = False
        cur_vni = {}

        for x in data:
            cur_indent = len(x) - len(x.lstrip())
            if x.strip().startswith("member vni"):
                in_vni_cxt = True
                cur_vni["vni"] = x
                cur_vni["indent"] = cur_indent
            elif cur_vni and (cur_indent <= cur_vni["indent"]):
                in_vni_cxt = False
            elif in_vni_cxt:
                data[data.index(x)] = cur_vni["vni"] + " " + x.strip()

        return "\n".join(data)

    def _post_parse(self, obj):
        """Converts the intermediate data structure
           to valid format as per argspec.
        :param obj: dict
        """
        vnis = obj.get("vnis", [])
        if vnis:
            obj["vnis"] = sorted(
                list(vnis.values()),
                key=lambda k, sk="vni_id": k[sk],
            )
