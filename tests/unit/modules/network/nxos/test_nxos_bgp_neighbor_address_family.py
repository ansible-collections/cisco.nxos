# (c) 2021 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import (
    nxos_bgp_neighbor_address_family,
)

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosBGPNeighborAddressFamilyModule(TestNxosModule):

    # Testing strategy
    # ------------------
    # (a) The unit tests cover `merged` and `replaced` for every attribute.
    #     Since `overridden` is essentially `replaced` but at a larger
    #     scale, these indirectly cover `overridden` as well.
    # (b) For linear attributes replaced is not valid and hence, those tests
    #     delete the attributes from the config subsection.
    # (c) The argspec for VRFs is same as the top-level spec and the config logic
    #     is re-used. Hence, those attributes are not explictly covered. However, a
    #     combination of VRF + top-level spec + AF is tested.

    module = nxos_bgp_neighbor_address_family

    def setUp(self):
        super(TestNxosBGPNeighborAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bgp_neighbor_address_family.bgp_neighbor_address_family.Bgp_neighbor_address_familyFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBGPNeighborAddressFamilyModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_bgp_additional_paths_merged(self):
        # test merged for config->address_family->additional_paths
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              neighbor 192.168.1.1
                address-family ipv4 unicast
                  no advertise local-labeled-route
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            
                        ),
                        dict(
                            afi="ipv4",
                            safi="unicast",
                            
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "additional-paths install backup",
            "additional-paths receive",
            "additional-paths selection route-map rmap1",
            "additional-paths send",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no additional-paths install backup",
            "additional-paths receive",
            "additional-paths selection route-map rmap2",
            "no additional-paths send",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
