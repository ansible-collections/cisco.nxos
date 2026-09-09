#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_vpc_interface config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.vpc_interfaces import (
    Vpc_interfacesTemplate,
)


class Vpc_interfaces(ResourceModule):
    """
    The nxos_vpc_interface config class
    """

    def __init__(self, module):
        super(Vpc_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="vpc_interfaces",
            tmplt=Vpc_interfacesTemplate(),
        )
        self.parsers = []

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in wantd.items():
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Generate set/delete commands for a single port-channel VPC entry."""
        begin = len(self.commands)

        w_vpc = want.get("vpc")
        h_vpc = have.get("vpc")
        w_peer_link = want.get("peer_link")
        h_peer_link = have.get("peer_link")

        if self.state in ["merged", "rendered"]:
            # Only make changes when want explicitly specifies vpc or peer_link
            if w_vpc and w_vpc != h_vpc:
                if h_peer_link:
                    self.commands.append("no vpc peer-link")
                if h_vpc:
                    self.commands.append("no vpc")
                self.commands.append("vpc {0}".format(w_vpc))
            elif w_peer_link is True and not h_peer_link:
                if h_vpc:
                    self.commands.append("no vpc")
                self.commands.append("vpc peer-link")
            if want.get("orphan_port_suspend") is True and not have.get("orphan_port_suspend"):
                self.commands.append("vpc orphan-port suspend")
        else:
            # replaced / overridden / deleted: fully reconcile
            if h_peer_link and not w_peer_link:
                self.commands.append("no vpc peer-link")
            if h_vpc and not w_vpc:
                self.commands.append("no vpc")
            if w_vpc and w_vpc != h_vpc:
                self.commands.append("vpc {0}".format(w_vpc))
            if w_peer_link is True and not h_peer_link:
                self.commands.append("vpc peer-link")
            if want.get("orphan_port_suspend") is True and not have.get("orphan_port_suspend"):
                self.commands.append("vpc orphan-port suspend")
            elif not want.get("orphan_port_suspend") and have.get("orphan_port_suspend"):
                self.commands.append("no vpc orphan-port suspend")

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "interface", False))
