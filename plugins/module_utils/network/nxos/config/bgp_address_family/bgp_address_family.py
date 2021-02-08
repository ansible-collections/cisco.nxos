#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The nxos_bgp_address_family config file.
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.bgp_address_family import (
    Bgp_address_familyTemplate,
)
import q


class Bgp_address_family(ResourceModule):
    """
    The nxos_bgp_address_family config class
    """

    def __init__(self, module):
        super(Bgp_address_family, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_address_family",
            tmplt=Bgp_address_familyTemplate(),
        )
        self.parsers = []

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
        wantd = deepcopy(self.want)
        haved = deepcopy(self.have)

        self._bgp_af_list_to_dict(wantd)
        self._bgp_af_list_to_dict(haved)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is overridden or deleted, remove superfluos config
        if self.state in ["deleted", "overridden"]:
            # for empty want we remove all AF configs
            if not self.want and self.state == "deleted":
                wantd = deepcopy(haved)

            # we should not delete anything in case of ASN mismatch
            if haved and haved["as_number"] == wantd.get("as_number"):
                remove = True if self.state == "deleted" else False

                have_af = haved.get("address_family", {})
                want_af = wantd.get("address_family", {})
                self._remove_af(want_af, have_af, remove=remove)

                wvrfs = wantd.get("vrfs", {})
                hvrfs = haved.get("vrfs", {})

                for k, hvrf in iteritems(hvrfs):
                    wvrf = wvrfs.pop(k, {})
                    self._remove_af(wvrf, hvrf, vrf=k, remove=remove)

        if self.state in ["merged", "replaced", "overridden"]:
            for k, want in iteritems(wantd):
                self._compare(want=want, have=haved.pop(k, {}))

        if self.commands and not self.commands[0].startswith("router bgp"):
            self.commands.insert(
                0, "router bgp {0}".format(haved["as_number"])
            )

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_address_family network resource.
        """
        # self.compare(parsers=self.parsers, want=want, have=have)
        pass

    def _bgp_af_list_to_dict(self, entry):
        def _build_key(data):
            """Build primary key for each dict

            :params x: dictionary
            :returns: primary key as tuple
            """
            # afi should always be present
            # safi and vrf are optional
            # a combination of these 3 uniquely
            # identifies an AF context
            afi = "afi_" + data["afi"]
            safi = "safi_" + data.get("safi", "")
            vrf = "vrf_" + data.get("vrf", "")

            return (afi, safi, vrf)

        af = {_build_key(x): x for x in entry.get("address_family", [])}

        temp = {}
        entry["vrfs"] = {}
        entry["address_family"] = {}

        # group AFs by VRFs
        # vrf_ denotes global AFs
        for k in af.keys():
            for x in k:
                if x.startswith("vrf_"):
                    if x not in temp:
                        temp[x] = {}
                    temp[x][k] = af[k]

        for k in temp.keys():
            if k == "vrf_":
                # populate global AFs
                entry["address_family"][k] = temp[k]
            else:
                # populate VRF AFs
                entry["vrfs"][k] = temp[k]

        entry["address_family"] = entry["address_family"].get("vrf_", {})

        # final structure: https://gist.github.com/NilashishC/628dae5fe39a4908e87c9e833bfbe57d

    def _remove_af(self, want_af, have_af, vrf=None, remove=False):
        cur_ptr = len(self.commands)
        for k, v in iteritems(have_af):
            # first conditional is for deleted
            # second conditional is for overridden
            if (remove and k in want_af) or (not remove and k not in want_af):
                self.addcmd(v, "address_family", True)
        if cur_ptr < len(self.commands) and vrf:
            self.commands.insert(cur_ptr, "vrf {0}".format(vrf))
