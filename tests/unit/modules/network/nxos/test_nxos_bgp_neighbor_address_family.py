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
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bgp_neighbor_address_family."
            "bgp_neighbor_address_family.Bgp_neighbor_address_familyFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBGPNeighborAddressFamilyModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_bgp_nbr_af_advertise_map_merged(self):
        # test merged for advertise_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    advertise-map rmap2 exist-map rmap3
                  address-family ipv4 multicast
                    advertise-map rmap1 non-exist-map rmap5
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    advertise_map=dict(
                                        route_map="rmap1", exist_map="rmap2"
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            advertise_map=dict(
                                                route_map="rmap2",
                                                exist_map="rmap3",
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            advertise_map=dict(
                                                route_map="rmap1",
                                                non_exist_map="rmap7",
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "advertise-map rmap1 exist-map rmap2",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "advertise-map rmap1 non-exist-map rmap7",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_advertise_map_replaced(self):
        # test replaced for advertise_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  advertise-map rmap1 exist-map rmap2
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    advertise-map rmap2 exist-map rmap3
                  address-family ipv4 multicast
                    advertise-map rmap1 non-exist-map rmap5
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    advertise_map=dict(
                                        route_map="rmap1", exist_map="rmap3"
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            advertise_map=dict(
                                                route_map="rmap2",
                                                exist_map="rmap3",
                                            ),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "advertise-map rmap1 exist-map rmap3",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no advertise-map rmap1 non-exist-map rmap5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_advertisement_interval_merged(self):
        # test merged for advertisement_interval
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    advertisement-interval 300
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    advertisement_interval=350,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            advertisement_interval=300,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            advertisement_interval=400,
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "advertisement-interval 350",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "advertisement-interval 400",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_advertisement_interval_replaced(self):
        # test replaced for advertisement_interval
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 unicast
                  advertisement-interval 410
                address-family ipv4 multicast
                  advertisement-interval 350
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    advertisement-interval 300
                  address-family ipv4 multicast
                    advertisement-interval 400
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="unicast"),
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    advertisement_interval=350,
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            advertisement_interval=300,
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 unicast",
            "no advertisement-interval 410",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no advertisement-interval 400",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_allowas_in_merged(self):
        # test merged for allowas_in
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    allowas-in 3
                  address-family ipv4 multicast
                    allowas-in 3
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    allowas_in=dict(max_occurences=8),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            allowas_in=dict(max_occurences=5),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            allowas_in=dict(max_occurences=3),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "allowas-in 8",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "allowas-in 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_allowas_in_replaced(self):
        # test replaced for allowas_in
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  allowas-in 8
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    allowas-in 5
                  address-family ipv4 multicast
                    allowas-in 3
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    allowas_in=dict(max_occurences=9),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            allowas_in=dict(max_occurences=5),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "allowas-in 9",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no allowas-in 3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_as_override_merged(self):
        # test merged for as_override
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                remote-as 65545
              vrf site-1
                neighbor 192.168.1.1
                  remote-as 65545
                  address-family ipv4 unicast
                    as-override
                  address-family ipv4 multicast
                    as-override
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    as_override=True,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            as_override=True,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            as_override=False,
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "as-override",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no as-override",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_as_override_replaced(self):
        # test replaced for as_override
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                remote-as 65545
                address-family ipv4 multicast
                  as-override
              vrf site-1
                neighbor 192.168.1.1
                  remote-as 65545
                  address-family ipv4 unicast
                    as-override
                  address-family ipv4 multicast
                    as-override
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast")
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            as_override=True,
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no as-override",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no as-override",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_capability_merged(self):
        # test merged for capability
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    capability additional-paths receive
                    capability additional-paths send disable
                  address-family ipv4 multicast
                    capability additional-paths receive disable
                    capability additional-paths send
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    capability=dict(
                                        additional_paths=dict(
                                            receive="enable", send="enable"
                                        )
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            capability=dict(
                                                additional_paths=dict(
                                                    receive="disable",
                                                    send="enable",
                                                )
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            capability=dict(
                                                additional_paths=dict(
                                                    receive="enable",
                                                    send="disable",
                                                )
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "capability additional-paths receive",
            "capability additional-paths send",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "capability additional-paths receive disable",
            "capability additional-paths send",
            "address-family ipv4 multicast",
            "capability additional-paths receive",
            "capability additional-paths send disable",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_capability_replaced(self):
        # test replaced for capability
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  capability additional-paths receive
                  capability additional-paths send
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    capability additional-paths receive disable
                    capability additional-paths send
                  address-family ipv4 multicast
                    capability additional-paths receive
                    capability additional-paths send disable
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    capability=dict(
                                        additional_paths=dict(send="enable")
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            capability=dict(
                                                additional_paths=dict(
                                                    receive="disable",
                                                    send="enable",
                                                )
                                            ),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no capability additional-paths receive",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no capability additional-paths receive",
            "no capability additional-paths send disable",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_originate_peer_as_merged(self):
        # test merged for default_originate, disable_peer_as_check
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    default-originate
                    disable-peer-as-check
                  address-family ipv4 multicast
                    default-originate route-map rmap1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    default_originate=dict(set=True),
                                ),
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    disable_peer_as_check=True,
                                    default_originate=dict(route_map="rmap1"),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            disable_peer_as_check=True,
                                            default_originate=dict(set=True),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            default_originate=dict(
                                                route_map="rmap2"
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "default-originate",
            "address-family ipv4 unicast",
            "default-originate route-map rmap1",
            "disable-peer-as-check",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "default-originate route-map rmap2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_originate_peer_as_merged(self):
        # test merged for default_originate, disable_peer_as_check
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  default-originate
                address-family ipv4 unicast
                  default-originate route-map rmap1
                  disable-peer-as-check
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    default-originate
                    disable-peer-as-check
                  address-family ipv4 multicast
                    default-originate route-map rmap1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast"),
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    default_originate=dict(route_map="rmap1"),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            disable_peer_as_check=True,
                                            default_originate=dict(set=True),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no default-originate",
            "address-family ipv4 unicast",
            "no disable-peer-as-check",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no default-originate route-map rmap1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_filter_list_inherit_merged(self):
        # test merged for filter_list, inherit
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    filter-list rmap1 in
                    filter-list rmap2 out
                    inherit peer-policy template-1 100
                  address-family ipv4 multicast
                    filter-list rmap1 out
                    inherit peer-policy template-1 300
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    filter_list=dict(
                                        inbound="rmap3", outbound="rmap4"
                                    ),
                                    inherit=dict(
                                        template="template-2", sequence=200
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            filter_list=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                            inherit=dict(
                                                template="template-1",
                                                sequence=100,
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            filter_list=dict(inbound="rmap2"),
                                            inherit=dict(
                                                template="template-1",
                                                sequence=400,
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "filter-list rmap3 in",
            "filter-list rmap4 out",
            "inherit peer-policy template-2 200",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "filter-list rmap2 in",
            "inherit peer-policy template-1 400",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_filter_list_inherit_replaced(self):
        # test replaced for filter_list, inherit
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  filter-list rmap3 in
                  filter-list rmap4 out
                  inherit peer-policy template-2 200
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    filter-list rmap1 in
                    filter-list rmap2 out
                    inherit peer-policy template-1 100
                  address-family ipv4 multicast
                    filter-list rmap1 out
                    filter-list rmap2 in
                    inherit peer-policy template-1 300
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    filter_list=dict(inbound="rmap3"),
                                    inherit=dict(
                                        template="template-2", sequence=200
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            filter_list=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                            inherit=dict(
                                                template="template-1",
                                                sequence=100,
                                            ),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no filter-list rmap4 out",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no filter-list rmap2 in",
            "no filter-list rmap1 out",
            "no inherit peer-policy template-1 300",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_maximum_prefix_merged(self):
        # test merged for maximum_prefix
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 multicast
                    maximum-prefix 12
                  address-family ipv4 unicast
                    maximum-prefix 12 80
                  address-family ipv6 multicast
                    maximum-prefix 12 85 warning-only
                  address-family ipv6 unicast
                    maximum-prefix 12 85 restart 1200
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    maximum_prefix=dict(max_prefix_limit=20),
                                ),
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    maximum_prefix=dict(
                                        max_prefix_limit=25,
                                        generate_warning_threshold=85,
                                    ),
                                ),
                                dict(
                                    afi="ipv6",
                                    safi="multicast",
                                    maximum_prefix=dict(
                                        max_prefix_limit=28,
                                        generate_warning_threshold=90,
                                        warning_only=True,
                                    ),
                                ),
                                dict(
                                    afi="ipv6",
                                    safi="unicast",
                                    maximum_prefix=dict(
                                        max_prefix_limit=30,
                                        generate_warning_threshold=95,
                                        restart_interval=1200,
                                    ),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=28
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=12,
                                                generate_warning_threshold=80,
                                            ),
                                        ),
                                        dict(
                                            afi="ipv6",
                                            safi="multicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=12,
                                                generate_warning_threshold=85,
                                                warning_only=True,
                                            ),
                                        ),
                                        dict(
                                            afi="ipv6",
                                            safi="unicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=12,
                                                generate_warning_threshold=85,
                                                restart_interval=1200,
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "maximum-prefix 20",
            "address-family ipv4 unicast",
            "maximum-prefix 25 85",
            "address-family ipv6 multicast",
            "maximum-prefix 28 90 warning-only",
            "address-family ipv6 unicast",
            "maximum-prefix 30 95 restart 1200",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "maximum-prefix 28",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_maximum_prefix_replaced(self):
        # test replaced for maximum_prefix
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  maximum-prefix 20
                address-family ipv4 unicast
                  maximum-prefix 25 85
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 multicast
                    maximum-prefix 12
                  address-family ipv4 unicast
                    maximum-prefix 12 80
                  address-family ipv6 multicast
                    maximum-prefix 12 85 warning-only
                  address-family ipv6 unicast
                    maximum-prefix 12 85 restart 1200
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="unicast"),
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    maximum_prefix=dict(max_prefix_limit=28),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=28
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            maximum_prefix=dict(
                                                max_prefix_limit=12,
                                                generate_warning_threshold=80,
                                            ),
                                        ),
                                        dict(afi="ipv6", safi="multicast"),
                                        dict(afi="ipv6", safi="unicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 unicast",
            "no maximum-prefix 25 85",
            "address-family ipv6 multicast",
            "maximum-prefix 28",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "maximum-prefix 28",
            "address-family ipv6 multicast",
            "no maximum-prefix 12 85 warning-only",
            "address-family ipv6 unicast",
            "no maximum-prefix 12 85 restart 1200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_next_hop_merged(self):
        # test merged for next_hop_self, next_hop_third_party
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    next-hop-self
                    no next-hop-third-party
                  address-family ipv4 multicast
                    next-hop-self all
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    next_hop_self=dict(set=True),
                                ),
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    next_hop_self=dict(all_routes=True),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            next_hop_self=dict(set=True),
                                            next_hop_third_party=True,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            next_hop_self=dict(
                                                all_routes=True
                                            ),
                                        ),
                                        dict(
                                            afi="ipv6",
                                            safi="multicast",
                                            next_hop_self=dict(
                                                all_routes=True
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "next-hop-self",
            "address-family ipv4 unicast",
            "next-hop-self all",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "next-hop-third-party",
            "address-family ipv6 multicast",
            "next-hop-self all",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_next_hop_replaced(self):
        # test replaced for next_hop_self, next_hop_third_party
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  next-hop-self
                address-family ipv4 unicast
                  next-hop-self all
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    next-hop-self
                    no next-hop-third-party
                  address-family ipv4 multicast
                    next-hop-self all
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast"),
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    next_hop_self=dict(all_routes=True),
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            next_hop_third_party=True,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            next_hop_self=dict(
                                                all_routes=True
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no next-hop-self",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "no next-hop-self",
            "next-hop-third-party",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_prefix_list_merged(self):
        # test merged for prefix_list
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    prefix-list rmap1 in
                    prefix-list rmap2 out
                  address-family ipv4 multicast
                    prefix-list rmap1 out
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    prefix_list=dict(
                                        inbound="rmap3", outbound="rmap4"
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            prefix_list=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            prefix_list=dict(inbound="rmap2"),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "prefix-list rmap3 in",
            "prefix-list rmap4 out",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "prefix-list rmap2 in",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_prefix_list_replaced(self):
        # test replaced for prefix_list
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  prefix-list rmap3 in
                  prefix-list rmap4 out
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    prefix-list rmap1 in
                    prefix-list rmap2 out
                  address-family ipv4 multicast
                    prefix-list rmap1 out
                    prefix-list rmap2 in
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    prefix_list=dict(inbound="rmap3"),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            prefix_list=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no prefix-list rmap4 out",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no prefix-list rmap2 in",
            "no prefix-list rmap1 out",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_rewrite_evpn_route_map_merged(self):
        # test merged for rewrite_evpn_rt_asn, route_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    route-map rmap1 in
                    route-map rmap2 out
                    rewrite-evpn-rt-asn
                  address-family ipv4 multicast
                    route-map rmap1 out
                    rewrite-evpn-rt-asn
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    route_map=dict(
                                        inbound="rmap3", outbound="rmap4"
                                    ),
                                    rewrite_evpn_rt_asn=True,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            route_map=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                            rewrite_evpn_rt_asn=True,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            route_map=dict(inbound="rmap2"),
                                            rewrite_evpn_rt_asn=True,
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "route-map rmap3 in",
            "route-map rmap4 out",
            "rewrite-evpn-rt-asn",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "route-map rmap2 in",
            "rewrite-evpn-rt-asn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_rewrite_evpn_route_map_replaced(self):
        # test replaced for rewrite_evpn_rt_asn, route_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  route-map rmap3 in
                  route-map rmap4 out
                  rewrite-evpn-rt-asn
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    route-map rmap1 in
                    route-map rmap2 out
                    rewrite-evpn-rt-asn
                  address-family ipv4 multicast
                    route-map rmap1 out
                    route-map rmap2 in
                    rewrite-evpn-rt-asn
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    route_map=dict(inbound="rmap3"),
                                    rewrite_evpn_rt_asn=True,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            route_map=dict(
                                                inbound="rmap1",
                                                outbound="rmap2",
                                            ),
                                            rewrite_evpn_rt_asn=True,
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no route-map rmap4 out",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no route-map rmap2 in",
            "no route-map rmap1 out",
            "no rewrite-evpn-rt-asn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_route_reflector_client_send_community_merged(self):
        # test merged for route_reflector_client
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    route-reflector-client
                    send-community
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    route_reflector_client=True,
                                    send_community=dict(extended=True),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            route_reflector_client=True,
                                            send_community=dict(set=True),
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            send_community=dict(set=True),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "route-reflector-client",
            "send-community extended",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "send-community",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_route_reflector_client_send_community_replaced(self):
        # test replaced for route_reflector_client
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  route-reflector-client
                  send-community extended
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    route-reflector-client
                    send-community
                  address-family ipv4 multicast
                    send-community
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    send_community=dict(extended=True),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            route_reflector_client=True,
                                            send_community=dict(set=True),
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no route-reflector-client",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no send-community",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_soft_reconfiguration_soo_merged(self):
        # test merged for soft_reconfiguration_inbound, soo
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    soft-reconfiguration inbound always
                    soo 65:28
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    soft_reconfiguration_inbound=dict(
                                        set=True
                                    ),
                                    soo="73:43",
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            soft_reconfiguration_inbound=dict(
                                                always=True
                                            ),
                                            soo="65:28",
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            soft_reconfiguration_inbound=dict(
                                                always=True
                                            ),
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "soft-reconfiguration inbound",
            "soo 73:43",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "soft-reconfiguration inbound always",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_soft_reconfiguration_soo_replaced(self):
        # test replaced for soft_reconfiguration_inbound, soo
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                  soft-reconfiguration inbound
                  soo 73:43
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    soft-reconfiguration inbound always
                    soo 65:28
                  address-family ipv4 multicast
                    soft-reconfiguration inbound always
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    soft_reconfiguration_inbound=dict(
                                        set=True
                                    ),
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            soft_reconfiguration_inbound=dict(
                                                always=True
                                            ),
                                            soo="65:28",
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no soo 73:43",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no soft-reconfiguration inbound always",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_suppress_inactive_unsuppress_merged(self):
        # test merged for suppress_inactive, unsuppress_map, weight
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    suppress-inactive
                    unsuppress-map rmap1
                  address-family ipv4 multicast
                    weight 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    suppress_inactive=True,
                                    unsuppress_map="rmap2",
                                    weight=20,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            suppress_inactive=True,
                                            unsuppress_map="rmap1",
                                            weight=25,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            suppress_inactive=True,
                                            unsuppress_map="rmap4",
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "suppress-inactive",
            "unsuppress-map rmap2",
            "weight 20",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "weight 25",
            "address-family ipv4 multicast",
            "suppress-inactive",
            "unsuppress-map rmap4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_suppress_inactive_unsuppress_replaced(self):
        # test replaced for suppress_inactive, unsuppress_map, weight
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
               neighbor 10.0.0.2
                address-family ipv4 multicast
                  suppress-inactive
                  unsuppress-map rmap2
                  weight 20
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                    suppress-inactive
                    unsuppress-map rmap1
                    weight 25
                  address-family ipv4 multicast
                    suppress-inactive
                    unsuppress-map rmap4
                    weight 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast")
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            suppress_inactive=True,
                                            unsuppress_map="rmap1",
                                            weight=25,
                                        ),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "no suppress-inactive",
            "no unsuppress-map rmap2",
            "no weight 20",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 multicast",
            "no suppress-inactive",
            "no unsuppress-map rmap4",
            "no weight 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_deleted(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
               neighbor 10.0.0.2
                address-family ipv4 multicast
                address-family ipv6 unicast
                address-family link-state
               neighbor 10.0.0.3
                 address-family ipv4 unicast
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                  address-family ipv4 multicast
                  address-family ipv6 unicast
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast"),
                                dict(afi="link-state"),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(afi="ipv4", safi="unicast"),
                                        dict(afi="ipv4", safi="multicast"),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "no address-family ipv4 multicast",
            "no address-family link-state",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "no address-family ipv4 unicast",
            "no address-family ipv4 multicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_deleted_all(self):
        # test deleted all
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                address-family ipv6 unicast
                address-family link-state
              neighbor 10.0.0.3
                address-family ipv4 unicast
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                  address-family ipv4 multicast
                  address-family ipv6 unicast
            """
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "no address-family ipv4 unicast",
            "no address-family ipv4 multicast",
            "no address-family link-state",
            "neighbor 10.0.0.3",
            "no address-family ipv4 unicast",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "no address-family ipv4 unicast",
            "no address-family ipv4 multicast",
            "no address-family ipv6 unicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_overridden(self):
        # test overridden
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
                address-family ipv6 unicast
                address-family link-state
              neighbor 10.0.0.3
                address-family ipv4 unicast
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 unicast
                  address-family ipv4 multicast
                  address-family ipv6 unicast
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.3",
                            address_family=[
                                dict(afi="ipv4", safi="unicast"),
                                dict(
                                    afi="link-state",
                                    route_reflector_client=True,
                                ),
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(afi="ipv4", safi="multicast")
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "no address-family ipv4 unicast",
            "no address-family ipv4 multicast",
            "no address-family link-state",
            "neighbor 10.0.0.3",
            "address-family link-state",
            "route-reflector-client",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "no address-family ipv4 multicast",
            "no address-family ipv6 unicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nbr_af_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.3
                address-family ipv4 unicast
                address-family link-state
              vrf site-1
                neighbor 192.168.1.1
                  address-family ipv4 multicast
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = dict(
            as_number="65536",
            neighbors=[
                dict(
                    neighbor_address="10.0.0.3",
                    address_family=[
                        dict(afi="ipv4", safi="unicast"),
                        dict(afi="link-state"),
                    ],
                )
            ],
            vrfs=[
                dict(
                    vrf="site-1",
                    neighbors=[
                        dict(
                            neighbor_address="192.168.1.1",
                            address_family=[
                                dict(afi="ipv4", safi="multicast")
                            ],
                        )
                    ],
                )
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_bgp_nbr_af_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65536
                      neighbor 10.0.0.3
                        address-family ipv4 unicast
                        address-family link-state
                      vrf site-1
                        neighbor 192.168.1.1
                          address-family ipv4 multicast
                    """
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )
        parsed = dict(
            as_number="65536",
            neighbors=[
                dict(
                    neighbor_address="10.0.0.3",
                    address_family=[
                        dict(afi="ipv4", safi="unicast"),
                        dict(afi="link-state"),
                    ],
                )
            ],
            vrfs=[
                dict(
                    vrf="site-1",
                    neighbors=[
                        dict(
                            neighbor_address="192.168.1.1",
                            address_family=[
                                dict(afi="ipv4", safi="multicast")
                            ],
                        )
                    ],
                )
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_bgp_nbr_af_rendered(self):
        # test rendered
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    suppress_inactive=True,
                                    unsuppress_map="rmap2",
                                    weight=20,
                                )
                            ],
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            neighbors=[
                                dict(
                                    neighbor_address="192.168.1.1",
                                    address_family=[
                                        dict(
                                            afi="ipv4",
                                            safi="unicast",
                                            suppress_inactive=True,
                                            unsuppress_map="rmap1",
                                            weight=25,
                                        ),
                                        dict(
                                            afi="ipv4",
                                            safi="multicast",
                                            suppress_inactive=True,
                                            unsuppress_map="rmap4",
                                        ),
                                    ],
                                )
                            ],
                        )
                    ],
                ),
                state="rendered",
            ),
            ignore_provider_arg,
        )
        rendered = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family ipv4 multicast",
            "suppress-inactive",
            "unsuppress-map rmap2",
            "weight 20",
            "vrf site-1",
            "neighbor 192.168.1.1",
            "address-family ipv4 unicast",
            "suppress-inactive",
            "unsuppress-map rmap1",
            "weight 25",
            "address-family ipv4 multicast",
            "suppress-inactive",
            "unsuppress-map rmap4",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(rendered))

    def test_nxos_bgp_nbr_af_gathered_empty(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = dict()
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_bgp_nbr_af_gathered_only_asn(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = dict(as_number="65563")
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_bgp_nbr_af_no_cmd(self):
        # test merged for rewrite_evpn_rt_asn, route_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family ipv4 multicast
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(afi="ipv4", safi="multicast")
                            ],
                        )
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_af_send_community(self):
        # test merged for send_community
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
              neighbor 10.0.0.2
                address-family l2vpn evpn
              neighbor 10.0.0.3
                address-family l2vpn evpn
                  send-community
                  send-community extended
            """
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbors=[
                        dict(
                            neighbor_address="10.0.0.2",
                            address_family=[
                                dict(
                                    afi="l2vpn",
                                    safi="evpn",
                                    send_community=dict(both=True),
                                )
                            ],
                        ),
                        dict(
                            neighbor_address="10.0.0.3",
                            address_family=[
                                dict(
                                    afi="l2vpn",
                                    safi="evpn",
                                    send_community=dict(both=True),
                                )
                            ],
                        ),
                        dict(
                            neighbor_address="10.0.0.4",
                            address_family=[
                                dict(
                                    afi="l2vpn",
                                    safi="evpn",
                                    send_community=dict(set=True),
                                )
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "neighbor 10.0.0.2",
            "address-family l2vpn evpn",
            "send-community",
            "send-community extended",
            "neighbor 10.0.0.4",
            "address-family l2vpn evpn",
            "send-community",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
