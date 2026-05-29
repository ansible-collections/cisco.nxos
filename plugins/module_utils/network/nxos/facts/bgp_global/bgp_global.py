# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos bgp_global fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_global.bgp_global import (
    Bgp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)


class Bgp_globalFacts(object):
    """The nxos bgp_global facts class"""

    def __init__(self, module):
        self._module = module
        self.argument_spec = Bgp_globalArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section '^router bgp'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bgp_global network resource

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

        # parse native config using the Bgp_global template
        bgp_global_parser = Bgp_globalTemplate(lines=data.splitlines(), module=self._module)
        obj = bgp_global_parser.parse()

        vrfs = obj.get("vrfs", {})

        # move global vals to their correct position in facts tree
        # this is only needed for keys that are valid for both global
        # and VRF contexts
        global_vals = vrfs.pop("vrf_", {})
        for key, value in global_vals.items():
            obj[key] = value

        # transform vrfs into a list
        if vrfs:
            obj["vrfs"] = sorted(list(obj["vrfs"].values()), key=lambda k, sk="vrf": k[sk])
            for vrf in obj["vrfs"]:
                self._post_parse(vrf)

        self._post_parse(obj)

        obj = utils.remove_empties(obj)

        ansible_facts["ansible_network_resources"].pop("bgp_global", None)
        params = utils.remove_empties(
            bgp_global_parser.validate_config(self.argument_spec, {"config": obj}, redact=True),
        )

        facts["bgp_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _flatten_config(self, data):
        """Flatten neighbor contexts in
            the running-config for easier parsing.
            Also filters out template peer configurations.
        :param obj: dict
        :returns: flattened running config
        """
        data = data.split("\n")
        in_nbr_cxt = False
        in_template_cxt = False
        cur_nbr = {}
        cur_template = {}
        filtered_data = []

        for x in data:
            cur_indent = len(x) - len(x.lstrip())

            # Skip template peer* blocks - they are managed by nxos_bgp_templates
            if x.strip().startswith("template peer"):
                in_template_cxt = True
                cur_template["indent"] = cur_indent
                continue
            elif in_template_cxt and cur_template and (cur_indent <= cur_template["indent"]):
                in_template_cxt = False
                cur_template = {}
            elif in_template_cxt:
                # Skip all lines within the template block
                continue

            # Handle neighbor context flattening
            if x.strip().startswith("neighbor"):
                in_nbr_cxt = True
                cur_nbr["nbr"] = x
                cur_nbr["indent"] = cur_indent
            elif cur_nbr and (cur_indent <= cur_nbr["indent"]):
                in_nbr_cxt = False
            elif in_nbr_cxt:
                filtered_data.append(cur_nbr["nbr"] + " " + x.strip())
                continue

            filtered_data.append(x)

        return "\n".join(filtered_data)

    def _post_parse(self, obj):
        """Converts the intermediate data structure
            to valid format as per argspec.
        :param obj: dict
        """
        conf_peers = obj.get("confederation", {}).get("peers")
        if conf_peers:
            obj["confederation"]["peers"] = conf_peers.split()
            obj["confederation"]["peers"].sort()

        neighbors = obj.get("neighbors", {})
        if neighbors:
            obj["neighbors"] = sorted(
                list(neighbors.values()),
                key=lambda k, sk="neighbor_address": k[sk],
            )
