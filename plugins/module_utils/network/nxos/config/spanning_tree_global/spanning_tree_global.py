#
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_spanning_tree_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
    get_from_dict,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.spanning_tree_global import (
    Spanning_tree_globalTemplate,
)


class Spanning_tree_global(ResourceModule):
    """
    The nxos_spanning_tree_global config class
    """

    def __init__(self, module):
        super(Spanning_tree_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="spanning_tree_global",
            tmplt=Spanning_tree_globalTemplate(),
        )
        self.parsers = [
            "bridge_assurance",
            "domain.identifier",
            "domain.disable",
            "domain.enable",
            "domain.clear_stats",
            "fcoe",
            "lc_issu",
            "loopguard_default",
            "mode",
            "mst.forward_time",
            "mst.hello_time",
            "mst.max_age",
            "mst.max_hops",
            "mst.simulate_pvst_global",
            "pathcost_method",
            "port_type.edge.bpdufilter",
            "port_type.edge.bpduguard",
            "port_type.default_type",
        ]

        self.configure_mst_parsers = [
            "mst.configure_mst.name",
            "mst.configure_mst.revision",
            "mst.configure_mst.private_vlan_sync",
        ]

        self.vlan_parsers = [
            "forward_time",
            "hello_time",
            "max_age",
            "priority",
            "root.primary",
            "root.secondary",
        ]

        self.pseudo_info_parsers = [
            "mst_info.designated_priority",
            "mst_info.root_priority",
            "vlan_info.designated_priority",
            "vlan_info.root_priority",
        ]

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
        wantd = self._sptg_list_to_dict(self.want)
        haved = self._sptg_list_to_dict(self.have)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd
        if self.state == "deleted":
            wantd = {}

        self._compare(want=wantd, have=haved)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Spanning_tree_global network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)
        self._list_compare(
            want=want.get("vlan", {}), 
            have=have.get("vlan", {}),
            parserlist=self.vlan_parsers,
        )
        self._compare_pesudo_info_items(want=want, have=have)
        self._compare_mst_configure(want=want, have=have)

    def _compare_mst_configure(self, want, have):
        begin = len(self.commands)
        self._complex_compare(want=want, have=have, parserlist=self.configure_mst_parsers)

        iv_want = want.get("mst", {}).get("configure_mst", {}).get("instance_vlan", {})
        iv_have = have.get("mst", {}).get("configure_mst", {}).get("instance_vlan", {})
        
        for want_key, want_entry in iteritems(iv_want):
            have_entry = iv_have.pop(want_key, {})
            if want_entry != have_entry:
                if have_entry and self.state in ["overridden", "replaced"]:
                    self.addcmd(have_entry, "instance_vlan", negate=True)
                self.addcmd(want_entry, "instance_vlan", False)

        for _k, hv in iteritems(iv_have):
            self.addcmd(hv, "instance_vlan", negate=True)
        
        if begin != len(self.commands):
            self.commands.insert(begin, "spanning-tree mst configuration")

    def _compare_pesudo_info_items(self, want, have):
        begin = len(self.commands)
        for typex in ["mst_info", "vlan_info"]:
            i_want = want.get("pseudo_info", {}).get(typex, {})
            i_have = have.get("pseudo_info", {}).get(typex, {})
            self._list_compare(
                want=i_want,
                have=i_have,
                parserlist=self.pseudo_info_parsers,
                typex=typex,
            )

        if begin != len(self.commands):
            self.commands.insert(begin, "spanning-tree pseudo-information")

    def _list_compare(self, want, have, parserlist, typex = None):
        for name, entry in iteritems(want):
            if typex:
                i_want = {typex: entry}
                i_have = {typex: have.pop(name, {})}
            else:
                i_want = entry
                i_have = have.pop(name, {})
            self._complex_compare(
                want=i_want,
                have=i_have,
                parserlist=parserlist,
            )
        for name, entry in iteritems(have):
            if typex:
                ix_have = {typex: entry}
            else:
                ix_have = entry
            self._complex_compare(
                want={},
                have=ix_have,
                parserlist=parserlist,
            )

    def _complex_compare(self, want, have, parserlist):
        self.compare(parsers=parserlist, want=want, have=have)

    def _sptg_list_to_dict(self, data):
        """Convert all list of dicts to dicts of dicts"""
        p_key = {
            "vlan": "vlan_range",
            "mst_info": "range",
            "vlan_info": "range",
            "instance_vlan": "vlan_range",
        }
        tmp_data = deepcopy(data)
        for k, _v in p_key.items():
            if k in tmp_data and k == "vlan":
                tmp_data[k] = {str(i[p_key[k]]): i for i in tmp_data[k]}
            if tmp_data.get("pseudo_info", {}).get(k) and k in ["mst_info", "vlan_info"]:
                tmp_data["pseudo_info"][k] = {
                    str(i[p_key[k]]): i for i in tmp_data["pseudo_info"][k]
                }
            if (
                tmp_data.get("mst", {}).get("configure_mst", {}).get("instance_vlan", {})
                and k == "instance_vlan"
            ):
                tmp_data["mst"]["configure_mst"][k] = {
                    str(i[p_key[k]]): i for i in tmp_data["mst"]["configure_mst"][k]
                }
        return tmp_data
