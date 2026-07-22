#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# AI-assisted test generation: test cases co-authored with Claude (Anthropic)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_rpm

from .nxos_module import TestNxosModule, set_module_args


MODULE_PATH = "ansible_collections.cisco.nxos.plugins.modules.nxos_rpm"


class TestNxosRpmHelpers(TestNxosModule):
    """Tests for helper functions called directly, not through main()."""

    module = nxos_rpm

    def setUp(self):
        super(TestNxosRpmHelpers, self).setUp()
        self.mock_run_commands = patch(MODULE_PATH + ".run_commands")
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(MODULE_PATH + ".load_config")
        self.load_config = self.mock_load_config.start()

        self.mock_time_sleep = patch(MODULE_PATH + ".time.sleep")
        self.time_sleep = self.mock_time_sleep.start()

        self.module_mock = MagicMock()

    def tearDown(self):
        super(TestNxosRpmHelpers, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_time_sleep.stop()

    def load_fixtures(self, commands=None, device=""):
        pass

    # ---------------------------------------------------------------
    # execute_show_command
    # ---------------------------------------------------------------
    def test_execute_show_command_returns_body_immediately(self):
        self.run_commands.return_value = ["some output"]
        result = nxos_rpm.execute_show_command("show version", self.module_mock)
        self.assertEqual(result, "some output")
        self.run_commands.assert_called_once()
        self.time_sleep.assert_not_called()

    def test_execute_show_command_retries_on_empty_body(self):
        self.run_commands.side_effect = [
            [""],
            [""],
            ["got data"],
        ]
        result = nxos_rpm.execute_show_command("show version", self.module_mock)
        self.assertEqual(result, "got data")
        self.assertEqual(self.run_commands.call_count, 3)
        self.assertEqual(self.time_sleep.call_count, 2)

    def test_execute_show_command_returns_none_after_10_retries(self):
        self.run_commands.return_value = [""]
        result = nxos_rpm.execute_show_command("show install", self.module_mock)
        self.assertIsNone(result)
        self.assertEqual(self.run_commands.call_count, 10)
        self.assertEqual(self.time_sleep.call_count, 10)

    # ---------------------------------------------------------------
    # remote_file_exists
    # ---------------------------------------------------------------
    def test_remote_file_exists_true(self):
        self.run_commands.return_value = ["  1234  somefile.rpm"]
        result = nxos_rpm.remote_file_exists(self.module_mock, "test.rpm", "bootflash")
        self.assertTrue(result)

    def test_remote_file_exists_false(self):
        self.run_commands.return_value = ["No such file or directory"]
        result = nxos_rpm.remote_file_exists(self.module_mock, "missing.rpm", "bootflash")
        self.assertFalse(result)

    # ---------------------------------------------------------------
    # config_cmd_operation
    # ---------------------------------------------------------------
    def test_config_cmd_operation_returns_on_none_msg(self):
        self.load_config.return_value = None
        result = nxos_rpm.config_cmd_operation(self.module_mock, "install add bootflash:test.rpm")
        self.assertIsNone(result)
        self.load_config.assert_called_once()
        self.time_sleep.assert_not_called()

    def test_config_cmd_operation_returns_on_success_msg(self):
        self.load_config.return_value = ["Install operation successful"]
        result = nxos_rpm.config_cmd_operation(self.module_mock, "install add bootflash:test.rpm")
        self.assertIsNone(result)
        self.load_config.assert_called_once()

    def test_config_cmd_operation_retries_on_another_install(self):
        self.load_config.side_effect = [
            ["Another install operation is in progress"],
            ["Another install operation is in progress"],
            None,
        ]
        nxos_rpm.config_cmd_operation(self.module_mock, "install add bootflash:test.rpm")
        self.assertEqual(self.load_config.call_count, 3)
        self.assertEqual(self.time_sleep.call_count, 2)

    def test_config_cmd_operation_retries_on_failed(self):
        self.load_config.side_effect = [
            ["Operation Failed due to timeout"],
            None,
        ]
        nxos_rpm.config_cmd_operation(self.module_mock, "install activate pkg forced")
        self.assertEqual(self.load_config.call_count, 2)
        self.assertEqual(self.time_sleep.call_count, 1)

    def test_config_cmd_operation_exhausts_retries(self):
        self.load_config.return_value = ["Another install operation is in progress"]
        nxos_rpm.config_cmd_operation(self.module_mock, "install add bootflash:test.rpm")
        self.assertEqual(self.load_config.call_count, 10)
        self.assertEqual(self.time_sleep.call_count, 10)

    # ---------------------------------------------------------------
    # validate_operation
    # ---------------------------------------------------------------
    def test_validate_operation_pkg_present_found(self):
        self.run_commands.return_value = ["nxos.sample-n9k_ALL-1.0.0"]
        nxos_rpm.validate_operation(
            self.module_mock,
            "show install active",
            "install activate pkg forced",
            "nxos.sample-n9k_ALL-1.0.0",
            False,
        )
        self.module_mock.fail_json.assert_not_called()

    def test_validate_operation_pkg_not_present_confirmed(self):
        self.run_commands.return_value = ["some other output"]
        nxos_rpm.validate_operation(
            self.module_mock,
            "show install active",
            "install deactivate pkg forced",
            "nxos.sample-n9k_ALL-1.0.0",
            True,
        )
        self.module_mock.fail_json.assert_not_called()

    def test_validate_operation_fails_after_10_retries_pkg_expected(self):
        self.run_commands.return_value = ["no matching pkg here"]
        nxos_rpm.validate_operation(
            self.module_mock,
            "show install active",
            "install activate pkg forced",
            "nxos.sample-n9k_ALL-1.0.0",
            False,
        )
        self.module_mock.fail_json.assert_called_once_with(
            msg='Operation "install activate pkg forced" Failed',
        )

    def test_validate_operation_fails_after_10_retries_pkg_not_expected(self):
        self.run_commands.return_value = ["nxos.sample-n9k_ALL-1.0.0 is still here"]
        nxos_rpm.validate_operation(
            self.module_mock,
            "show install active",
            "install deactivate pkg forced",
            "nxos.sample-n9k_ALL-1.0.0",
            True,
        )
        self.module_mock.fail_json.assert_called_once_with(
            msg='Operation "install deactivate pkg forced" Failed',
        )

    def test_validate_operation_succeeds_after_retries(self):
        self.run_commands.side_effect = [
            ["no match"],
            ["no match"],
            ["nxos.sample-n9k_ALL-1.0.0 is active"],
        ]
        nxos_rpm.validate_operation(
            self.module_mock,
            "show install active",
            "install activate pkg forced",
            "nxos.sample-n9k_ALL-1.0.0",
            False,
        )
        self.module_mock.fail_json.assert_not_called()
        self.assertEqual(self.time_sleep.call_count, 2)

    # ---------------------------------------------------------------
    # activate_reload
    # ---------------------------------------------------------------
    def test_activate_reload_flag_true_returns_on_error_code(self):
        self.load_config.return_value = [-32603]
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertEqual(result, "install activate nxos.sample forced")

    def test_activate_reload_flag_false_returns_on_error_code(self):
        self.load_config.return_value = [-32603]
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", False)
        self.assertEqual(result, "install deactivate nxos.sample forced")

    def test_activate_reload_returns_on_socket_closed(self):
        self.load_config.return_value = ["Socket is closed"]
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertEqual(result, "install activate nxos.sample forced")

    def test_activate_reload_retries_on_another_install(self):
        self.load_config.side_effect = [
            ["Another install operation is in progress"],
            [-32603],
        ]
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertEqual(result, "install activate nxos.sample forced")
        self.assertEqual(self.time_sleep.call_count, 1)

    def test_activate_reload_retries_on_failed(self):
        self.load_config.side_effect = [
            ["Operation Failed"],
            ["Socket is closed"],
        ]
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertEqual(result, "install activate nxos.sample forced")
        self.assertEqual(self.time_sleep.call_count, 1)

    def test_activate_reload_returns_none_after_10_iterations(self):
        self.load_config.return_value = None
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertIsNone(result)
        self.assertEqual(self.load_config.call_count, 10)

    def test_activate_reload_non_matching_string_msg(self):
        # msg is a non-empty string that doesn't match any retry condition
        self.load_config.side_effect = [
            ["some unrecognized message"],
        ] * 10
        result = nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        self.assertIsNone(result)
        self.assertEqual(self.load_config.call_count, 10)
        # No sleep is called for non-matching string messages
        self.time_sleep.assert_not_called()

    def test_activate_reload_ignore_timeout_option(self):
        self.load_config.return_value = [-32603]
        nxos_rpm.activate_reload(self.module_mock, "nxos.sample", True)
        expected_opts = {"ignore_timeout": True}
        actual_call = self.load_config.call_args
        self.assertEqual(actual_call[0][3], expected_opts)

    # ---------------------------------------------------------------
    # terminal_operation
    # ---------------------------------------------------------------
    def test_terminal_operation_enable(self):
        self.load_config.return_value = None
        result = nxos_rpm.terminal_operation(self.module_mock, True)
        self.assertEqual(result, "terminal dont-ask")

    def test_terminal_operation_disable(self):
        self.load_config.return_value = None
        result = nxos_rpm.terminal_operation(self.module_mock, False)
        self.assertEqual(result, "no terminal dont-ask")

    # ---------------------------------------------------------------
    # add_operation
    # ---------------------------------------------------------------
    def test_add_operation(self):
        # config_cmd_operation returns None (success)
        self.load_config.return_value = None
        # validate_operation: execute_show_command returns body containing pkg
        self.run_commands.return_value = ["nxos.sample-n9k_ALL-1.0.0 is inactive"]
        result = nxos_rpm.add_operation(
            self.module_mock,
            "show install inactive",
            "bootflash",
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "nxos.sample-n9k_ALL-1.0.0",
        )
        self.assertEqual(result, "install add bootflash:nxos.sample-n9k_ALL-1.0.0.rpm")

    # ---------------------------------------------------------------
    # activate_operation
    # ---------------------------------------------------------------
    def test_activate_operation(self):
        self.load_config.return_value = None
        self.run_commands.return_value = ["nxos.sample-n9k_ALL-1.0.0 is active"]
        result = nxos_rpm.activate_operation(
            self.module_mock,
            "show install active",
            "nxos.sample-n9k_ALL-1.0.0",
        )
        self.assertEqual(result, "install activate nxos.sample-n9k_ALL-1.0.0 forced")

    # ---------------------------------------------------------------
    # commit_operation
    # ---------------------------------------------------------------
    def test_commit_operation(self):
        self.load_config.return_value = None
        self.run_commands.return_value = ["nxos.sample-n9k_ALL-1.0.0 is committed"]
        result = nxos_rpm.commit_operation(
            self.module_mock,
            "show install committed",
            "nxos.sample-n9k_ALL-1.0.0",
            False,
        )
        self.assertEqual(result, "install commit nxos.sample-n9k_ALL-1.0.0")

    # ---------------------------------------------------------------
    # deactivate_operation
    # ---------------------------------------------------------------
    def test_deactivate_operation(self):
        self.load_config.return_value = None
        self.run_commands.return_value = ["other packages only"]
        result = nxos_rpm.deactivate_operation(
            self.module_mock,
            "show install active",
            "nxos.sample-n9k_ALL-1.0.0",
            True,
        )
        self.assertEqual(result, "install deactivate nxos.sample-n9k_ALL-1.0.0 forced")

    # ---------------------------------------------------------------
    # remove_operation
    # ---------------------------------------------------------------
    def test_remove_operation(self):
        self.load_config.return_value = None
        # validate_operation needs pkg NOT in body (pkg_not_present=True)
        self.run_commands.return_value = ["other packages"]
        result = nxos_rpm.remove_operation(
            self.module_mock,
            "show install inactive",
            "nxos.sample-n9k_ALL-1.0.0",
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "terminal dont-ask")
        self.assertEqual(result[1], "install remove nxos.sample-n9k_ALL-1.0.0 forced")
        self.assertEqual(result[2], "no terminal dont-ask")


class TestNxosRpmInstallRemove(TestNxosModule):
    """Tests for install_remove_rpm covering all state branches."""

    module = nxos_rpm

    def setUp(self):
        super(TestNxosRpmInstallRemove, self).setUp()
        self.mock_run_commands = patch(MODULE_PATH + ".run_commands")
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(MODULE_PATH + ".load_config")
        self.load_config = self.mock_load_config.start()

        self.mock_time_sleep = patch(MODULE_PATH + ".time.sleep")
        self.time_sleep = self.mock_time_sleep.start()

        self.module_mock = MagicMock()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosRpmInstallRemove, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_time_sleep.stop()

    def load_fixtures(self, commands=None, device=""):
        pass

    def _setup_show_responses(self, responses):
        """Set up sequential responses for execute_show_command calls.

        Each call to run_commands returns a single-element list.
        """
        self.run_commands.side_effect = [[r] for r in responses]

    # ---------------------------------------------------------------
    # state=present branches
    # ---------------------------------------------------------------
    def test_present_full_install_flow(self):
        """pkg not in inactive, not in active -> add, activate, commit."""
        self._setup_show_responses(
            [
                # show install inactive
                "no packages",
                # show install active
                "no packages",
                # add_operation -> validate_operation -> show install inactive
                "nxos.sample-n9k_ALL-1.0.0 listed",
                # show install pkg-info (no reload patch)
                "Patch Type    :  normal",
                # activate_operation -> validate_operation -> show install active
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install committed
                "no committed packages",
                # show install patches
                "nxos.sample-n9k_ALL-1.0.0 patched",
                # commit_operation -> validate_operation -> show install committed
                "nxos.sample-n9k_ALL-1.0.0 committed",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        self.assertEqual(len(result), 3)
        self.assertIn("install add", result[0])
        self.assertIn("install activate", result[1])
        self.assertIn("install commit", result[2])

    def test_present_already_inactive_needs_activate_and_commit(self):
        """pkg already in inactive but not in active -> skip add, activate, commit."""
        self._setup_show_responses(
            [
                # show install inactive: pkg present
                "nxos.sample-n9k_ALL-1.0.0 listed",
                # show install active: pkg not present
                "no packages",
                # show install pkg-info (no reload)
                "Patch Type    :  normal",
                # activate_operation -> validate -> show install active
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install committed
                "no committed packages",
                # show install patches
                "nxos.sample-n9k_ALL-1.0.0 patch",
                # commit_operation -> validate -> show install committed
                "nxos.sample-n9k_ALL-1.0.0 committed",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        # No add command, just activate + commit
        self.assertEqual(len(result), 2)
        self.assertIn("install activate", result[0])
        self.assertIn("install commit", result[1])

    def test_present_already_active_needs_commit(self):
        """pkg already active but not committed -> commit only."""
        self._setup_show_responses(
            [
                # show install inactive
                "no packages",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info
                "Patch Type    :  normal",
                # pkg already in active -> skip activate
                # show install committed: pkg not present
                "no committed packages",
                # show install patches: pkg present
                "nxos.sample-n9k_ALL-1.0.0 patch",
                # commit_operation -> validate -> show install committed
                "nxos.sample-n9k_ALL-1.0.0 committed",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        self.assertEqual(len(result), 1)
        self.assertIn("install commit", result[0])

    def test_present_already_active_and_committed(self):
        """pkg already active and committed -> idempotent, empty commands."""
        self._setup_show_responses(
            [
                # show install inactive
                "no packages",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info
                "Patch Type    :  normal",
                # pkg already in active -> skip activate
                # show install committed: pkg present
                "nxos.sample-n9k_ALL-1.0.0 committed",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        self.assertEqual(result, [])

    def test_present_reload_patch(self):
        """Reload patch: add then activate_reload and return early."""
        self._setup_show_responses(
            [
                # show install inactive
                "no packages",
                # show install active
                "no packages",
                # add_operation -> validate -> show install inactive
                "nxos.sample-n9k_ALL-1.0.0 listed",
                # show install pkg-info -> reload patch
                "Patch Type    :  reload",
            ],
        )
        # add_operation calls config_cmd_operation (load_config returns None),
        # then activate_reload calls load_config (returns error code -32603)
        self.load_config.side_effect = [None, [-32603]]
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        self.assertEqual(len(result), 2)
        self.assertIn("install add", result[0])
        self.assertIn("install activate", result[1])

    def test_present_not_in_patches_fails(self):
        """Active but not in patches and not committed -> fail_json."""
        self._setup_show_responses(
            [
                # show install inactive
                "no packages",
                # show install active: pkg present (via add, but we go through
                # inactive/active check first - here pkg not in either)
                "no packages",
                # add_operation -> validate -> show install inactive
                "nxos.sample-n9k_ALL-1.0.0 listed",
                # show install pkg-info
                "Patch Type    :  normal",
                # activate_operation -> validate -> show install active
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install committed: not present
                "no committed",
                # show install patches: not present
                "no patches here",
            ],
        )
        nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "present",
        )
        self.module_mock.fail_json.assert_called_once()
        call_args = self.module_mock.fail_json.call_args
        self.assertIn("Failed", call_args[1]["msg"])

    # ---------------------------------------------------------------
    # state=absent branches
    # ---------------------------------------------------------------
    def test_absent_committed_and_active_deactivate_commit_remove(self):
        """pkg in commit and active (non-reload) -> deactivate, commit, remove."""
        self._setup_show_responses(
            [
                # show install committed: pkg present
                "nxos.sample-n9k_ALL-1.0.0 committed",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info: not reload
                "Patch Type    :  normal",
                # deactivate_operation -> validate -> show install active: pkg gone
                "no active packages",
                # execute_show_command(show_commit) after deactivate
                "nxos.sample-n9k_ALL-1.0.0 committed",
                # commit_operation -> validate -> show install committed: pkg gone
                "no committed packages",
                # remove_operation -> terminal_operation (load_config)
                # remove_operation -> validate -> show install inactive: pkg gone
                "no inactive packages",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        # deactivate + commit + terminal_on + remove + terminal_off
        self.assertTrue(len(result) >= 4)

    def test_absent_committed_and_active_reload_patch(self):
        """pkg in commit and active, reload patch -> activate_reload (deactivate), return."""
        self._setup_show_responses(
            [
                # show install committed: pkg present
                "nxos.sample-n9k_ALL-1.0.0 committed",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info: reload
                "Patch Type    :  reload",
            ],
        )
        self.load_config.return_value = [-32603]
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        self.assertEqual(len(result), 1)
        self.assertIn("install deactivate", result[0])

    def test_absent_committed_not_active(self):
        """pkg in commit but not active -> commit, remove."""
        self._setup_show_responses(
            [
                # show install committed: pkg present
                "nxos.sample-n9k_ALL-1.0.0 committed",
                # show install active: pkg not present
                "no active packages",
                # show install pkg-info
                "Patch Type    :  normal",
                # commit_operation -> validate -> show install committed: pkg gone
                "no committed packages",
                # remove_operation -> terminal -> validate -> show install inactive: pkg gone
                "no inactive packages",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        # commit + terminal_on + remove + terminal_off
        self.assertTrue(len(result) >= 3)

    def test_absent_active_not_committed_non_reload(self):
        """pkg in active but not committed, not reload -> deactivate, remove."""
        self._setup_show_responses(
            [
                # show install committed: pkg not present
                "no committed packages",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info
                "Patch Type    :  normal",
                # deactivate_operation -> validate -> show install inactive: pkg not gone
                # (pkg_not_present=False means we wait for pkg to appear in inactive)
                "nxos.sample-n9k_ALL-1.0.0 deactivated",
                # remove_operation -> terminal -> validate -> show install inactive: pkg gone
                "no inactive packages",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        # deactivate + terminal_on + remove + terminal_off
        self.assertTrue(len(result) >= 3)

    def test_absent_active_not_committed_reload(self):
        """pkg in active but not committed, reload -> activate_reload, return."""
        self._setup_show_responses(
            [
                # show install committed: not present
                "no committed packages",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info: reload
                "Patch Type    :  reload",
            ],
        )
        self.load_config.return_value = [-32603]
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        self.assertEqual(len(result), 1)
        self.assertIn("install deactivate", result[0])

    def test_absent_only_inactive(self):
        """pkg only in inactive -> remove only."""
        self._setup_show_responses(
            [
                # show install committed: not present
                "no committed packages",
                # show install active: not present
                "no active packages",
                # show install pkg-info
                "Patch Type    :  normal",
                # show install inactive: pkg present -> remove
                "nxos.sample-n9k_ALL-1.0.0 inactive",
                # remove_operation -> terminal -> validate -> inactive: pkg gone
                "no inactive packages",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        # terminal_on + remove + terminal_off
        self.assertEqual(len(result), 3)

    def test_absent_committed_active_after_deactivate_no_commit_needed(self):
        """pkg in commit and active, after deactivate pkg no longer in commit -> skip commit."""
        self._setup_show_responses(
            [
                # show install committed: pkg present
                "nxos.sample-n9k_ALL-1.0.0 committed",
                # show install active: pkg present
                "nxos.sample-n9k_ALL-1.0.0 active",
                # show install pkg-info: not reload
                "Patch Type    :  normal",
                # deactivate_operation -> validate -> show install active: pkg gone
                "no active packages",
                # execute_show_command(show_commit) after deactivate: pkg gone
                "no committed packages",
                # remove_operation -> terminal -> validate -> inactive: pkg gone
                "no inactive packages",
            ],
        )
        result = nxos_rpm.install_remove_rpm(
            self.module_mock,
            "nxos.sample-n9k_ALL-1.0.0.rpm",
            "bootflash",
            "absent",
        )
        # deactivate + terminal_on + remove + terminal_off (no commit)
        cmds_str = " ".join(str(c) for c in result)
        self.assertNotIn("install commit", cmds_str)


class TestNxosRpmMain(TestNxosModule):
    """Tests for the main() entry point."""

    module = nxos_rpm

    def setUp(self):
        super(TestNxosRpmMain, self).setUp()
        self.mock_run_commands = patch(MODULE_PATH + ".run_commands")
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(MODULE_PATH + ".load_config")
        self.load_config = self.mock_load_config.start()

        self.mock_time_sleep = patch(MODULE_PATH + ".time.sleep")
        self.time_sleep = self.mock_time_sleep.start()

        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosRpmMain, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_time_sleep.stop()

    def load_fixtures(self, commands=None, device=""):
        pass

    def test_main_present_remote_file_not_found(self):
        """state=present and remote file doesn't exist -> fail_json."""
        set_module_args(dict(pkg="test.rpm", state="present"))
        # remote_file_exists calls execute_show_command -> "No such file"
        self.run_commands.return_value = ["No such file or directory"]
        result = self.execute_module(failed=True)
        self.assertIn("doesn't exist", result["msg"])

    def test_main_present_already_installed_unchanged(self):
        """state=present, pkg already active and committed -> no change."""
        set_module_args(dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="present"))
        self.run_commands.side_effect = [
            # remote_file_exists -> dir bootflash:/nxos.sample-n9k_ALL-1.0.0.rpm
            ["  1234  nxos.sample-n9k_ALL-1.0.0.rpm"],
            # install_remove_rpm:
            # show install inactive
            ["no packages"],
            # show install active: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 active"],
            # show install pkg-info
            ["Patch Type    :  normal"],
            # show install committed: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 committed"],
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_main_present_installs_rpm(self):
        """state=present, full add+activate+commit flow -> changed."""
        set_module_args(dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="present"))
        self.run_commands.side_effect = [
            # remote_file_exists -> file found
            ["  1234  nxos.sample-n9k_ALL-1.0.0.rpm"],
            # install_remove_rpm:
            # show install inactive
            ["no packages"],
            # show install active
            ["no packages"],
            # add_operation -> validate -> show install inactive: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 listed"],
            # show install pkg-info
            ["Patch Type    :  normal"],
            # activate_operation -> validate -> show install active: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 active"],
            # show install committed
            ["no committed"],
            # show install patches
            ["nxos.sample-n9k_ALL-1.0.0 patch"],
            # commit_operation -> validate -> show install committed: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 committed"],
        ]
        result = self.execute_module(changed=True)
        self.assertTrue(len(result["commands"]) >= 3)

    def test_main_absent_removes_rpm(self):
        """state=absent, pkg committed and active -> deactivate, commit, remove."""
        set_module_args(dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="absent"))
        self.run_commands.side_effect = [
            # install_remove_rpm:
            # show install committed: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 committed"],
            # show install active: pkg present
            ["nxos.sample-n9k_ALL-1.0.0 active"],
            # show install pkg-info
            ["Patch Type    :  normal"],
            # deactivate_operation -> validate -> show install active: pkg gone
            ["no active packages"],
            # execute_show_command(show_commit) after deactivate
            ["nxos.sample-n9k_ALL-1.0.0 committed"],
            # commit_operation -> validate -> show install committed: pkg gone
            ["no committed packages"],
            # remove_operation -> terminal -> validate -> inactive: pkg gone
            ["no inactive packages"],
        ]
        result = self.execute_module(changed=True)
        self.assertTrue(len(result["commands"]) >= 3)

    def test_main_absent_nothing_to_remove_unchanged(self):
        """state=absent, pkg not anywhere -> unchanged."""
        set_module_args(dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="absent"))
        self.run_commands.side_effect = [
            # show install committed: not present
            ["no committed packages"],
            # show install active: not present
            ["no active packages"],
            # show install pkg-info
            ["Patch Type    :  normal"],
            # show install inactive: not present
            ["no inactive packages"],
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_main_absent_no_remote_file_check(self):
        """state=absent does not call remote_file_exists."""
        set_module_args(dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="absent"))
        self.run_commands.side_effect = [
            # No remote_file_exists call for absent
            # show install committed
            ["no committed packages"],
            # show install active
            ["no active packages"],
            # show install pkg-info
            ["Patch Type    :  normal"],
            # show install inactive
            ["no inactive packages"],
        ]
        result = self.execute_module(changed=False)
        # Verify dir command (remote_file_exists) was NOT called
        for c in self.run_commands.call_args_list:
            cmds = c[0][1]  # Second positional arg to run_commands
            for cmd_dict in cmds:
                self.assertNotIn("dir ", cmd_dict.get("command", ""))

    def test_main_aggregate_mode(self):
        """Test aggregate mode with multiple packages."""
        set_module_args(
            dict(
                aggregate=[
                    dict(pkg="pkg1.rpm", state="absent"),
                    dict(pkg="pkg2.rpm", state="absent"),
                ],
            ),
        )
        # Both packages absent everywhere -> unchanged
        self.run_commands.side_effect = [
            # pkg1:
            ["no committed"],
            ["no active"],
            ["Patch Type    :  normal"],
            ["no inactive"],
            # pkg2:
            ["no committed"],
            ["no active"],
            ["Patch Type    :  normal"],
            ["no inactive"],
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_main_aggregate_mode_with_changes(self):
        """Test aggregate mode where one package produces changes."""
        set_module_args(
            dict(
                aggregate=[
                    dict(pkg="pkg1.rpm", state="absent"),
                    dict(pkg="pkg2.rpm", state="absent"),
                ],
            ),
        )
        self.run_commands.side_effect = [
            # pkg1: only in inactive -> remove
            ["no committed"],
            ["no active"],
            ["Patch Type    :  normal"],
            ["pkg1 in inactive"],
            # remove_operation -> terminal -> validate -> gone
            ["no inactive"],
            # pkg2: not anywhere
            ["no committed"],
            ["no active"],
            ["Patch Type    :  normal"],
            ["no inactive"],
        ]
        result = self.execute_module(changed=True)
        self.assertTrue(len(result["commands"]) > 0)

    def test_main_aggregate_inherits_defaults(self):
        """Test that aggregate items inherit top-level defaults."""
        set_module_args(
            dict(
                aggregate=[
                    dict(pkg="pkg1.rpm"),
                ],
                state="absent",
                file_system="slot0",
            ),
        )
        self.run_commands.side_effect = [
            ["no committed"],
            ["no active"],
            ["Patch Type    :  normal"],
            ["no inactive"],
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_main_custom_file_system(self):
        """Test state=present with custom file_system."""
        set_module_args(
            dict(pkg="nxos.sample-n9k_ALL-1.0.0.rpm", state="present", file_system="slot0"),
        )
        self.run_commands.side_effect = [
            # remote_file_exists -> dir slot0:/nxos.sample-n9k_ALL-1.0.0.rpm
            ["  1234  nxos.sample-n9k_ALL-1.0.0.rpm"],
            # Already installed idempotent
            ["no packages"],
            ["nxos.sample-n9k_ALL-1.0.0 active"],
            ["Patch Type    :  normal"],
            ["nxos.sample-n9k_ALL-1.0.0 committed"],
        ]
        result = self.execute_module(changed=False)
        # Verify the dir command used the custom file system
        first_call = self.run_commands.call_args_list[0]
        cmd = first_call[0][1][0]["command"]
        self.assertIn("slot0:", cmd)
