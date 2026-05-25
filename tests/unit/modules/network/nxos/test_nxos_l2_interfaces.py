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

from ansible_collections.cisco.nxos.plugins.modules import nxos_l2_interfaces
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule


ignore_provider_arg = True


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

        self.mock_get_pc_members = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces."
            "L2_interfacesFacts._get_port_channel_members_from_device",
        )
        self.get_pc_members = self.mock_get_pc_members.start()
        self.get_pc_members.return_value = set()

        self.maxDiff = None

    def tearDown(self):
        super(TestNxosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()
        self.mock_get_pc_members.stop()

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
            "switchport trunk allowed vlan add 10-12",
            "interface Ethernet1/7",
            "switchport trunk allowed vlan add 21-22,101",
            "interface Ethernet1/8",
            "switchport trunk native vlan 10",
            "switchport trunk allowed vlan add 1-4000",
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
            "switchport trunk allowed vlan add 10-12",
            "interface Ethernet1/8",
            "switchport trunk native vlan 10",
            "switchport trunk allowed vlan add 1-4094",
            "interface Ethernet1/9",
            "switchport mode trunk",
            "switchport trunk native vlan 18",
            "switchport trunk allowed vlan add 222",
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
            "switchport trunk allowed vlan add 10-12",
            "interface Ethernet1/7",
            "no cdp enable",
            "switchport trunk native vlan 25",
            "interface Ethernet1/8",
            "switchport trunk allowed vlan remove 100-200,250",
            "switchport trunk allowed vlan add 33",
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
            "switchport trunk allowed vlan remove 30-40,50-60",
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
            "switchport trunk allowed vlan remove 5,13-500",
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
            "switchport trunk allowed vlan remove 10-19,251-349,351-500",
            "switchport trunk allowed vlan add 3999",
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
            "switchport trunk allowed vlan remove 20,30",
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
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
            "switchport trunk allowed vlan add 10-12",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)

    def test_l2_interfaces_deleted_fails_pc_member(self):
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
        self.get_pc_members.return_value = {"Ethernet1/4"}
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
        self.get_pc_members.return_value = {"Ethernet1/1"}
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


class TestGetPortChannelMembersFromDevice(TestNxosModule):
    """Direct tests for _get_port_channel_members_from_device (lines 47-57)."""

    module = nxos_l2_interfaces

    def setUp(self):
        super().setUp()
        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

    def tearDown(self):
        super().tearDown()
        self.mock_get_resource_connection_facts.stop()

    def test_parse_port_channel_summary(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces import (
            L2_interfacesFacts,
        )
        from unittest.mock import MagicMock

        module = MagicMock()
        facts = L2_interfacesFacts(module)
        connection = MagicMock()
        connection.get.return_value = dedent(
            """\
            --------------------------------------------------------------------------------
            Group Port-       Type     Protocol  Member Ports
                  Channel
            --------------------------------------------------------------------------------
            10    Po10(SU)    Eth      LACP      Eth1/1(P)    Eth1/2(P)
            20    Po20(SU)    Eth      LACP      Eth1/3(P)
            """,
        )

        result = facts._get_port_channel_members_from_device(connection)
        self.assertEqual(result, {"Ethernet1/1", "Ethernet1/2", "Ethernet1/3"})

    def test_parse_port_channel_summary_with_3slot_interface(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces import (
            L2_interfacesFacts,
        )
        from unittest.mock import MagicMock

        module = MagicMock()
        facts = L2_interfacesFacts(module)
        connection = MagicMock()
        connection.get.return_value = dedent(
            """\
            Group Port-       Type     Protocol  Member Ports
                  Channel
            10    Po10(SU)    Eth      LACP      Eth1/2/3(P)
            """,
        )

        result = facts._get_port_channel_members_from_device(connection)
        self.assertEqual(result, {"Ethernet1/2/3"})

    def test_parse_port_channel_summary_exception(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces import (
            L2_interfacesFacts,
        )
        from unittest.mock import MagicMock

        module = MagicMock()
        facts = L2_interfacesFacts(module)
        connection = MagicMock()
        connection.get.side_effect = Exception("command not supported")

        result = facts._get_port_channel_members_from_device(connection)
        self.assertEqual(result, set())

    def test_parse_port_channel_summary_empty(self):
        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces import (
            L2_interfacesFacts,
        )
        from unittest.mock import MagicMock

        module = MagicMock()
        facts = L2_interfacesFacts(module)
        connection = MagicMock()
        connection.get.return_value = ""

        result = facts._get_port_channel_members_from_device(connection)
        self.assertEqual(result, set())


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
