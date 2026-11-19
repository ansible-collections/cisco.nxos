# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The nxos_features fact class.
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.features.features import (
    FeaturesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.features import (
    FeaturesTemplate,
)


class FeaturesFacts(object):
    """The nxos_features fact class."""

    def __init__(self, module):
        self._module = module
        self.argument_spec = FeaturesArgs.argument_spec

    def get_features_data(self, connection):
        """
        Get the feature commands of the running configuration.

        The all keyword is needed, the plain running configuration hides the features that are
        enabled by default, for example ssh.
        """

        return connection.get("show running-config all | include '^feature|^no feature'")

    def populate_facts(self, connection, ansible_facts, data=None):
        """
        Populate the facts for the features network resource.

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}

        if not data:
            data = self.get_features_data(connection)

        features_parser = FeaturesTemplate(lines=data.splitlines(), module=self._module)
        obj = features_parser.parse()

        obj = sorted(obj.values(), key=lambda k: k["name"])

        ansible_facts["ansible_network_resources"].pop("features", None)
        params = utils.remove_empties(
            features_parser.validate_config(self.argument_spec, {"config": obj}, redact=True),
        )

        facts["features"] = params.get("config", [])
        ansible_facts["ansible_network_resources"].update(facts)

        return ansible_facts
