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

from ansible.module_utils.connection import ConnectionError

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces import (
    Interfaces,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    search_system_default_switchport,
)
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

        self.mock_get_admin_states = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces."
            "Interfaces.get_admin_states",
        )
        self.get_admin_states = self.mock_get_admin_states.start()
        self.get_admin_states.return_value = {}
        self.maxDiff = None

    def tearDown(self):
        super(TestNxosInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()
        self.mock_get_admin_states.stop()

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
            # loopback3 already up (NX-OS default) — no command expected
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
            # loopback3 already up (NX-OS default) — no command expected
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
            # loopback3 already up (NX-OS default) — no command expected
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

    def test_system_default_switchport_lines_with_carriage_returns(self):
        """The 'system default switchport' lines are read the same with CRLF and LF line endings."""
        for newline in ["\n", "\r\n"]:
            text = newline.join(
                ["no system default switchport", "system default switchport shutdown", ""],
            )
            mode = search_system_default_switchport(text)
            self.assertEqual(mode.group(1), "no ")
            shutdown = search_system_default_switchport(text, shutdown=True)
            self.assertIsNone(shutdown.group(1))
            text = newline.join(
                ["system default switchport", "no system default switchport shutdown", ""],
            )
            self.assertIsNone(search_system_default_switchport(text).group(1))
            self.assertEqual(search_system_default_switchport(text, shutdown=True).group(1), "no ")
        self.assertIsNone(search_system_default_switchport("interface Ethernet1/1\n"))

    def _admin_state_playbook(self, states, config, state="merged"):
        """Run the module with the admin states that the 'all' view reports."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/40
          interface Ethernet1/41
            no switchport
          interface Ethernet1/42
            switchport
          interface Ethernet1/43
            switchport
          interface Ethernet1/44
          interface Ethernet1/45
          interface loopback1
          interface mgmt0
          interface port-channel2
          interface Ethernet1/50
            no shutdown
        """,
        )
        self.get_admin_states.return_value = states
        set_module_args(dict(config=config, state=state))

    def test_admin_state_from_all_view(self):
        # An interface in its default admin state has no shutdown line in the plain running
        # config, the 'all' view tells its admin state. Same rule for routed and L2 ports.
        self._admin_state_playbook(
            {
                "ethernet1/40": False,
                "ethernet1/41": True,
                "ethernet1/42": False,
                "ethernet1/43": True,
                "ethernet1/44": False,
                "ethernet1/45": True,
            },
            [
                dict(name="Ethernet1/40", enabled=False),
                dict(name="Ethernet1/41", enabled=True),
                dict(name="Ethernet1/42", enabled=True),
                dict(name="Ethernet1/43", enabled=False),
                dict(name="Ethernet1/44", enabled=True),
                dict(name="Ethernet1/45", enabled=False),
            ],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/42",
                "no shutdown",
                "interface Ethernet1/43",
                "shutdown",
                "interface Ethernet1/44",
                "no shutdown",
                "interface Ethernet1/45",
                "shutdown",
            ],
        )
        self.get_admin_states.assert_called()

    def test_admin_state_from_all_view_idempotent_in_every_state(self):
        # The admin state that the device has is a no-op for merged, replaced and overridden,
        # and deleted does not touch it.
        states = {"ethernet1/40": False, "ethernet1/42": False, "ethernet1/43": True}
        config = [
            dict(name="Ethernet1/40", enabled=False),
            dict(name="Ethernet1/42", enabled=False),
            dict(name="Ethernet1/43", enabled=True),
        ]
        for state in ("merged", "replaced"):
            self._admin_state_playbook(states, config, state=state)
            self.execute_module(changed=False, commands=[])

        # overridden with the gathered configuration of the whole device
        self._admin_state_playbook(
            states,
            [dict(name="Ethernet1/50", enabled=True)] + config,
            state="overridden",
        )
        self.execute_module(changed=False, commands=[])

        self._admin_state_playbook(states, config[:1], state="deleted")
        self.execute_module(changed=False, commands=[])

    def test_admin_state_from_all_view_up_by_default_types(self):
        # loopbacks, mgmt0 and port-channels are read from the 'all' view as well
        self._admin_state_playbook(
            {"loopback1": True, "mgmt0": True, "port-channel2": False},
            [
                dict(name="loopback1", enabled=True),
                dict(name="mgmt0", enabled=True),
                dict(name="port-channel2", enabled=True),
            ],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface port-channel2", "no shutdown"])

        self._admin_state_playbook(
            {"loopback1": True, "mgmt0": True, "port-channel2": True},
            [dict(name="loopback1", enabled=False)],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface loopback1", "shutdown"])

    def test_admin_state_interface_missing_from_all_view(self):
        # An interface that the 'all' view does not list is handled as before: no admin state,
        # except for the types that are up by default.
        self._admin_state_playbook(
            {},
            [
                dict(name="Ethernet1/40", enabled=False),
                dict(name="Ethernet1/41", enabled=True),
                dict(name="loopback1", enabled=True),
            ],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/40", "shutdown", "interface Ethernet1/41", "no shutdown"],
        )

    def test_admin_state_is_only_read_when_needed(self):
        # An admin state line in the plain running config, an interface that does not exist
        # yet and no wanted admin state need no lookup.
        self._admin_state_playbook(
            {},
            [
                dict(name="Ethernet1/50", enabled=True),
                dict(name="Ethernet1/60", enabled=True),
                dict(name="Ethernet1/40", description="no admin state wanted"),
            ],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/40",
                "description no admin state wanted",
                "interface Ethernet1/60",
                "no shutdown",
            ],
        )
        self.get_admin_states.assert_not_called()

    def test_admin_state_when_the_mode_changes(self):
        # An interface that changes between L2 and L3 in this run gets the default admin state
        # of the new mode, its current admin state says nothing.
        self._admin_state_playbook(
            {"ethernet1/42": True, "ethernet1/44": True},
            [
                dict(name="Ethernet1/42", mode="layer3", enabled=True),
                dict(name="Ethernet1/44", mode="layer2", enabled=True),
            ],
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "interface Ethernet1/42",
                    "no shutdown",
                    "no switchport",
                    "interface Ethernet1/44",
                    "no shutdown",
                    "switchport",
                ],
            ),
        )

    def test_parse_admin_states(self):
        data = dedent(
            """\
          interface mgmt0
            no shutdown
          interface Ethernet1/1
            shutdown
          interface Ethernet1/31.210
            shutdown
          interface Vlan10
            no shutdown
          interface loopback0
        """,
        )
        self.assertEqual(
            Interfaces._parse_admin_states(data),
            {
                "mgmt0": True,
                "ethernet1/1": False,
                "ethernet1/31.210": False,
                "vlan10": True,
            },
        )
        self.assertEqual(Interfaces._parse_admin_states(None), {})

    # The interfaces of a leaf, every type, with and without an admin state line. The
    # 'all' view of the device tells the admin state of the ones that show no line.
    ALL_TYPES = dedent(
        """\
      interface mgmt0
        description MGMT
        vrf member management
        ip address 192.0.2.10/24
      interface Vlan1
      interface Vlan10
        no shutdown
      interface Ethernet1/17
        switchport
        switchport access vlan 100
        no shutdown
      interface Ethernet1/40
      interface Ethernet1/41
        shutdown
      interface Ethernet1/49
        no switchport
        no shutdown
      interface port-channel20
        switchport
      interface loopback1
      interface nve1
        no shutdown
    """,
    )
    ALL_TYPES_STATES = {
        "mgmt0": True,
        "vlan1": False,
        "vlan10": True,
        "ethernet1/17": True,
        "ethernet1/40": False,
        "ethernet1/41": False,
        "ethernet1/49": True,
        "port-channel20": True,
        "loopback1": True,
        "nve1": True,
    }
    ALL_TYPES_NAMES = [
        "mgmt0",
        "Vlan1",
        "Vlan10",
        "Ethernet1/17",
        "Ethernet1/40",
        "Ethernet1/41",
        "Ethernet1/49",
        "port-channel20",
        "loopback1",
        "nve1",
    ]

    def _all_types_playbook(self, states, config=None, state="merged", **kwargs):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = self.ALL_TYPES
        self.get_admin_states.return_value = states
        args = dict(state=state, **kwargs)
        if config is not None:
            args["config"] = config
        set_module_args(args)

    def _all_types_config(self):
        """Every interface of the device listed with the admin state that it has."""
        config = []
        for name in self.ALL_TYPES_NAMES:
            entry = dict(name=name, enabled=self.ALL_TYPES_STATES[name.lower()])
            if name == "mgmt0":
                entry["description"] = "MGMT"
            config.append(entry)
        return config

    def test_every_interface_type_unchanged_gives_no_commands(self):
        # The configuration that the device has is a no-op for every interface type, in
        # every state that compares the configuration.
        for state in ("merged", "replaced", "overridden"):
            self._all_types_playbook(self.ALL_TYPES_STATES, self._all_types_config(), state)
            self.execute_module(changed=False, commands=[])

    def test_every_interface_type_flipped_gives_exactly_one_command(self):
        for name in self.ALL_TYPES_NAMES:
            up = self.ALL_TYPES_STATES[name.lower()]
            for state in ("merged", "replaced"):
                self._all_types_playbook(
                    self.ALL_TYPES_STATES,
                    [dict(name=name, enabled=not up)],
                    state,
                )
                result = self.execute_module(changed=True)
                admin = ["no shutdown" if not up else "shutdown"]
                self.assertEqual(result["commands"][0], "interface " + name, name)
                self.assertEqual(result["commands"][-1], admin[0], name)
                self.assertEqual(
                    [c for c in result["commands"] if c in ("shutdown", "no shutdown")],
                    admin,
                    name,
                )

    def test_mgmt0_in_the_configuration_gets_no_admin_state_command_when_it_is_up(self):
        # The switches are managed through mgmt0, and it is the vPC peer keepalive interface.
        # A mgmt0 that is in the configuration and up never gets a shutdown or no shutdown,
        # whatever else is configured for it, in every state, with the 'all' view that lists
        # it and with one that does not.
        for states in (self.ALL_TYPES_STATES, {}):
            for state in ("merged", "replaced", "overridden"):
                # Ethernet1/40 shows no line and, without the 'all' view, nothing about its state
                config = [
                    dict(name=name, enabled=self.ALL_TYPES_STATES[name.lower()])
                    for name in self.ALL_TYPES_NAMES
                    if name not in ("mgmt0", "Ethernet1/40")
                ] + [dict(name="mgmt0", enabled=True, description="MGMT")]
                self._all_types_playbook(states, config, state)
                result = self.execute_module(changed=False)
                self.assertEqual(result["commands"], [])
        # a changed description is the only command of mgmt0
        self._all_types_playbook(
            self.ALL_TYPES_STATES,
            [dict(name="mgmt0", enabled=True, description="OOB")],
            "merged",
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface mgmt0", "description OOB"])
        # state deleted with mgmt0 in the configuration does not shut it
        self._all_types_playbook(
            self.ALL_TYPES_STATES,
            [dict(name="mgmt0", enabled=True)],
            "deleted",
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface mgmt0", "no description MGMT"])

    def test_mgmt0_that_is_not_in_the_configuration_is_never_shut(self):
        # An interface that is not in the configuration is only shut when its running config
        # shows 'no shutdown'. mgmt0 shows no admin state line, so overridden and deleted never
        # shut it, whatever the 'all' view says. The switches are managed through it.
        listed = [dict(name="Ethernet1/17", enabled=True)]
        # merged and replaced never touch an interface that is not in the configuration
        for state in ("merged", "replaced"):
            self._all_types_playbook(self.ALL_TYPES_STATES, listed, state)
            self.execute_module(changed=False, commands=[])
        for states in (self.ALL_TYPES_STATES, {}, dict(self.ALL_TYPES_STATES, mgmt0=False)):
            for state in ("overridden", "deleted"):
                self._all_types_playbook(states, listed if state == "overridden" else None, state)
                result = self.execute_module(changed=True)
                self.assertEqual(
                    result["commands"][:2],
                    ["interface mgmt0", "no description MGMT"],
                )
                self.assertNotIn("shutdown", result["commands"][:3])
        # the 'all' view is not even read for it
        self.get_admin_states.assert_not_called()

    def test_overridden_shuts_only_the_unlisted_interfaces_that_show_no_shutdown(self):
        # Every type. An unlisted interface that shows 'no shutdown' is shut, one that shows
        # 'shutdown' (also an SVI in its default state, the facts make it explicit) is not shut again,
        # and one that shows no admin state line is left alone, whatever the 'all' view says.
        expected = [
            "interface mgmt0",
            "no description MGMT",
            "interface Vlan10",
            "shutdown",
            "interface Ethernet1/49",
            "shutdown",
            "interface nve1",
            "shutdown",
        ]
        for states in (self.ALL_TYPES_STATES, {}):
            self._all_types_playbook(
                states,
                [dict(name="Ethernet1/17", enabled=True)],
                "overridden",
            )
            result = self.execute_module(changed=True)
            self.assertEqual(result["commands"], expected)
        self.get_admin_states.assert_not_called()

    def test_deleted_shuts_only_the_interfaces_that_show_no_shutdown(self):
        # With a configuration only its interfaces are deleted, without one all of them. Only the
        # ones that show 'no shutdown' are shut, as before, the 'all' view is not used.
        self._all_types_playbook(
            self.ALL_TYPES_STATES,
            [dict(name="Ethernet1/17"), dict(name="loopback1"), dict(name="Ethernet1/41")],
            "deleted",
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/17", "shutdown", "no switchport"],
        )
        self._all_types_playbook(self.ALL_TYPES_STATES, None, "deleted")
        result = self.execute_module(changed=True)
        self.assertEqual(
            [c for c in result["commands"] if c.startswith("interface ")],
            [
                "interface mgmt0",
                "interface Vlan10",
                "interface Ethernet1/17",
                "interface Ethernet1/49",
                "interface port-channel20",
                "interface nve1",
            ],
        )
        # port-channel20 is there for 'no switchport', the L2 default mode that deleted restores
        self.assertEqual(
            [c for c in result["commands"] if c in ("shutdown", "no shutdown")],
            ["shutdown", "shutdown", "shutdown", "shutdown"],
        )
        self.get_admin_states.assert_not_called()

    def test_overridden_unlisted_interfaces_that_are_shut_are_not_shut_again(self):
        # An unlisted interface that already shows 'shutdown', or an SVI in its
        # default shutdown state (the facts make it explicit), must not get a
        # 'shutdown' command again, or overridden would never be idempotent.
        # An unlisted interface that is up is still shut.
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan1
          interface Ethernet1/1
            description foo
          interface Ethernet1/6
            no shutdown
          interface Ethernet1/7
            shutdown
        """,
        )
        set_module_args(
            dict(config=[dict(name="Ethernet1/1", description="foo")], state="overridden"),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface Ethernet1/6", "shutdown"])

    def test_overridden_unlisted_interfaces_that_are_shut_idempotent(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan1
          interface Ethernet1/1
            description foo
          interface Ethernet1/7
            shutdown
        """,
        )
        set_module_args(
            dict(config=[dict(name="Ethernet1/1", description="foo")], state="overridden"),
        )
        self.execute_module(changed=False, commands=[])

    def test_admin_state_lookup_that_the_device_does_not_take(self):
        # If the device does not take the command of the 'all' view the module goes on as
        # it did before, with a warning: the admin state is unknown, the up by default types
        # stay as they are.
        self.mock_get_admin_states.stop()
        try:
            self.get_resource_connection_facts.return_value.get.side_effect = ConnectionError(
                "command not supported",
            )
            self._all_types_playbook(
                {},
                [
                    dict(name="Ethernet1/40", enabled=False),
                    dict(name="loopback1", enabled=True),
                    dict(name="mgmt0", enabled=True, description="MGMT"),
                ],
                "merged",
            )
            with patch("ansible.module_utils.basic.AnsibleModule.warn") as warn:
                result = self.execute_module(changed=True)
            self.assertEqual(result["commands"], ["interface Ethernet1/40", "shutdown"])
            warn.assert_called_once()
            self.assertIn("Could not read the admin state", warn.call_args[0][0])
            self.assertIn("command not supported", warn.call_args[0][0])
        finally:
            self.get_admin_states = self.mock_get_admin_states.start()

    def test_gathered_rendered_and_parsed_do_not_read_the_all_view(self):
        self._all_types_playbook(self.ALL_TYPES_STATES, None, "gathered")
        result = self.execute_module(changed=False)
        enabled = {i["name"]: i.get("enabled") for i in result["gathered"]}
        # what the plain running config shows: only the lines, no admin state is made up
        self.assertEqual(enabled["Ethernet1/40"], None)
        self.assertEqual(enabled["mgmt0"], None)
        self.assertEqual(enabled["Vlan1"], False)
        self.assertEqual(enabled["Ethernet1/41"], False)
        self.assertEqual(enabled["Ethernet1/49"], True)
        self._all_types_playbook(
            self.ALL_TYPES_STATES,
            [dict(name="Ethernet1/40", enabled=False)],
            "rendered",
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], ["interface Ethernet1/40", "shutdown"])
        self._all_types_playbook(
            self.ALL_TYPES_STATES,
            None,
            "parsed",
            running_config=self.ALL_TYPES,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            {i["name"]: i.get("enabled") for i in result["parsed"]}["Ethernet1/40"],
            None,
        )
        self.get_admin_states.assert_not_called()

    def test_loopback_enabled_idempotency(self):
        # NX-OS loopbacks are always-up by default and never show 'no shutdown'
        # in running-config.  Setting enabled: true on an already-up loopback
        # must be idempotent (no commands generated).
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface loopback0
            description RID
            ip address 10.0.0.1/32
          interface loopback1
          interface loopback2
            shutdown
        """,
        )

        playbook = dict(
            config=[
                # Up loopbacks with no explicit admin state — must be idempotent
                dict(name="loopback0", enabled=True),
                dict(name="loopback1", enabled=True),
                # Explicitly shut-down loopback — must still emit no shutdown
                dict(name="loopback2", enabled=True),
            ],
            state="merged",
        )
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertNotIn("interface loopback0", result["commands"])
        self.assertNotIn("interface loopback1", result["commands"])
        self.assertIn("interface loopback2", result["commands"])
        self.assertIn("no shutdown", result["commands"])

    def test_mgmt_and_port_channel_enabled_idempotency(self):
        # mgmt0 and port-channels are admin-up by default and, like loopbacks,
        # never show 'no shutdown' in running-config. enabled: true on an
        # already-up one must be idempotent, an explicit shutdown must still be
        # undone and a subinterface has its own admin state.
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            vrf member management
            ip address 192.0.2.10/24
          interface port-channel20
            switchport
            switchport mode trunk
          interface port-channel21
            shutdown
          interface port-channel22.100
            encapsulation dot1q 100
        """,
        )

        playbook = dict(
            config=[
                dict(name="mgmt0", enabled=True),
                dict(name="port-channel20", enabled=True),
                dict(name="port-channel21", enabled=True),
                dict(name="port-channel22.100", enabled=True),
            ],
            state="merged",
        )
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertNotIn("interface mgmt0", result["commands"])
        self.assertNotIn("interface port-channel20", result["commands"])
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel21",
                "no shutdown",
                "interface port-channel22.100",
                "no shutdown",
            ],
        )

    def test_mgmt_and_port_channel_enabled_replaced_and_shutdown(self):
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface mgmt0
            ip address 192.0.2.10/24
          interface port-channel20
            switchport
        """,
        )
        # replaced with enabled: true is idempotent
        set_module_args(
            dict(
                config=[
                    dict(name="mgmt0", enabled=True),
                    dict(name="port-channel20", enabled=True),
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
        # enabled: false still shuts an up port-channel down
        set_module_args(dict(config=[dict(name="port-channel20", enabled=False)], state="merged"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface port-channel20", "shutdown"])

    def test_new_layer2_interface_with_system_default_switchport(self):
        # AAP-88449: a missing interface must get an explicit "switchport"
        # even when the platform default is already layer2. Otherwise
        # nxos_l2_interfaces fails with "% Invalid command" on
        # "switchport mode ...".
        self.exec_get_defaults.return_value = {
            "default_mode": "layer2",
            "L2_enabled": True,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/1
          interface port-channel2
            switchport
        """,
        )

        playbook = dict(
            config=[
                dict(
                    name="port-channel30",
                    description="test",
                    enabled=True,
                    mode="layer2",
                ),
                # Existing interfaces that already match the platform default
                # must stay idempotent (no extra switchport line).
                dict(name="Ethernet1/1", mode="layer2"),
                dict(name="port-channel2", mode="layer2"),
            ],
            state="merged",
        )
        merged = [
            "interface port-channel30",
            "description test",
            "switchport",
            "no shutdown",
        ]
        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))
        self.assertIn("switchport", result["commands"])

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

    def test_vlan_default_shutdown_gathered(self):
        # test gathering the implicit default shutdown state of SVIs
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan10
            description implicit default shutdown
          interface Vlan11
            no shutdown
          interface Vlan12
            shutdown
          interface Vlan13
            description do not shutdown this svi
        """,
        )

        playbook = dict()
        playbook["state"] = "gathered"

        gathered_facts = [
            {
                "name": "Vlan10",
                "description": "implicit default shutdown",
                "enabled": False,
            },
            {
                "name": "Vlan11",
                "enabled": True,
            },
            {
                "name": "Vlan12",
                "enabled": False,
            },
            {
                "name": "Vlan13",
                "description": "do not shutdown this svi",
                "enabled": False,
            },
        ]

        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered_facts)

    def test_vlan_default_shutdown_idempotent(self):
        # test that the default state of an implicitly shutdown SVI is a no-op
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Vlan10
            description do not shutdown this svi
          interface Vlan11
            no shutdown
        """,
        )

        playbook = dict(
            config=[
                dict(name="Vlan10", description="do not shutdown this svi", enabled=False),
                dict(name="Vlan11", enabled=True),
            ],
        )
        playbook["state"] = "merged"
        set_module_args(playbook)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

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

    def test_nxos_interfaces_negotiate_auto_disable(self):
        """Setting negotiate_auto: false should emit 'no negotiate auto'."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/43
            speed 1000
            duplex full
        """,
        )

        playbook = dict(
            config=[
                dict(
                    name="Ethernet1/43",
                    speed="1000",
                    duplex="full",
                    negotiate_auto=False,
                ),
            ],
            state="merged",
        )

        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertIn("no negotiate auto", result["commands"])
        self.assertIn("interface Ethernet1/43", result["commands"])

    def test_nxos_interfaces_negotiate_auto_enable(self):
        """Setting negotiate_auto: true on an interface that has 'no negotiate auto'
        should emit 'negotiate auto' to restore the default."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/43
            speed 1000
            duplex full
            no negotiate auto
        """,
        )

        playbook = dict(
            config=[
                dict(
                    name="Ethernet1/43",
                    negotiate_auto=True,
                ),
            ],
            state="merged",
        )

        set_module_args(playbook)
        result = self.execute_module(changed=True)
        self.assertIn("negotiate auto", result["commands"])
        self.assertIn("interface Ethernet1/43", result["commands"])

    def test_nxos_interfaces_negotiate_auto_idempotent_true_default_have(self):
        """negotiate_auto: true when have has no key (device at default) → no change."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/43
            speed 1000
        """,
        )

        set_module_args(
            dict(
                config=[dict(name="Ethernet1/43", negotiate_auto=True)],
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_nxos_interfaces_negotiate_auto_idempotent_false_already_disabled(self):
        """negotiate_auto: false when have already has 'no negotiate auto' → no change."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/43
            speed 1000
            no negotiate auto
        """,
        )

        set_module_args(
            dict(
                config=[dict(name="Ethernet1/43", negotiate_auto=False)],
                state="merged",
            ),
        )
        self.execute_module(changed=False)

    def test_nxos_interfaces_negotiate_auto_replaced_omitted_restores_default(self):
        """replaced with negotiate_auto omitted when have has 'no negotiate auto' → emit 'negotiate auto'."""
        self.exec_get_defaults.return_value = {
            "default_mode": "layer3",
            "L2_enabled": False,
        }
        self.execute_show_command.return_value = dedent(
            """\
          interface Ethernet1/43
            speed 1000
            no negotiate auto
        """,
        )

        set_module_args(
            dict(
                config=[dict(name="Ethernet1/43", speed="1000")],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("negotiate auto", result["commands"])
        self.assertNotIn("no negotiate auto", result["commands"])
