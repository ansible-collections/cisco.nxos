#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.nxos.plugins.modules import nxos_static_routes
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch

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

    def test_nxos_static_routes_merged(self):
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
              ip route 10.0.10.0/25 10.0.10.3 name wewew tag 22323 11
              ip route 10.0.11.0/25 10.0.11.10 tag 22 11
              ip route 10.0.11.0/25 10.0.11.12 vrf Test tag 22 11
              ip route 192.0.2.48/28 loopback22 192.0.2.13
              ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
              ipv6 route 2200:10::/36 mgmt0 2048:ae12::1 tag 22 11
              ipv6 route 2200:10::/36 port-channel22 2048:ae12::1
              ipv6 route 2200:10::/36 Ethernet2/1 2048:ae12::1 name iamname 22
            vrf context trial_vrf
              ip route 192.0.2.64/28 192.0.2.22 tag 4
              ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.32/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.40",
                                                interface="Ethernet1/2",
                                                admin_distance=5,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        result = self.execute_module(changed=True)
        commands = ["ip route 192.0.2.32/28 Ethernet1/2 192.0.2.40 5"]
        self.assertEqual(result["commands"], commands)

    def test_nxos_static_routes_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.16/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.24",
                                                route_name="initial_route",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_static_routes_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.16/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.50",
                                                tag=12,
                                                route_name="replaced_route",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "configure terminal",
            "no ip route 192.0.2.16/28 192.0.2.24 name initial_route",
            "ip route 192.0.2.16/28 192.0.2.50 name replaced_route tag 12",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.16/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.24",
                                                route_name="initial_route",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_static_routes_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.112/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.68",
                                                route_name="overridden_route",
                                                dest_vrf="end_vrf",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "configure terminal",
            "no ip route 192.0.2.16/28 192.0.2.24 name initial_route",
            "ip route 192.0.2.112/28 192.0.2.68 vrf end_vrf name overridden_route",
            "vrf context test",
            "no ipv6 route 2001:db8:12::/32 2001:db8::1001 name ipv6_route 3",
            "no ip route 192.0.2.96/28 192.0.2.122 vrf dest_vrf",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="test",
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.96/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.122",
                                                dest_vrf="dest_vrf",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        address_families=[
                            dict(
                                afi="ipv4",
                                routes=[
                                    dict(
                                        dest="192.0.2.16/28",
                                        next_hops=[
                                            dict(
                                                forward_router_address="192.0.2.24",
                                                route_name="initial_route",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_static_routes_deletedvrf(self):
        set_module_args(dict(config=[dict(vrf="test")], state="deleted"))
        commands = [
            "vrf context test",
            "no ip route 192.0.2.96/28 192.0.2.122 vrf dest_vrf",
            "no ipv6 route 2001:db8:12::/32 2001:db8::1001 name ipv6_route 3",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_deletedafi(self):
        set_module_args(
            dict(
                config=[dict(address_families=[dict(afi="ipv4")])],
                state="deleted",
            ),
        )
        commands = [
            "configure terminal",
            "no ip route 192.0.2.16/28 192.0.2.24 name initial_route",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_deleteddest(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="test",
                        address_families=[dict(afi="ipv4", routes=[dict(dest="192.0.2.96/28")])],
                    ),
                ],
                state="deleted",
            ),
        )
        commands = [
            "vrf context test",
            "no ip route 192.0.2.96/28 192.0.2.122 vrf dest_vrf",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_static_routes_deletedroute(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        vrf="test",
                        address_families=[
                            dict(
                                afi="ipv6",
                                routes=[
                                    dict(
                                        dest="2001:db8:12::/32",
                                        next_hops=[
                                            dict(
                                                forward_router_address="2001:db8::1001",
                                                route_name="ipv6_route",
                                                admin_distance=3,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="deleted",
            ),
        )
        commands = [
            "vrf context test",
            "no ipv6 route 2001:db8:12::/32 2001:db8::1001 name ipv6_route 3",
        ]
        self.execute_module(changed=True, commands=commands)

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
                                                interface="Eth1/4",
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
        self.assertEqual(sorted(result["rendered"]), sorted(commands), result["rendered"])

    def test_nxos_static_routes_parsed(self):
        set_module_args(
            dict(
                running_config="""ip route 192.0.2.16/28 192.0.2.24 name initial_route
        vrf context test
          ip route 192.0.2.96/28 192.0.2.122 vrf dest_vrf
          ipv6 route 2001:db8:12::/32 2001:db8::1001 name ipv6_route 3""",
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "vrf": "test",
                "address_families": [
                    {
                        "routes": [
                            {
                                "dest": "192.0.2.96/28",
                                "next_hops": [
                                    {
                                        "dest_vrf": "dest_vrf",
                                        "forward_router_address": "192.0.2.122",
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv4",
                    },
                    {
                        "routes": [
                            {
                                "dest": "2001:db8:12::/32",
                                "next_hops": [
                                    {
                                        "route_name": "ipv6_route",
                                        "forward_router_address": "2001:db8::1001",
                                        "admin_distance": 3,
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv6",
                    },
                ],
            },
            {
                "address_families": [
                    {
                        "routes": [
                            {
                                "dest": "192.0.2.16/28",
                                "next_hops": [
                                    {
                                        "route_name": "initial_route",
                                        "forward_router_address": "192.0.2.24",
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv4",
                    },
                ],
            },
        ]
        self.assertEqual(result["parsed"], compare_list, result["parsed"])

    def test_nxos_static_routes_gathered(self):
        set_module_args(dict(config=[], state="gathered"))
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "vrf": "test",
                "address_families": [
                    {
                        "routes": [
                            {
                                "dest": "192.0.2.96/28",
                                "next_hops": [
                                    {
                                        "dest_vrf": "dest_vrf",
                                        "forward_router_address": "192.0.2.122",
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv4",
                    },
                    {
                        "routes": [
                            {
                                "dest": "2001:db8:12::/32",
                                "next_hops": [
                                    {
                                        "route_name": "ipv6_route",
                                        "forward_router_address": "2001:db8::1001",
                                        "admin_distance": 3,
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv6",
                    },
                ],
            },
            {
                "address_families": [
                    {
                        "routes": [
                            {
                                "dest": "192.0.2.16/28",
                                "next_hops": [
                                    {
                                        "route_name": "initial_route",
                                        "forward_router_address": "192.0.2.24",
                                    },
                                ],
                            },
                        ],
                        "afi": "ipv4",
                    },
                ],
            },
        ]
        self.assertEqual(result["gathered"], compare_list, result["gathered"])
