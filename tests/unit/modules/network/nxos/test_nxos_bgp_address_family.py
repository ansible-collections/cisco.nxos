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
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_bgp_address_family

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosBGPAddressFamilyModule(TestNxosModule):
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

    module = nxos_bgp_address_family

    def setUp(self):
        super(TestNxosBGPAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bgp_address_family.bgp_address_family.Bgp_address_familyFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBGPAddressFamilyModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_bgp_additional_paths_merged(self):
        # test merged for config->address_family->additional_paths
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  additional-paths install backup
                  additional-paths send
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            additional_paths=dict(
                                install_backup=True,
                                receive=True,
                                selection=dict(route_map="rmap1"),
                                send=True,
                            ),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            additional_paths=dict(
                                install_backup=False,
                                receive=True,
                                selection=dict(route_map="rmap2"),
                                send=False,
                            ),
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

    def test_nxos_bgp_additional_paths_replaced(self):
        # test replaced for config->address_family->additional_paths
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                additional-paths install backup
                additional-paths receive
                additional-paths selection route-map rmap1
                additional-paths send
              vrf site-1
                address-family ipv4 unicast
                  additional-paths send
              vrf site-2
                address-family ipv6 multicast
                  additional-paths receive
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            additional_paths=dict(selection=dict(route_map="rmap1")),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            additional_paths=dict(install_backup=True),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no additional-paths install backup",
            "no additional-paths receive",
            "no additional-paths send",
            "vrf site-1",
            "address-family ipv4 unicast",
            "additional-paths install backup",
            "no additional-paths send",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_l2vpn_keys_merged(self):
        # test merged for config->address_family->advertise_pip, advertise_system_mac, allow_vni_in_ethertag
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family l2vpn evpn
                advertise-pip
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="l2vpn",
                            safi="evpn",
                            advertise_pip=False,
                            advertise_system_mac=True,
                            allow_vni_in_ethertag=True,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family l2vpn evpn",
            "no advertise-pip",
            "advertise-system-mac",
            "allow-vni-in-ethertag",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_l2vpn_keys_replaced(self):
        # test replaced for config->address_family->advertise_pip, advertise_system_mac, allow_vni_in_ethertag
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family l2vpn evpn
                advertise-system-mac
                allow-vni-in-ethertag
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[dict(afi="l2vpn", safi="evpn", advertise_pip=True)],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family l2vpn evpn",
            "advertise-pip",
            "no advertise-system-mac",
            "no allow-vni-in-ethertag",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_client_to_client_merged(self):
        # test merged for config->address_family->client_to_client
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  no client-to-client reflection
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            client_to_client=dict(no_reflection=True),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            client_to_client=dict(no_reflection=False),
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
            "no client-to-client reflection",
            "vrf site-1",
            "address-family ipv4 unicast",
            "client-to-client reflection",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_client_to_client_replaced(self):
        # test replaced for config->address_family->client_to_client
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 unicast
                no client-client reflection
              address-family ipv4 multicast
              vrf site-1
                address-family ipv4 unicast
                  no client-to-client reflection
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            client_to_client=dict(no_reflection=True),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            client_to_client=dict(no_reflection=True),
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
            "client-to-client reflection",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_aggregate_address_merged(self):
        # test merged for config->address_family->aggregate_address
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  aggregate-address 192.168.1.0/24 as-set
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(prefix="192.168.1.0/24", summary_only=True),
                                dict(
                                    prefix="192.168.2.0/24",
                                    advertise_map="rmap1",
                                    as_set=True,
                                    attribute_map="rmap2",
                                ),
                                dict(
                                    prefix="192.168.3.0/24",
                                    suppress_map="rmap3",
                                ),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            aggregate_address=[
                                dict(prefix="10.0.0.0/8", summary_only=True),
                                dict(
                                    prefix="11.0.0.0/8",
                                    advertise_map="rmap1",
                                    as_set=True,
                                    attribute_map="rmap2",
                                ),
                            ],
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
            "aggregate-address 192.168.1.0/24 summary-only",
            "aggregate-address 192.168.2.0/24 advertise-map rmap1 as-set attribute-map rmap2",
            "aggregate-address 192.168.3.0/24 suppress-map rmap3",
            "vrf site-1",
            "address-family ipv4 unicast",
            "aggregate-address 10.0.0.0/8 summary-only",
            "aggregate-address 11.0.0.0/8 advertise-map rmap1 as-set attribute-map rmap2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_aggregate_address_replaced(self):
        # test replaced for config->address_family->aggregate_address
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                aggregate-address 192.168.1.0/24 summary-only
                aggregate-address 192.168.2.0/24 advertise-map rmap1 as-set attribute-map rmap2
                aggregate-address 192.168.3.0/24 suppress-map rmap3
              address-family ipv4 unicast
                aggregate-address 192.168.4.0/24 summary-only
              vrf site-1
                address-family ipv4 unicast
                aggregate-address 10.0.0.0/8 summary-only
                aggregate-address 11.0.0.0/8 advertise-map rmap1 as-set attribute-map rmap2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            aggregate_address=[
                                dict(
                                    prefix="192.168.2.0/24",
                                    advertise_map="rmap1",
                                    as_set=True,
                                    attribute_map="rmap2",
                                ),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            aggregate_address=[
                                dict(prefix="12.0.0.0/8", summary_only=True),
                                dict(
                                    prefix="14.0.0.0/8",
                                    advertise_map="rmap1",
                                    as_set=True,
                                    attribute_map="rmap3",
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "aggregate-address 192.168.2.0/24 advertise-map rmap1 as-set attribute-map rmap2",
            "no aggregate-address 192.168.1.0/24 summary-only",
            "no aggregate-address 192.168.3.0/24 suppress-map rmap3",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no aggregate-address 10.0.0.0/8 summary-only",
            "aggregate-address 12.0.0.0/8 summary-only",
            "aggregate-address 14.0.0.0/8 advertise-map rmap1 as-set attribute-map rmap3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampen_igp_metric_merged(self):
        # test merged for config->address_family->dampen_igp_metric
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  dampen-igp-metric 1200
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast", dampen_igp_metric=300),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            dampen_igp_metric=1800,
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
            "dampen-igp-metric 300",
            "vrf site-1",
            "address-family ipv4 unicast",
            "dampen-igp-metric 1800",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampen_igp_metric_replaced(self):
        # test merged for config->address_family->dampen_igp_metric
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                dampen-igp-metric 300
              vrf site-1
                address-family ipv4 unicast
                  dampen-igp-metric 1800
                address-family ipv6 unicast
                  dampen-igp-metric 1200
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            dampen_igp_metric=1800,
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no dampen-igp-metric 300",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampening_merged(self):
        # test merged for config->address_family->dampening
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 unicast
                dampening
              vrf site-1
                address-family ipv4 unicast
                  dampening 3 22 23 23
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="unicast",
                            dampening=dict(set=False),
                        ),
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            dampening=dict(
                                decay_half_life=4,
                                start_reuse_route=23,
                                start_suppress_route=24,
                                max_suppress_time=25,
                            ),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            dampening=dict(
                                decay_half_life=3,
                                start_reuse_route=22,
                                start_suppress_route=23,
                                max_suppress_time=24,
                            ),
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 unicast",
            "no dampening",
            "address-family ipv4 multicast",
            "dampening 4 23 24 25",
            "vrf site-1",
            "address-family ipv4 unicast",
            "dampening 3 22 23 24",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampening_replaced(self):
        # test replaced for config->address_family->dampening
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                dampening 4 23 24 25
              address-family ipv4 unicast
                dampening 4 23 25 27
              vrf site-1
                address-family ipv4 unicast
                  dampening 3 22 23 23
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            dampening=dict(
                                decay_half_life=3,
                                start_reuse_route=22,
                                start_suppress_route=23,
                                max_suppress_time=23,
                            ),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no dampening 4 23 24 25",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampening_route_map_merged(self):
        # test merged for config->address_family->dampening->route_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  dampening route-map rmap1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            dampening=dict(route_map="rmap3"),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            dampening=dict(route_map="rmap2"),
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
            "dampening route-map rmap3",
            "vrf site-1",
            "address-family ipv4 unicast",
            "dampening route-map rmap2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_dampening_route_map_replaced(self):
        # test replaced for config->address_family->dampening->route_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                dampening route-map rmap3
              vrf site-1
                address-family ipv4 unicast
                  dampening route-map rmap1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            dampening=dict(route_map="rmap3"),
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no dampening route-map rmap1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_default_information_merged(self):
        # test merged for config->address_family->default_information
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  default-information originate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            default_information=dict(originate=True),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            default_information=dict(originate=False),
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
            "default-information originate",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no default-information originate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_default_information_replaced(self):
        # test replaced for config->address_family->default_information
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                default-information originate
              vrf site-1
                address-family ipv4 unicast
                  default-information originate
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            default_information=dict(originate=True),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no default-information originate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_default_metric_merged(self):
        # test merged for config->address_family->default_metric
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  default-metric 6400
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast", default_metric=7200),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            default_metric=10000,
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
            "default-metric 7200",
            "vrf site-1",
            "address-family ipv4 unicast",
            "default-metric 10000",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_default_metric_replaced(self):
        # test replaced for config->address_family->default_metric
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                default-metric 7200
              addres-family ipv6 unicast
                default-metric 8400
              vrf site-1
                address-family ipv4 unicast
                  default-metric 6400
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            default_metric=6400,
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no default-metric 8400",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_distance_merged(self):
        # test merged for config->address_family->distance
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  distance 20 18 2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            distance=dict(ebgp_routes=25, ibgp_routes=12, local_routes=4),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            distance=dict(ebgp_routes=20, ibgp_routes=18, local_routes=3),
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
            "distance 25 12 4",
            "vrf site-1",
            "address-family ipv4 unicast",
            "distance 20 18 3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_distance_replaced(self):
        # test replaced for config->address_family->distance
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                distance 25 12 4
              address-family ipv4 unicast
                distance 26 12 4
              vrf site-1
                address-family ipv4 unicast
                  distance 20 18 2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            distance=dict(ebgp_routes=20, ibgp_routes=18, local_routes=2),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no distance 25 12 4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_export_gateway_ip_merged(self):
        # test merged for config->address_family->export_gateway_ip
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  export-gateway-ip
              vrf site-2
                address-family ipv4 unicast
                  export-gateway-ip
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            export_gateway_ip=False,
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="multicast",
                            export_gateway_ip=True,
                        ),
                        dict(
                            vrf="site-2",
                            afi="ipv4",
                            safi="multicast",
                            export_gateway_ip=True,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no export-gateway-ip",
            "address-family ipv4 multicast",
            "export-gateway-ip",
            "vrf site-2",
            "address-family ipv4 multicast",
            "export-gateway-ip",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_export_gateway_ip_replaced(self):
        # test replaced for config->address_family->export_gateway_ip
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  export-gateway-ip
                address-family ipv4 multicast
                  export-gateway-ip
              vrf site-2
                address-family ipv4 unicast
                  export-gateway-ip
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            export_gateway_ip=False,
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="multicast"),
                        dict(
                            vrf="site-2",
                            afi="ipv4",
                            safi="unicast",
                            export_gateway_ip=True,
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no export-gateway-ip",
            "address-family ipv4 multicast",
            "no export-gateway-ip",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_inject_map_merged(self):
        # test merged for config->address_family->inject_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  inject-map rmap1 exist-map rmap2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            inject_map=[
                                dict(
                                    route_map="rmap1",
                                    exist_map="rmap2",
                                    copy_attributes=True,
                                ),
                                dict(route_map="rmap1", exist_map="rmap3"),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            inject_map=[
                                dict(
                                    route_map="rmap3",
                                    exist_map="rmap4",
                                    copy_attributes=True,
                                ),
                            ],
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
            "inject-map rmap1 exist-map rmap2 copy-attributes",
            "inject-map rmap1 exist-map rmap3",
            "vrf site-1",
            "address-family ipv4 unicast",
            "inject-map rmap3 exist-map rmap4 copy-attributes",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_inject_map_replaced(self):
        # test replaced for config->address_family->inject_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                inject-map rmap1 exist-map rmap2 copy-attributes
                inject-map rmap1 exist-map rmap3
              vrf site-1
                address-family ipv4 unicast
                  inject-map rmap3 exist-map rmap4 copy-attributes
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            inject_map=[dict(route_map="rmap1", exist_map="rmap3")],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            inject_map=[
                                dict(
                                    route_map="rmap3",
                                    exist_map="rmap4",
                                    copy_attributes=True,
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no inject-map rmap1 exist-map rmap2 copy-attributes",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_maximum_paths_merged(self):
        # test merged for config->address_family->maximum_paths
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                maximum-paths 12
              vrf site-1
                address-family ipv4 unicast
                  maximum-paths 14
                  maximum-paths eibgp 64
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            maximum_paths=dict(parallel_paths=15, ibgp=dict(parallel_paths=64)),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            maximum_paths=dict(
                                parallel_paths=14,
                                eibgp=dict(parallel_paths=68),
                                local=dict(parallel_paths=30),
                            ),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="multicast",
                            maximum_paths=dict(mixed=dict(parallel_paths=40)),
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
            "maximum-paths 15",
            "maximum-paths ibgp 64",
            "vrf site-1",
            "address-family ipv4 unicast",
            "maximum-paths eibgp 68",
            "maximum-paths local 30",
            "address-family ipv4 multicast",
            "maximum-paths mixed 40",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_maximum_paths_replaced(self):
        # test replaced for config->address_family->maximum_paths
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                maximum-paths 15
                maximum-paths ibgp 64
              vrf site-1
                address-family ipv4 unicast
                  maximum-paths eibgp 68
                  maximum-paths local 30
                address-family ipv4 multicast
                  maximum-paths mixed 40
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            maximum_paths=dict(parallel_paths=15, ibgp=dict(parallel_paths=64)),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            maximum_paths=dict(local=dict(parallel_paths=30)),
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="multicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no maximum-paths eibgp 68",
            "address-family ipv4 multicast",
            "no maximum-paths mixed 40",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_network_merged(self):
        # test merged for config->address_family->network
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  network 192.168.1.0/24 route-map rmap1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            networks=[
                                dict(prefix="192.168.1.0/24", route_map="rmap2"),
                                dict(prefix="192.168.2.0/24"),
                                dict(prefix="192.168.3.0/24", route_map="rmap3"),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            networks=[
                                dict(prefix="10.0.0.0/8"),
                                dict(prefix="11.0.0.0/8", route_map="rmap2"),
                            ],
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
            "network 192.168.1.0/24 route-map rmap2",
            "network 192.168.2.0/24",
            "network 192.168.3.0/24 route-map rmap3",
            "vrf site-1",
            "address-family ipv4 unicast",
            "network 10.0.0.0/8",
            "network 11.0.0.0/8 route-map rmap2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_network_replaced(self):
        # test replaced for config->address_family->network
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                network 192.168.1.0/24 route-map rmap2
                network 192.168.2.0/24
                network 192.168.3.0/24 route-map rmap3
              vrf site-1
                address-family ipv4 unicast
                  network 10.0.0.0/8
                  network 11.0.0.0/8 route-map rmap2
                  network 192.168.1.0/24 route-map rmap1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            networks=[dict(prefix="192.168.3.0/24", route_map="rmap4")],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            networks=[dict(prefix="11.0.0.0/8", route_map="rmap2")],
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no network 192.168.1.0/24 route-map rmap2",
            "no network 192.168.2.0/24",
            "network 192.168.3.0/24 route-map rmap4",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no network 10.0.0.0/8",
            "no network 192.168.1.0/24 route-map rmap1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nexthop_merged(self):
        # test merged for config->address_family->network
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  nexthop route-map rmap2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            nexthop=dict(
                                route_map="rmap1",
                                trigger_delay=dict(critical_delay=120, non_critical_delay=180),
                            ),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            nexthop=dict(
                                trigger_delay=dict(critical_delay=110, non_critical_delay=170),
                            ),
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
            "nexthop route-map rmap1",
            "nexthop trigger-delay critical 120 non-critical 180",
            "vrf site-1",
            "address-family ipv4 unicast",
            "nexthop trigger-delay critical 110 non-critical 170",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_nexthop_replaced(self):
        # test replaced for config->address_family->network
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                nexthop route-map rmap1
                nexthop trigger-delay critical 120 non-critical 180
              vrf site-1
                address-family ipv4 unicast
                  nexthop route-map rmap2
                  nexthop trigger-delay critical 110 non-critical 170
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            nexthop=dict(route_map="rmap1"),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            nexthop=dict(
                                trigger_delay=dict(critical_delay=110, non_critical_delay=170),
                            ),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no nexthop trigger-delay critical 120 non-critical 180",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no nexthop route-map rmap2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_redistribute_merged(self):
        # test merged for config->address_family->redistribute
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  redistribute eigrp 100 route-map test-17
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number=65563,
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="test-1",
                                ),
                                dict(
                                    protocol="eigrp",
                                    id="101",
                                    route_map="test-2",
                                ),
                                dict(protocol="static", route_map="test-4"),
                                dict(protocol="hmm", route_map="test-5"),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="test-18",
                                ),
                                dict(
                                    protocol="ospf",
                                    id="101",
                                    route_map="test-2",
                                ),
                            ],
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
            "redistribute eigrp 100 route-map test-1",
            "redistribute eigrp 101 route-map test-2",
            "redistribute static route-map test-4",
            "redistribute hmm route-map test-5",
            "vrf site-1",
            "address-family ipv4 unicast",
            "redistribute eigrp 100 route-map test-18",
            "redistribute ospf 101 route-map test-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_redistribute_replaced(self):
        # test replaced for config->address_family->redistribute
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                redistribute eigrp 100 route-map test-1
                redistribute eigrp 101 route-map test-2
                redistribute static route-map test-4
                redistribute hmm route-map test-5
              vrf site-1
                address-family ipv4 unicast
                  redistribute eigrp 100 route-map test-18
                  redistribute ospf 101 route-map test-2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number=65563,
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="test-1",
                                ),
                                dict(protocol="static", route_map="test-5"),
                                dict(protocol="hmm", route_map="test-5"),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            redistribute=[
                                dict(
                                    protocol="ospf",
                                    id="101",
                                    route_map="test-2",
                                ),
                            ],
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no redistribute eigrp 101 route-map test-2",
            "redistribute static route-map test-5",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no redistribute eigrp 100 route-map test-18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_retain_merged(self):
        # test merged for config->address_family->retain
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  retain route-target all
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            retain=dict(route_target=dict(retain_all=True)),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            retain=dict(route_target=dict(route_map="rmap1")),
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
            "retain route-target all",
            "vrf site-1",
            "address-family ipv4 unicast",
            "retain route-target route-map rmap1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_retain_replaced(self):
        # test replaced for config->address_family->retain
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                retain route-target all
              vrf site-1
                address-family ipv4 unicast
                  retain route-target route-map rmap1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            retain=dict(route_target=dict(retain_all=True)),
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no retain route-target route-map rmap1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_suppress_inactive_merged(self):
        # test merged for config->address_family->suppress_inactive
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  suppress-inactive
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            suppress_inactive=True,
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            suppress_inactive=False,
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
            "suppress-inactive",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no suppress-inactive",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_suppress_inactive_replaced(self):
        # test replaced for config->address_family->suppress_inactive
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                suppress-inactive
              vrf site-1
                address-family ipv4 unicast
                  suppress-inactive
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            suppress_inactive=True,
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no suppress-inactive",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_table_map_merged(self):
        # test merged for config->address_family->table_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  table-map rmap1 filter
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            table_map=dict(name="rmap2", filter=True),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            table_map=dict(name="rmap1", filter=True),
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
            "table-map rmap2 filter",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_table_map_replaced(self):
        # test replaced for config->address_family->table_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  table-map rmap1 filter
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            table_map=dict(name="rmap2", filter=True),
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "table-map rmap2 filter",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no table-map rmap1 filter",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_timers_merged(self):
        # test merged for config->address_family->table_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            timers=dict(
                                bestpath_defer=dict(defer_time=120, maximum_defer_time=380),
                            ),
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            timers=dict(
                                bestpath_defer=dict(defer_time=110, maximum_defer_time=350),
                            ),
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
            "timers bestpath-defer 120 maximum 380",
            "vrf site-1",
            "address-family ipv4 unicast",
            "timers bestpath-defer 110 maximum 350",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_timers_replaced(self):
        # test replaced for config->address_family->table_map
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                timers bestpath-defer 120 maximum 380
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            timers=dict(
                                bestpath_defer=dict(defer_time=120, maximum_defer_time=380),
                            ),
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no timers bestpath-defer 100 maximum 350",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_wait_igp_convergence_merged(self):
        # test merged for config->address_family->wait_igp_convergence
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
                  wait-igp-convergence
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            wait_igp_convergence=True,
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            wait_igp_convergence=False,
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
            "wait-igp-convergence",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no wait-igp-convergence",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_wait_igp_convergence_replaced(self):
        # test replaced for config->address_family->wait_igp_convergence
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
              vrf site-1
                address-family ipv4 unicast
                  wait-igp-convergence
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(
                            afi="ipv4",
                            safi="unicast",
                            wait_igp_convergence=True,
                        ),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "no wait-igp-convergence",
            "address-family ipv4 unicast",
            "wait-igp-convergence",
            "vrf site-1",
            "address-family ipv4 unicast",
            "no wait-igp-convergence",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_af_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    router bgp 65563
                      address-family ipv4 multicast
                        wait-igp-convergence
                      vrf site-1
                        address-family ipv4 unicast
                          timers bestpath-defer 100 maximum 350
                    """,
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )
        parsed = dict(
            as_number="65563",
            address_family=[
                dict(afi="ipv4", safi="multicast", wait_igp_convergence=True),
                dict(
                    vrf="site-1",
                    afi="ipv4",
                    safi="unicast",
                    timers=dict(bestpath_defer=dict(defer_time=100, maximum_defer_time=350)),
                ),
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_bgp_af_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
              neighbor 192.168.1.0
                address-family ipv6 unicast
              neighbor 192.168.2.0
                address-family ipv6 multicast
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
                neighbor 192.168.3.0
                  address-family ipv6 multicast
            """,
        )

        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = dict(
            as_number="65563",
            address_family=[
                dict(afi="ipv4", safi="multicast", wait_igp_convergence=True),
                dict(
                    vrf="site-1",
                    afi="ipv4",
                    safi="unicast",
                    timers=dict(bestpath_defer=dict(defer_time=100, maximum_defer_time=350)),
                ),
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_bgp_af_gathered_empty(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            """,
        )

        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})

    def test_nxos_bgp_af_rendered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number=65563,
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            redistribute=[
                                dict(
                                    protocol="eigrp",
                                    id="100",
                                    route_map="test-1",
                                ),
                                dict(protocol="static", route_map="test-5"),
                            ],
                        ),
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            redistribute=[
                                dict(
                                    protocol="ospf",
                                    id="101",
                                    route_map="test-2",
                                ),
                            ],
                        ),
                    ],
                ),
                state="rendered",
            ),
            ignore_provider_arg,
        )
        rendered = [
            "router bgp 65563",
            "address-family ipv4 multicast",
            "redistribute eigrp 100 route-map test-1",
            "redistribute static route-map test-5",
            "vrf site-1",
            "address-family ipv4 unicast",
            "redistribute ospf 101 route-map test-2",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(rendered))

    def test_nxos_bgp_af_delete(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
              neighbor 192.168.1.0
                address-family ipv6 unicast
              neighbor 192.168.2.0
                address-family ipv6 multicast
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
                address-family ipv6 multicast
                neighbor 192.168.3.0
                  address-family ipv6 multicast
              vrf site-2
                address-family ipv6 unicast
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(afi="ipv4", safi="multicast"),
                        dict(vrf="site-1", afi="ipv4", safi="unicast"),
                        dict(vrf="site-1", afi="ipv6", safi="multicast"),
                        dict(vrf="site-2", afi="ipv6", safi="unicast"),
                    ],
                ),
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "no address-family ipv4 multicast",
            "vrf site-1",
            "no address-family ipv4 unicast",
            "no address-family ipv6 multicast",
            "exit",
            "vrf site-2",
            "no address-family ipv6 unicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_af_idempotent(self):
        # test idempotent
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            wait_igp_convergence=True,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        self.execute_module(changed=False)

    def test_nxos_bgp_af_overridden(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
              neighbor 192.168.1.0
                address-family ipv6 unicast
              neighbor 192.168.2.0
                address-family ipv6 multicast
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
                address-family ipv6 multicast
                neighbor 192.168.3.0
                  address-family ipv6 multicast
              vrf site-2
                address-family ipv6 unicast
            """,
        )

        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            afi="ipv4",
                            safi="multicast",
                            wait_igp_convergence=False,
                        ),
                    ],
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "no address-family ipv4 unicast",
            "no address-family ipv6 multicast",
            "exit",
            "vrf site-2",
            "no address-family ipv6 unicast",
            "exit",
            "address-family ipv4 multicast",
            "no wait-igp-convergence",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_af_delete_1(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              address-family ipv4 multicast
                wait-igp-convergence
              address-family ipv6 unicast
              neighbor 192.168.1.0
                address-family ipv6 unicast
              neighbor 192.168.2.0
                address-family ipv6 multicast
              vrf site-1
                address-family ipv4 unicast
                  timers bestpath-defer 100 maximum 350
                address-family ipv6 multicast
                neighbor 192.168.3.0
                  address-family ipv6 multicast
              vrf site-2
                address-family ipv6 unicast
            """,
        )

        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "router bgp 65563",
            "no address-family ipv4 multicast",
            "no address-family ipv6 unicast",
            "vrf site-1",
            "no address-family ipv4 unicast",
            "no address-family ipv6 multicast",
            "exit",
            "vrf site-2",
            "no address-family ipv6 unicast",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_vrf_af_advertise_l2vpn_evpn(self):
        # test merged for config->vrf->address_family->advertise l2vpn evpn
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
              vrf site-2
                address-family ipv4 unicast
                  advertise l2vpn evpn
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            advertise_l2vpn_evpn=True,
                        ),
                        dict(
                            vrf="site-2",
                            afi="ipv4",
                            safi="unicast",
                            advertise_l2vpn_evpn=False,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "advertise l2vpn evpn",
            "vrf site-2",
            "address-family ipv4 unicast",
            "no advertise l2vpn evpn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_vrf_af_advertise_l2vpn_evpn_replaced(self):
        # test replaced for config->vrf->address_family->advertise l2vpn evpn
        self.get_config.return_value = dedent(
            """\
            router bgp 65563
              vrf site-1
                address-family ipv4 unicast
              vrf site-2
                address-family ipv4 unicast
                  advertise l2vpn evpn
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65563",
                    address_family=[
                        dict(
                            vrf="site-1",
                            afi="ipv4",
                            safi="unicast",
                            advertise_l2vpn_evpn=True,
                        ),
                        dict(vrf="site-2", afi="ipv4", safi="unicast"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65563",
            "vrf site-1",
            "address-family ipv4 unicast",
            "advertise l2vpn evpn",
            "vrf site-2",
            "address-family ipv4 unicast",
            "no advertise l2vpn evpn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
