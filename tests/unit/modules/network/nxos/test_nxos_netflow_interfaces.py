# (c) 2026 Red Hat Inc.
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

from copy import deepcopy
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_netflow_interfaces
from ansible_collections.cisco.nxos.tests.unit.modules.utils import AnsibleFailJson

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

# `show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"`:
# the device displays trailing spaces on the monitor lines, the parser ignores them
BASE = dedent(
    """\
        interface Vlan100
        interface Vlan200
          ip flow monitor MON_V4 input
        interface port-channel10
          ip flow monitor MON_V4 input
          ip flow monitor MON_V4 output
        interface Ethernet1/1
          ip flow monitor MON_V4 input
          ipv6 flow monitor MON_V6 input
        interface Ethernet1/2
        interface Ethernet1/3
          layer2-switched flow monitor MON_L2 input
        interface Ethernet1/4.10
          ip flow monitor MON_V4 input
        """,
)


def _mon(protocol, monitor, direction="input"):
    return dict(monitor=monitor, direction=direction, protocol=protocol)


BASE_FACTS = [
    dict(name="Ethernet1/1", flow_monitors=[_mon("ipv4", "MON_V4"), _mon("ipv6", "MON_V6")]),
    dict(name="Ethernet1/3", flow_monitors=[_mon("layer2_switched", "MON_L2")]),
    dict(name="Ethernet1/4.10", flow_monitors=[_mon("ipv4", "MON_V4")]),
    dict(name="Vlan200", flow_monitors=[_mon("ipv4", "MON_V4")]),
    dict(
        name="port-channel10",
        flow_monitors=[_mon("ipv4", "MON_V4"), _mon("ipv4", "MON_V4", "output")],
    ),
]


class TestNxosNetflowInterfacesModule(TestNxosModule):
    module = nxos_netflow_interfaces

    def setUp(self):
        super(TestNxosNetflowInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.netflow_interfaces.netflow_interfaces.Netflow_interfacesFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

        # the device in the tests does not change, the check that the commands were applied is
        # only active in the tests that ask for it
        self.mock_check_applied = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.netflow_interfaces.netflow_interfaces.Netflow_interfaces._check_applied",
        )
        self.mock_check_applied.start()
        self.check_applied_active = False

    def _check_applied(self):
        self.mock_check_applied.stop()
        self.check_applied_active = True

    def tearDown(self):
        super(TestNxosNetflowInterfacesModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()
        if not self.check_applied_active:
            self.mock_check_applied.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    def _fail(self, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(failed=True)

    # facts

    def test_nxos_netflow_interfaces_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_netflow_interfaces_gathered(self):
        self.get_config.return_value = BASE
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)

    def test_nxos_netflow_interfaces_parsed_lines_with_trailing_spaces(self):
        cfg = "interface Ethernet1/9\n  ip flow monitor MON_V4 input  \n  ipv6 flow monitor MON_V6 output \n"
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            [
                dict(
                    name="Ethernet1/9",
                    flow_monitors=[_mon("ipv4", "MON_V4"), _mon("ipv6", "MON_V6", "output")],
                ),
            ],
        )

    def test_nxos_netflow_interfaces_gathered_nothing(self):
        self.get_config.return_value = "interface Ethernet1/1\ninterface Ethernet1/2\n"
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], [])

    # rendered

    def test_nxos_netflow_interfaces_rendered(self):
        result = self._run(
            False,
            config=[
                dict(
                    name="Eth1/3",
                    flow_monitors=[
                        dict(monitor="MON_L2", protocol="layer2_switched", direction="input"),
                        dict(monitor="MON_V6", protocol="ipv6", direction="input"),
                        dict(monitor="MON_V4", direction="output"),
                        dict(monitor="MON_V4", direction="input"),
                    ],
                ),
            ],
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            [
                "interface Ethernet1/3",
                "ip flow monitor MON_V4 input",
                "ip flow monitor MON_V4 output",
                "ipv6 flow monitor MON_V6 input",
                "layer2-switched flow monitor MON_L2 input",
            ],
        )

    # merged

    def test_nxos_netflow_interfaces_idempotent_with_the_gathered_data(self):
        self.get_config.return_value = BASE
        for state in ["merged", "replaced", "overridden"]:
            self._run(False, config=deepcopy(BASE_FACTS), state=state)

    def test_nxos_netflow_interfaces_idempotent_with_short_names(self):
        self.get_config.return_value = BASE
        config = [
            dict(name="Eth1/1", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            dict(name="Po10", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            dict(name="vlan200", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
        ]
        for state in ["merged", "replaced"]:
            self._run(state == "replaced", config=deepcopy(config), state=state)

    def test_nxos_netflow_interfaces_merged_adds(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/2",
                    flow_monitors=[
                        dict(monitor="MON_V6", protocol="ipv6", direction="input"),
                        dict(monitor="MON_V4", direction="input"),
                    ],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/2",
                "ip flow monitor MON_V4 input",
                "ipv6 flow monitor MON_V6 input",
            ],
        )

    def test_nxos_netflow_interfaces_merged_keeps_what_is_not_given(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/1",
                    flow_monitors=[dict(monitor="MON_V4", direction="output")],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/1", "ip flow monitor MON_V4 output"],
        )

    def test_nxos_netflow_interfaces_merged_another_monitor_replaces_the_old_one_first(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/1",
                    flow_monitors=[dict(monitor="MON_V4B", direction="input")],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ip flow monitor MON_V4 input",
                "ip flow monitor MON_V4B input",
            ],
        )

    def test_nxos_netflow_interfaces_merged_without_flow_monitors_changes_nothing(self):
        self.get_config.return_value = BASE
        self._run(False, config=[dict(name="Ethernet1/1")], state="merged")

    def test_nxos_netflow_interfaces_merged_the_same_monitor_twice_is_accepted(self):
        self.get_config.return_value = BASE
        monitor = dict(monitor="MON_V4", direction="input")
        self._run(
            False,
            config=[dict(name="Ethernet1/1", flow_monitors=[monitor, deepcopy(monitor)])],
            state="merged",
        )

    def test_nxos_netflow_interfaces_two_entries_of_an_interface_are_combined(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(name="Eth1/2", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
                dict(
                    name="Ethernet1/2",
                    flow_monitors=[dict(monitor="MON_V4", direction="output")],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/2",
                "ip flow monitor MON_V4 input",
                "ip flow monitor MON_V4 output",
            ],
        )

    # replaced

    def test_nxos_netflow_interfaces_replaced_removes_what_is_not_given(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(name="Ethernet1/1", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
                dict(name="Vlan200", flow_monitors=[dict(monitor="MON_V4B", direction="input")]),
            ],
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ipv6 flow monitor MON_V6 input",
                "interface Vlan200",
                "no ip flow monitor MON_V4 input",
                "ip flow monitor MON_V4B input",
            ],
        )

    def test_nxos_netflow_interfaces_replaced_without_flow_monitors_removes_them(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(name="port-channel10")], state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel10",
                "no ip flow monitor MON_V4 input",
                "no ip flow monitor MON_V4 output",
            ],
        )

    def test_nxos_netflow_interfaces_replaced_a_new_interface(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(name="Ethernet1/9", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            ],
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/9", "ip flow monitor MON_V4 input"],
        )

    # overridden

    def test_nxos_netflow_interfaces_overridden_removes_the_other_interfaces(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(name="Ethernet1/1", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
                dict(
                    name="Ethernet1/3",
                    flow_monitors=[
                        dict(monitor="MON_L2", protocol="layer2_switched", direction="input"),
                    ],
                ),
                dict(
                    name="Ethernet1/4.10",
                    flow_monitors=[dict(monitor="MON_V4", direction="input")],
                ),
                dict(name="Vlan200", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            ],
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ipv6 flow monitor MON_V6 input",
                "interface port-channel10",
                "no ip flow monitor MON_V4 input",
                "no ip flow monitor MON_V4 output",
            ],
        )

    # deleted

    def test_nxos_netflow_interfaces_deleted_listed(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Eth1/1"), dict(name="Ethernet1/2")],
            state="deleted",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ip flow monitor MON_V4 input",
                "no ipv6 flow monitor MON_V6 input",
            ],
        )

    def test_nxos_netflow_interfaces_deleted_everything(self):
        self.get_config.return_value = BASE
        result = self._run(True, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ip flow monitor MON_V4 input",
                "no ipv6 flow monitor MON_V6 input",
                "interface Ethernet1/3",
                "no layer2-switched flow monitor MON_L2 input",
                "interface Ethernet1/4.10",
                "no ip flow monitor MON_V4 input",
                "interface Vlan200",
                "no ip flow monitor MON_V4 input",
                "interface port-channel10",
                "no ip flow monitor MON_V4 input",
                "no ip flow monitor MON_V4 output",
            ],
        )

    def test_nxos_netflow_interfaces_deleted_nothing_to_delete(self):
        self.get_config.return_value = "interface Ethernet1/1\n"
        self._run(False, state="deleted")
        self._run(False, config=[dict(name="Ethernet1/1")], state="deleted")

    # validation and modes

    def test_nxos_netflow_interfaces_two_monitors_for_a_protocol_and_direction_are_rejected(self):
        self.get_config.return_value = BASE
        result = self._fail(
            config=[
                dict(
                    name="Ethernet1/2",
                    flow_monitors=[
                        dict(monitor="MON_V4", direction="input"),
                        dict(monitor="MON_V4B", direction="input"),
                    ],
                ),
            ],
            state="merged",
        )
        self.assertIn("only one flow monitor is possible", result["msg"])

    def test_nxos_netflow_interfaces_wrong_values_are_rejected(self):
        for flow_monitor in [
            dict(monitor="MON_V4", direction="both"),
            dict(monitor="MON_V4", direction="input", protocol="ipv5"),
            dict(direction="input"),
            dict(monitor="MON_V4"),
        ]:
            self._fail(
                config=[dict(name="Ethernet1/1", flow_monitors=[flow_monitor])],
                state="rendered",
            )

    def test_nxos_netflow_interfaces_empty_config(self):
        set_module_args(dict(config=[], state="merged"), ignore_provider_arg)
        result = self.execute_module(failed=True)
        self.assertIn("must not be empty", result["msg"])

    def test_nxos_netflow_interfaces_check_mode_sends_nothing(self):
        self.get_config.return_value = BASE
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/2",
                        flow_monitors=[dict(monitor="MON_V4", direction="input")],
                    ),
                ],
                state="merged",
                _ansible_check_mode=True,
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/2", "ip flow monitor MON_V4 input"],
        )
        self.get_resource_connection.return_value.edit_config.assert_not_called()

    # negative cases

    def test_nxos_netflow_interfaces_rejected_command_fails_with_the_text_of_the_device(self):
        self.get_config.return_value = BASE
        error = (
            "b'ip flow monitor NOPE input\\r\\r\\nError: Monitor NOPE does not exist."
            "\\r\\n\\rswitch(config-if)# '"
        )
        self.get_resource_connection.return_value.edit_config.side_effect = Exception(error)
        result = self._fail(
            config=[
                dict(name="Ethernet1/2", flow_monitors=[dict(monitor="NOPE", direction="input")]),
            ],
            state="merged",
        )
        self.assertIn("The device rejected a command", result["msg"])
        self.assertIn("Monitor NOPE does not exist.", result["msg"])
        self.assertNotIn("\\r", result["msg"])
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/2", "ip flow monitor NOPE input"],
        )

    def test_nxos_netflow_interfaces_rejected_command_text_without_bytes_marker(self):
        self.get_config.return_value = BASE
        self.get_resource_connection.return_value.edit_config.side_effect = Exception("boom")
        result = self._fail(
            config=[
                dict(name="Ethernet1/2", flow_monitors=[dict(monitor="M", direction="input")]),
            ],
            state="merged",
        )
        self.assertTrue(result["msg"].endswith(": boom"))

    def test_nxos_netflow_interfaces_command_accepted_but_not_applied_fails(self):
        # the egress TCAM is not carved: the device only logs a message
        self._check_applied()
        self.get_config.return_value = BASE
        result = self._fail(
            config=[
                dict(
                    name="Ethernet1/2",
                    flow_monitors=[dict(monitor="MON_V4", direction="output")],
                ),
            ],
            state="merged",
        )
        self.assertIn("did not apply: Ethernet1/2: ip flow monitor MON_V4 output", result["msg"])
        self.assertIn("egr-netflow", result["msg"])

    def test_nxos_netflow_interfaces_applied_commands_pass_the_check(self):
        self._check_applied()
        after = BASE.replace(
            "interface Ethernet1/2\n",
            "interface Ethernet1/2\n  ip flow monitor MON_V4 input  \n",
        )
        self.get_config.side_effect = [BASE, after]
        result = self._run(
            True,
            config=[
                dict(name="Eth1/2", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            ],
            state="merged",
        )
        self.assertEqual(result["after"][1]["name"], "Ethernet1/2")

    def test_nxos_netflow_interfaces_not_applied_is_not_checked_in_check_mode(self):
        self._check_applied()
        self.get_config.return_value = BASE
        set_module_args(
            dict(
                config=[
                    dict(
                        name="Ethernet1/2",
                        flow_monitors=[dict(monitor="MON_V4", direction="output")],
                    ),
                ],
                state="merged",
                _ansible_check_mode=True,
            ),
            ignore_provider_arg,
        )
        self.execute_module(changed=True)

    def test_nxos_netflow_interfaces_name_variants_are_the_same_interface(self):
        self.get_config.return_value = BASE
        for name in ["Eth1/1", "eth1/1", "ethernet1/1", "ETHERNET1/1", "Ethernet1/1"]:
            for state in ["merged", "replaced"]:
                self._run(
                    False,
                    config=[
                        dict(
                            name=name,
                            flow_monitors=[
                                dict(monitor="MON_V4", direction="input"),
                                dict(monitor="MON_V6", protocol="ipv6", direction="input"),
                            ],
                        ),
                    ],
                    state=state,
                )

    def test_nxos_netflow_interfaces_name_variants_of_other_interface_types(self):
        self.get_config.return_value = BASE
        for name in ["Po10", "po10", "port-channel10", "Port-Channel10"]:
            self._run(
                False,
                config=[
                    dict(
                        name=name,
                        flow_monitors=[
                            dict(monitor="MON_V4", direction="input"),
                            dict(monitor="MON_V4", direction="output"),
                        ],
                    ),
                ],
                state="merged",
            )
        for name in ["Vlan200", "vlan200", "VLAN200"]:
            self._run(
                False,
                config=[
                    dict(name=name, flow_monitors=[dict(monitor="MON_V4", direction="input")]),
                ],
                state="merged",
            )

    def test_nxos_netflow_interfaces_parsed_garbage_gives_nothing(self):
        cfg = "%%% not a config\ninterface\n  ip flow monitor\nfoo\n  ip flow monitor A sideways\n"
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(result["parsed"], [])

    def test_nxos_netflow_interfaces_parsed_ignores_the_other_lines(self):
        cfg = dedent(
            """\
            interface Ethernet1/1
              description x
              ip flow monitor MON_V4 input
              ip address 192.0.2.1/24
              ipv6 flow monitor MON_V6 input
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            [
                dict(
                    name="Ethernet1/1",
                    flow_monitors=[_mon("ipv4", "MON_V4"), _mon("ipv6", "MON_V6")],
                ),
            ],
        )

    def test_nxos_netflow_interfaces_parsed_without_running_config_fails(self):
        self._fail(state="parsed")
        self._fail(running_config="", state="parsed")

    def test_nxos_netflow_interfaces_rendered_without_config_fails(self):
        self._fail(state="rendered")

    def test_nxos_netflow_interfaces_config_and_running_config_exclude_each_other(self):
        result = self._fail(
            config=[dict(name="Ethernet1/1")],
            running_config=BASE,
            state="parsed",
        )
        self.assertIn("mutually exclusive", result["msg"])

    def test_nxos_netflow_interfaces_required_config_for_the_states(self):
        for state in ["merged", "replaced", "overridden", "rendered"]:
            self._fail(state=state)
            self._fail(config=[], state=state)

    def test_nxos_netflow_interfaces_invalid_argspec_values(self):
        entry = dict(name="Ethernet1/1")
        cases = [
            (
                dict(config=[dict(entry, flow_monitors=[dict(monitor="M", direction="both")])]),
                "must be one of",
            ),
            (
                dict(
                    config=[
                        dict(
                            entry,
                            flow_monitors=[dict(monitor="M", direction="input", protocol="ipx")],
                        ),
                    ],
                ),
                "must be one of",
            ),
            (
                dict(config=[dict(entry, flow_monitors=[dict(direction="input")])]),
                "missing required",
            ),
            (dict(config=[dict(entry, flow_monitors=[dict(monitor="M")])]), "missing required"),
            (dict(config=[dict(flow_monitors=[])]), "missing required"),
            (dict(config=[dict(entry, bogus=1)]), "Unsupported parameters"),
            (dict(config=[dict(entry, flow_monitors=["text"])]), "dictionary requested"),
            (dict(config="text"), "dictionary requested"),
            (dict(config=[dict(entry)], state="bogus"), "must be one of"),
        ]
        for args, text in cases:
            args.setdefault("state", "merged")
            result = self._fail(**args)
            self.assertIn(text, result["msg"])

    def test_nxos_netflow_interfaces_merged_empty_interface_list_entry_changes_nothing(self):
        self.get_config.return_value = BASE
        self._run(False, config=[dict(name="Ethernet1/2", flow_monitors=[])], state="merged")

    def test_nxos_netflow_interfaces_replaced_entry_without_monitors_wipes_the_interface(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(name="Eth1/3", flow_monitors=[])], state="replaced")
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/3", "no layer2-switched flow monitor MON_L2 input"],
        )

    def test_nxos_netflow_interfaces_deleted_unknown_interface_changes_nothing(self):
        self.get_config.return_value = BASE
        self._run(False, config=[dict(name="Ethernet1/99")], state="deleted")

    def test_nxos_netflow_interfaces_gathered_without_the_feature_is_empty(self):
        # the device prints nothing when 'feature netflow' is not enabled
        self.get_config.return_value = ""
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], [])
        self._run(False, state="deleted")

    def test_nxos_netflow_interfaces_overridden_removes_every_other_direction_and_protocol(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="port-channel10",
                    flow_monitors=[dict(monitor="MON_V4", direction="output")],
                ),
            ],
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel10",
                "no ip flow monitor MON_V4 input",
                "interface Ethernet1/1",
                "no ip flow monitor MON_V4 input",
                "no ipv6 flow monitor MON_V6 input",
                "interface Ethernet1/3",
                "no layer2-switched flow monitor MON_L2 input",
                "interface Ethernet1/4.10",
                "no ip flow monitor MON_V4 input",
                "interface Vlan200",
                "no ip flow monitor MON_V4 input",
            ],
        )

    # reviewer lessons: the device is not validated, CRLF, garbage, warnings

    def test_nxos_netflow_interfaces_odd_device_values_do_not_block_other_interfaces(self):
        odd = dedent(
            """\
            interface Ethernet1/7
              ip flow monitor weird-name.with:odd/chars input
              ipv6 flow monitor 1234567890123456789012345678901234567890123456789012345678901234 input
            interface Ethernet1/8
            """,
        )
        self.get_config.return_value = odd
        result = self._run(
            True,
            config=[
                dict(name="Ethernet1/8", flow_monitors=[dict(monitor="MON_V4", direction="input")]),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/8", "ip flow monitor MON_V4 input"],
        )
        result = self._run(True, config=[dict(name="Ethernet1/7")], state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/7",
                "no ip flow monitor weird-name.with:odd/chars input",
                "no ipv6 flow monitor 1234567890123456789012345678901234567890123456789012345678901234 input",
            ],
        )

    def test_nxos_netflow_interfaces_crlf_line_endings(self):
        crlf = BASE.replace("\n", "\r\n")
        result = self._run(False, running_config=crlf, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)
        self.get_config.return_value = crlf
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)
        self._run(False, config=deepcopy(BASE_FACTS), state="replaced")

    def test_nxos_netflow_interfaces_parsed_fuzz_gives_a_result_or_a_clean_failure(self):
        samples = [
            "",
            "\r\n\r\n",
            "interface\r\n  ip flow monitor\r\n",
            "interface Ethernet1/1\n  ip flow monitor " + "A" * 100000 + " input\n",
            "interface Ethernet1/1\n  ip flow monitor A input extra\n",
            "interface Ethernet1/1\n  ip flow monitor 99999999999999999999 input\n",
            "\x01\x02 interface Ethernet1/1\n",
            "interface Ethernet1/1\n" * 1000,
            "interface Ethernet1/1\n  ip flow monitor A input\n" * 500,
        ]
        for sample in samples:
            set_module_args(dict(running_config=sample, state="parsed"), ignore_provider_arg)
            try:
                result = self.execute_module(changed=False)
            except AnsibleFailJson as exc:
                # only the empty text is refused
                self.assertEqual(sample, "")
                self.assertIn("must not be empty", exc.args[0]["msg"])
            else:
                self.assertIsInstance(result["parsed"], list)

    def test_nxos_netflow_interfaces_deleted_warns_about_the_interfaces_without_monitors(self):
        self.get_config.return_value = BASE
        with patch("ansible.module_utils.basic.AnsibleModule.warn") as warn:
            self._run(
                True,
                config=[dict(name="Ethernet1/1"), dict(name="Eth1/2"), dict(name="Ethernet1/9")],
                state="deleted",
            )
        text = " ".join(call.args[0] for call in warn.call_args_list)
        self.assertIn("Ethernet1/2, Ethernet1/9", text)
        self.assertNotIn("Ethernet1/1,", text)
