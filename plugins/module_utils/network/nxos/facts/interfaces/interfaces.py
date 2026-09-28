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
        """Make the default shutdown state of SVIs explicit.

        NX-OS omits the admin state from `show running-config` for SVIs that
        are in their default shutdown state; only `no shutdown` is written, for
        SVIs explicitly brought up. Without this, a default-shutdown SVI is
        indistinguishable from an enabled one and gets reported as
        `enabled: true`.

        Inject `shutdown` into any `interface VlanXXX` block that declares
        neither `shutdown` nor `no shutdown`, so the template parses it as
        `enabled: false`.

        :param data: running-config to preprocess
        :returns: running-config with SVI admin state made explicit
        """
        svi_block = re.compile(r"(?m)^(interface Vlan\S+\n)((?:[ \t]+.*\n?)*)")
        admin_state = re.compile(r"(?m)^[ \t]+(?:no[ \t]+)?shutdown[ \t]*$")

        def _inject(match):
            header, body = match.group(1), match.group(2)
            if admin_state.search(body):
                return header + body
            return header + "  shutdown\n" + body

        return svi_block.sub(_inject, data)

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
