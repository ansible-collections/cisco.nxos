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

from ansible_collections.cisco.nxos.plugins.modules import nxos_interfaces
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule


ignore_provider_arg = True


class TestNxosInterfacesModule(TestNxosModule):
    module = nxos_interfaces

    def setUp(self):
        super(TestNxosInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.interfaces.interfaces."
            "InterfacesFacts._get_interface_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.mock_exec_get_defaults_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces."
            "Interfaces.get_interface_defaults",
        )
        self.exec_get_defaults = self.mock_exec_get_defaults_command.start()
        self.maxDiff = None

    def tearDown(self):
        super(TestNxosInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_interfaces_merged(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            description do not manage mgmt0!
          interface Ethernet1/1
            description foo
          interface Ethernet1/2
            description bar
            speed 1000
            duplex full
            mtu 4096
            ip forward
            fabric forwarding mode anycast-gateway
          interface Ethernet1/3
          interface Ethernet1/4
          interface Ethernet1/5
          interface Ethernet1/6
            no shutdown
          interface loopback0
            description test-loopback
        """,
        )

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/2",
                    speed=10000,
                    duplex="auto",
                    mtu=1500,
                    ip_forward=False,
                    fabric_forwarding_anycast_gateway=False,
                ),
                dict(
                    name="Ethernet1/3",
                    description="ansible",
                    mode="layer3",
                    service_policy={
                        "type_options": {
                            "qos": {
                                "output": "test-policy",
                            },
                        },
                    },
                ),
                dict(
                    name="Ethernet1/3.101",
                    description="test-sub-intf",
                    enabled=False,
                ),
                dict(name="Ethernet1/4", mode="layer2", mac_address="00:11:22:33:44:55"),
                dict(name="Ethernet1/5", logging={"link_status": True}),
                dict(
                    name="Ethernet1/6",
                    service_policy={
                        "input": "test-policy",
                    },
                ),
                dict(name="loopback1", description="test-loopback", logging={"trunk_status": True}),
            ],
            state="merged",
        )

        merged = [
            # Update existing device states with any differences in the playbook.
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "speed 10000",
            "mtu 1500",
            "duplex auto",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "interface Ethernet1/3",
            "description ansible",
            "service-policy type qos output test-policy",
            "interface Ethernet1/4",
            "mac-address 00:11:22:33:44:55",
            "switchport",
            "interface Ethernet1/5",
            "logging event port link-status",
            "interface loopback1",
            "description test-loopback",
            "logging event port trunk-status",
            "interface Ethernet1/6",
            "service-policy input test-policy",
            "interface Ethernet1/3.101",
            "shutdown",
            "description test-sub-intf",
        ]

        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_nxos_interfaces_deleted(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            description do not manage mgmt0!
          interface Ethernet1/1
            description foo
          interface Ethernet1/2
            description bar
            speed 1000
            duplex full
            mtu 4096
            ip forward
            fabric forwarding mode anycast-gateway
          interface Ethernet1/3
            service-policy type qos output test-policy
          interface Ethernet1/4
          interface Ethernet1/5
          interface Ethernet1/6
            no shutdown
          interface loopback0
            description test-loopback
        """,
        )

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/2",
                    speed=10000,
                    duplex="auto",
                    mtu=1500,
                    ip_forward=False,
                    fabric_forwarding_anycast_gateway=False,
                ),
                dict(name="Ethernet1/3", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/3.101",
                    description="test-sub-intf",
                    enabled=False,
                ),
                dict(name="Ethernet1/4", mode="layer2"),
                dict(name="Ethernet1/5"),
                dict(name="loopback1", description="test-loopback"),
            ],
            state="deleted",
        )

        deleted = [
            # Reset existing device state to default values. Scope is limited to
            # objects in the play. Ignores any play attrs other than 'name'.
            "interface Ethernet1/1",
            "no description foo",
            "interface Ethernet1/2",
            "no description bar",
            "no speed 1000",
            "no mtu 4096",
            "no duplex full",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "interface Ethernet1/3",
            "no service-policy type qos output test-policy",
        ]
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], deleted)

    def test_nxos_interfaces_replaced(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            description do not manage mgmt0!
          interface Ethernet1/1
            description foo
          interface Ethernet1/2
            description bar
            speed 1000
            duplex full
            mtu 4096
            ip forward
            fabric forwarding mode anycast-gateway
          interface Ethernet1/3
          interface Ethernet1/4
          interface Ethernet1/5
          interface Ethernet1/6
            no shutdown
          interface loopback0
            description test-loopback
        """,
        )

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/2",
                    speed=10000,
                    duplex="auto",
                    mtu=1500,
                    ip_forward=False,
                    fabric_forwarding_anycast_gateway=False,
                ),
                dict(name="Ethernet1/3", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/3.101",
                    description="test-sub-intf",
                    enabled=False,
                    logging={"link_status": True},
                ),
                dict(name="Ethernet1/4", mode="layer2"),
                dict(
                    name="Ethernet1/5",
                    service_policy={
                        "input": "test-policy",
                    },
                ),
                dict(name="loopback1", description="test-loopback"),
            ],
            state="replaced",
        )
        replaced = [
            # Scope is limited to objects in the play. The play is the source of
            # truth for the objects that are explicitly listed.
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "no description bar",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "speed 10000",
            "duplex auto",
            "mtu 1500",
            "interface Ethernet1/3",
            "description ansible",
            "interface Ethernet1/3.101",
            "logging event port link-status",
            "description test-sub-intf",
            "shutdown",
            "interface Ethernet1/4",
            "switchport",
            "interface Ethernet1/5",
            "service-policy input test-policy",
            "interface loopback1",
            "description test-loopback",
        ]
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(replaced))

    def test_nxos_interfaces_overridden(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            description do not manage mgmt0!
          interface Ethernet1/1
            description foo
          interface Ethernet1/2
            description bar
            speed 1000
            duplex full
            mtu 4096
            ip forward
            fabric forwarding mode anycast-gateway
          interface Ethernet1/3
            service-policy type qos output test-policy
          interface Ethernet1/4
          interface Ethernet1/5
            logging event port link-status
          interface Ethernet1/6
            no shutdown
          interface loopback0
            description test-loopback
        """,
        )

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/2",
                    speed=10000,
                    duplex="auto",
                    mtu=1500,
                    ip_forward=False,
                    fabric_forwarding_anycast_gateway=False,
                ),
                dict(name="Ethernet1/3", description="ansible", mode="layer3"),
                dict(
                    name="Ethernet1/3.101",
                    description="test-sub-intf",
                    enabled=False,
                ),
                dict(name="Ethernet1/4", mode="layer2"),
                dict(name="Ethernet1/5"),
                dict(name="loopback1", description="test-loopback"),
            ],
            state="replaced",
        )
        overridden = [
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "no description bar",
            "speed 10000",
            "mtu 1500",
            "duplex auto",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "interface Ethernet1/3",
            "description ansible",
            "no service-policy type qos output test-policy",
            "interface Ethernet1/3.101",
            "shutdown",
            "description test-sub-intf",
            "interface Ethernet1/4",
            "switchport",
            "interface Ethernet1/5",
            "no logging event port link-status",
            "interface loopback1",
            "description test-loopback",
        ]
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(overridden))

    def test_3(self):
        # Testing 'enabled' with different 'system default' settings.
        # This is the same as test_2 with some minor changes.
        self.exec_get_defaults.return_value = {
            "default_mode": "layer2",
            "L2_enabled": True,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
          interface Ethernet1/1
          interface Ethernet1/2
            no switchport
            no shutdown
          interface Ethernet1/3
            no switchport
          interface loopback1
          interface loopback2
            shutdown
          interface loopback3
          interface loopback8
          interface loopback9
            shutdown
          interface port-channel2
          interface port-channel3
            shutdown
        """,
        )

        playbook = dict(
            config=[
                # Set non-default states on existing objs
                dict(name="Ethernet1/1", mode="layer3", enabled=True),
                dict(name="loopback1", enabled=False),
                # Set default states on existing objs
                dict(name="Ethernet1/2", enabled=False),
                dict(name="loopback2", enabled=True),
                # Set explicit default state on existing objs (no chg)
                dict(name="loopback3", enabled=True),
                dict(name="port-channel3", enabled=True),
                # Set default state on non-existent objs; no state changes but need to create intf
                dict(name="loopback4", enabled=True),
                dict(name="port-channel4", enabled=True),
                dict(name="Ethernet1/4.101"),
            ],
        )
        merged = [
            "interface Ethernet1/1",
            "no shutdown",
            "no switchport",
            "interface Ethernet1/2",
            "shutdown",
            "interface loopback1",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface loopback3",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))

        # Test with an older image version which has different defaults
        merged_legacy = [
            "interface Ethernet1/1",
            "no shutdown",
            "no switchport",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface loopback3",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
        ]
        result = self.execute_module(changed=True, device="legacy")
        self.assertEqual(sorted(result["commands"]), sorted(merged_legacy))

        deleted = [
            "interface Ethernet1/2",
            "switchport",
            "shutdown",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

        replaced = [
            "interface Ethernet1/1",
            "no switchport",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface loopback3",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(replaced))

    def test_4(self):
        # Basic idempotence test
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/1
          interface Ethernet1/2
            switchport
            speed 1000
            shutdown
        """,
        )

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", mode="layer3"),
                dict(name="Ethernet1/2", mode="layer2", enabled=False),
            ],
        )
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook)
        self.execute_module(changed=False, commands=merged)

    def test_5(self):
        # 'state: deleted' without 'config'; clean all objects.
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/1
            switchport
          interface Ethernet1/2
            speed 1000
            no shutdown
        """,
        )

        playbook = dict()
        deleted = [
            "interface Ethernet1/1",
            "no switchport",
            "interface Ethernet1/2",
            "no speed 1000",
            "shutdown",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(sorted(result["commands"]), sorted(deleted))

    def test_6_gathered(self):
        # check for parsing correct contexts
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface nve1
            no shutdown
            source-interface loopback1
            logging event port link-status
          interface Ethernet1/1
            switchport
            description interface
          interface Ethernet1/2
            speed 1000
            service-policy type qos output test-policy
            no shutdown
          interface loopback1
        """,
        )

        playbook = dict()
        playbook["state"] = "gathered"

        gathered_facts = [
            {
                "name": "nve1",
                "enabled": True,
                "logging": {
                    "link_status": True,
                },
            },
            {
                "name": "Ethernet1/1",
                "mode": "layer2",
                "description": "interface",
            },
            {
                "enabled": True,
                "name": "Ethernet1/2",
                "speed": "1000",
                "service_policy": {
                    "type_options": {
                        "qos": {
                            "output": "test-policy",
                        },
                    },
                },
            },
            {"name": "loopback1"},
        ]
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        print(result["gathered"])
        self.assertEqual(result["gathered"], gathered_facts)

    def test_7_purged(self):
        # check for parsing correct contexts
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan1
          interface Vlan42
            mtu 1800
          interface port-channel10
          interface port-channel11
          interface Ethernet1/1
          interface Ethernet1/2
          interface Ethernet1/2.100
            description sub-intf
        """,
        )

        playbook = dict(
            config=[
                dict(name="Vlan42"),
                dict(name="port-channel10"),
                dict(name="Ethernet1/2.100"),
            ],
        )
        playbook["state"] = "purged"

        commands = [
            "no interface port-channel10",
            "no interface Ethernet1/2.100",
            "no interface Vlan42",
        ]

        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vlan_enabled(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan9
            no shutdown
          interface Vlan10
        """,
        )

        playbook = dict(
            config=[
                dict(name="Vlan9", enabled=False),
                dict(name="Vlan10", enabled=True),
                dict(name="Vlan11", enabled=True),
            ],
        )
        merged = [
            "interface Vlan9",
            "shutdown",
            "interface Vlan10",
            "no shutdown",
            "interface Vlan11",
            "no shutdown",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))

    def test_mode_mtu(self):
        # test mode change with MTU
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/28
                description Auto_Cable_Testing
                mtu 3456
            """,
        )

        playbook = dict(
            config=[
                dict(
                    name="Ethernet1/28",
                    description="Ansible Port Turn Up1",
                    mode="layer2",
                    mtu="9216",
                    speed="1000",
                    duplex="full",
                    enabled=True,
                ),
            ],
        )
        replaced = [
            "interface Ethernet1/28",
            "description Ansible Port Turn Up1",
            "switchport",
            "mtu 9216",
            "speed 1000",
            "duplex full",
            "no shutdown",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(replaced))
