#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_bgp_global config file.
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)


class Bgp_global(ResourceModule):
    """
    The nxos_bgp_global config class
    """

    def __init__(self, module):
        super(Bgp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_global",
            tmplt=Bgp_globalTemplate(),
        )
        # VRF parsers = 29
        self.parsers = [
            "allocate_index",
            "affinity_group.group_id",
            "bestpath.always_compare_med",
            "bestpath.as_path.ignore",
            "bestpath.as_path.multipath_relax",
            "bestpath.compare_neighborid",
            "bestpath.compare_routerid",
            "bestpath.cost_community_ignore",
            "bestpath.igp_metric_ignore",
            "bestpath.med.confed",
            "bestpath.med.missing_as_worst",
            "bestpath.med.non_deterministic",
            "cluster_id",
            "local_as",
            "confederation.identifier",
            "graceful_restart",
            "graceful_restart.restart_time",
            "graceful_restart.stalepath_time",
            "graceful_restart.helper",
            "log_neighbor_changes",
            "maxas_limit",
            "neighbor_down.fib_accelerate",
            "reconnect_interval",
            "router_id",
            "timers.bestpath_limit",
            "timers.bgp",
            "timers.prefix_peer_timeout",
            "timers.prefix_peer_wait",
            # end VRF parsers
            "disable_policy_batching",
            "disable_policy_batching.ipv4.prefix_list",
            "disable_policy_batching.ipv6.prefix_list",
            "disable_policy_batching.nexthop",
            "dynamic_med_interval",
            "enforce_first_as",
            "enhanced_error",
            "fast_external_fallover",
            "flush_routes",
            "graceful_shutdown.activate",
            "graceful_shutdown.aware",
            "isolate",
            "nexthop.suppress_default_resolution",
            "shutdown",
            "suppress_fib_pending",
            "fabric_soo",
            "rd",
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
        for entry in self.want, self.have:
            self._bgp_list_to_dict(entry)

        # if state is deleted, clean up global params
        if self.state == "deleted":
            if not self.want or (self.have.get("asn") == self.want.get("asn")):
                self._compare(want={}, have=self.have)

        elif self.state == "purged":
            self.addcmd(self.have or {}, "asn", True)

        else:
            wantd = self.want
            # if state is merged, merge want onto have and then compare
            if self.state == "merged":
                wantd = dict_merge(self.have, self.want)

            self._compare(want=wantd, have=self.have)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_global network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)
        self._compare_confederation_peers(want, have)
        self._compare_neighbors(want, have)
        self._vrfs_compare(want=want, have=have)

        if len(self.commands) != begin:
            self.commands.insert(
                begin,
                self._tmplt.render(
                    want or have,
                    "vrf" if "vrf" in (want.keys() or have.keys()) else "asn",
                    False,
                ),
            )

    def _compare_confederation_peers(self, want, have):
        w_cpeers = want.get("confederation", {}).get("peers", [])
        h_cpeers = have.get("confederation", {}).get("peers", [])

        if set(w_cpeers) != set(h_cpeers):
            if self.state in ["replaced", "deleted"]:
                # if there are peers already configured
                # we need to remove those before we pass
                # the new ones otherwise the device appends
                # them to the existing ones
                if h_cpeers:
                    self.addcmd(have, "confederation.peers", True)

            self.addcmd(want, "confederation.peers", False)

    def _compare_neighbors(self, want, have):
        nbr_parsers = [
            "remote_as",
            "neighbor_affinity_group.group_id",
            "bmp_activate_server",
            "capability",
            "description",
            "disable_connected_check",
            "dont_capability_negotiate",
            "dscp",
            "dynamic_capability",
            "ebgp_multihop",
            "graceful_shutdown",
            "inherit.peer",
            "inherit.peer_session",
            "local_as",
            "log_neighbor_changes",
            "low_memory",
            "password",
            "path_attribute",
            "peer_type",
            "remove_private_as",
            "shutdown",
            "timers",
            "transport",
            "ttl_security",
            "update_source",
        ]
        wnbrs = want.get("neighbors", {})
        hnbrs = have.get("neighbors", {})

        # neighbors have separate contexts in NX-OS
        for name, entry in iteritems(wnbrs):
            begin = len(self.commands)
            self.compare(
                parsers=nbr_parsers, want=entry, have=hnbrs.pop(name, {})
            )
            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render(entry, "neighbor_address", False)
                )
        # remove remaining items in have for replaced
        for name, entry in iteritems(hnbrs):
            self.addcmd(entry, "neighbor_address", True)

    def _vrfs_compare(self, want, have):
        wvrfs = want.get("vrfs", {})
        hvrfs = have.get("vrfs", {})
        for name, entry in iteritems(wvrfs):
            self._compare(want=entry, have=hvrfs.pop(name, {}))
        # cleanup remaining VRFs
        # but do not negate it entirely
        # instead remove only those attributes
        # that this module manages
        for name, entry in iteritems(hvrfs):
            self._compare(want={}, have=entry)

    def _bgp_list_to_dict(self, entry):
        if "neighbors" in entry:
            entry["neighbors"] = {
                x["neighbor_address"]: x for x in entry.get("neighbors", [])
            }
        if "vrfs" in entry:
            entry["vrfs"] = {x["vrf"]: x for x in entry.get("vrfs", [])}
            for _k, vrf in iteritems(entry["vrfs"]):
                self._bgp_list_to_dict(vrf)
