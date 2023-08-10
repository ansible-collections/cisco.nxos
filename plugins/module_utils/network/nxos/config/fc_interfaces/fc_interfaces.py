#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_fc_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.fc_interfaces import (
    Fc_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


class Fc_interfaces(ResourceModule):
    """
    The nxos_fc_interfaces config class
    """

    def __init__(self, module):
        super(Fc_interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="fc_interfaces",
            tmplt=Fc_interfacesTemplate(),
        )
        self.parsers = ["description", "speed",
                        "mode", "trunk_mode", "analytics"]
        # self.parsers = ["description", "speed",
        #                 "mode", "trunk_mode", "analytics_scsi", "analytics_nvme"]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        wantd = {entry['name']: entry for entry in self.want}
        haved = {entry['name']: entry for entry in self.have}

        for each in wantd, haved:
            self.normalize_interface_names(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state in ["deleted", "purged"]:
            haved = {k: v for k, v in iteritems(
                haved) if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _calculate_ana_config(self, want_ana, have_ana):
        if want_ana == have_ana:
            return []
        # want "" have scsi  - no analytics type fc-scsi
        # want "" have nvme  - no analytics type fc-nvme
        # want "" have all   - no analytics type fc-all
        if want_ana == "" and have_ana == "fc-scsi":
            return ["no analytics type fc-scsi"]
        if want_ana == "" and have_ana == "fc-nvme":
            return ["no analytics type fc-nvme"]
        if want_ana == "" and have_ana == "fc-all":
            return ["no analytics type fc-all"]

        # want scsi have ""   - analytics type fc-scsi
        # want scsi have all  - no analytics type fc-nvme
        # want scsi have nvme - no analytics type fc-nvme ; analytics type
        # fc-scsi
        if want_ana == "fc-scsi" and have_ana == "":
            return ["analytics type fc-all"]
        if want_ana == "fc-scsi" and have_ana == "fc-all":
            return ["no analytics type fc-nvme"]
        if want_ana == "fc-scsi" and have_ana == "fc-nvme":
            return ["no analytics type fc-nvme", "analytics type fc-scsi"]

        # want nvme have ""    - analytics type fc-nvme
        # want nvme have all   - no analytics type fc-scsi
        # want nvme have scsi  - no analytics type fc-scsi ; analytics type
        # fc-nvme
        if want_ana == "fc-nvme" and have_ana == "":
            return ["analytics type fc-nvme"]
        if want_ana == "fc-nvme" and have_ana == "fc-all":
            return ["no analytics type fc-scsi"]
        if want_ana == "fc-nvme" and have_ana == "fc-scsi":
            return ["no analytics type fc-scsi", "analytics type fc-nvme"]

        # want all have ""    - analytics type fc-all
        # want all have scsi  - analytics type fc-all
        # want all have nvme  - analytics type fc-all
        if want_ana == "fc-all":
            return ["analytics type fc-all"]

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Fc_interfaces network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        if want.get("enabled") != have.get("enabled"):
            if want.get("enabled"):
                self.addcmd(want, "enabled", True)
            else:
                if want:
                    self.addcmd(want, "enabled", False)
                elif have.get("enabled"):
                    # handles deleted as want be blank and only
                    # negates if no shutdown
                    self.addcmd(have, "enabled", False)

        c = self._calculate_ana_config(
            want.get("analytics", ""), have.get("analytics", ""))
        new_cmds = []
        for eachc in self.commands:
            if "analytics" in eachc:
                continue
            else:
                new_cmds.append(eachc)

        self.commands = new_cmds + c
        # import q
#         q(want)
#         q(have)
#         q(self.commands)
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(
                want or have, "interface", False))

    def purge(self, have):
        """Handle operation for purged state"""
        self.commands.append(self._tmplt.render(have, "interface", True))

    def normalize_interface_names(self, param):
        if param:
            for _k, val in iteritems(param):
                val["name"] = normalize_interface(val["name"])
        return param
