#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Tests generated with AI assistance (Claude)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_udld_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosUdldInterfaceModule(TestNxosModule):
    module = nxos_udld_interface

    def setUp(self):
        super(TestNxosUdldInterfaceModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosUdldInterfaceModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    # ------------------------------------------------------------------ #
    #  Integration tests exercising main() via execute_module             #
    # ------------------------------------------------------------------ #

    def test_nxos_udld_interface_no_change(self):
        self.run_commands.return_value = [
            '{"TABLE_interface": {"ROW_interface": '
            '{"udld-port-aggressive-mode": "enabled",'
            '"udld-port-status": "enabled"}}}',
        ]
        set_module_args(
            dict(
                mode="aggressive",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_udld_present_aggressive(self):
        """Switch from disabled to aggressive mode."""
        self.run_commands.side_effect = [
            ["udld disable"],  # initial: mode=disabled
            ["udld aggressive"],  # end_state: mode=aggressive
        ]
        set_module_args(
            dict(
                mode="aggressive",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["end_state"], {"mode": "aggressive"})
        self.load_config.assert_called_once()

    def test_udld_present_enabled(self):
        """Switch from disabled to enabled mode -- two config batches."""
        self.run_commands.side_effect = [
            ["udld disable"],  # initial: mode=disabled
            ["no udld enable"],  # inside config_udld_interface2
            ["udld enable"],  # end_state: mode=enabled
        ]
        set_module_args(
            dict(
                mode="enabled",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["end_state"], {"mode": "enabled"})
        self.assertEqual(self.load_config.call_count, 2)

    def test_udld_present_disabled(self):
        """Switch from enabled to disabled mode -- two config batches."""
        self.run_commands.side_effect = [
            ["udld enable"],  # initial: mode=enabled
            ["no udld disable"],  # inside config_udld_interface2
            ["udld disable"],  # end_state: mode=disabled
        ]
        set_module_args(
            dict(
                mode="disabled",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["end_state"], {"mode": "disabled"})
        self.assertEqual(self.load_config.call_count, 2)

    def test_udld_absent_aggressive(self):
        """Remove aggressive mode via state=absent."""
        self.run_commands.side_effect = [
            ["udld aggressive"],  # initial: mode=aggressive
            ["udld aggressive"],  # inside remove function
            [""],  # end_state
        ]
        set_module_args(
            dict(
                mode="aggressive",
                interface="Ethernet1/1",
                state="absent",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["existing"], {"mode": "aggressive"})

    def test_udld_absent_enabled(self):
        """Remove enabled mode via state=absent."""
        self.run_commands.side_effect = [
            ["udld enable"],  # initial: mode=enabled
            ["udld enable"],  # inside remove function
            [""],  # end_state
        ]
        set_module_args(
            dict(
                mode="enabled",
                interface="Ethernet1/1",
                state="absent",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["existing"], {"mode": "enabled"})

    def test_udld_absent_no_match(self):
        """No change when state=absent and existing mode differs from proposed."""
        self.run_commands.return_value = ["udld enable"]
        set_module_args(
            dict(
                mode="aggressive",
                interface="Ethernet1/1",
                state="absent",
            ),
        )
        result = self.execute_module(changed=False)

    def test_udld_check_mode_present_aggressive(self):
        """Check mode returns commands without applying for aggressive."""
        self.run_commands.return_value = ["udld disable"]
        set_module_args(
            dict(
                mode="aggressive",
                interface="Ethernet1/1",
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface ethernet1/1", "udld aggressive"],
        )
        self.load_config.assert_not_called()

    def test_udld_check_mode_present_enabled(self):
        """Check mode for enabled exits after first config batch."""
        self.run_commands.return_value = ["udld disable"]
        set_module_args(
            dict(
                mode="enabled",
                interface="Ethernet1/1",
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface ethernet1/1", "no udld aggressive"],
        )
        self.load_config.assert_not_called()

    def test_udld_present_no_change_enabled(self):
        """No change when existing mode already matches proposed enabled."""
        self.run_commands.return_value = ["udld enable"]
        set_module_args(
            dict(
                mode="enabled",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)

    def test_udld_present_no_change_disabled(self):
        """No change when existing mode already matches proposed disabled."""
        self.run_commands.return_value = ["udld disable"]
        set_module_args(
            dict(
                mode="disabled",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)

    # ------------------------------------------------------------------ #
    #  Direct tests for get_udld_interface body parsing                   #
    # ------------------------------------------------------------------ #

    def test_get_udld_interface_aggressive(self):
        self.run_commands.return_value = ["udld aggressive"]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": "aggressive"})
        self.assertEqual(mode_str, "aggressive")

    def test_get_udld_interface_no_udld_enable(self):
        self.run_commands.return_value = ["no udld enable"]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": "disabled"})
        self.assertEqual(mode_str, "no udld enable")

    def test_get_udld_interface_no_udld_disable(self):
        self.run_commands.return_value = ["no udld disable"]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": "enabled"})
        self.assertEqual(mode_str, "no udld disable")

    def test_get_udld_interface_udld_disable(self):
        self.run_commands.return_value = ["udld disable"]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": "disabled"})
        self.assertEqual(mode_str, "udld disable")

    def test_get_udld_interface_udld_enable(self):
        self.run_commands.return_value = ["udld enable"]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": "enabled"})
        self.assertEqual(mode_str, "udld enable")

    def test_get_udld_interface_empty_body(self):
        """No pattern matched -- mode is None."""
        self.run_commands.return_value = [""]
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {"mode": None})
        self.assertIsNone(mode_str)

    def test_get_udld_interface_index_error(self):
        """Returns empty dict when run_commands raises IndexError."""
        self.run_commands.return_value = []
        result, mode_str = nxos_udld_interface.get_udld_interface(
            None,
            "ethernet1/1",
        )
        self.assertEqual(result, {})
        self.assertIsNone(mode_str)

    # ------------------------------------------------------------------ #
    #  Direct tests for get_commands_config_udld_interface1               #
    # ------------------------------------------------------------------ #

    def test_get_commands_config1_aggressive(self):
        result = nxos_udld_interface.get_commands_config_udld_interface1(
            {"mode": "aggressive"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "udld aggressive"],
        )

    def test_get_commands_config1_non_aggressive(self):
        """Any mode other than aggressive produces 'no udld aggressive'."""
        result = nxos_udld_interface.get_commands_config_udld_interface1(
            {"mode": "enabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld aggressive"],
        )

    # ------------------------------------------------------------------ #
    #  Direct tests for get_commands_config_udld_interface2               #
    # ------------------------------------------------------------------ #

    def test_get_commands_config2_enabled_from_no_udld_enable(self):
        """enabled + mode_str='no udld enable' -> 'udld enable'."""
        self.run_commands.return_value = ["no udld enable"]
        result = nxos_udld_interface.get_commands_config_udld_interface2(
            {"mode": "enabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "udld enable"],
        )

    def test_get_commands_config2_enabled_from_other(self):
        """enabled + mode_str != 'no udld enable' -> 'no udld disable'."""
        self.run_commands.return_value = ["udld disable"]
        result = nxos_udld_interface.get_commands_config_udld_interface2(
            {"mode": "enabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld disable"],
        )

    def test_get_commands_config2_disabled_from_no_udld_disable(self):
        """disabled + mode_str='no udld disable' -> 'udld disable'."""
        self.run_commands.return_value = ["no udld disable"]
        result = nxos_udld_interface.get_commands_config_udld_interface2(
            {"mode": "disabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "udld disable"],
        )

    def test_get_commands_config2_disabled_from_other(self):
        """disabled + mode_str != 'no udld disable' -> 'no udld enable'."""
        self.run_commands.return_value = ["udld enable"]
        result = nxos_udld_interface.get_commands_config_udld_interface2(
            {"mode": "disabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld enable"],
        )

    # ------------------------------------------------------------------ #
    #  Direct tests for get_commands_remove_udld_interface                #
    # ------------------------------------------------------------------ #

    def test_get_commands_remove_aggressive(self):
        self.run_commands.return_value = ["udld aggressive"]
        result = nxos_udld_interface.get_commands_remove_udld_interface(
            {"mode": "aggressive"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld aggressive"],
        )

    def test_get_commands_remove_enabled_udld_enable(self):
        """enabled + mode_str='udld enable' -> 'no udld enable'."""
        self.run_commands.return_value = ["udld enable"]
        result = nxos_udld_interface.get_commands_remove_udld_interface(
            {"mode": "enabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld enable"],
        )

    def test_get_commands_remove_enabled_other(self):
        """enabled + mode_str != 'udld enable' -> 'udld disable'."""
        self.run_commands.return_value = ["no udld disable"]
        result = nxos_udld_interface.get_commands_remove_udld_interface(
            {"mode": "enabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "udld disable"],
        )

    def test_get_commands_remove_disabled_no_udld_disable(self):
        """disabled + mode_str='no udld disable' -> 'udld disable'."""
        self.run_commands.return_value = ["no udld disable"]
        result = nxos_udld_interface.get_commands_remove_udld_interface(
            {"mode": "disabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "udld disable"],
        )

    def test_get_commands_remove_disabled_other(self):
        """disabled + mode_str != 'no udld disable' -> 'no udld enable'."""
        self.run_commands.return_value = ["udld disable"]
        result = nxos_udld_interface.get_commands_remove_udld_interface(
            {"mode": "disabled"},
            "ethernet1/1",
            None,
            {},
        )
        self.assertEqual(
            result,
            ["interface ethernet1/1", "no udld enable"],
        )

    # ------------------------------------------------------------------ #
    #  Direct test for flatten_list                                       #
    # ------------------------------------------------------------------ #

    def test_flatten_list(self):
        result = nxos_udld_interface.flatten_list(
            [["a", "b"], "c", ["d"]],
        )
        self.assertEqual(result, ["a", "b", "c", "d"])

    def test_flatten_list_empty(self):
        result = nxos_udld_interface.flatten_list([])
        self.assertEqual(result, [])
