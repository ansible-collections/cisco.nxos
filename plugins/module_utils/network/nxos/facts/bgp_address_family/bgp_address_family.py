# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos bgp_address_family fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_address_family.bgp_address_family import (
    Bgp_address_familyArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.bgp_address_family import (
    Bgp_address_familyTemplate,
)


class Bgp_address_familyFacts(object):
    """The nxos bgp_address_family facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Bgp_address_familyArgs.argument_spec

    def get_config(self, connection):
        """Wrapper method for `connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return connection.get("show running-config | section '^router bgp'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Bgp_address_family network resource

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

        data = self._flatten_config(data)

        # parse native config using the Bgp_address_family template
        bgp_address_family_parser = Bgp_address_familyTemplate(lines=data.splitlines())
        objs = bgp_address_family_parser.parse()
        if objs:
            nbr = []
            if "address_family" in objs:
                # remove neighbor AF entries
                for k, v in objs["address_family"].items():
                    if not k.startswith("nbr_"):
                        nbr.append(k)
                for x in nbr:
                    del objs["address_family"][x]

                objs["address_family"] = list(objs["address_family"].values())
                # sort list of dictionaries
                for x in objs["address_family"]:
                    if "aggregate_address" in x:
                        x["aggregate_address"] = sorted(
                            x["aggregate_address"],
                            key=lambda k, s="prefix": k[s],
                        )
                    if "networks" in x:
                        x["networks"] = sorted(x["networks"], key=lambda k, s="prefix": k[s])
                    if "redistribute" in x:
                        x["redistribute"] = sorted(
                            x["redistribute"],
                            key=lambda k: (k.get("id", -1), k["protocol"]),
                        )
                objs["address_family"] = sorted(
                    objs["address_family"],
                    key=lambda k: (
                        k.get("afi", ""),
                        k.get("safi", ""),
                        k.get("vrf", ""),
                    ),
                )

        ansible_facts["ansible_network_resources"].pop("bgp_address_family", None)

        params = utils.remove_empties(utils.validate_config(self.argument_spec, {"config": objs}))

        facts["bgp_address_family"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts

    def _flatten_config(self, data):
        """Flatten contexts in the BGP
            running-config for easier parsing.
        :param data: str running config
        :returns: flattened running config
        """
        lines = data.split("\n")
        cur_vrf = None
        cur_nbr = None
        cur_template = None

        for index, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            cur_indent = len(line) - len(line.lstrip())

            if stripped.startswith("template peer"):
                cur_template = {"line": line, "indent": cur_indent}
                cur_nbr = None
                continue
            if (
                cur_template is not None
                and cur_indent <= cur_template["indent"]
                and not stripped.startswith(("address-family", "neighbor"))
            ):
                cur_template = None
            if cur_template is not None:
                lines[index] = cur_template["line"] + " " + stripped
                continue

            if stripped.startswith("vrf "):
                cur_vrf = {"line": line, "indent": cur_indent}
                cur_nbr = None
                continue
            if (
                cur_vrf is not None
                and cur_indent <= cur_vrf["indent"]
                and not stripped.startswith(("address-family", "neighbor"))
            ):
                cur_vrf = None
                cur_nbr = None
            if stripped.startswith("neighbor"):
                cur_nbr = {"line": line, "indent": cur_indent}
                continue
            if (
                cur_nbr is not None
                and cur_indent <= cur_nbr["indent"]
                and not stripped.startswith("address-family")
            ):
                cur_nbr = None
            if stripped.startswith("address-family"):
                prepend = ""
                if cur_vrf is not None:
                    prepend += cur_vrf["line"]
                if cur_nbr is not None:
                    prepend += (" " if prepend else "") + cur_nbr["line"].strip()
                if prepend:
                    lines[index] = prepend + " " + stripped

        return "\n".join(lines)
