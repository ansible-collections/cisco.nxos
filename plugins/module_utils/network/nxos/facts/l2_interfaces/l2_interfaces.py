# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos l2_interfaces fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""
import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.l2_interfaces import (
    L2_interfacesTemplate,
)


class L2_interfacesFacts(object):
    """The nxos l2_interfaces facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = L2_interfacesArgs.argument_spec

    def _get_interface_config(self, connection):
        return connection.get("show running-config | section ^interface")

    def _default_for_allowed_vlans(self, parsed_config):
        """Handle default for allowed vlans"""

        # Process allowed_vlans
        for interface in parsed_config:
            # if trunk and allowed vlan is empty then apply default
            # check if ...allowed vlan none command is not there
            # if vlan none command is there then don't apply default
            if interface.get("trunk"):
                if not interface.get("trunk", {}).get("allowed_vlans") and not interface.get(
                    "trunk",
                    {},
                ).get("allowed_vlans_none"):
                    interface["trunk"]["allowed_vlans"] = "1-4094"

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for L2_interfaces network resource

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

        data = self._flatten_vlans(data)

        # parse native config using the L2_interfaces template
        l2_interfaces_parser = L2_interfacesTemplate(lines=data.splitlines(), module=self._module)
        objs = list(l2_interfaces_parser.parse().values())

        # process defaults for allowed vlan
        self._default_for_allowed_vlans(objs)

        ansible_facts["ansible_network_resources"].pop("l2_interfaces", None)

        params = utils.remove_empties(
            l2_interfaces_parser.validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["l2_interfaces"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _flatten_vlans(self, data):
        """
        Flatten the vlan lines if it also contains lines that mention 'switchport trunk allowed vlan add'
        as we will merge all the entries in a list
        :param obj: data
        :returns: flattened vlan entries as switchport trunk allowed vlan
        """
        lines = data.split("\n")
        vlans = ""
        cur_indent = 0
        result = []
        for line_index in range(len(lines)):
            line = str(lines[line_index])
            # If line starts with one of these entries, that is special one liner entry
            if re.match(r"\s+switchport\strunk\sallowed\svlan\s(none|all|except|remove)", line):
                result.append(line)

            # If line starts with  allowed vlan add
            elif re.match(r"\s+switchport\strunk\sallowed\svlan\sadd", line):
                if vlans:
                    vlans += "," + line.rsplit("add", maxsplit=1)[-1].strip()
                else:
                    vlans = line.rsplit("add", maxsplit=1)[-1].strip()
                cur_indent = len(line) - len(line.lstrip())

            # If line starts only with allowed vlan
            elif re.match(r"\s+switchport\strunk\sallowed\svlan", line):
                vlans = line.rsplit("vlan", maxsplit=1)[-1].strip()
                cur_indent = len(line) - len(line.lstrip())

            else:
                if vlans:
                    result.append(f"{' ' * cur_indent}switchport trunk allowed vlan {vlans}")
                    vlans = ""
                result.append(line)

        if vlans:
            result.append(f"{' ' * cur_indent}switchport trunk allowed vlan {vlans}")

        return "\n".join(result)
