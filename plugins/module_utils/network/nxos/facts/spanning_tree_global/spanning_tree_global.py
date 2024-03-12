# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos spanning_tree_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.spanning_tree_global.spanning_tree_global import (
    Spanning_tree_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.spanning_tree_global import (
    Spanning_tree_globalTemplate,
)


class Spanning_tree_globalFacts(object):
    """The nxos spanning_tree_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Spanning_tree_globalArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        summary = connection.get("show spanning-tree summary")
        general = connection.get("show running-config spanning-tree")
        return summary + general

    def _convert_to_str(self, config_list, key_name):
        """Convert range values to strings
        """

        for obj in config_list:
            if isinstance(obj.get(key_name), list) or isinstance(obj.get(key_name), tuple):
                vals = [str(x) for x in obj[key_name]]
                obj[key_name] = ",".join(vals)
            if isinstance(obj.get(key_name), int):
                obj[key_name] = str(obj[key_name])
        return config_list

    def _dict_to_list(self, objs):
        """Convert a dict to a list of dicts
        """ 

        mst_obj = objs.get("mst", {})
        configure_mst_obj = mst_obj.get("configure_mst", {})
        instance_vlan_obj = configure_mst_obj.get("instance_vlan", {})

        if instance_vlan_obj:
            objs["mst"]["configure_mst"]["instance_vlan"] = list(instance_vlan_obj.values())
            objs["mst"]["configure_mst"]["instance_vlan"] = self._convert_to_str(
                objs["mst"]["configure_mst"]["instance_vlan"], "vlan_range"
            )
    
        pseudo_obj = objs.get("pseudo_info", {})
        pseudo_mst_obj = pseudo_obj.get("mst_info", {})
        pseudo_vlan_obj = pseudo_obj.get("vlan_info", {})

        if pseudo_mst_obj:
            objs["pseudo_info"]["mst_info"] = list(pseudo_mst_obj.values())
            objs["pseudo_info"]["mst_info"] = self._convert_to_str(objs["pseudo_info"]["mst_info"], "range")
        
        if pseudo_vlan_obj:
            objs["pseudo_info"]["vlan_info"] = list(pseudo_vlan_obj.values())
            objs["pseudo_info"]["vlan_info"] = self._convert_to_str(objs["pseudo_info"]["vlan_info"], "range")

        if "vlan" in objs:
            objs["vlan"] = list(objs["vlan"].values())
            objs["vlan"] = self._convert_to_str(objs["vlan"], "vlan_range")

        return objs

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Spanning_tree_global network resource

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

        # parse native config using the Spanning_tree_global template
        spanning_tree_global_parser = Spanning_tree_globalTemplate(
            lines=data.splitlines(),
            module=self._module,
        )
        objs = spanning_tree_global_parser.parse()

        facts_output = self._dict_to_list(objs)

        ansible_facts["ansible_network_resources"].pop("spanning_tree_global", None)

        params = utils.remove_empties(
            spanning_tree_global_parser.validate_config(
                self.argument_spec,
                {"config": facts_output},
                redact=True,
            ),
        )

        facts["spanning_tree_global"] = params["config"]
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
