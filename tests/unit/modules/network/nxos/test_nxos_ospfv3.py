# (c) 2019 Red Hat Inc.
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
from ansible_collections.cisco.nxos.plugins.modules import nxos_ospfv3

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosOspfv3Module(TestNxosModule):

    module = nxos_ospfv3

    def setUp(self):
        super(TestNxosOspfv3Module, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ospfv3.ospfv3.Ospfv3Facts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosOspfv3Module, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_ospfv3_af_areas_filter_list_merged(self):
        # test merged for config->processes->af->areas->filter_list
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 100
                area 1.1.1.1 filter-list route-map test-11 in
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        filter_list=[
                                            dict(
                                                route_map="test-1",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-2",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        filter_list=[
                                            dict(
                                                route_map="test-3",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-4",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 filter-list route-map test-1 in",
            "area 1.1.1.1 filter-list route-map test-2 out",
            "area 1.1.1.2 filter-list route-map test-3 in",
            "area 1.1.1.2 filter-list route-map test-4 out",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_filter_list_replaced(self):
        # test replaced for config->processes->af->areas->filter_list
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.4 filter-list route-map test-11 out
                area 1.1.1.4 filter-list route-map test-12 in
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        filter_list=[
                                            dict(
                                                route_map="test-1",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-2",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        filter_list=[
                                            dict(
                                                route_map="test-3",
                                                direction="in",
                                            ),
                                            dict(
                                                route_map="test-4",
                                                direction="out",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.4 filter-list route-map test-11 out",
            "no area 1.1.1.4 filter-list route-map test-12 in",
            "area 1.1.1.1 filter-list route-map test-1 in",
            "area 1.1.1.1 filter-list route-map test-2 out",
            "area 1.1.1.2 filter-list route-map test-3 in",
            "area 1.1.1.2 filter-list route-map test-4 out",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_ranges_merged(self):
        # test merged for config->processes->af->areas->rang
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 range 2001:db2::/32
                area 1.1.1.1 range 2001:db3::/32 cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.1",
                                        ranges=[
                                            dict(
                                                prefix="2001:db3::/32",
                                                cost="20",
                                            )
                                        ],
                                    ),
                                    dict(
                                        area_id="1.1.1.2",
                                        ranges=[
                                            dict(
                                                prefix="2001:db4::/32", cost=11
                                            ),
                                            dict(
                                                prefix="2001:db5::/32",
                                                not_advertise=True,
                                            ),
                                            dict(
                                                prefix="2001:db7::/32",
                                                not_advertise=True,
                                                cost=18,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 range 2001:db3::/32 cost 20",
            "area 1.1.1.2 range 2001:db4::/32 cost 11",
            "area 1.1.1.2 range 2001:db5::/32 not-advertise",
            "area 1.1.1.2 range 2001:db7::/32 not-advertise cost 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_ranges_replaced(self):
        # test replaced for config->processes->af->areas->ranges
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 range 2001:db2::/32
                area 1.1.1.1 range 2001:db3::/32 cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(
                                        area_id="1.1.1.2",
                                        ranges=[
                                            dict(
                                                prefix="2001:db4::/32", cost=11
                                            ),
                                            dict(
                                                prefix="2001:db5::/32",
                                                not_advertise=True,
                                            ),
                                            dict(
                                                prefix="2001:db7::/32",
                                                not_advertise=True,
                                                cost=18,
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.1 range 2001:db2::/32",
            "no area 1.1.1.1 range 2001:db3::/32",
            "area 1.1.1.2 range 2001:db4::/32 cost 11",
            "area 1.1.1.2 range 2001:db5::/32 not-advertise",
            "area 1.1.1.2 range 2001:db7::/32 not-advertise cost 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_default_cost_merged(self):
        # test merged for config->processes->af->areas->default_cost
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(area_id="1.1.1.1", default_cost=12),
                                    dict(area_id="1.1.1.2", default_cost=200),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "area 1.1.1.1 default-cost 12",
            "area 1.1.1.2 default-cost 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_areas_default_cost_replaced(self):
        # test merged for config->processes->af->areas->default_cost
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                area 1.1.1.1 default-cost 10
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                areas=[
                                    dict(area_id="1.1.1.2", default_cost=200)
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no area 1.1.1.1 default-cost 10",
            "area 1.1.1.2 default-cost 200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_default_information_merged(self):
        # test merged for config->processes->af->default_information
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                default-information originate    
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                default_information=dict(
                                    originate=dict(
                                        always=True, route_map="test-2"
                                    )
                                ),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "default-information originate always route-map test-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_default_information_replaced(self):
        # test replaced for config->processes->af->default_information
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                default-information originate always test-2   
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                default_information=dict(
                                    originate=dict(set=True)
                                ),
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "default-information originate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_distance_merged(self):
        # test merged for config->processes->af->distance
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                distance 20
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6", safi="unicast", distance=35
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "distance 35",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_distance_replaced(self):
        # test replaced for config->processes->af->distance
        # `distance` is a linear attribute so replaced test
        # can only be removal of this attribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                distance 20
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no distance 20",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_maximum_paths_merged(self):
        # test merged for config->processes->af->maximum_paths
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                maximum-paths 18
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6", safi="unicast", maximum_paths=27
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "maximum-paths 27",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_maximum_paths_replaced(self):
        # test replaced for config->processes->af->maximum_paths
        # `maximum_paths` is a linear attribute so replaced test
        # can only be removal of this attribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                maximum-paths 18
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no maximum-paths 18",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_redistribute_merged(self):
        # test merged for config->processes->af->redistribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                redistribute eigrp 100 route-map test-17
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
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
                                    dict(
                                        protocol="bgp",
                                        id="65563",
                                        route_map="test-3",
                                    ),
                                    dict(
                                        protocol="static", route_map="test-4"
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "redistribute eigrp 100 route-map test-1",
            "redistribute eigrp 101 route-map test-2",
            "redistribute bgp 65563 route-map test-3",
            "redistribute static route-map test-4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_redistribute_replaced(self):
        # test replaced for config->processes->af->redistribute
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                redistribute eigrp 100 route-map test-1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                redistribute=[
                                    dict(
                                        protocol="eigrp",
                                        id="101",
                                        route_map="test-2",
                                    ),
                                    dict(
                                        protocol="bgp",
                                        id="65563",
                                        route_map="test-3",
                                    ),
                                    dict(
                                        protocol="static", route_map="test-4"
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no redistribute eigrp 100 route-map test-1",
            "redistribute eigrp 101 route-map test-2",
            "redistribute bgp 65563 route-map test-3",
            "redistribute static route-map test-4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_summary_address_merged(self):
        # test merged for config->processes->af->summary_address
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                summary_address=[
                                    dict(prefix="2001:db2::/32", tag=19),
                                    dict(
                                        prefix="2001:db3::/32",
                                        not_advertise=True,
                                    ),
                                ],
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "summary-address 2001:db2::/32 tag 19",
            "summary-address 2001:db3::/32 not-advertise",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_summary_address_replaced(self):
        # test replaced for config->processes->af->summary_address
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32 tag 19
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                summary_address=[
                                    dict(
                                        prefix="2001:db3::/32",
                                        not_advertise=True,
                                    )
                                ],
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no summary-address 2001:db2::/32 tag 19",
            "summary-address 2001:db3::/32 not-advertise",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_table_map_merged(self):
        # test merged for config->processes->af->table_map
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                summary-address 2001:db2::/32 tag 19
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                table_map=dict(name="test-1", filter=True),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "table-map test-1 filter",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_table_map_replaced(self):
        # test replaced for config->processes->af->table_map
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                table-map test-1 filter
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                table_map=dict(name="test-2"),
                            ),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "table-map test-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_timers_merged(self):
        # test merged for config->processes->af->timers
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                timers throttle spf 1000 20 2800
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(
                                afi="ipv6",
                                safi="unicast",
                                timers=dict(
                                    throttle=dict(
                                        spf=dict(
                                            initial_spf_delay=1100,
                                            max_wait_time=2805,
                                        )
                                    )
                                ),
                            ),
                        )
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "timers throttle spf 1100 20 2805",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ospfv3_af_timers_replaced(self):
        # test replaced for config->processes->af->timers
        self.get_config.return_value = dedent(
            """\
            router ospfv3 100
              address-family ipv6 unicast
                timers throttle spf 1000 20 2800
            """
        )
        set_module_args(
            dict(
                config=dict(
                    processes=[
                        dict(
                            process_id="100",
                            address_family=dict(afi="ipv6", safi="unicast"),
                        )
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router ospfv3 100",
            "address-family ipv6 unicast",
            "no timers throttle spf 1000 20 2800",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
