#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_route_maps config file.
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
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.route_maps import (
    Route_mapsTemplate,
)


class Route_maps(ResourceModule):
    """
    The nxos_route_maps config class
    """

    def __init__(self, module):
        super(Route_maps, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="route_maps",
            tmplt=Route_mapsTemplate(),
        )
        # TO-DO: populate all parsers
        self.parsers = ["description", "continue", "match.as_number.asn"]

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
        wantd = self._route_maps_list_to_dict(self.want)
        haved = self._route_maps_list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    for _hk, hentry in iteritems(have.get("entries", {})):
                        self.commands.append(
                            self._tmplt.render(hentry, "route_map", True)
                        )

        for wk, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(wk, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Route_maps network resource.
        """
        w_entries = want.get("entries", {})
        h_entries = have.get("entries", {})
        self._compare_entries(want=w_entries, have=h_entries)

    def _compare_entries(self, want, have):
        for wk, wentry in iteritems(want):
            begin = len(self.commands)
            self.compare(
                parsers=self.parsers, want=wentry, have=have.pop(wk, {})
            )
            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render(wentry, "route_map", False)
                )
        # remove superfluos entries from have
        for _hk, hentry in iteritems(have):
            self.commands.append(self._tmplt.render(hentry, "route_map", True))

    def _route_maps_list_to_dict(self, entry):
        entry = {x["route_map"]: x for x in entry}
        for rmap, data in iteritems(entry):
            if "entries" in data:
                for x in data["entries"]:
                    x.update({"route_map": rmap})
                data["entries"] = {
                    (rmap, entry["action"], entry.get("sequence")): entry
                    for entry in data["entries"]
                }
        return entry
