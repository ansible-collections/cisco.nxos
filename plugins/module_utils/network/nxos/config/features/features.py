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

    def generate_commands(self):
        """
        Generate configuration commands to send based on
        want, have and desired state.

        The features are compared by name. The commands that enable a feature are sent in the
        order of the configuration, the commands that disable a feature after them.
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
            if self.state == "overridden":
                disable.extend(
                    name for name, enabled in haved.items() if enabled and name not in wantd
                )
        elif self.state == "deleted":
            # Without config every enabled feature is disabled.
            names = list(wantd) if self.want else list(haved)
            disable.extend(name for name in names if haved.get(name) is True)
        elif self.state == "rendered":
            for name, enabled in wantd.items():
                (enable if enabled else disable).append(name)

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
