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
                    "allowed_vlans": "30-45,47",
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
                    "allowed_vlans": "210",
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
                    },
                ],
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "switchport mode trunk",
            "switchport trunk allowed vlan 10-12",
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
                            "allowed_vlans": "25-27",
                        },
                    },
                    {
                        "name": "Ethernet1/8",
                        "trunk": {
                            "allowed_vlans": "none",
                        },
                    },
                ],
                state="replaced",
            ),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "switchport access vlan 8",
            "switchport trunk allowed vlan 10-12",
            "interface Ethernet1/7",
            "no switchport trunk native vlan 15",
            "interface Ethernet1/8",
            "switchport trunk allowed vlan none",
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
            "switchport access vlan 6",
            "switchport trunk allowed vlan 10-12",
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
            """,
        )

        set_module_args(
            dict(state="deleted"),
        )

        expected_commands = [
            "interface Ethernet1/6",
            "no switchport trunk native vlan 10",
            "interface Ethernet1/7",
            "no switchport mode trunk",
            "no switchport trunk allowed vlan",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], expected_commands)
