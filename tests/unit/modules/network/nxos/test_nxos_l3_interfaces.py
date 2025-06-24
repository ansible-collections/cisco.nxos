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
                        ipv4=dict(
                            address=[
                                dict(dhcp=True),
                                dict(
                                    ip_address="10.0.0.2",
                                    ip_network_mask="10.0.0.1",
                                    route_preference=70,
                                    tag=97,
                                ),
                                dict(
                                    ip_network_mask="10.0.0.3/9",
                                    secondary=True,
                                ),
                            ],
                            redirects=True,
                            unreachables=True,
                            proxy_arp=True,
                            port_unreachable=True,
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
                        ),
                        ipv6=dict(
                            address=[
                                dict(dhcp=True),
                                dict(use_link_local_only=True),
                                dict(autoconfig=True),
                                dict(
                                    ipv6_address="2001:db8::1/32",
                                    route_preference=70,
                                    tag=97,
                                ),
                                dict(
                                    ipv6_address="2001:db8::/64",
                                    eui64=True,
                                ),
                            ],
                            redirects=True,
                            unreachables=True,
                            dhcp=dict(
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
                    ),
                ],
                state="merged",
            ),
        )

        commands = [
            "interface Ethernet1/1",
            "mac-address 00:11:22:33:44:55",
            "ip redirects",
            "ip unreachables",
            "ip proxy-arp",
            "ip port-unreachable",
            "ip verify unicast source reachable-via any allow-default",
            "ip dhcp smart-relay",
            "ip dhcp option82 suboption circuit-id abc",
            "ip dhcp relay information trusted",
            "ip dhcp relay subnet-selection 10.0.0.7",
            "ip dhcp relay source-interface port-channel 455",
            "ipv6 redirects",
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
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_l3_interface_merged_idemp(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/1
              mac-address 00:11:22:33:44:55
              ip verify unicast source reachable-via any allow-default
              ip dhcp smart-relay
              ip dhcp option82 suboption circuit-id abc
              ip dhcp relay information trusted
              ip dhcp relay subnet-selection 10.0.0.7
              ip dhcp relay source-interface port-channel 455
              ipv6 dhcp smart-relay
              ip address dhcp
              ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97
              ip address 10.0.0.3/9 secondary
              ipv6 address dhcp
              ipv6 address use-link-local-only
              ipv6 address autoconfig
              ipv6 address 2001:db8::1/32 route-preference 70 tag 97
              ipv6 address 2001:db8::/64 eui64
              ip dhcp relay address 11.0.0.1 use-vrf xyz
              ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf xyz
            """,
        )

        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/1",
                        mac_address="00:11:22:33:44:55",
                        ipv4=dict(
                            address=[
                                dict(dhcp=True),
                                dict(
                                    ip_address="10.0.0.2",
                                    ip_network_mask="10.0.0.1",
                                    route_preference=70,
                                    tag=97,
                                ),
                                dict(
                                    ip_network_mask="10.0.0.3/9",
                                    secondary=True,
                                ),
                            ],
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
                        ),
                        ipv6=dict(
                            address=[
                                dict(dhcp=True),
                                dict(use_link_local_only=True),
                                dict(autoconfig=True),
                                dict(
                                    ipv6_address="2001:db8::1/32",
                                    route_preference=70,
                                    tag=97,
                                ),
                                dict(
                                    ipv6_address="2001:db8::/64",
                                    eui64=True,
                                ),
                            ],
                            dhcp=dict(
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
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    # def test_nxos_l3_interface_deleted(self):
    #     self.execute_show_command.return_value = dedent(
    #         """\
    #         interface Ethernet1/1
    #           no ip unreachables
    #           no ip proxy-arp
    #           no ipv6 unreachables
    #           interface Ethernet1/2
    #           mac-address 00:11:22:33:44:55
    #           ip redirects
    #           ip unreachables
    #           ip proxy-arp
    #           ip port-unreachable
    #           ip verify unicast source reachable-via any allow-default
    #           ip dhcp smart-relay
    #           ip dhcp option82 suboption circuit-id abc
    #           ip dhcp relay information trusted
    #           ip dhcp relay subnet-selection 10.0.0.7
    #           ip dhcp relay source-interface port-channel 455
    #           ipv6 redirects
    #           ipv6 unreachables
    #           ipv6 dhcp smart-relay
    #           ip address dhcp
    #           ip address 10.0.0.2 10.0.0.1 route-preference 70 tag 97
    #           ip address 10.0.0.3/9 secondary
    #           ipv6 address dhcp
    #           ipv6 address use-link-local-only
    #           ipv6 address autoconfig
    #           ipv6 address 2001:db8::1/32 route-preference 70 tag 97
    #           ipv6 address 2001:db8::/64 eui64
    #           ip dhcp relay address 11.0.0.1 use-vrf xyz
    #           ipv6 dhcp relay address 2001:0db8::1:abcd interface vlan 51 use-vrf xyz
    #         """,
    #     )

    #     set_module_args(
    #         dict(
    #             config={
    #                 "vrfs": [
    #                     {
    #                         "name": "test1",
    #                     },
    #                 ],
    #             },
    #             state="deleted",
    #         ),
    #     )

    #     commands = [
    #         "vrf context test1",
    #         "no description this is descrition",
    #         "no ip auto-discard",
    #         "no ip domain-name redx.com",
    #         "no ip icmp-errors source-interface port-channel 1",
    #         "no ip multicast multipath resilient",
    #         "no ip multicast multipath legacy",
    #         "no vni 5",
    #         "no ip domain-list anisble.com",
    #         "no ip domain-list res.com",
    #         "no ip domain-list redhat.com",
    #         "no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1",
    #         "no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1",
    #         "no ip mroute 192.168.1.0/24 192.168.1.1",
    #         "no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1",
    #         "no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24",
    #         "no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24",
    #         "no ip route 192.0.0.0/24 192.0.2.22",
    #         "no ip route 192.0.0.0/24 192.0.2.22 vrf temp1",
    #         "no ip route 192.0.2.0/24 192.0.2.22 tag 2 4",
    #     ]
    #     result = self.execute_module(changed=True)
    #     self.assertEqual(sorted(result["commands"]), sorted(commands))
