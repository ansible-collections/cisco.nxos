# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_l3_interfaces

from .nxos_module import TestNxosModule, set_module_args


class TestNxosL3InterfaceModule(TestNxosModule):
    """Test the nxos_l3_interfaces module."""

    module = nxos_l3_interfaces

    def setUp(self):
        """Set up for nxos_l3_interfaces module tests."""
        super(TestNxosL3InterfaceModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l3_interfaces.l3_interfaces."
            "L3_interfacesFacts.get_l3_interfaces_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosL3InterfaceModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_l3_interface_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              bandwidth inherit 1000
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        dot1q=100,
                        evpn_multisite_tracking="fabric-tracking",
                        redirects=False,
                        unreachables=True,
                        proxy_arp=True,
                        port_unreachable=True,
                        ipv6_redirects=True,
                        ipv6_unreachables=True,
                        dhcp=dict(
                            ipv4=dict(
                                option82=dict(
                                    suboption=dict(
                                        circuit_id="abc",
                                    ),
                                ),
                                smart_relay=True,
                                relay=dict(
                                    information=dict(trusted=True),
                                    subnet_selection=dict(subnet_ip="10.0.0.7"),
                                    source_interface=dict(
                                        interface_type="port-channel",
                                        interface_id="455",
                                    ),
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                smart_relay=True,
                                relay=dict(
                                    source_interface=dict(
                                        interface_type="port-channel",
                                        interface_id="455",
                                    ),
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            vrf_name="xyz",
                                            interface_type="vlan",
                                            interface_id="51",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        ipv6_verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(address="dhcp"),
                            dict(
                                address="10.0.0.2",
                                ip_network_mask="10.0.0.1",
                                route_preference=70,
                                tag=97,
                            ),
                            dict(
                                ip_network_mask="10.0.0.3/9",
                                secondary=True,
                            ),
                        ],
                        ipv6=[
                            dict(address="dhcp"),
                            dict(address="use-link-local-only"),
                            dict(address="autoconfig"),
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                            dict(
                                address="2001:db8::/64",
                                eui64=True,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )

        commands = [
            "interface Ethernet1/1",
            "mac-address 00:11:22:33:44:55",
            "encapsulation dot1q 100",
            "evpn multisite fabric-tracking",
            "no ip redirects",
            "ip unreachables",
            "ip proxy-arp",
            "ip port-unreachable",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp smart-relay",
            "ip dhcp option82 suboption circuit-id abc",
            "ip dhcp relay information trusted",
            "ip dhcp relay subnet-selection 10.0.0.7",
            "ip dhcp relay source-interface port-channel 455",
            "ipv6 unreachables",
            "ipv6 dhcp smart-relay",
            "ip address dhcp",
            "ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97",
            "ip address 10.0.0.3/9 secondary",
            "ipv6 address dhcp",
            "ipv6 address use-link-local-only",
            "ipv6 address autoconfig",
            "ipv6 address 2001:db8::1/32 route-preference 70 tag 97",
            "ipv6 address 2001:db8::/64 eui64",
            "ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf xyz",
            "ipv6 verify unicast source reachable-via any allow-default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_l3_interface_merged_idemp(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/1
             mac-address 00:11:22:33:44:55
             ip address dhcp
             ip verify unicast source reachable-via any allow-default
             ip dhcp relay address 11.0.0.1 use-vrf xyz
             ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc
             ipv6 address 2001:db8::1/32 route-preference 70 tag 97
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="vlan",
                                            interface_id="51",
                                            vrf_name="abc",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(address="dhcp"),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_l3_interface_deleted(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/1
              mac-address 00:11:22:33:44:55
              ip address dhcp
              ip verify unicast source reachable-via any allow-default
              ip dhcp relay address 11.0.0.1 use-vrf xyz
              ipv6 address 2001:db8::1/32 route-preference 70 tag 97
              ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc
              no ip redirects
            """,
        )

        set_module_args(dict(state="deleted"))

        commands = [
            "interface Ethernet1/1",
            "ip redirects",
            "no mac-address 00:11:22:33:44:55",
            "no ip address dhcp",
            "no ip verify unicast source reachable-via any allow-default",
            "no ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "no ipv6 address 2001:db8::1/32 route-preference 70 tag 97",
            "no ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_l3_interface_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              mac-address 00:11:22:33:44:54
              ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97
            interface Ethernet1/2
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/2",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="vlan",
                                            interface_id="51",
                                            vrf_name="abc",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(ip_network_mask="10.0.0.1", secondary=True),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface Ethernet1/1",
            "no mac-address 00:11:22:33:44:54",
            "no ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97",
            "interface Ethernet1/2",
            "mac-address 00:11:22:33:44:55",
            "ip address 10.0.0.1 secondary",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "ipv6 address 2001:db8::1/32 route-preference 70 tag 97",
            "ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc",
            "no ip redirects",
            "no ipv6 redirects",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_l3_interface_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              mac-address 00:11:22:33:44:50
              ip address 11.0.0.2 11.0.0.1 route-preference 45 tag 81
            interface Ethernet1/2
              mac-address 00:11:22:33:44:54
              ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/2",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="vlan",
                                            interface_id="51",
                                            vrf_name="abc",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(ip_network_mask="10.0.0.1", secondary=True),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "no ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97",
            "mac-address 00:11:22:33:44:55",
            "ip address 10.0.0.1 secondary",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "ipv6 address 2001:db8::1/32 route-preference 70 tag 97",
            "ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc",
            "no ip redirects",
            "no ipv6 redirects",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_l3_interface_replaced_idem(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              mac-address 00:11:22:33:44:55
              ip address dhcp
              ip verify unicast source reachable-via any allow-default
              ip dhcp relay address 11.0.0.1 use-vrf xyz
              ipv6 address 2001:db8::1/32 route-preference 70 tag 97
              ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc
              no ip redirects
              no ipv6 redirects
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="vlan",
                                            interface_id="51",
                                            vrf_name="abc",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(address="dhcp"),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_l3_interface_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="vlan",
                                            interface_id="51",
                                            vrf_name="abc",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(address="dhcp"),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=70,
                                tag=97,
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface Ethernet1/1",
            "mac-address 00:11:22:33:44:55",
            "ip address dhcp",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "ipv6 address 2001:db8::1/32 route-preference 70 tag 97",
            "ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))

    def test_nxos_l3_interface_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              mac-address 00:11:22:33:44:55
              ip address dhcp
              ip verify unicast source reachable-via any allow-default
              ip dhcp relay address 11.0.0.1 use-vrf xyz
              ipv6 address 2001:db8::1/32 route-preference 70 tag 97
              ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
        )
        result = self.execute_module(changed=False)
        gathered = [
            {
                "name": "Ethernet1/1",
                "mac_address": "00:11:22:33:44:55",
                "verify": {
                    "unicast": {
                        "source": {
                            "reachable_via": {
                                "mode": "any",
                                "allow_default": True,
                            },
                        },
                    },
                },
                "dhcp": {
                    "ipv4": {
                        "relay": {
                            "address": [
                                {
                                    "relay_ip": "11.0.0.1",
                                    "vrf_name": "xyz",
                                },
                            ],
                        },
                    },
                    "ipv6": {
                        "relay": {
                            "address": [
                                {
                                    "relay_ip": "2001:0db8::1:abcd",
                                    "vrf_name": "abc",
                                    "interface_type": "vlan",
                                    "interface_id": "51",
                                },
                            ],
                        },
                    },
                },
                "ipv4": [
                    {"address": "dhcp"},
                ],
                "ipv6": [
                    {
                        "address": "2001:db8::1/32",
                        "route_preference": 70,
                        "tag": 97,
                    },
                ],
            },
        ]
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_l3_interface_overridden_same_value(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
              mac-address 00:11:22:33:44:54
              ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97
              ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf abc
              ipv6 address 2001:db8::1/32 route-preference 24 tag 43
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        verify=dict(
                            unicast=dict(
                                source=dict(
                                    reachable_via=dict(
                                        mode="any",
                                        allow_default=True,
                                    ),
                                ),
                            ),
                        ),
                        dhcp=dict(
                            ipv4=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="11.0.0.1",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                            ipv6=dict(
                                relay=dict(
                                    address=[
                                        dict(
                                            relay_ip="2001:0db8::1:abcd",
                                            interface_type="ethernet",
                                            interface_id="21",
                                            vrf_name="xyz",
                                        ),
                                    ],
                                ),
                            ),
                        ),
                        ipv4=[
                            dict(ip_network_mask="10.0.0.1", secondary=True),
                        ],
                        ipv6=[
                            dict(
                                address="2001:db8::1/32",
                                route_preference=65,
                                tag=200,
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "interface Ethernet1/1",
            "no ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97",
            "no ip redirects",
            "no ipv6 redirects",
            "mac-address 00:11:22:33:44:55",
            "ip address 10.0.0.1 secondary",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp relay address 11.0.0.1 use-vrf xyz",
            "ipv6 address 2001:db8::1/32 route-preference 65 tag 200",
            "ipv6 dhcp relay address 2001:0db8::1:abcd interface ethernet 21 use-vrf xyz",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))
