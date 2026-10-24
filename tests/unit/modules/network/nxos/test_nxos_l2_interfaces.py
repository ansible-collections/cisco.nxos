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
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    get_routed_interfaces,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_l2_interfaces
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule


ignore_provider_arg = True

ETH25 = "Ethernet1/25"
BPDUGUARD = "spanning-tree bpduguard"
STP_STORM_BLOCK = dedent(
    """
    interface Ethernet1/25
      switchport
      switchport mode trunk
      spanning-tree port-priority 64
      spanning-tree cost 100
      spanning-tree link-type point-to-point
      spanning-tree port type edge trunk
      spanning-tree bpduguard enable
      spanning-tree guard root
      storm-control broadcast level 0.01
      storm-control multicast level 1.00
      storm-control unicast level 5.00
    """,
)
STP_STORM_FACTS = {
    "name": ETH25,
    "mode": "trunk",
    "spanning_tree": {
        "port_priority": 64,
        "cost": 100,
        "link_type": "point_to_point",
        "port_type": "edge_trunk",
        "bpduguard": True,
        "guard": "root",
    },
    "storm_control": {
        "broadcast": {"level": "0.01"},
        "multicast": {"level": "1.00"},
        "unicast": {"level": "5.00"},
    },
}
STP_STORM_REMOVE = [
    "interface Ethernet1/25",
    "no spanning-tree port type edge trunk",
    "no spanning-tree bpduguard",
    "no spanning-tree guard",
    "no spanning-tree cost",
    "no spanning-tree port-priority",
    "no spanning-tree link-type",
    "no storm-control broadcast level 0.01",
    "no storm-control multicast level 1.00",
    "no storm-control unicast level 5.00",
]


class TestNxosL2InterfacesModule(TestNxosModule):
    module = nxos_l2_interfaces

    def setUp(self):
        super(TestNxosL2InterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces."
            "L2_interfacesFacts._get_interface_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.maxDiff = None

    def tearDown(self):
        super(TestNxosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_l2_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport mode trunk
             switchport access vlan 20
             switchport trunk native vlan 40
             switchport trunk allowed vlan 30-45,47
             switchport trunk allowed vlan add 50,52,54
            interface Ethernet1/2
             switchport mode trunk
             switchport trunk native vlan 20
             switchport trunk allowed vlan 10,20,30
            interface Ethernet1/4
             speed 1000
             service-policy type qos output test-policy
             no shutdown
            """,
        )

        set_module_args(
            dict(
                state="gathered",
            ),
        )

        expected = [
            {
                "access": {"vlan": 20},
                "mode": "trunk",
                "name": "Ethernet1/6",
                "trunk": {
                    "allowed_vlans": "30-45,47,50,52,54",
                    "native_vlan": 40,
                },
            },
            {
                "mode": "trunk",
                "name": "Ethernet1/2",
                "trunk": {
                    "allowed_vlans": "10,20,30",
                    "native_vlan": 20,
                },
            },
            {
                "name": "Ethernet1/4",
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], expected)

    def test_l2_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """
                    interface nve1
                     no shutdown
                     host-reachability protocol bgp
                     advertise virtual-rmac
                     source-interface loopback1
                    interface Ethernet1/799
                     switchport mode dot1q-tunnel
                    interface Ethernet1/800
                     switchport access vlan 18
                     switchport trunk allowed vlan 210
                     switchport trunk allowed vlan add 300,310
                    interface Ethernet1/801
                     switchport trunk allowed vlan 2,4,15
                    interface Ethernet1/802
                     switchport mode fex-fabric
                    interface Ethernet1/803
                     switchport mode fabricpath
                    interface loopback1
                    """,
                ),
                state="parsed",
            ),
        )

        expected = [
            {
                "name": "nve1",
            },
            {
                "mode": "dot1q-tunnel",
                "name": "Ethernet1/799",
            },
            {
                "access": {
                    "vlan": 18,
                },
                "name": "Ethernet1/800",
                "trunk": {
                    "allowed_vlans": "210,300,310",
                },
            },
            {
                "name": "Ethernet1/801",
                "trunk": {
                    "allowed_vlans": "2,4,15",
                },
            },
            {
                "mode": "fex-fabric",
                "name": "Ethernet1/802",
            },
            {
                "mode": "fabricpath",
                "name": "Ethernet1/803",
            },
            {
                "name": "loopback1",
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], expected)

    def test_l2_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """
            default interface Ethernet1/6
            interface Ethernet1/6
             switchport
             no cdp enable
            interface Ethernet1/7
             switchport mode trunk
             switchport trunk allowed vlan 23-100
            interface Ethernet1/8
             switchport mode trunk
             no cdp enable
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/6",
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                        "cdp_enable": True,
                    },
                    {
                        "name": "Ethernet1/7",
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "21-101",
                        },
                    },
                    {
                        "name": "Ethernet1/8",
                        "mode": "trunk",
                        "trunk": {
                            "native_vlan": 10,
                            "allowed_vlans": "1-4000",
                        },
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "cdp enable",
            "switchport mode trunk",
            "switchport trunk allowed vlan 10-12",
            "interface Ethernet1/7",
            "switchport trunk allowed vlan add 21-22,101",
            "interface Ethernet1/8",
            "switchport trunk native vlan 10",
            "switchport trunk allowed vlan 1-4000",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_merged_subset_superset(self):
        self.execute_show_command.return_value = dedent(
            """
            default interface Ethernet1/6
            interface Ethernet1/6
             switchport
             no cdp enable
            interface Ethernet1/7
             switchport mode trunk
             switchport trunk allowed vlan 23-100
            interface Ethernet1/8
             switchport mode trunk
             no cdp enable
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/6",
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                        "cdp_enable": True,
                    },
                    {
                        "name": "Ethernet1/7",
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "23-99",
                        },
                    },
                    {
                        "name": "Ethernet1/8",
                        "mode": "trunk",
                        "trunk": {
                            "native_vlan": 10,
                            "allowed_vlans": "1-4094",
                        },
                    },
                    {
                        "name": "Ethernet1/9",
                        "mode": "trunk",
                        "trunk": {
                            "native_vlan": 18,
                            "allowed_vlans": "222",
                        },
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "cdp enable",
            "switchport mode trunk",
            "switchport trunk allowed vlan 10-12",
            "interface Ethernet1/8",
            "switchport trunk native vlan 10",
            "switchport trunk allowed vlan 1-4094",
            "interface Ethernet1/9",
            "switchport mode trunk",
            "switchport trunk native vlan 18",
            "switchport trunk allowed vlan 222",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """
            default interface Ethernet1/6
            default interface Ethernet1/7
            default interface Ethernet1/8
            interface Ethernet1/6
             switchport
             switchport access vlan 5
            interface Ethernet1/7
             switchport
             switchport trunk native vlan 15
             switchport trunk allowed vlan 25-27
            interface Ethernet1/8
             switchport
             switchport trunk allowed vlan 100-200
             switchport trunk allowed vlan add 250
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/6",
                        "access": {
                            "vlan": "8",
                        },
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                    {
                        "name": "Ethernet1/7",
                        "trunk": {
                            "native_vlan": 25,
                            "allowed_vlans": "25-27",
                        },
                    },
                    {
                        "name": "Ethernet1/8",
                        "trunk": {
                            "allowed_vlans": "33",
                        },
                        "cdp_enable": True,
                    },
                ],
                state="replaced",
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no cdp enable",
            "switchport access vlan 8",
            "switchport trunk allowed vlan 10-12",
            "interface Ethernet1/7",
            "no cdp enable",
            "switchport trunk native vlan 25",
            "interface Ethernet1/8",
            "switchport trunk allowed vlan 33",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_replaced_with_multiple_add_lines_idempotent(self):
        """Test idempotency when device has multiple add lines that match desired config"""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/10
             no cdp enable
             switchport
             switchport trunk allowed vlan 10-20
             switchport trunk allowed vlan add 30-40
             switchport trunk allowed vlan add 50-60
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/10",
                        "trunk": {
                            "allowed_vlans": "10-20,30-40,50-60",
                        },
                    },
                ],
                state="replaced",
            ),
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_replaced_with_multiple_add_lines_partial_remove(self):
        """Test replaced state removes VLANs correctly when device has multiple add lines"""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/10
             switchport
             switchport trunk allowed vlan 10-20
             switchport trunk allowed vlan add 30-40
             switchport trunk allowed vlan add 50-60
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/10",
                        "trunk": {
                            "allowed_vlans": "10-20",
                        },
                    },
                ],
                state="replaced",
            ),
        )

        expected_commands = [
            "interface Ethernet1/10",
            "no cdp enable",
            "switchport trunk allowed vlan 10-20",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """
            default interface Ethernet1/6
            default interface Ethernet1/7
            interface Ethernet1/6
             switchport
             switchport trunk allowed vlan 11
            interface Ethernet1/7
             switchport
             switchport trunk allowed vlan 10-500
             switchport trunk allowed vlan add 5
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/7",
                        "access": {
                            "vlan": "6",
                        },
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no switchport trunk allowed vlan",
            "interface Ethernet1/7",
            "no cdp enable",
            "switchport access vlan 6",
            "switchport trunk allowed vlan 10-12",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_overridden_idempotent_and_section(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             no cdp enable
             switchport
             switchport access vlan 6
             switchport trunk allowed vlan 10-500
            interface Ethernet1/7
             no cdp enable
             switchport
             switchport access vlan 6
             switchport trunk allowed vlan 10-500
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/6",
                        "access": {
                            "vlan": "6",
                        },
                        "trunk": {
                            "allowed_vlans": "20-250,350,3999",
                        },
                    },
                    {
                        "name": "Ethernet1/7",
                        "access": {
                            "vlan": "6",
                        },
                        "trunk": {
                            "allowed_vlans": "10-500",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "switchport trunk allowed vlan 20-250,350,3999",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_overridden_with_multiple_add_lines_idempotent(self):
        """Test idempotency in overridden state with multiple add lines"""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/10
             no cdp enable
             switchport
             switchport trunk allowed vlan 100
             switchport trunk allowed vlan add 200
             switchport trunk allowed vlan add 300-350
            interface Ethernet1/11
             no cdp enable
             switchport
             switchport trunk allowed vlan 10-50
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/10",
                        "trunk": {
                            "allowed_vlans": "100,200,300-350",
                        },
                    },
                    {
                        "name": "Ethernet1/11",
                        "trunk": {
                            "allowed_vlans": "10-50",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_overridden_with_multiple_add_lines_partial_remove(self):
        """Test overridden state removes VLANs correctly with multiple add lines"""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/10
             switchport
             switchport trunk allowed vlan 10
             switchport trunk allowed vlan add 20
             switchport trunk allowed vlan add 30
            interface Ethernet1/11
             switchport
             switchport trunk allowed vlan 100-200
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/10",
                        "trunk": {
                            "allowed_vlans": "10",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        expected_commands = [
            "interface Ethernet1/11",
            "no switchport trunk allowed vlan",
            "interface Ethernet1/10",
            "no cdp enable",
            "switchport trunk allowed vlan 10",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """
            default interface Ethernet1/6
            default interface Ethernet1/7
            interface Ethernet1/6
             switchport
             switchport trunk native vlan 10
            interface Ethernet1/7
             switchport
             switchport mode trunk
             switchport trunk allowed vlan 20
             switchport trunk allowed vlan add 20
            """,
        )

        set_module_args(
            dict(state="deleted"),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no switchport trunk native vlan 10",
            "no switchport trunk allowed vlan",
            "interface Ethernet1/7",
            "no switchport mode trunk",
            "no switchport trunk allowed vlan",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_gathered_filters_pc_members(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport mode trunk
             switchport trunk allowed vlan 30-45,47
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk allowed vlan 10,20,30
             channel-group 10 mode active
            interface Ethernet1/2
             switchport mode trunk
             switchport trunk native vlan 20
            """,
        )

        set_module_args(
            dict(
                state="gathered",
            ),
        )

        expected = [
            {
                "mode": "trunk",
                "name": "Ethernet1/6",
                "trunk": {
                    "allowed_vlans": "30-45,47",
                },
            },
            {
                "mode": "trunk",
                "name": "Ethernet1/2",
                "trunk": {
                    "allowed_vlans": "1-4094",
                    "allowed_vlans_implicit": True,
                    "native_vlan": 20,
                },
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], expected)

    def test_l2_interfaces_parsed_filters_pc_members(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """
                    interface Ethernet1/800
                     switchport access vlan 18
                    interface Ethernet1/801
                     switchport trunk allowed vlan 2,4,15
                     channel-group 20 mode active
                    interface Ethernet1/802
                     switchport mode fex-fabric
                    """,
                ),
                state="parsed",
            ),
        )

        expected = [
            {
                "access": {
                    "vlan": 18,
                },
                "name": "Ethernet1/800",
            },
            {
                "mode": "fex-fabric",
                "name": "Ethernet1/802",
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], expected)

    def test_l2_interfaces_merged_fails_pc_member(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
            interface Ethernet1/4
             switchport mode trunk
             channel-group 10 mode active
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                    {
                        "name": "Ethernet1/6",
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                ],
            ),
        )

        result = self.execute_module(failed=True)
        self.assertIn("Ethernet1/4 is a port-channel member", result["msg"])

    def test_l2_interfaces_replaced_fails_pc_member(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport access vlan 5
            interface Ethernet1/4
             switchport mode trunk
             channel-group 10 mode active
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                    {
                        "name": "Ethernet1/6",
                        "access": {
                            "vlan": "8",
                        },
                    },
                ],
                state="replaced",
            ),
        )

        result = self.execute_module(failed=True)
        self.assertIn("Ethernet1/4 is a port-channel member", result["msg"])

    def test_l2_interfaces_overridden_skips_pc_members(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport trunk allowed vlan 11
            interface Ethernet1/7
             switchport
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk allowed vlan 100-200
             channel-group 10 mode active
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/7",
                        "access": {
                            "vlan": "6",
                        },
                        "trunk": {
                            "allowed_vlans": "10-12",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no switchport trunk allowed vlan",
            "interface Ethernet1/7",
            "no cdp enable",
            "switchport access vlan 6",
            "switchport trunk allowed vlan 10-12",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_deleted_fails_pc_member(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport trunk native vlan 10
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk allowed vlan 20
             channel-group 10 mode active
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                    },
                ],
                state="deleted",
            ),
        )

        result = self.execute_module(failed=True)
        self.assertIn("Ethernet1/4 is a port-channel member", result["msg"])

    def test_l2_interfaces_deleted_all_skips_pc_members(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport trunk native vlan 10
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk allowed vlan 20
             channel-group 10 mode active
            """,
        )

        set_module_args(
            dict(state="deleted"),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no switchport trunk native vlan 10",
            "no switchport trunk allowed vlan",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_replaced_pc_member_only(self):
        """Exact reproduction of user's playbook: replaced state with only a port-channel member."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/1
             switchport
             switchport mode trunk
             switchport trunk native vlan 20
             switchport trunk allowed vlan 100-102,300
             channel-group 10 mode active
            interface Ethernet1/2
             switchport
             switchport access vlan 5
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Eth1/1",
                        "cdp_enable": True,
                        "mode": "trunk",
                        "trunk": {
                            "allowed_vlans": "100-102,300",
                            "native_vlan": 20,
                        },
                    },
                ],
                state="replaced",
            ),
        )

        result = self.execute_module(failed=True)
        self.assertIn("Ethernet1/1 is a port-channel member", result["msg"])

    def test_l2_interfaces_merged_cdp_disable(self):
        """Test merged state with cdp_enable explicitly set to False (line 214)."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport access vlan 10
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/6",
                        "access": {"vlan": 10},
                        "cdp_enable": False,
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no cdp enable",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_deleted_all_restores_cdp(self):
        """Test deleted state with no config restores cdp when have_cdp is False (lines 216-217)."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             no cdp enable
             switchport trunk native vlan 10
            """,
        )

        set_module_args(
            dict(state="deleted"),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "cdp enable",
            "no switchport trunk native vlan 10",
            "no switchport trunk allowed vlan",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_parsed_vlan_special_cases(self):
        """Test parsing of vlan none/all/except special cases (line 143)."""
        set_module_args(
            dict(
                running_config=dedent(
                    """
                    interface Ethernet1/1
                     switchport mode trunk
                     switchport trunk allowed vlan none
                    interface Ethernet1/2
                     switchport mode trunk
                     switchport trunk allowed vlan all
                    """,
                ),
                state="parsed",
            ),
        )

        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        eth1 = next(p for p in parsed if p["name"] == "Ethernet1/1")
        self.assertEqual(eth1["mode"], "trunk")
        self.assertNotIn("allowed_vlans", eth1.get("trunk", {}))

    def test_l2_interfaces_parsed_vlan_add_without_prior_set(self):
        """Test parsing when 'vlan add' appears without a preceding 'vlan' set line (line 150)."""
        set_module_args(
            dict(
                running_config=dedent(
                    """
                    interface Ethernet1/10
                     switchport
                     switchport trunk allowed vlan add 100-200
                    """,
                ),
                state="parsed",
            ),
        )

        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        eth10 = next(p for p in parsed if p["name"] == "Ethernet1/10")
        self.assertEqual(eth10["trunk"]["allowed_vlans"], "100-200")

    def test_l2_interfaces_parsed_trailing_vlans(self):
        """Test parsing when data ends with vlan lines (no trailing non-vlan line) (line 165)."""
        set_module_args(
            dict(
                running_config="interface Ethernet1/5\n switchport\n switchport trunk allowed vlan 50-60",
                state="parsed",
            ),
        )

        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        eth5 = next(p for p in parsed if p["name"] == "Ethernet1/5")
        self.assertEqual(eth5["trunk"]["allowed_vlans"], "50-60")

    def test_l2_interfaces_overridden_idempotent_with_pc_members(self):
        """Overridden with port-channel members excluded is idempotent."""
        self.execute_show_command.return_value = dedent(
            """
            interface port-channel20
             switchport
             switchport mode trunk
             switchport trunk native vlan 20
             switchport trunk allowed vlan 100-102,300
            interface Ethernet1/49
             switchport
             switchport mode trunk
             switchport trunk native vlan 20
             switchport trunk allowed vlan 100-102,300
             channel-group 20 mode active
            interface Ethernet1/50
             switchport
             switchport mode trunk
             switchport trunk native vlan 20
             switchport trunk allowed vlan 100-102,300
             channel-group 20 mode active
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "port-channel20",
                        "mode": "trunk",
                        "cdp_enable": True,
                        "trunk": {
                            "native_vlan": 20,
                            "allowed_vlans": "100-102,300",
                        },
                    },
                ],
                state="overridden",
            ),
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_merged_implicit_default_trunk_set(self):
        """Merged state uses SET when have is implicit default (1-4094).

        Customer scenario: trunk port with native_vlan but no explicit
        allowed_vlans. Using merged to restrict VLANs should generate a
        plain SET command, not ADD (which would be a no-op).
        """
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk native vlan 99
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "100,200",
                        },
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/4",
            "switchport trunk allowed vlan 100,200",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_merged_implicit_default_trunk_idempotent(self):
        """Second run after implicit SET is idempotent — have is now explicit."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk native vlan 99
             switchport trunk allowed vlan 100,200
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "100,200",
                        },
                    },
                ],
            ),
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_merged_explicit_trunk_still_adds(self):
        """Merged with explicit have VLANs still uses ADD (not SET)."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk native vlan 99
             switchport trunk allowed vlan 100,200
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "300,400",
                        },
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/4",
            "switchport trunk allowed vlan add 300,400",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_replaced_implicit_trunk_unchanged(self):
        """Replaced state behavior is NOT changed by the implicit marker."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk native vlan 99
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "Ethernet1/4",
                        "trunk": {
                            "allowed_vlans": "100,200",
                        },
                    },
                ],
                state="replaced",
            ),
        )

        expected_commands = [
            "interface Ethernet1/4",
            "no cdp enable",
            "no switchport mode trunk",
            "no switchport trunk native vlan 99",
            "switchport trunk allowed vlan 100,200",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_gathered_implicit_flag(self):
        """Gathered facts include allowed_vlans_implicit when VLANs are synthesized."""
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/4
             switchport mode trunk
             switchport trunk native vlan 99
            interface Ethernet1/5
             switchport mode trunk
             switchport trunk allowed vlan 100,200
            """,
        )

        set_module_args(
            dict(
                state="gathered",
            ),
        )

        expected = [
            {
                "mode": "trunk",
                "name": "Ethernet1/4",
                "trunk": {
                    "allowed_vlans": "1-4094",
                    "allowed_vlans_implicit": True,
                    "native_vlan": 99,
                },
            },
            {
                "mode": "trunk",
                "name": "Ethernet1/5",
                "trunk": {
                    "allowed_vlans": "100,200",
                },
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], expected)

    def _run(self, show, config=None, state="merged", changed=True, failed=False, **extra):
        self.execute_show_command.return_value = show
        args = dict(state=state, **extra)
        if config is not None:
            args["config"] = config
        set_module_args(args)
        return self.execute_module(changed=changed, failed=failed)

    def _stp_cfg(self, name=ETH25, **sections):
        return [dict(name=name, **sections)]

    def test_l2_interfaces_stp_storm_gathered(self):
        result = self._run(STP_STORM_BLOCK, state="gathered", changed=False)
        self.assertEqual(result["gathered"], [STP_STORM_FACTS])

    def test_l2_interfaces_stp_storm_parsed_all_options(self):
        running = dedent(
            """
            interface port-channel20
              spanning-tree port type network
              spanning-tree bpduguard disable
              spanning-tree bpdufilter enable
              spanning-tree guard loop
              spanning-tree link-type shared
              spanning-tree mst 0,2-4 cost 200
              spanning-tree mst 0,2-4 port-priority 32
              spanning-tree mst 5 cost 10
              spanning-tree vlan 1,3-5 port-priority 96
              spanning-tree cost auto
              storm-control broadcast level pps 1000
              storm-control multicast level 10.5
              storm-control action shutdown
            """,
        )
        result = self._run(None, state="parsed", changed=False, running_config=running)
        self.assertEqual(
            result["parsed"],
            [
                {
                    "name": "port-channel20",
                    "spanning_tree": {
                        "port_type": "network",
                        "bpduguard": False,
                        "bpdufilter": True,
                        "guard": "loop",
                        "link_type": "shared",
                        "mst": [
                            {"instances": "0,2-4", "cost": 200, "port_priority": 32},
                            {"instances": "5", "cost": 10},
                        ],
                        "vlans": [{"vlans": "1,3-5", "port_priority": 96}],
                    },
                    "storm_control": {
                        "broadcast": {"pps": 1000},
                        "multicast": {"level": "10.5"},
                        "action": "shutdown",
                    },
                },
            ],
        )

    def test_l2_interfaces_stp_storm_rendered(self):
        config = self._stp_cfg(
            spanning_tree={
                "port_type": "edge_trunk",
                "bpduguard": True,
                "bpdufilter": False,
                "guard": "none",
                "cost": 100,
                "port_priority": 64,
                "link_type": "point_to_point",
                "mst": [{"instances": "4,3,2", "cost": 5, "port_priority": 32}],
                "vlans": [{"vlans": "1,3-5", "cost": 7}],
            },
            storm_control={
                "broadcast": {"level": "0.01"},
                "multicast": {"pps": 0},
                "unicast": {"level": "1"},
                "action": "trap",
            },
        )
        result = self._run(None, config, state="rendered", changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "interface Ethernet1/25",
                "spanning-tree port type edge trunk",
                BPDUGUARD + " enable",
                "spanning-tree bpdufilter disable",
                "spanning-tree guard none",
                "spanning-tree cost 100",
                "spanning-tree port-priority 64",
                "spanning-tree link-type point-to-point",
                "storm-control broadcast level 0.01",
                "storm-control multicast level pps 0",
                "storm-control unicast level 1.00",
                "storm-control action trap",
                "spanning-tree mst 2-4 cost 5",
                "spanning-tree mst 2-4 port-priority 32",
                "spanning-tree vlan 1,3-5 cost 7",
            ],
        )

    def test_l2_interfaces_stp_storm_merged_adds_and_keeps(self):
        config = self._stp_cfg(
            spanning_tree={"port_type": "edge", "link_type": "shared"},
            storm_control={"broadcast": {"level": "0.50"}, "action": "shutdown"},
        )
        result = self._run(STP_STORM_BLOCK, config)
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/25",
                "spanning-tree port type edge",
                "spanning-tree link-type shared",
                "storm-control broadcast level 0.50",
                "storm-control action shutdown",
            ],
        )

    def test_l2_interfaces_stp_storm_merged_idempotent_decimal(self):
        facts = dict(STP_STORM_FACTS, mode="trunk")
        config = [
            dict(
                facts,
                storm_control={"broadcast": {"level": "0.010"}, "unicast": {"level": "5.0"}},
            ),
        ]
        result = self._run(STP_STORM_BLOCK, config, changed=False)
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_stp_storm_merged_level_to_pps(self):
        config = self._stp_cfg(storm_control={"broadcast": {"pps": 5000}})
        result = self._run(STP_STORM_BLOCK, config)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/25", "storm-control broadcast level pps 5000"],
        )

    def test_l2_interfaces_stp_storm_merged_pps_to_level_and_idempotent(self):
        show = "interface Ethernet1/25\n  storm-control broadcast level pps 5000\n"
        result = self._run(show, self._stp_cfg(storm_control={"broadcast": {"level": "2"}}))
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/25", "storm-control broadcast level 2.00"],
        )
        result = self._run(
            show,
            self._stp_cfg(storm_control={"broadcast": {"pps": 5000}}),
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_stp_storm_merged_port_channel_from_default(self):
        config = self._stp_cfg(
            "Port-Channel20",
            spanning_tree={"port_type": "network", "bpduguard": True},
        )
        result = self._run("interface port-channel20\n  switchport\n", config)
        self.assertEqual(
            result["commands"],
            ["interface port-channel20", "spanning-tree port type network", BPDUGUARD + " enable"],
        )

    def test_l2_interfaces_stp_storm_replaced_removes_single_line(self):
        facts = dict(STP_STORM_FACTS, cdp_enable=True)
        facts["spanning_tree"] = {k: v for k, v in facts["spanning_tree"].items() if k != "guard"}
        result = self._run(STP_STORM_BLOCK, [facts], state="replaced")
        self.assertEqual(result["commands"], ["interface Ethernet1/25", "no spanning-tree guard"])

    def test_l2_interfaces_stp_storm_replaced_idempotent(self):
        result = self._run(
            STP_STORM_BLOCK,
            [dict(STP_STORM_FACTS, cdp_enable=True)],
            state="replaced",
            changed=False,
        )
        self.assertEqual(result["commands"], [])

    def test_l2_interfaces_stp_storm_replaced_restore_to_default(self):
        result = self._run(
            STP_STORM_BLOCK,
            [{"name": ETH25, "mode": "trunk", "cdp_enable": True}],
            state="replaced",
        )
        self.assertEqual(result["commands"], STP_STORM_REMOVE)

    def test_l2_interfaces_stp_storm_overridden_removes_unlisted(self):
        show = (
            STP_STORM_BLOCK
            + "interface Ethernet1/26\n  spanning-tree port type edge\n  storm-control action trap\n"
        )
        config = [dict(STP_STORM_FACTS, cdp_enable=True)]
        result = self._run(show, config, state="overridden")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/26",
                "no spanning-tree port type edge",
                "no storm-control action trap",
            ],
        )

    def test_l2_interfaces_stp_storm_deleted(self):
        show = STP_STORM_BLOCK + "interface Ethernet1/26\n  spanning-tree bpduguard enable\n"
        result = self._run(show, [{"name": ETH25}], state="deleted")
        self.assertEqual(
            result["commands"],
            STP_STORM_REMOVE[:1] + ["no switchport mode trunk"] + STP_STORM_REMOVE[1:],
        )
        result = self._run(show, state="deleted")
        self.assertIn("no spanning-tree bpduguard", result["commands"])
        self.assertEqual(result["commands"].count("interface Ethernet1/26"), 1)

    def test_l2_interfaces_stp_storm_bpduguard_tri_state(self):
        show = "interface Ethernet1/25\n"
        cases = [
            (show, True, ["interface Ethernet1/25", BPDUGUARD + " enable"]),
            (show, False, ["interface Ethernet1/25", BPDUGUARD + " disable"]),
            (
                show + "  " + BPDUGUARD + " disable\n",
                True,
                ["interface Ethernet1/25", BPDUGUARD + " enable"],
            ),
            (
                show + "  " + BPDUGUARD + " enable\n",
                False,
                ["interface Ethernet1/25", BPDUGUARD + " disable"],
            ),
            (show + "  " + BPDUGUARD + " disable\n", False, []),
            (show + "  " + BPDUGUARD + " enable\n", None, []),
        ]
        for have, value, commands in cases:
            spanning_tree = {} if value is None else {"bpduguard": value}
            config = self._stp_cfg(spanning_tree=spanning_tree)
            result = self._run(have, config, changed=bool(commands))
            self.assertEqual(result["commands"], commands, (have, value))

    def test_l2_interfaces_stp_storm_bpduguard_unset_removed_by_replaced(self):
        for state in ("enable", "disable"):
            show = "interface Ethernet1/25\n  " + BPDUGUARD + " " + state + "\n"
            result = self._run(show, [{"name": ETH25, "cdp_enable": True}], state="replaced")
            self.assertEqual(result["commands"], ["interface Ethernet1/25", "no " + BPDUGUARD])

    def test_l2_interfaces_stp_storm_mst_vlans_lists(self):
        show = dedent(
            """
            interface Ethernet1/25
              spanning-tree mst 0,2-4 cost 200
              spanning-tree mst 5 port-priority 32
              spanning-tree vlan 1,3-5 cost 10
            """,
        )
        config = self._stp_cfg(
            spanning_tree={
                "mst": [
                    {"instances": "0, 4,2,3", "cost": 100, "port_priority": 64},
                    {"instances": "5", "port_priority": 32},
                ],
                "vlans": [{"vlans": "3-5,1", "cost": 10}, {"vlans": "100", "port_priority": 128}],
            },
        )
        result = self._run(show, config)
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/25",
                "spanning-tree mst 0,2-4 cost 100",
                "spanning-tree mst 0,2-4 port-priority 64",
                "spanning-tree vlan 100 port-priority 128",
            ],
        )

    def test_l2_interfaces_stp_storm_mst_vlans_replaced_removes_entries(self):
        show = dedent(
            """
            interface Ethernet1/25
              spanning-tree mst 0,2-4 cost 200
              spanning-tree mst 5 port-priority 32
              spanning-tree vlan 1,3-5 cost 10
            """,
        )
        config = self._stp_cfg(
            spanning_tree={"mst": [{"instances": "0,2-4", "cost": 200}]},
            cdp_enable=True,
        )
        result = self._run(show, config, state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/25",
                "no spanning-tree mst 5 port-priority",
                "no spanning-tree vlan 1,3-5 cost",
            ],
        )

    def test_l2_interfaces_stp_storm_invalid_input_fails_before_commands(self):
        cases = {
            "mutually exclusive": {"storm_control": {"broadcast": {"level": "1", "pps": 10}}},
            "pps must be": {"storm_control": {"unicast": {"pps": 200000001}}},
            "must be a decimal": {"storm_control": {"unicast": {"level": "abc"}}},
            "must be a decimal ": {"storm_control": {"unicast": {"level": "100.5"}}},
            "at most two decimals": {"storm_control": {"unicast": {"level": "0.001"}}},
            "not a valid list": {"spanning_tree": {"mst": [{"instances": "x"}]}},
            "outside the range": {"spanning_tree": {"vlans": [{"vlans": "0-5"}]}},
        }
        for message, sections in cases.items():
            result = self._run(STP_STORM_BLOCK, self._stp_cfg(**sections), failed=True)
            self.assertIn(message.strip().split(" ")[0], result["msg"])
            self.assertNotIn("commands", result)

    def test_l2_interfaces_stp_storm_layer3_port_ignored(self):
        show = dedent(
            """
            interface Ethernet1/30
              no switchport
              spanning-tree bpduguard enable
              ip address 192.0.2.1/24
            interface Ethernet1/25
              switchport
            """,
        )
        result = self._run(show, state="gathered", changed=False)
        self.assertEqual(result["gathered"], [{"name": "Ethernet1/30"}, {"name": ETH25}])
        config = self._stp_cfg(
            "Ethernet1/30",
            spanning_tree={"bpduguard": True},
            storm_control={"action": "trap"},
        )
        with patch("ansible.module_utils.basic.AnsibleModule.warn") as warn:
            result = self._run(show, config, changed=False)
        self.assertEqual(result["commands"], [])
        warn.assert_called_once()
        self.assertIn("layer-3", warn.call_args[0][0])

    def test_get_routed_interfaces(self):
        config = "interface Ethernet1/1\n  no switchport\ninterface Ethernet1/2\n  switchport\n"
        self.assertEqual(get_routed_interfaces(config), {"Ethernet1/1"})


class TestGetPortChannelMembersUtil(TestNxosModule):
    """Direct tests for get_port_channel_members utility function."""

    module = nxos_l2_interfaces

    def setUp(self):
        super().setUp()

    def test_get_port_channel_members_multiple(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
            get_port_channel_members,
        )

        config = dedent(
            """\
            interface Ethernet1/1
             switchport
             channel-group 10 mode active
            interface Ethernet1/2
             switchport
             switchport access vlan 5
            interface Ethernet1/3
             switchport
             channel-group 20 mode passive
            """,
        )

        result = get_port_channel_members(config)
        self.assertEqual(result, {"Ethernet1/1", "Ethernet1/3"})

    def test_get_port_channel_members_none(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
            get_port_channel_members,
        )

        config = dedent(
            """\
            interface Ethernet1/1
             switchport
             switchport access vlan 5
            interface Ethernet1/2
             switchport mode trunk
            """,
        )

        result = get_port_channel_members(config)
        self.assertEqual(result, set())

    def test_get_port_channel_members_empty(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
            get_port_channel_members,
        )

        result = get_port_channel_members("")
        self.assertEqual(result, set())
