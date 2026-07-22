#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# AI-generated unit tests for nxos_vrrp module.
# Generated to increase coverage from 44.39% by testing state transitions,
# VRRP group management, validation, config helpers, error paths, and check mode.
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrrp
from ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp import (
    apply_key_map,
    execute_show_command,
    flatten_list,
    get_commands_config_vrrp,
    get_existing_vrrp,
    get_interface_mode,
    get_vrr_status,
    is_default,
    validate_params,
)

from .nxos_module import TestNxosModule, set_module_args


def _full_existing():
    """Return a baseline existing VRRP config dict."""
    return {
        "group": "10",
        "vip": "192.0.2.1",
        "priority": "100",
        "preempt": False,
        "authentication": "",
        "interval": "1",
        "admin_state": "shutdown",
    }


class TestNxosVrrpModule(TestNxosModule):
    module = nxos_vrrp

    def setUp(self):
        super(TestNxosVrrpModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()
        self.get_interface_mode.return_value = ("layer3", "Ethernet1/1")

        self.mock_get_existing_vrrp = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_existing_vrrp",
        )
        self.get_existing_vrrp = self.mock_get_existing_vrrp.start()

    def tearDown(self):
        super(TestNxosVrrpModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_get_interface_type.stop()
        self.mock_get_interface_mode.stop()
        self.mock_get_existing_vrrp.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    # ------------------------------------------------------------------
    # No-change baseline
    # ------------------------------------------------------------------

    def test_nxos_vrrp_no_change(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                priority="100",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    # ------------------------------------------------------------------
    # state=present with new group (no existing config)
    # ------------------------------------------------------------------

    def test_present_new_vrrp_group(self):
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                state="present",
            ),
        )
        result = self.execute_module(
            changed=True,
            commands=[
                "interface ethernet1/1",
                "vrrp 10",
                "address 192.0.2.1",
                "shutdown",
            ],
            sort=False,
        )

    def test_present_new_group_with_priority_and_preempt(self):
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="20",
                interface="Ethernet1/1",
                vip="10.1.1.1",
                priority="150",
                preempt=True,
                state="present",
            ),
        )
        result = self.changed(changed=True)
        cmds = result["commands"]
        self.assertIn("address 10.1.1.1", cmds)
        self.assertIn("priority 150", cmds)
        self.assertIn("preempt", cmds)

    # ------------------------------------------------------------------
    # state=present with changes to existing group
    # ------------------------------------------------------------------

    def test_present_change_priority(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                priority="200",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("priority 200", result["commands"])

    def test_present_change_interval(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                interval="5",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("advertisement-interval 5", result["commands"])

    def test_present_change_vip(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="10.0.0.1",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("address 10.0.0.1", result["commands"])

    def test_present_enable_preempt(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                preempt=True,
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("preempt", result["commands"])

    def test_present_disable_preempt(self):
        existing = _full_existing()
        existing["preempt"] = True
        self.get_existing_vrrp.return_value = existing
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                preempt=False,
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("no preempt", result["commands"])

    def test_present_set_authentication(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                authentication="AUTHKEY",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("authentication text AUTHKEY", result["commands"])

    def test_present_change_admin_state(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                admin_state="no shutdown",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("no shutdown", result["commands"])

    # ------------------------------------------------------------------
    # state=absent
    # ------------------------------------------------------------------

    def test_absent_removes_existing_group(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                state="absent",
            ),
        )
        result = self.execute_module(
            changed=True,
            commands=[
                "interface ethernet1/1",
                "no vrrp 10",
            ],
            sort=False,
        )

    def test_absent_no_change_when_not_existing(self):
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                state="absent",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # ------------------------------------------------------------------
    # Error cases
    # ------------------------------------------------------------------

    def test_present_without_vip_fails(self):
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("vip", result["msg"])

    def test_loopback_interface_rejected(self):
        self.get_interface_type.return_value = "loopback"
        self.mock_is_default = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.is_default",
        )
        is_default = self.mock_is_default.start()
        is_default.return_value = False
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="loopback0",
                vip="10.0.0.1",
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("Loopback", result["msg"])
        self.mock_is_default.stop()

    def test_layer2_interface_rejected(self):
        self.get_interface_mode.return_value = ("layer2", "Ethernet1/1")
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="10.0.0.1",
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("layer2", result["msg"].lower())

    def test_dne_interface_rejected(self):
        self.get_interface_type.return_value = "svi"
        self.mock_is_default = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.is_default",
        )
        is_default = self.mock_is_default.start()
        is_default.return_value = "DNE"
        self.get_existing_vrrp.return_value = {}
        set_module_args(
            dict(
                group="10",
                interface="vlan999",
                vip="10.0.0.1",
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("does not exist", result["msg"])
        self.mock_is_default.stop()

    # ------------------------------------------------------------------
    # Check mode
    # ------------------------------------------------------------------

    def test_check_mode_no_load_config(self):
        self.get_existing_vrrp.return_value = _full_existing()
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="10.0.0.1",
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("address 10.0.0.1", result["commands"])
        self.load_config.assert_not_called()

    # ------------------------------------------------------------------
    # Direct helper: get_commands_config_vrrp()
    # ------------------------------------------------------------------

    def test_get_commands_vip(self):
        delta = {"vip": "10.1.1.1"}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertEqual(cmds[0], "vrrp 10")
        self.assertIn("address 10.1.1.1", cmds)

    def test_get_commands_priority(self):
        delta = {"priority": "150"}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("priority 150", cmds)

    def test_get_commands_interval(self):
        delta = {"interval": "5"}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("advertisement-interval 5", cmds)

    def test_get_commands_preempt_true(self):
        delta = {"preempt": True}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("preempt", cmds)
        self.assertNotIn("no preempt", cmds)

    def test_get_commands_preempt_false(self):
        delta = {"preempt": False}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("no preempt", cmds)

    def test_get_commands_authentication_set(self):
        delta = {"authentication": "SECRET"}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("authentication text SECRET", cmds)

    def test_get_commands_authentication_default_with_existing(self):
        delta = {"authentication": "default"}
        existing = {"authentication": "OLD"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertIn("no authentication", cmds)

    def test_get_commands_authentication_default_no_existing(self):
        delta = {"authentication": "default"}
        existing = {"authentication": ""}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertNotIn("no authentication", cmds)

    def test_get_commands_admin_state(self):
        delta = {"admin_state": "no shutdown"}
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertIn("no shutdown", cmds)

    def test_get_commands_priority_default_with_change(self):
        delta = {"priority": "default"}
        existing = {"priority": "200"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertIn("priority 100", cmds)

    def test_get_commands_priority_default_already_default(self):
        delta = {"priority": "default"}
        existing = {"priority": "100"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        # no priority command emitted because existing == default
        priority_cmds = [c for c in cmds if "priority" in c]
        self.assertEqual(priority_cmds, [])

    def test_get_commands_interval_default(self):
        delta = {"interval": "default"}
        existing = {"interval": "5"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertIn("advertisement-interval 1", cmds)

    def test_get_commands_vip_default(self):
        delta = {"vip": "default"}
        existing = {"vip": "10.0.0.1"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertIn("address 0.0.0.0", cmds)

    def test_get_commands_admin_state_default(self):
        delta = {"admin_state": "default"}
        existing = {"admin_state": "no shutdown"}
        cmds = get_commands_config_vrrp(delta, existing, "10")
        self.assertIn("shutdown", cmds)

    def test_get_commands_empty_delta(self):
        cmds = get_commands_config_vrrp({}, {}, "10")
        self.assertEqual(cmds, [])

    def test_get_commands_multiple_changes(self):
        delta = {
            "vip": "10.1.1.1",
            "priority": "200",
            "interval": "3",
            "preempt": True,
            "authentication": "KEY",
            "admin_state": "no shutdown",
        }
        cmds = get_commands_config_vrrp(delta, {}, "10")
        self.assertEqual(cmds[0], "vrrp 10")
        self.assertIn("address 10.1.1.1", cmds)
        self.assertIn("priority 200", cmds)
        self.assertIn("advertisement-interval 3", cmds)
        self.assertIn("preempt", cmds)
        self.assertIn("authentication text KEY", cmds)
        self.assertIn("no shutdown", cmds)

    # ------------------------------------------------------------------
    # Direct helpers: flatten_list() and apply_key_map()
    # ------------------------------------------------------------------

    def test_flatten_list_mixed(self):
        result = flatten_list([["a", "b"], "c", ["d"]])
        self.assertEqual(result, ["a", "b", "c", "d"])

    def test_flatten_list_empty(self):
        result = flatten_list([])
        self.assertEqual(result, [])

    def test_apply_key_map(self):
        key_map = {"sh_group_id": "group", "sh_vip_addr": "vip"}
        table = {"sh_group_id": "10", "sh_vip_addr": "10.0.0.1", "other": "x"}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"group": "10", "vip": "10.0.0.1"})

    def test_apply_key_map_with_none(self):
        key_map = {"key": "mapped"}
        table = {"key": None}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"mapped": None})

    # ------------------------------------------------------------------
    # Default values through main()
    # ------------------------------------------------------------------

    def test_present_priority_default(self):
        existing = _full_existing()
        existing["priority"] = "200"
        self.get_existing_vrrp.return_value = existing
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                priority="default",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("priority 100", result["commands"])

    def test_present_interval_default(self):
        existing = _full_existing()
        existing["interval"] = "5"
        self.get_existing_vrrp.return_value = existing
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                interval="default",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("advertisement-interval 1", result["commands"])

    def test_present_admin_state_default(self):
        existing = _full_existing()
        existing["admin_state"] = "no shutdown"
        self.get_existing_vrrp.return_value = existing
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                admin_state="default",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("shutdown", result["commands"])

    def test_present_authentication_default_removes(self):
        existing = _full_existing()
        existing["authentication"] = "OLDKEY"
        self.get_existing_vrrp.return_value = existing
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                authentication="default",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("no authentication", result["commands"])


class TestNxosVrrpHelpers(unittest.TestCase):
    """Tests for device-interaction helper functions in nxos_vrrp."""

    def setUp(self):
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()
        self.module = MagicMock()

    def tearDown(self):
        self.mock_run_commands.stop()

    # ------------------------------------------------------------------
    # execute_show_command
    # ------------------------------------------------------------------

    def test_execute_show_command_show_run_uses_text(self):
        self.run_commands.return_value = ["some text output"]
        result = execute_show_command("show run interface Eth1/1", self.module)
        call_args = self.run_commands.call_args
        commands_arg = call_args[0][1]
        self.assertEqual(commands_arg[0]["output"], "text")
        self.assertEqual(commands_arg[0]["command"], "show run interface Eth1/1")
        self.assertEqual(result, "some text output")

    def test_execute_show_command_non_show_run_uses_json(self):
        json_data = {"key": "value"}
        self.run_commands.return_value = [json_data]
        result = execute_show_command("show vrrp detail interface Eth1/1", self.module)
        call_args = self.run_commands.call_args
        commands_arg = call_args[0][1]
        self.assertEqual(commands_arg[0]["output"], "json")
        self.assertEqual(result, json_data)

    # ------------------------------------------------------------------
    # apply_key_map (additional coverage via helper class)
    # ------------------------------------------------------------------

    def test_apply_key_map_converts_truthy_to_str(self):
        key_map = {"a": "alpha"}
        table = {"a": 42}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"alpha": "42"})

    def test_apply_key_map_falsy_value_preserved(self):
        key_map = {"a": "alpha"}
        table = {"a": 0}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"alpha": 0})

    def test_apply_key_map_unmapped_keys_ignored(self):
        key_map = {"a": "alpha"}
        table = {"a": "1", "b": "2"}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"alpha": "1"})

    # ------------------------------------------------------------------
    # is_default
    # ------------------------------------------------------------------

    def test_is_default_normal_config_returns_false(self):
        self.run_commands.return_value = [
            "interface Ethernet1/1\n  ip address 10.0.0.1/24\n  no shutdown",
        ]
        result = is_default("Ethernet1/1", self.module)
        self.assertFalse(result)

    def test_is_default_minimal_config_returns_true(self):
        self.run_commands.return_value = ["interface Ethernet1/1"]
        result = is_default("Ethernet1/1", self.module)
        self.assertTrue(result)

    def test_is_default_invalid_body_returns_dne(self):
        self.run_commands.return_value = ["Invalid interface"]
        result = is_default("Ethernet99/99", self.module)
        self.assertEqual(result, "DNE")

    def test_is_default_key_error_returns_dne(self):
        self.run_commands.side_effect = KeyError("missing key")
        result = is_default("Ethernet1/1", self.module)
        self.assertEqual(result, "DNE")

    # ------------------------------------------------------------------
    # get_interface_mode
    # ------------------------------------------------------------------

    def test_get_interface_mode_ethernet_routed(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/1",
                        "eth_mode": "routed",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("Ethernet1/1", "ethernet", self.module)
        self.assertEqual(mode, "routed")
        self.assertEqual(name, "Ethernet1/1")

    def test_get_interface_mode_ethernet_access_is_layer2(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/2",
                        "eth_mode": "access",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("Ethernet1/2", "ethernet", self.module)
        self.assertEqual(mode, "layer2")

    def test_get_interface_mode_ethernet_trunk_is_layer2(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/3",
                        "eth_mode": "trunk",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("Ethernet1/3", "ethernet", self.module)
        self.assertEqual(mode, "layer2")

    def test_get_interface_mode_ethernet_no_eth_mode_defaults_layer3(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/1",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("Ethernet1/1", "ethernet", self.module)
        self.assertEqual(mode, "layer3")

    def test_get_interface_mode_svi(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Vlan10",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("Vlan10", "svi", self.module)
        self.assertEqual(mode, "layer3")
        self.assertEqual(name, "Vlan10")

    def test_get_interface_mode_unknown_type(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "mgmt0",
                    },
                },
            },
        ]
        mode, name = get_interface_mode("mgmt0", "management", self.module)
        self.assertEqual(mode, "unknown")

    # ------------------------------------------------------------------
    # get_vrr_status
    # ------------------------------------------------------------------

    def test_get_vrr_status_no_shutdown_found(self):
        body = "interface Vlan10\n  vrrp 10\n    priority 100\n    no shutdown\nend"
        self.run_commands.return_value = [body]
        result = get_vrr_status("10", self.module, "Vlan10")
        self.assertEqual(result, "no shutdown")

    def test_get_vrr_status_no_match_returns_shutdown(self):
        body = "interface Vlan10\n  vrrp 10\n    priority 100\n    shutdown\nend"
        self.run_commands.return_value = [body]
        result = get_vrr_status("10", self.module, "Vlan10")
        self.assertEqual(result, "shutdown")

    # ------------------------------------------------------------------
    # get_existing_vrrp
    # ------------------------------------------------------------------

    def test_get_existing_vrrp_dict_format_preempt_enable(self):
        json_body = {
            "TABLE_vrrp_group": {
                "ROW_vrrp_group": {
                    "sh_group_id": "10",
                    "sh_vip_addr": "192.0.2.1",
                    "sh_priority": "100",
                    "sh_group_preempt": "Enable",
                    "sh_auth_text": "",
                    "sh_adv_interval": "1",
                },
            },
        }
        vrr_body = "interface Vlan10\n  vrrp 10\n    no shutdown\nend"
        self.run_commands.side_effect = [
            [json_body],
            [vrr_body],
        ]
        result = get_existing_vrrp("Vlan10", "10", self.module, "Vlan10")
        self.assertEqual(result["group"], "10")
        self.assertEqual(result["vip"], "192.0.2.1")
        self.assertTrue(result["preempt"])
        self.assertEqual(result["admin_state"], "no shutdown")

    def test_get_existing_vrrp_list_format_preempt_disable(self):
        json_body = {
            "TABLE_vrrp_group": [
                {
                    "ROW_vrrp_group": {
                        "sh_group_id": "10",
                        "sh_vip_addr": "192.0.2.1",
                        "sh_priority": "100",
                        "sh_group_preempt": "Disable",
                        "sh_auth_text": "KEY",
                        "sh_adv_interval": "1",
                    },
                },
                {
                    "ROW_vrrp_group": {
                        "sh_group_id": "20",
                        "sh_vip_addr": "10.0.0.1",
                        "sh_priority": "200",
                        "sh_group_preempt": "Enable",
                        "sh_auth_text": "",
                        "sh_adv_interval": "3",
                    },
                },
            ],
        }
        vrr_body = "interface Vlan10\n  vrrp 10\n    shutdown\nend"
        self.run_commands.side_effect = [
            [json_body],
            [vrr_body],
        ]
        result = get_existing_vrrp("Vlan10", "10", self.module, "Vlan10")
        self.assertEqual(result["group"], "10")
        self.assertFalse(result["preempt"])
        self.assertEqual(result["authentication"], "KEY")
        self.assertEqual(result["admin_state"], "shutdown")

    def test_get_existing_vrrp_no_matching_group(self):
        json_body = {
            "TABLE_vrrp_group": {
                "ROW_vrrp_group": {
                    "sh_group_id": "20",
                    "sh_vip_addr": "10.0.0.1",
                    "sh_priority": "200",
                    "sh_group_preempt": "Enable",
                    "sh_auth_text": "",
                    "sh_adv_interval": "3",
                },
            },
        }
        self.run_commands.return_value = [json_body]
        result = get_existing_vrrp("Vlan10", "10", self.module, "Vlan10")
        self.assertEqual(result, {})

    def test_get_existing_vrrp_empty_body_returns_empty(self):
        self.run_commands.return_value = [None]
        result = get_existing_vrrp("Vlan10", "10", self.module, "Vlan10")
        self.assertEqual(result, {})

    # ------------------------------------------------------------------
    # validate_params
    # ------------------------------------------------------------------

    def test_validate_params_group_boundary_min(self):
        self.module.params = {"group": "1"}
        validate_params("group", self.module)
        self.module.fail_json.assert_not_called()

    def test_validate_params_group_boundary_max(self):
        self.module.params = {"group": "255"}
        validate_params("group", self.module)
        self.module.fail_json.assert_not_called()

    def test_validate_params_group_too_high(self):
        self.module.params = {"group": "256"}
        validate_params("group", self.module)
        self.module.fail_json.assert_called_once()

    def test_validate_params_group_too_low(self):
        self.module.params = {"group": "0"}
        validate_params("group", self.module)
        self.module.fail_json.assert_called_once()

    def test_validate_params_group_non_numeric(self):
        self.module.params = {"group": "abc"}
        validate_params("group", self.module)
        self.module.fail_json.assert_called_once()

    def test_validate_params_valid_priority(self):
        self.module.params = {"priority": "100"}
        validate_params("priority", self.module)
        self.module.fail_json.assert_not_called()

    def test_validate_params_priority_too_high(self):
        self.module.params = {"priority": "255"}
        validate_params("priority", self.module)
        self.module.fail_json.assert_called_once()

    def test_validate_params_priority_too_low(self):
        self.module.params = {"priority": "0"}
        validate_params("priority", self.module)
        self.module.fail_json.assert_called_once()
