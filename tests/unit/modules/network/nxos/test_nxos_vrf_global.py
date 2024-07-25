# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_global

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfGlobalModule(TestNxosModule):
    """Test the nxos_vrf_global module."""

    module = nxos_vrf_global

    def setUp(self):
        """Set up for nxos_vrf_global module tests."""
        super(TestNxosVrfGlobalModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vrf_global.vrf_global."
            "Vrf_globalFacts.get_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosVrfGlobalModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_vrf_global_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "description": "this is descrition",
                            "ip": {
                                "auto_discard": True,
                                "domain_list": [
                                    "anisble.com",
                                    "redhat.com",
                                    "res.com",
                                ],
                                "domain_name": "redx.com",
                                "icmp_err": {
                                    "source_interface": {
                                        "interface": "port-channel",
                                        "interface_value": "1",
                                    },
                                },
                                "igmp": {
                                    "ssm_translate": [
                                        {
                                            "group": "232.0.0.0/8",
                                            "source": "10.1.1.1",
                                        },
                                        {
                                            "group": "239.1.2.3/24",
                                            "source": "192.168.1.1",
                                        },
                                    ],
                                },
                                "mroutes": [
                                    {
                                        "group": "192.168.1.0/24",
                                        "source": "192.168.1.1",
                                    },
                                    {
                                        "group": "192.168.1.0/24",
                                        "preference": 2,
                                        "source": "192.168.1.2",
                                        "vrf": "temp1",
                                    },
                                ],
                                "multicast": {
                                    "multipath": {
                                        "resilient": True,
                                        "splitting_type": {
                                            "legacy": True,
                                        },
                                    },
                                    "rpf": [
                                        {
                                            "group_list_range": "238.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                        {
                                            "group_list_range": "239.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                    ],
                                },
                                "name_server": {
                                    "address_list": [
                                        "192.168.0.1",
                                        "192.168.0.2",
                                        "192.168.1.1",
                                        "192.169.1.3",
                                    ],
                                    "use_vrf": {
                                        "source_address": "192.168.0.1",
                                        "vrf": "temp1",
                                    },
                                },
                                "route": [
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                    },
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                        "vrf": "temp1",
                                    },
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.2.0/24",
                                        "tags": {
                                            "route_pref": 4,
                                            "tag_value": 2,
                                        },
                                    },
                                ],
                            },
                            "ipv6": {
                                "mld_ssm_translate": [
                                    {
                                        "group": "ff28::/16",
                                        "source": "2001:db8:0:abcd::2",
                                    },
                                    {
                                        "group": "ff30::/16",
                                        "source": "2001:db8:0:abcd::5",
                                    },
                                ],
                                "multicast": {
                                    "group_range_prefix_list": "temp2",
                                    "multipath": {
                                        "resilient": True,
                                        "splitting_type": {
                                            "none": True,
                                        },
                                    },
                                },
                            },
                            "multicast": {
                                "service_reflect": [
                                    {
                                        "map_to": "Ethernet2/2",
                                        "service_interface": "Ethernet1/1",
                                    },
                                    {
                                        "map_to": "Ethernet4/2",
                                        "service_interface": "Ethernet2/1",
                                    },
                                ],
                            },
                            "name": "test1",
                            "vni": {
                                "vni_number": 5,
                            },
                        },
                    ],
                },
                state="merged",
            ),
        )
        commands = [
            "vrf context test1",
            "description this is descrition",
            "ip auto-discard",
            "ip domain-name redx.com",
            "ip name-server 192.168.0.1 192.168.0.2 192.168.1.1 192.169.1.3",
            "ip icmp-errors source-interface port-channel 1",
            "ip multicast multipath resilient",
            "ip multicast multipath legacy",
            "ip name-server 192.168.0.1 use-vrf temp1",
            "vni 5",
            "ipv6 multicast group-range prefix-list temp2",
            "ipv6 multicast multipath resilient",
            "ipv6 multicast multipath none",
            "ip domain-list res.com",
            "ip domain-list redhat.com",
            "ip domain-list anisble.com",
            "ip igmp ssm-translate 232.0.0.0/8 10.1.1.1",
            "ip igmp ssm-translate 239.1.2.3/24 192.168.1.1",
            "ip mroute 192.168.1.0/24 192.168.1.1",
            "ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1",
            "ip multicast rpf select vrf temp1 group-list 238.1.0.0/24",
            "ip multicast rpf select vrf temp1 group-list 239.1.0.0/24",
            "ip route 192.0.0.0/24 192.0.2.22",
            "ip route 192.0.0.0/24 192.0.2.22 vrf temp1",
            "ip route 192.0.2.0/24 192.0.2.22 tag 2 4",
            "multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2",
            "multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2",
            "ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2",
            "ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::5",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_global_merged_idemp(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context test1
             ip domain-name redx.com
             ip domain-list anisble.com
             ip domain-list redhat.com
             ip domain-list res.com
             ip name-server 192.168.0.1 192.168.0.2 192.168.1.1 192.169.1.3
             ip name-server 192.168.0.1 use-vrf temp1
             multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2
             multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2
             description this is descrition
             vni 5
             ip auto-discard
             ip route 192.0.0.0/24 192.0.2.22
             ip route 192.0.0.0/24 192.0.2.22 vrf temp1
             ip route 192.0.2.0/24 192.0.2.22 tag 2 4
             ip mroute 192.168.1.0/24 192.168.1.1
             ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
             ip icmp-errors source-interface po1
             ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
             ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
             ip multicast multipath legacy
             ip multicast multipath resilient
             ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
             ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
             ip multicast group-range prefix-list temp2
             ipv6 multicast multipath none
             ipv6 multicast multipath resilient
             ipv6 multicast group-range prefix-list temp2
             ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2
             ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::1
             ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::2
             ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::3
             ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::5
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "description": "this is descrition",
                            "ip": {
                                "auto_discard": True,
                                "domain_list": [
                                    "anisble.com",
                                    "redhat.com",
                                    "res.com",
                                ],
                                "domain_name": "redx.com",
                                "icmp_err": {
                                    "source_interface": {
                                        "interface": "port-channel",
                                        "interface_value": "1",
                                    },
                                },
                                "igmp": {
                                    "ssm_translate": [
                                        {
                                            "group": "232.0.0.0/8",
                                            "source": "10.1.1.1",
                                        },
                                        {
                                            "group": "239.1.2.3/24",
                                            "source": "192.168.1.1",
                                        },
                                    ],
                                },
                                "mroutes": [
                                    {
                                        "group": "192.168.1.0/24",
                                        "source": "192.168.1.1",
                                    },
                                    {
                                        "group": "192.168.1.0/24",
                                        "preference": 2,
                                        "source": "192.168.1.2",
                                        "vrf": "temp1",
                                    },
                                ],
                                "multicast": {
                                    "multipath": {
                                        "resilient": True,
                                        "splitting_type": {
                                            "legacy": True,
                                        },
                                    },
                                    "rpf": [
                                        {
                                            "group_list_range": "238.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                        {
                                            "group_list_range": "239.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                    ],
                                },
                                "name_server": {
                                    "address_list": [
                                        "192.168.0.1",
                                        "192.168.0.2",
                                        "192.168.1.1",
                                        "192.169.1.3",
                                    ],
                                    "use_vrf": {
                                        "source_address": "192.168.0.1",
                                        "vrf": "temp1",
                                    },
                                },
                                "route": [
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                    },
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                        "vrf": "temp1",
                                    },
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.2.0/24",
                                        "tags": {
                                            "route_pref": 4,
                                            "tag_value": 2,
                                        },
                                    },
                                ],
                            },
                            "ipv6": {
                                "mld_ssm_translate": [
                                    {
                                        "group": "ff28::/16",
                                        "source": "2001:db8:0:abcd::2",
                                    },
                                    {
                                        "group": "ff30::/16",
                                        "source": "2001:db8:0:abcd::5",
                                    },
                                ],
                                "multicast": {
                                    "group_range_prefix_list": "temp2",
                                    "multipath": {
                                        "resilient": True,
                                        "splitting_type": {
                                            "none": True,
                                        },
                                    },
                                },
                            },
                            "multicast": {
                                "service_reflect": [
                                    {
                                        "map_to": "Ethernet2/2",
                                        "service_interface": "Ethernet1/1",
                                    },
                                    {
                                        "map_to": "Ethernet4/2",
                                        "service_interface": "Ethernet2/1",
                                    },
                                ],
                            },
                            "name": "test1",
                            "vni": {
                                "vni_number": 5,
                            },
                        },
                    ],
                },
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_vrf_global_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
             ip name-server 192.168.255.1
             ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
             description this is descrition
             ip domain-name redx.com
             ip domain-list anisble.com
             ip domain-list redhat.com
             ip domain-list res.com
             vni 5
             ip auto-discard
             ip route 192.0.0.0/24 192.0.2.22
             ip route 192.0.0.0/24 192.0.2.22 vrf temp1
             ip route 192.0.2.0/24 192.0.2.22 tag 2 4
             ip mroute 192.168.1.0/24 192.168.1.1
             ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
             ip icmp-errors source-interface po1
             ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
             ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
             ip multicast multipath legacy
             ip multicast multipath resilient
             ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
             ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
             ip multicast group-range prefix-list temp2
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "name": "test1",
                        },
                    ],
                },
                state="deleted",
            ),
        )

        commands = [
            "vrf context test1",
            "no description this is descrition",
            "no ip auto-discard",
            "no ip domain-name redx.com",
            "no ip icmp-errors source-interface port-channel 1",
            "no ip multicast multipath resilient",
            "no ip multicast multipath legacy",
            "no vni 5",
            "no ip domain-list anisble.com",
            "no ip domain-list res.com",
            "no ip domain-list redhat.com",
            "no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1",
            "no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1",
            "no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24",
            "no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24",
            "no ip route 192.0.0.0/24 192.0.2.22",
            "no ip route 192.0.0.0/24 192.0.2.22 vrf temp1",
            "no ip route 192.0.2.0/24 192.0.2.22 tag 2 4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_ios_vrf_global_deleted_empty(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list anisble.com
              ip domain-list res.com
            """,
        )
        set_module_args(dict(config=dict(), state="deleted"))
        commands = [
            "vrf context management",
            "no ip name-server 192.168.255.1",
            "no ip route 0.0.0.0/0 192.168.255.1",
            "vrf context test1",
            "no description this is descrition",
            "no ip domain-name redx.com",
            "no ip domain-list anisble.com",
            "no ip domain-list res.com",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_global_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list anisble.com
              ip domain-list res.com
              vni 5
              ip auto-discard
              ip route 192.0.0.0/24 192.0.2.22
              ip route 192.0.0.0/24 192.0.2.22 vrf temp1
              ip route 192.0.2.0/24 192.0.2.22 tag 2 4
              ip mroute 192.168.1.0/24 192.168.1.1
              ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
              ip icmp-errors source-interface po1
              ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
              ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
              ip multicast multipath legacy
              ip multicast multipath resilient
              ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
              ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
              ip multicast group-range prefix-list temp2
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "name": "test1",
                            "vni": {
                                "vni_number": 6,
                            },
                            "description": "test description",
                            "ip": {
                                "auto_discard": False,
                                "domain_list": [
                                    "redhat.com",
                                    "greeblue.com",
                                ],
                                "domain_name": "redblue.com",
                                "icmp_err": {
                                    "source_interface": {
                                        "interface": "port-channel",
                                        "interface_value": "3",
                                    },
                                },
                            },
                        },
                    ],
                },
                state="overridden",
            ),
        )
        commands = [
            "vrf context management",
            "no ip name-server 192.168.255.1",
            "no ip route 0.0.0.0/0 192.168.255.1",
            "vrf context test1",
            "description test description",
            "no ip auto-discard",
            "ip domain-name redblue.com",
            "ip icmp-errors source-interface port-channel 3",
            "no ip multicast multipath resilient",
            "no ip multicast multipath legacy",
            "vni 6",
            "ip domain-list redhat.com",
            "ip domain-list greeblue.com",
            "no ip domain-list res.com",
            "no ip domain-list anisble.com",
            "no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1",
            "no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1",
            "no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24",
            "no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24",
            "no ip route 192.0.0.0/24 192.0.2.22",
            "no ip route 192.0.0.0/24 192.0.2.22 vrf temp1",
            "no ip route 192.0.2.0/24 192.0.2.22 tag 2 4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list anisble.com
              ip domain-list res.com
              vni 5
              ip auto-discard
              ip route 192.0.0.0/24 192.0.2.22
              ip route 192.0.0.0/24 192.0.2.22 vrf temp1
              ip route 192.0.2.0/24 192.0.2.22 tag 2 4
              ip mroute 192.168.1.0/24 192.168.1.1
              ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
              ip icmp-errors source-interface po1
              ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
              ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
              ip multicast multipath legacy
              ip multicast multipath resilient
              ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
              ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
              ip multicast group-range prefix-list temp2
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "name": "test1",
                            "vni": {
                                "vni_number": 6,
                            },
                            "description": "test description",
                            "ip": {
                                "auto_discard": False,
                                "domain_list": [
                                    "redhat.com",
                                    "greeblue.com",
                                ],
                                "domain_name": "redblue.com",
                                "icmp_err": {
                                    "source_interface": {
                                        "interface": "port-channel",
                                        "interface_value": "3",
                                    },
                                },
                            },
                            "multicast": {
                                "service_reflect": [
                                    {
                                        "map_to": "Ethernet2/2",
                                        "service_interface": "Ethernet1/1",
                                    },
                                    {
                                        "map_to": "Ethernet4/2",
                                        "service_interface": "Ethernet2/1",
                                    },
                                ],
                            },
                        },
                    ],
                },
                state="replaced",
            ),
        )
        commands = [
            "vrf context test1",
            "description test description",
            "no ip auto-discard",
            "ip domain-name redblue.com",
            "ip icmp-errors source-interface port-channel 3",
            "no ip multicast multipath resilient",
            "no ip multicast multipath legacy",
            "vni 6",
            "ip domain-list redhat.com",
            "ip domain-list greeblue.com",
            "no ip domain-list anisble.com",
            "no ip domain-list res.com",
            "no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1",
            "no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.1",
            "no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1",
            "no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24",
            "no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24",
            "no ip route 192.0.0.0/24 192.0.2.22",
            "no ip route 192.0.0.0/24 192.0.2.22 vrf temp1",
            "no ip route 192.0.2.0/24 192.0.2.22 tag 2 4",
            "multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2",
            "multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_global_replaced_idemp(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list redhat.com
              ip domain-list res.com
              vni 5
              ip auto-discard
              ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
              ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
              ip route 192.0.0.0/24 192.0.2.22
              ip route 192.0.0.0/24 192.0.2.22 vrf temp1
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "name": "management",
                            "ip": {
                                "name_server": {
                                    "address_list": [
                                        "192.168.255.1",
                                    ],
                                },
                                "route": [
                                    {
                                        "destination": "192.168.255.1",
                                        "source": "0.0.0.0/0",
                                    },
                                ],
                            },
                        },
                        {
                            "name": "test1",
                            "description": "this is descrition",
                            "vni": {
                                "vni_number": 5,
                            },
                            "ip": {
                                "auto_discard": True,
                                "domain_list": [
                                    "redhat.com",
                                    "res.com",
                                ],
                                "domain_name": "redx.com",
                                "multicast": {
                                    "rpf": [
                                        {
                                            "group_list_range": "238.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                        {
                                            "group_list_range": "239.1.0.0/24",
                                            "vrf_name": "temp1",
                                        },
                                    ],
                                },
                                "route": [
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                    },
                                    {
                                        "destination": "192.0.2.22",
                                        "source": "192.0.0.0/24",
                                        "vrf": "temp1",
                                    },
                                ],
                            },
                        },
                    ],
                },
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_vrf_global_purged(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list redhat.com
              ip domain-list res.com
              vni 5
              ip auto-discard
              ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
              ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
              ip route 192.0.0.0/24 192.0.2.22
              ip route 192.0.0.0/24 192.0.2.22 vrf temp1
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [],
                },
                state="purged",
            ),
        )
        commands = ["no vrf context management", "no vrf context test1"]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_global_purged_2(self):
        self.execute_show_command.return_value = dedent(
            """\
            vrf context management
              ip name-server 192.168.255.1
              ip route 0.0.0.0/0 192.168.255.1
            vrf context test1
              description this is descrition
              ip domain-name redx.com
              ip domain-list redhat.com
              ip domain-list res.com
              vni 5
              ip auto-discard
              ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
              ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
              ip route 192.0.0.0/24 192.0.2.22
              ip route 192.0.0.0/24 192.0.2.22 vrf temp1
            """,
        )

        set_module_args(
            dict(
                config={
                    "vrfs": [
                        {
                            "name": "test1",
                        },
                    ],
                },
                state="purged",
            ),
        )
        commands = ["no vrf context test1"]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_global_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    vrf context management
                      ip name-server 192.168.255.1
                      ip route 0.0.0.0/0 192.168.255.1
                    vrf context test1
                      description this is descrition
                      ip domain-name redx.com
                      ip domain-list redhat.com
                      vni 5
                      ip auto-discard
                      ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
                      ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
                      ip route 192.0.0.0/24 192.0.2.22
                      ip route 192.0.0.0/24 192.0.2.22 vrf temp1
                    """,
                ),
                state="parsed",
            ),
        )

        parsed_item = {
            "vrfs": [
                {
                    "name": "management",
                    "ip": {
                        "name_server": {
                            "address_list": [
                                "192.168.255.1",
                            ],
                        },
                        "route": [
                            {
                                "destination": "192.168.255.1",
                                "source": "0.0.0.0/0",
                            },
                        ],
                    },
                },
                {
                    "name": "test1",
                    "description": "this is descrition",
                    "vni": {
                        "vni_number": 5,
                    },
                    "ip": {
                        "auto_discard": True,
                        "domain_list": [
                            "redhat.com",
                        ],
                        "domain_name": "redx.com",
                        "multicast": {
                            "rpf": [
                                {
                                    "group_list_range": "238.1.0.0/24",
                                    "vrf_name": "temp1",
                                },
                                {
                                    "group_list_range": "239.1.0.0/24",
                                    "vrf_name": "temp1",
                                },
                            ],
                        },
                        "route": [
                            {
                                "destination": "192.0.2.22",
                                "source": "192.0.0.0/24",
                            },
                            {
                                "destination": "192.0.2.22",
                                "source": "192.0.0.0/24",
                                "vrf": "temp1",
                            },
                        ],
                    },
                },
            ],
        }
        result = self.execute_module(changed=False)
        self.assertEqual(parsed_item, result["parsed"])
