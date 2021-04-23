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
    get_from_dict,
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
        self.linear_parsers = [
            "description",
            "continue_sequence",
            "set.as_path.prepend.last_as",
            "set.as_path.tag",
            "set.comm_list",
            "set.dampening",
            "set.extcomm_list",
            "set.forwarding_address",
            "set.null_interface",
            "set.ip.address.prefix_list",
            "set.ip.precedence",
            "set.ipv6.address.prefix_list",
            "set.ipv6.precedence",
            "set.label_index",
            "set.level",
            "set.local_preference",
            "set.metric",
            "set.metric_type",
            "set.nssa_only",
            "set.origin",
            "set.path_selection",
            "set.tag",
            "set.weight",
        ]
        self.complex_parsers = [
            "match.as_number.asn",
            "match.as_number.as_path_list",
            "match.as_path",
            "match.community.community_list",
            "match.evpn.route_types",
            "match.extcommunity.extcommunity_list",
            "match.interfaces",
            "match.ip.address.access_list",
            "match.ip.address.prefix_lists",
            "match.ip.multicast",
            "match.ip.next_hop.prefix_lists",
            "match.ip.route_source.prefix_lists",
            "match.ipv6.address.access_list",
            "match.ipv6.address.prefix_lists",
            "match.ipv6.multicast",
            "match.ipv6.next_hop.prefix_lists",
            "match.ipv6.route_source.prefix_lists",
            "match.mac_list",
            "match.metric",
            "match.ospf_area",
            "match.route_types",
            "match.source_protocol",
            "match.tags",
            "set.as_path.prepend.as_number",
            "set.distance",
            "set.evpn.gateway_ip",
            "set.community",
        ]

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
            hentry = have.pop(wk, {})
            begin = len(self.commands)

            self._compare_lists(wentry, hentry)
            self.compare(parsers=self.linear_parsers, want=wentry, have=hentry)

            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render(wentry, "route_map", False)
                )
        # remove superfluos entries from have
        for _hk, hentry in iteritems(have):
            self.commands.append(self._tmplt.render(hentry, "route_map", True))

    def _compare_lists(self, want, have):
        for x in self.complex_parsers:
            wx = get_from_dict(want, x) or []
            hx = get_from_dict(have, x) or []

            if isinstance(wx, list):
                wx = set(wx)
            if isinstance(hx, list):
                hx = set(hx)

            if wx != hx:
                # negate existing config so that want is not appended
                # in case of replaced or overridden
                if self.state in ["replaced", "overridden"] and hx:
                    self.addcmd(have, x, negate=True)
                self.addcmd(want, x)

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
