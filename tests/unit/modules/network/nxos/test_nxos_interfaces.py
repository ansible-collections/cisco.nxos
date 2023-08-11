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

from ansible_collections.cisco.nxos.plugins.modules import nxos_interfaces
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosInterfacesModule(TestNxosModule):
    module = nxos_interfaces

    def setUp(self):
        super(TestNxosInterfacesModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS",
        )
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces.Interfaces.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_get_system_defaults = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces.Interfaces.get_system_defaults",
        )
        self.get_system_defaults = self.mock_get_system_defaults.start()

        self.mock_get_platform = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces.Interfaces.get_platform",
        )
        self.get_platform = self.mock_get_platform.start()

    def tearDown(self):
        super(TestNxosInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_system_defaults.stop()
        self.mock_get_platform.stop()

    def load_fixtures(self, commands=None, device=""):
        self.mock_FACT_LEGACY_SUBSETS.return_value = dict()
        self.get_resource_connection_config.return_value = None
        self.edit_config.return_value = None
        if device == "legacy":
            # call execute_module() with device='legacy' to use this codepath
            self.get_platform.return_value = "N3K-Cxxx"
        else:
            self.get_platform.return_value = "N9K-Cxxx"

    SHOW_RUN_INTF = "show running-config | section ^interface"

    def test_1(self):
        # Overall general test for each state: merged, deleted, overridden, replaced
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
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
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

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
        )
        merged = [
            # Update existing device states with any differences in the playbook.
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "speed 10000",
            "duplex auto",
            "mtu 1500",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "interface Ethernet1/3",
            "description ansible",
            "interface Ethernet1/3.101",
            "description test-sub-intf",
            "interface Ethernet1/4",
            "switchport",
            "interface loopback1",
            "description test-loopback",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        deleted = [
            # Reset existing device state to default values. Scope is limited to
            # objects in the play. Ignores any play attrs other than 'name'.
            "interface Ethernet1/1",
            "no description",
            "interface Ethernet1/2",
            "no description",
            "no speed",
            "no duplex",
            "no mtu",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        replaced = [
            # Scope is limited to objects in the play. The play is the source of
            # truth for the objects that are explicitly listed.
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "no description",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "speed 10000",
            "duplex auto",
            "mtu 1500",
            "interface Ethernet1/3",
            "description ansible",
            "interface Ethernet1/3.101",
            "description test-sub-intf",
            "interface Ethernet1/4",
            "switchport",
            "interface loopback1",
            "description test-loopback",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

        overridden = [
            # The play is the source of truth. Similar to replaced but the scope
            # includes all objects on the device; i.e. it will also reset state
            # on objects not found in the play.
            "interface Ethernet1/1",
            "description ansible",
            "interface Ethernet1/2",
            "no description",
            "no ip forward",
            "no fabric forwarding mode anycast-gateway",
            "speed 10000",
            "duplex auto",
            "mtu 1500",
            "interface Ethernet1/6",
            "shutdown",
            "interface loopback0",
            "no description",
            "interface Ethernet1/3",
            "description ansible",
            "interface Ethernet1/4",
            "switchport",
            "interface Ethernet1/3.101",
            "description test-sub-intf",
            "interface loopback1",
            "description test-loopback",
            "interface mgmt0",
            "no description",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

    def test_2(self):
        # 'enabled'/shutdown behaviors are tricky:
        # - different default states for different interface types for different
        #   platforms, based on 'system default switchport' settings
        # - virtual interfaces may not exist yet
        # - idempotence for interfaces with all default states
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
            """\
          interface mgmt0
          interface Ethernet1/1
          interface Ethernet1/2
            switchport
            shutdown
          interface Ethernet1/3
            switchport
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
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

        playbook = dict(
            config=[
                # Set non-default states on existing objs
                dict(name="Ethernet1/1", mode="layer3", enabled=True),
                dict(name="loopback1", enabled=False),
                # Set default states on existing objs
                dict(name="Ethernet1/2", enabled=True),
                dict(name="loopback2", enabled=True),
                # Set explicit default state on existing objs (no chg)
                dict(name="Ethernet1/3", enabled=True),
                dict(name="loopback3", enabled=True),
                dict(name="port-channel3", enabled=True),
                dict(name="loopback4", enabled=True),
                dict(name="port-channel4", enabled=True),
                dict(name="Ethernet1/4.101"),
            ],
        )
        # Testing with newer code version
        merged = [
            "interface Ethernet1/1",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "no shutdown",
            "interface loopback2",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        deleted = [
            # e1/2 becomes L3 so enable default changes to false
            "interface Ethernet1/2",
            "no switchport",
            "interface loopback2",
            "no shutdown",
            "interface Ethernet1/3",
            "no switchport",
            "interface port-channel3",
            "no shutdown",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        replaced = [
            "interface Ethernet1/1",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "no switchport",
            "no shutdown",
            "interface loopback2",
            "no shutdown",
            "interface Ethernet1/3",
            "no switchport",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

        overridden = [
            "interface Ethernet1/2",
            "no switchport",
            "no shutdown",
            "interface Ethernet1/3",
            "no switchport",
            "no shutdown",
            "interface loopback2",
            "no shutdown",
            "interface loopback9",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface Ethernet1/1",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

    def test_3(self):
        # Testing 'enabled' with different 'system default' settings.
        # This is the same as test_2 with some minor changes.
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L2 !!
          !
          system default switchport
          system default switchport shutdown
        """,
        )
        intf = dedent(
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
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

        playbook = dict(
            config=[
                # Set non-default states on existing objs
                dict(name="Ethernet1/1", mode="layer3", enabled=True),
                dict(name="loopback1", enabled=False),
                # Set default states on existing objs
                dict(name="Ethernet1/2", enabled=False),
                dict(name="loopback2", enabled=True),
                # Set explicit default state on existing objs (no chg)
                dict(name="Ethernet1/3", enabled=False),
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
            "no switchport",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        # Test with an older image version which has different defaults
        merged_legacy = [
            "interface Ethernet1/1",
            "no switchport",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface Ethernet1/3",
            "shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        self.execute_module(changed=True, commands=merged_legacy, device="legacy")

        deleted = [
            "interface Ethernet1/2",
            "switchport",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface Ethernet1/3",
            "switchport",
            "interface port-channel3",
            "no shutdown",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        replaced = [
            "interface Ethernet1/1",
            "no switchport",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface Ethernet1/2",
            "switchport",
            "shutdown",
            "interface loopback2",
            "no shutdown",
            "interface Ethernet1/3",
            "switchport",
            "interface port-channel3",
            "no shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

        playbook = dict(
            config=[
                # Set non-default states on existing objs
                dict(name="Ethernet1/1", mode="layer3", enabled=True),
                dict(name="loopback1", enabled=False),
                # Set default states on existing objs
                dict(name="Ethernet1/2", enabled=False),
                dict(name="loopback2", enabled=True),
                # Set explicit default state on existing objs (no chg)
                dict(name="Ethernet1/3", enabled=False),
                dict(name="loopback3", enabled=True),
                dict(name="port-channel3", enabled=True),
                # Set default state on non-existent objs; no state changes but need to create intf
                dict(name="loopback4", enabled=True),
                dict(name="port-channel4", enabled=True),
                dict(name="Ethernet1/4.101", enabled=False),
                dict(name="Ethernet1/4.102", enabled=True),
            ],
        )

        overridden = [
            "interface Ethernet1/2",
            "switchport",
            "shutdown",
            "interface Ethernet1/3",
            "switchport",
            "interface loopback2",
            "no shutdown",
            "interface loopback9",
            "no shutdown",
            "interface port-channel3",
            "no shutdown",
            "interface Ethernet1/1",
            "no switchport",
            "no shutdown",
            "interface loopback1",
            "shutdown",
            "interface loopback4",
            "no shutdown",
            "interface port-channel4",
            "no shutdown",
            "interface Ethernet1/4.101",
            "interface Ethernet1/4.102",
            "no shutdown",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

    def test_4(self):
        # Basic idempotence test
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
            """\
          interface Ethernet1/1
          interface Ethernet1/2
            switchport
            speed 1000
            shutdown
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

        playbook = dict(
            config=[
                dict(name="Ethernet1/1", mode="layer3"),
                dict(name="Ethernet1/2", mode="layer2", enabled=False),
            ],
        )
        merged = []
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=False, commands=merged)

    def test_5(self):
        # 'state: deleted' without 'config'; clean all objects.
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
            """\
          interface Ethernet1/1
            switchport
          interface Ethernet1/2
            speed 1000
            no shutdown
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

        playbook = dict()
        deleted = [
            "interface Ethernet1/1",
            "no switchport",
            "interface Ethernet1/2",
            "no speed",
            "shutdown",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

    def test_6_gathered(self):
        # check for parsing correct contexts
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
            """\
          interface nve1
            no shutdown
            source-interface loopback1
          interface Ethernet1/1
            switchport
            description interface
          interface Ethernet1/2
            speed 1000
            no shutdown
          interface loopback1
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

        playbook = dict()
        playbook["state"] = "gathered"

        gathered_facts = [
            {"name": "nve1", "enabled": True},
            {
                "name": "Ethernet1/1",
                "mode": "layer2",
                "description": "interface",
            },
            {"name": "Ethernet1/2", "enabled": True, "speed": "1000"},
            {"name": "loopback1"},
        ]
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered_facts)

    def test_7_purged(self):
        # check for parsing correct contexts
        sysdefs = dedent(
            """\
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
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
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

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

        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vlan_enabled(self):
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
          no system default switchport shutdown
        """,
        )
        intf = dedent(
            """\
          interface Vlan9
            no shutdown
          interface Vlan10
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

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
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

    def test_mode_mtu(self):
        # test mode change with MTU
        sysdefs = dedent(
            """\
          !
          ! Interfaces default to L3 !!
          !
          no system default switchport
        """,
        )
        intf = dedent(
            """\
          interface Ethernet1/28
            description Auto_Cable_Testing
            mtu 9216
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_RUN_INTF: intf}
        self.get_system_defaults.return_value = sysdefs

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
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)
