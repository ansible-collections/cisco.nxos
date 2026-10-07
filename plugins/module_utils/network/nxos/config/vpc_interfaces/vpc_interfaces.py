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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
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

        if self.state == "merged":
            wantd = self._merge_with_have(wantd, haved)

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

    def _merge_with_have(self, wantd, haved):
        """Layer want on top of have so that a single compare path can be used
        for every state. Attributes the playbook does not mention are inherited
        from the device, which is what ``merged`` means, while attributes it
        does mention win even when they are ``false``.

        Interfaces present only on the device are left out: under ``merged``
        they can never produce a command.
        """
        merged = {}

        for name, want in wantd.items():
            entry = dict_merge(haved.get(name, {}), want)

            # `vpc <id>` and `vpc peer-link` cannot coexist on one interface,
            # so asking for either explicitly clears the other rather than
            # inheriting a conflicting value from the device
            if want.get("vpc"):
                entry["peer_link"] = False
            elif want.get("peer_link"):
                entry["vpc"] = None

            merged[name] = entry

        return merged

    def _compare(self, want, have):
        """Generate set/delete commands for a single interface entry."""
        begin = len(self.commands)

        w_vpc = want.get("vpc")
        h_vpc = have.get("vpc")
        w_orphan = bool(want.get("orphan_port_suspend"))
        h_orphan = bool(have.get("orphan_port_suspend"))

        # NX-OS refuses to make a port-channel part of a VPC while it still
        # carries `vpc orphan-port suspend`, so the suspend line is withdrawn
        # before the VPC ID is applied and restored afterwards when it stays
        vpc_changing = bool(w_vpc) and w_vpc != h_vpc

        if h_orphan and (not w_orphan or vpc_changing):
            self.commands.append("no vpc orphan-port suspend")

        # the peer-link and the VPC ID share the same `vpc` sub-command, so the
        # existing value has to be withdrawn before a different one is applied
        if have.get("peer_link") and not want.get("peer_link"):
            self.commands.append("no vpc peer-link")
        if h_vpc and w_vpc != h_vpc:
            self.commands.append("no vpc")
        if w_vpc and w_vpc != h_vpc:
            self.commands.append("vpc {0}".format(w_vpc))
        if want.get("peer_link") and not have.get("peer_link"):
            self.commands.append("vpc peer-link")

        if w_orphan and (not h_orphan or vpc_changing):
            self.commands.append("vpc orphan-port suspend")

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "interface", False))
