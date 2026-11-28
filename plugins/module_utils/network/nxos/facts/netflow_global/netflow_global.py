# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos netflow_global fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import utils

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.netflow_global.netflow_global import (
    Netflow_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.netflow_global import (
    IGNORED,
    PROTECT,
    SECTIONS,
    Netflow_globalTemplate,
)


def _unprotect(value):
    """Remove the text that keeps the template from turning a text into a number."""
    if isinstance(value, dict):
        return dict((key, _unprotect(item)) for key, item in value.items())
    if isinstance(value, list):
        return [_unprotect(item) for item in value]
    if isinstance(value, str) and value.startswith(PROTECT):
        return value.replace(PROTECT, "", 1)
    return value


class Netflow_globalFacts(object):
    """The nxos netflow_global facts class"""

    def __init__(self, module, subspec="config", options="options"):
        self._module = module
        self.argument_spec = Netflow_globalArgs.argument_spec

    def get_config(self, connection):
        # the flow commands only exist when `feature netflow` is enabled
        return connection.get("show running-config | section ^flow")

    @staticmethod
    def _split(data):
        """The lines of the running configuration of each section, the lines of the
        devices that use CRLF or add trailing spaces are accepted.
        """
        blocks = dict((section, []) for section in SECTIONS)
        blocks["global"] = []
        current = "global"
        for line in data.splitlines():
            if not line.strip():
                continue
            if not line.startswith(" "):
                current = "global"
                for section in SECTIONS:
                    if line.startswith("flow {0} ".format(section)):
                        current = section
            blocks[current].append(line.rstrip())
        return blocks

    def populate_facts(self, connection, ansible_facts, data=None):
        """Populate the facts for Netflow_global network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_config(connection)

        blocks = self._split(data)
        objs = {}
        unparsed = []
        for section, lines in blocks.items():
            parser = Netflow_globalTemplate(lines=lines, module=self._module, section=section)
            objs.update(parser.parse())
            unparsed.extend(
                line
                for line in lines
                if not IGNORED.match(line)
                and not any(re.match(p["getval"], line) for p in parser.PARSERS)
            )
        if unparsed:
            self._module.warn(
                "these lines of the running configuration are not managed by the module and ignored: {0}".format(
                    "; ".join(line.strip() for line in unparsed),
                ),
            )

        for monitor in objs.get("monitors", {}).values():
            if "exporter_names" in monitor:
                monitor["exporters"] = [_unprotect(name) for name in monitor.pop("exporter_names")]
        objs = _unprotect(objs)
        for key in ("exporters", "records", "monitors"):
            if key in objs:
                objs[key] = list(objs[key].values())

        ansible_facts["ansible_network_resources"].pop("netflow_global", None)

        params = utils.remove_empties(
            Netflow_globalTemplate(module=self._module).validate_config(
                self.argument_spec,
                {"config": objs},
                redact=True,
            ),
        )

        facts["netflow_global"] = params.get("config", {})
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
