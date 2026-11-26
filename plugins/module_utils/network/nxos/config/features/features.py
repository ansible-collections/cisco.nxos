# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The nxos_features config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.features import (
    FeaturesTemplate,
)


class Features(ResourceModule):
    """The nxos_features config class."""

    def __init__(self, module):
        super().__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="features",
            tmplt=FeaturesTemplate(),
        )

    def execute_module(self):
        """Execute the module."""

        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def get_plain_features(self):
        """
        Get the feature lines of the plain running configuration.

        The plain running configuration only shows the features that were changed from their
        default, a feature that is enabled by default, for example ssh, is not in it. The facts
        use the all view, so they cannot tell the two apart.
        """

        return self._connection.get("show running-config | include '^feature'")

    def _explicit_features(self):
        """The names of the features that have a feature line in the plain running configuration."""

        names = set()
        for line in self.get_plain_features().splitlines():
            match = re.match(r"^feature\s+(\S.*?)\s*$", line)
            if match:
                names.add(match.group(1))
        return names

    def generate_commands(self):
        """
        Generate configuration commands to send based on
        want, have and desired state.

        The features are compared by name. The commands that enable a feature are sent in the
        order of the configuration, the commands that disable a feature after them and in the
        reverse order of the configuration, so that a feature that depends on another one is
        disabled first.

        The states overridden and deleted without config return the features to their default.
        They only disable the features that have a feature line in the plain running
        configuration, the features that are enabled by default are left alone. A feature that is
        listed is always set as given.
        """
        wantd = self._normalize(self.want)
        haved = self._normalize(self.have)

        enable = []
        disable = []

        if self.state in ["merged", "replaced", "overridden"]:
            for name, enabled in wantd.items():
                if enabled and haved.get(name) is not True:
                    enable.append(name)
                elif not enabled and haved.get(name) is True:
                    disable.append(name)
            disable.reverse()
            if self.state == "overridden":
                explicit = self._explicit_features()
                disable.extend(
                    name
                    for name, enabled in haved.items()
                    if enabled and name not in wantd and name in explicit
                )
        elif self.state == "deleted":
            if self.want:
                disable.extend(name for name in reversed(list(wantd)) if haved.get(name) is True)
            else:
                explicit = self._explicit_features()
                disable.extend(
                    name for name, enabled in haved.items() if enabled and name in explicit
                )
        elif self.state == "rendered":
            for name, enabled in wantd.items():
                if enabled:
                    enable.append(name)
                else:
                    disable.append(name)
            disable.reverse()

        for name in enable:
            self.addcmd({"name": name}, "feature", False)
        for name in disable:
            self.addcmd({"name": name}, "feature", True)

    def _normalize(self, config):
        """
        Convert the facts or argspec data to a dictionary of the feature name and the state.

        A feature that is given twice with different values is rejected.
        """
        data = {}
        for entry in config or []:
            name = entry["name"].strip()
            enabled = bool(entry.get("enabled"))
            if name in data and data[name] != enabled:
                self._module.fail_json(
                    msg="The feature '{0}' is given with both enabled true and false.".format(
                        name,
                    ),
                )
            data[name] = enabled
        return data
