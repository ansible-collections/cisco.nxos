#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_static_routes

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosStaticRoutesModule(TestNxosModule):
    module = nxos_static_routes

    def setUp(self):
        super(TestNxosStaticRoutesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.static_routes.static_routes.Static_routesFacts.get_static_routes_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosStaticRoutesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_static_routes_all_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.80/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )

        config = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 3,
                                        "route_name": "replaced_route1",
                                    },
                                    {
                                        "interface": "Ethernet1/2",
                                        "forward_router_address": "192.0.2.45",
                                        "dest_vrf": "destinationVRF",
                                        "route_name": "replaced_route2",
                                    },
                                ],
                                "dest": "192.0.2.16/28",
                            },
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.26", "tag": 12},
                                ],
                                "dest": "192.0.2.80/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "Test",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.13"},
                                    {
                                        "forward_router_address": "192.0.2.14",
                                        "admin_distance": 5,
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "management",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.168.255.1"},
                                ],
                                "dest": "0.0.0.0/0",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "newvrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.10.3",
                                        "admin_distance": 11,
                                        "tag": 22323,
                                        "route_name": "test_name",
                                    },
                                ],
                                "dest": "10.0.10.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.11.10",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "forward_router_address": "10.0.11.12",
                                        "admin_distance": 11,
                                        "dest_vrf": "Test",
                                        "tag": 22,
                                    },
                                ],
                                "dest": "10.0.11.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "interface": "loopback22",
                                        "forward_router_address": "192.0.2.13",
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 5,
                                        "dest_vrf": "dest",
                                    },
                                    {
                                        "interface": "mgmt0",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "interface": "port-channel22",
                                        "forward_router_address": "2048:ae12::1",
                                    },
                                    {
                                        "interface": "Ethernet2/1",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 22,
                                        "route_name": "test_name2",
                                    },
                                ],
                                "dest": "2200:10::/36",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "trial_vrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.22", "tag": 4},
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 1,
                                        "route_name": "merged_route",
                                    },
                                ],
                                "dest": "192.0.2.64/28",
                            },
                        ],
                    },
                ],
            },
        ]

        for state in ["merged", "replaced", "overridden"]:
            set_module_args({"config": config, "state": state})
            result = self.execute_module(changed=False)
            self.assertEqual(result["commands"], [])

    def test_nxos_static_routes_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 3,
                                                "route_name": "replaced_route1",
                                            },
                                            {
                                                "interface": "Ethernet1/2",
                                                "forward_router_address": "192.0.2.45",
                                                "dest_vrf": "destinationVRF",
                                                "route_name": "replaced_route2",
                                            },
                                        ],
                                        "dest": "192.0.2.16/28",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.26",
                                                "tag": 12,
                                            },
                                        ],
                                        "dest": "192.0.2.80/28",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "Test",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {"forward_router_address": "192.0.2.13"},
                                            {
                                                "forward_router_address": "192.0.2.14",
                                                "admin_distance": 5,
                                            },
                                        ],
                                        "dest": "192.0.2.48/28",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "management",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {"forward_router_address": "192.168.255.1"},
                                        ],
                                        "dest": "0.0.0.0/0",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "newvrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.0.10.3",
                                                "admin_distance": 11,
                                                "tag": 22323,
                                                "route_name": "test_name",
                                            },
                                        ],
                                        "dest": "10.0.10.0/25",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "10.0.11.10",
                                                "admin_distance": 11,
                                                "tag": 22,
                                            },
                                            {
                                                "forward_router_address": "10.0.11.12",
                                                "admin_distance": 11,
                                                "dest_vrf": "Test",
                                                "tag": 22,
                                            },
                                        ],
                                        "dest": "10.0.11.0/25",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "interface": "loopback22",
                                                "forward_router_address": "192.0.2.13",
                                            },
                                        ],
                                        "dest": "192.0.2.48/28",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.15",
                                                "track": 1,
                                                "route_name": "new_route",
                                            },
                                        ],
                                        "dest": "192.0.2.49/28",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "2048:ae12::1",
                                                "admin_distance": 5,
                                                "dest_vrf": "dest",
                                            },
                                            {
                                                "interface": "mgmt0",
                                                "forward_router_address": "2048:ae12::1",
                                                "admin_distance": 11,
                                                "tag": 22,
                                            },
                                            {
                                                "interface": "port-channel22",
                                                "forward_router_address": "2048:ae12::1",
                                            },
                                            {
                                                "interface": "Ethernet2/1",
                                                "forward_router_address": "2048:ae12::1",
                                                "admin_distance": 22,
                                                "route_name": "test_name2",
                                            },
                                        ],
                                        "dest": "2200:10::/36",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "trial_vrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.22",
                                                "tag": 4,
                                            },
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 1,
                                                "route_name": "merged_route",
                                            },
                                        ],
                                        "dest": "192.0.2.64/28",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "ip route 192.0.2.80/28 192.0.2.26 tag 12",
            "ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2",
            "vrf context newvrf",
            "ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11",
            "ip route 10.0.11.0/25 10.0.11.10 tag 22 11",
            "ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11",
            "ip route 192.0.2.48/28 loopback22 192.0.2.13",
            "ip route 192.0.2.49/28 192.0.2.15 track 1 name new_route",
            "ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5",
            "ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11",
            "ipv6 route 2200:10::/36 port-channel22 2048:ae12::1",
            "ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22",
            "vrf context Test",
            "ip route 192.0.2.48/28 192.0.2.13",
            "ip route 192.0.2.48/28 192.0.2.14 5",
            "vrf context trial_vrf",
            "ip route 192.0.2.64/28 192.0.2.22 tag 4",
            "ip route 192.0.2.64/28 192.0.2.23 name merged_route 1",
            "vrf context management",
            "ip route 0.0.0.0/0 192.168.255.1",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.80/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 3,
                                                "route_name": "replaced_route1",
                                            },
                                            {
                                                "interface": "Ethernet1/2",
                                                "forward_router_address": "192.0.2.45",
                                                "dest_vrf": "destinationVRF",
                                                "route_name": "replaced_route2",
                                            },
                                        ],
                                        "dest": "192.0.2.16/28",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.27",
                                                "tag": 13,
                                            },
                                        ],
                                        "dest": "192.0.2.80/28",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "trial_vrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 1,
                                                "route_name": "merged_route",
                                            },
                                        ],
                                        "dest": "192.0.2.0/28",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "ip route 192.0.2.80/28 192.0.2.27 tag 13",
            "no ip route 192.0.2.80/28 192.0.2.26 tag 12",
            "vrf context trial_vrf",
            "ip route 192.0.2.0/28 192.0.2.23 name merged_route 1",
            "no ip route 192.0.2.64/28 192.0.2.22 tag 4",
            "no ip route 192.0.2.64/28 192.0.2.23 name merged_route 1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 3,
                                                "route_name": "replaced_route1",
                                            },
                                            {
                                                "interface": "Ethernet1/2",
                                                "forward_router_address": "192.0.2.45",
                                                "dest_vrf": "destinationVRF",
                                                "route_name": "replaced_route2",
                                            },
                                        ],
                                        "dest": "192.0.2.16/28",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.27",
                                                "tag": 13,
                                            },
                                        ],
                                        "dest": "192.0.2.80/28",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "trial_vrf",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 1,
                                                "route_name": "merged_route",
                                            },
                                        ],
                                        "dest": "192.0.2.0/28",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3",
            "ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2",
            "ip route 192.0.2.80/28 192.0.2.27 tag 13",
            "no ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3",
            "no ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2",
            "no ip route 192.0.2.79/28 192.0.2.26 tag 12",
            "vrf context trial_vrf",
            "ip route 192.0.2.0/28 192.0.2.23 name merged_route 1",
            "no ip route 192.0.2.64/28 192.0.2.22 tag 4",
            "no ip route 192.0.2.64/28 192.0.2.23 name merged_route 1",
            "vrf context Test",
            "no ip route 192.0.2.48/28 192.0.2.13",
            "no ip route 192.0.2.48/28 192.0.2.14 5",
            "vrf context management",
            "no ip route 0.0.0.0/0 192.168.255.1",
            "vrf context newvrf",
            "no ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11",
            "no ip route 10.0.11.0/25 10.0.11.10 tag 22 11",
            "no ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11",
            "no ip route 192.0.2.48/28 loopback22 192.0.2.13",
            "no ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5",
            "no ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11",
            "no ipv6 route 2200:10::/36 port-channel22 2048:ae12::1",
            "no ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_deletedvrf(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(dict(config=[dict(vrf="Test")], state="deleted"))
        commands = [
            "vrf context Test",
            "no ip route 192.0.2.48/28 192.0.2.13",
            "no ip route 192.0.2.48/28 192.0.2.14 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_deletedafi(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[dict(address_families=[dict(afi="ipv4")])],
                state="deleted",
            ),
        )
        commands = [
            "no ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3",
            "no ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2",
            "no ip route 192.0.2.79/28 192.0.2.26 tag 12",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_deleteddest(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="Test",
                        address_families=[
                            dict(afi="ipv4", routes=[dict(dest="192.0.2.48/28")]),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        commands = [
            "vrf context Test",
            "no ip route 192.0.2.48/28 192.0.2.13",
            "no ip route 192.0.2.48/28 192.0.2.14 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_deletedroute(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.23",
                                                "admin_distance": 3,
                                                "route_name": "replaced_route1",
                                            },
                                            {
                                                "interface": "Ethernet1/2",
                                                "forward_router_address": "192.0.2.45",
                                                "dest_vrf": "destinationVRF",
                                                "route_name": "replaced_route2",
                                            },
                                        ],
                                        "dest": "192.0.2.16/28",
                                    },
                                    {
                                        "next_hops": [
                                            {
                                                "forward_router_address": "192.0.2.26",
                                                "tag": 12,
                                            },
                                        ],
                                        "dest": "192.0.2.80/28",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "vrf": "Test",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "routes": [
                                    {
                                        "next_hops": [
                                            {"forward_router_address": "192.0.2.13"},
                                            {
                                                "forward_router_address": "192.0.2.14",
                                                "admin_distance": 5,
                                            },
                                        ],
                                        "dest": "192.0.2.48/28",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "no ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3",
            "no ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2",
            "no ip route 192.0.2.79/28 192.0.2.26 tag 12",
            "vrf context Test",
            "no ip route 192.0.2.48/28 192.0.2.13",
            "no ip route 192.0.2.48/28 192.0.2.14 5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="testvrf",
                        address_families=[
                            dict(
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="1200:10::/64",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2048:ae12::/64",
                                                interface="Ethernet1/4",
                                                admin_distance=5,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "vrf context testvrf",
            "ipv6 route 1200:10::/64 Ethernet1/4 2048:ae12::/64 5",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    def test_nxos_static_routes_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
                    ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
                    ip route 192.0.2.80/28 192.0.2.26 tag 12
                    vrf context Test
                      ip route 192.0.2.48/28 192.0.2.13
                      ip route 192.0.2.48/28 192.0.2.14 5
                    vrf context management
                      ip name-server 192.168.255.1
                      ip route 0.0.0.0/0 192.168.255.1
                    vrf context newvrf
                      ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
                      ip route 10.0.11.0/25 10.0.11.10 tag 22 11
                      ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
                      ip route 192.0.2.48/28 loopback22 192.0.2.13
                      ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
                      ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
                      ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
                      ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
                    vrf context trial_vrf
                      ip route 192.0.2.64/28 192.0.2.22 tag 4
                      ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 3,
                                        "route_name": "replaced_route1",
                                    },
                                    {
                                        "interface": "Ethernet1/2",
                                        "forward_router_address": "192.0.2.45",
                                        "dest_vrf": "destinationVRF",
                                        "route_name": "replaced_route2",
                                    },
                                ],
                                "dest": "192.0.2.16/28",
                            },
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.26", "tag": 12},
                                ],
                                "dest": "192.0.2.80/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "Test",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.13"},
                                    {
                                        "forward_router_address": "192.0.2.14",
                                        "admin_distance": 5,
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "management",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.168.255.1"},
                                ],
                                "dest": "0.0.0.0/0",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "newvrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.10.3",
                                        "admin_distance": 11,
                                        "tag": 22323,
                                        "route_name": "test_name",
                                    },
                                ],
                                "dest": "10.0.10.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.11.10",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "forward_router_address": "10.0.11.12",
                                        "admin_distance": 11,
                                        "dest_vrf": "Test",
                                        "tag": 22,
                                    },
                                ],
                                "dest": "10.0.11.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "interface": "loopback22",
                                        "forward_router_address": "192.0.2.13",
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 5,
                                        "dest_vrf": "dest",
                                    },
                                    {
                                        "interface": "mgmt0",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "interface": "port-channel22",
                                        "forward_router_address": "2048:ae12::1",
                                    },
                                    {
                                        "interface": "Ethernet2/1",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 22,
                                        "route_name": "test_name2",
                                    },
                                ],
                                "dest": "2200:10::/36",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "trial_vrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.22", "tag": 4},
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 1,
                                        "route_name": "merged_route",
                                    },
                                ],
                                "dest": "192.0.2.64/28",
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(result["parsed"], compare_list)

    def test_nxos_static_routes_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip route 192.0.2.17/28 192.0.2.23 name replaced_route1 3
            ip route 192.0.2.17/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
            ip route 192.0.2.79/28 192.0.2.26 tag 12
            vrf context Test
              ip route 192.0.2.48/28 192.0.2.13
              ip route 192.0.2.48/28 192.0.2.14 5
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context newvrf
              ip route 10.0.10.0/25 10.0.10.3 name test_name tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name test_name2 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(dict(config=[], state="gathered"))
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 3,
                                        "route_name": "replaced_route1",
                                    },
                                    {
                                        "interface": "Ethernet1/2",
                                        "forward_router_address": "192.0.2.45",
                                        "dest_vrf": "destinationVRF",
                                        "route_name": "replaced_route2",
                                    },
                                ],
                                "dest": "192.0.2.17/28",
                            },
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.26", "tag": 12},
                                ],
                                "dest": "192.0.2.79/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "Test",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.13"},
                                    {
                                        "forward_router_address": "192.0.2.14",
                                        "admin_distance": 5,
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "management",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.168.255.1"},
                                ],
                                "dest": "0.0.0.0/0",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "newvrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.10.3",
                                        "admin_distance": 11,
                                        "tag": 22323,
                                        "route_name": "test_name",
                                    },
                                ],
                                "dest": "10.0.10.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "10.0.11.10",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "forward_router_address": "10.0.11.12",
                                        "admin_distance": 11,
                                        "dest_vrf": "Test",
                                        "tag": 22,
                                    },
                                ],
                                "dest": "10.0.11.0/25",
                            },
                            {
                                "next_hops": [
                                    {
                                        "interface": "loopback22",
                                        "forward_router_address": "192.0.2.13",
                                    },
                                ],
                                "dest": "192.0.2.48/28",
                            },
                        ],
                    },
                    {
                        "afi": "ipv6",
                        "routes": [
                            {
                                "next_hops": [
                                    {
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 5,
                                        "dest_vrf": "dest",
                                    },
                                    {
                                        "interface": "mgmt0",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 11,
                                        "tag": 22,
                                    },
                                    {
                                        "interface": "port-channel22",
                                        "forward_router_address": "2048:ae12::1",
                                    },
                                    {
                                        "interface": "Ethernet2/1",
                                        "forward_router_address": "2048:ae12::1",
                                        "admin_distance": 22,
                                        "route_name": "test_name2",
                                    },
                                ],
                                "dest": "2200:10::/36",
                            },
                        ],
                    },
                ],
            },
            {
                "vrf": "trial_vrf",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "routes": [
                            {
                                "next_hops": [
                                    {"forward_router_address": "192.0.2.22", "tag": 4},
                                    {
                                        "forward_router_address": "192.0.2.23",
                                        "admin_distance": 1,
                                        "route_name": "merged_route",
                                    },
                                ],
                                "dest": "192.0.2.64/28",
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(result["gathered"], compare_list, result["gathered"])
