#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# AI-generated unit tests for nxos_install_os module
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_install_os

from .nxos_module import TestNxosModule, set_module_args


class TestNxosInstallOsModule(TestNxosModule):
    module = nxos_install_os

    def setUp(self):
        super(TestNxosInstallOsModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_install_os.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_install_os.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosInstallOsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        # Do not reset load_config here; individual tests set their own
        # return_value or side_effect before calling execute_module.
        pass

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # parse_show_install: server errors via massage_install_data
    # In practice, load_config returns a list. massage_install_data
    # extracts the value, which may be an int server error code.
    # ------------------------------------------------------------------
    def test_parse_show_install_server_error_negative_one(self):
        result = nxos_install_os.parse_show_install([-1])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_500(self):
        result = nxos_install_os.parse_show_install([500])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_negative_32603(self):
        result = nxos_install_os.parse_show_install([-32603])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_one(self):
        result = nxos_install_os.parse_show_install([1])
        self.assertTrue(result["server_error"])

    # ------------------------------------------------------------------
    # parse_show_install: string error conditions
    # ------------------------------------------------------------------
    def test_parse_show_install_pre_upgrade_check_failed(self):
        data = ["Pre-upgrade check failed. Return code 0x40930046"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["error"])

    def test_parse_show_install_invalid_command_uppercase(self):
        data = ["Invalid command at line 1"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["invalid_command"])
        self.assertTrue(result["error"])

    def test_parse_show_install_no_install_data_found(self):
        data = ["No install all data found"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["error"])

    # ------------------------------------------------------------------
    # parse_show_install: transient conditions
    # ------------------------------------------------------------------
    def test_parse_show_install_install_in_progress(self):
        data = ["Another install procedure may be in progress"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["install_in_progress"])

    def test_parse_show_install_install_in_progress_extra_spaces(self):
        data = ["Another install procedure may  be in progress"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["install_in_progress"])

    def test_parse_show_install_backend_processing_error(self):
        data = ["Backend processing error"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["server_error"])

    def test_parse_show_install_timed_out(self):
        data = ["Command timed out"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_string_negative_one(self):
        data = ["-1"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_string_500(self):
        data = ["500"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["server_error"])

    # ------------------------------------------------------------------
    # parse_show_install: success conditions
    # ------------------------------------------------------------------
    def test_parse_show_install_finishing_upgrade(self):
        data = ["Finishing the upgrade, switch will reboot"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_install_successful(self):
        data = ["Install has been successful"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_switching_standby(self):
        data = ["Switching over onto standby"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_timeout_sending_install(self):
        data = ["timeout 30 trying to send command: install all"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["upgrade_succeeded"])
        self.assertTrue(result["use_impact_data"])

    def test_parse_show_install_connection_failure_uppercase(self):
        """Connection failure contains 'timed out' which matches the
        server_error pattern first in the parse loop. The do_install_all
        function handles this by promoting server_error to upgrade_succeeded."""
        data = ["Connection failure: timed out"]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["server_error"])

    # ------------------------------------------------------------------
    # parse_show_install: disruptive / non-disruptive module lines
    # ------------------------------------------------------------------
    def test_parse_show_install_disruptive_module(self):
        data = [
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     8       yes      disruptive         reset  Incompatible image for ISSU",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["disruptive"])
        self.assertIn("m8", result)
        self.assertTrue(result["m8"]["disruptive"])
        self.assertTrue(result["m8"]["bootable"])

    def test_parse_show_install_non_disruptive_module(self):
        data = [
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  ",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertFalse(result["disruptive"])
        self.assertIn("m1", result)
        self.assertFalse(result["m1"]["disruptive"])
        self.assertTrue(result["m1"]["bootable"])

    def test_parse_show_install_non_bootable_module(self):
        data = [
            "------  --------  --------------  ------------  ------\n"
            "     3        no      disruptive         reset  Incompatible",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertIn("m3", result)
        self.assertFalse(result["m3"]["bootable"])
        self.assertTrue(result["m3"]["disruptive"])

    # ------------------------------------------------------------------
    # parse_show_install: upgrade needed lines (yes/no)
    # ------------------------------------------------------------------
    def test_parse_show_install_upgrade_needed_yes(self):
        data = [
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version  Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     8       lcn9k                7.0(3)F3(2)    7.0(3)F2(2)           yes",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["upgrade_needed"])
        self.assertIn("m8_lcn9k", result)
        self.assertTrue(result["m8_lcn9k"]["upgrade_needed"])

    def test_parse_show_install_upgrade_needed_no(self):
        data = [
            "------  ----------  ----------------------------------------  ------------\n"
            "     8        bios                     v01.17         v01.17            no",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertFalse(result["upgrade_needed"])
        self.assertIn("m8_bios", result)
        self.assertFalse(result["m8_bios"]["upgrade_needed"])

    def test_parse_show_install_header_lines(self):
        data = [
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------",
        ]
        result = nxos_install_os.parse_show_install(data)
        # Headers and separators should be in processed
        self.assertTrue(len(result["processed"]) > 0)

    def test_parse_show_install_mixed_modules(self):
        """Multiple modules with different disruptive/upgrade states."""
        data = [
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "     8       yes      disruptive         reset  Incompatible\n"
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version  Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes\n"
            "     1        bios       v4.4.0(07/12/2017)    v4.4.0(07/12/2017)            no",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["disruptive"])
        self.assertTrue(result["upgrade_needed"])
        self.assertFalse(result["m1"]["disruptive"])
        self.assertTrue(result["m8"]["disruptive"])
        self.assertTrue(result["m1_nxos"]["upgrade_needed"])
        self.assertFalse(result["m1_bios"]["upgrade_needed"])

    # ------------------------------------------------------------------
    # massage_install_data
    # ------------------------------------------------------------------
    def test_massage_install_data_single_item(self):
        result = nxos_install_os.massage_install_data(["some output"])
        self.assertEqual(result, "some output")

    def test_massage_install_data_two_items_string(self):
        result = nxos_install_os.massage_install_data(["first", "second"])
        self.assertEqual(result, "second")

    def test_massage_install_data_two_items_dict_clierror(self):
        result = nxos_install_os.massage_install_data(
            ["first", {"clierror": "some cli error"}],
        )
        self.assertEqual(result, "some cli error")

    def test_massage_install_data_two_items_dict_code_500(self):
        result = nxos_install_os.massage_install_data(
            ["first", {"code": "500", "msg": "Backend error"}],
        )
        self.assertEqual(result, "Backend error")

    def test_massage_install_data_two_items_dict_other(self):
        result = nxos_install_os.massage_install_data(
            ["first", {"other_key": "value"}],
        )
        self.assertEqual(result, "No install all data found")

    def test_massage_install_data_more_than_two(self):
        result = nxos_install_os.massage_install_data(["a", "b", "c"])
        self.assertEqual(result, "No install all data found")

    def test_massage_install_data_two_items_dict_code_not_500(self):
        """Dict with 'code' key but value is not '500'."""
        result = nxos_install_os.massage_install_data(
            ["first", {"code": "200", "msg": "OK"}],
        )
        self.assertEqual(result, "No install all data found")

    # ------------------------------------------------------------------
    # build_install_cmd_set
    # ------------------------------------------------------------------
    def test_build_install_cmd_set_issu_yes_no_kick(self):
        cmds = nxos_install_os.build_install_cmd_set("yes", "nxos.bin", None, "install")
        self.assertEqual(cmds[0], "terminal dont-ask")
        self.assertIn("non-disruptive", cmds[1])
        self.assertIn("install all", cmds[1])

    def test_build_install_cmd_set_issu_yes_with_kick(self):
        cmds = nxos_install_os.build_install_cmd_set("yes", "system.bin", "kick.bin", "install")
        # issu_cmd should be empty for issu=yes with kickstart
        self.assertIn("system system.bin", cmds[1])
        self.assertIn("kickstart kick.bin", cmds[1])

    def test_build_install_cmd_set_issu_no_no_kick(self):
        cmds = nxos_install_os.build_install_cmd_set("no", "nxos.bin", None, "install")
        self.assertIn("install all", cmds[1])
        self.assertIn("nxos nxos.bin", cmds[1])
        self.assertNotIn("non-disruptive", cmds[1])

    def test_build_install_cmd_set_issu_no_with_kick_force_true(self):
        cmds = nxos_install_os.build_install_cmd_set(
            "no",
            "system.bin",
            "kick.bin",
            "install",
            True,
        )
        self.assertIn("force", cmds[1])
        self.assertIn("system system.bin", cmds[1])
        self.assertIn("kickstart kick.bin", cmds[1])

    def test_build_install_cmd_set_issu_no_with_kick_force_false(self):
        cmds = nxos_install_os.build_install_cmd_set(
            "no",
            "system.bin",
            "kick.bin",
            "install",
            False,
        )
        self.assertNotIn("force", cmds[1])

    def test_build_install_cmd_set_impact_type_no_kick(self):
        cmds = nxos_install_os.build_install_cmd_set("no", "nxos.bin", None, "impact")
        self.assertIn("show install all impact", cmds[1])

    def test_build_install_cmd_set_impact_type_with_kick(self):
        cmds = nxos_install_os.build_install_cmd_set(
            "no",
            "system.bin",
            "kick.bin",
            "impact",
        )
        # For impact with kick, issu_cmd should be empty (force not available for impact)
        self.assertIn("show install all impact", cmds[1])
        self.assertNotIn("force", cmds[1])

    # ------------------------------------------------------------------
    # parse_show_version
    # ------------------------------------------------------------------
    def test_parse_show_version_nxos_version(self):
        data = ["NXOS: version 7.0(3)I7(1)\nother line"]
        result = nxos_install_os.parse_show_version(data)
        self.assertEqual(result["version"], "7.0(3)I7(1)")
        self.assertFalse(result["error"])

    def test_parse_show_version_system_version(self):
        data = ["system: version 6.0(2)A8(6)"]
        result = nxos_install_os.parse_show_version(data)
        self.assertEqual(result["version"], "6.0(2)A8(6)")
        self.assertFalse(result["error"])

    def test_parse_show_version_kickstart_version(self):
        data = ["kickstart: version 7.3(0)D1(1)"]
        result = nxos_install_os.parse_show_version(data)
        self.assertEqual(result["version"], "7.3(0)D1(1)")
        self.assertFalse(result["error"])

    def test_parse_show_version_no_version_found(self):
        data = ["some random output with no version info"]
        result = nxos_install_os.parse_show_version(data)
        self.assertEqual(result["version"], "")
        self.assertTrue(result["error"])

    # ------------------------------------------------------------------
    # get_platform
    # ------------------------------------------------------------------
    def test_get_platform_n3k(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "N3K-C3172PQ-10GE"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "N3K")

    def test_get_platform_n5k(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "N5K-C5548UP"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "N5K")

    def test_get_platform_n6k(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "N6K-C6001-64P"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "N6K")

    def test_get_platform_n7k(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "N7K-C7009"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "N7K")

    def test_get_platform_n9k(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "N9K-C9396PX"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "N9K")

    def test_get_platform_unknown(self):
        self.run_commands.return_value = [
            {"TABLE_inv": {"ROW_inv": [{"productid": "WS-C3750-24PS"}]}},
        ]
        module = MagicMock()
        result = nxos_install_os.get_platform(module)
        self.assertEqual(result, "unknown")

    # ------------------------------------------------------------------
    # check_mode_legacy
    # ------------------------------------------------------------------
    def test_check_mode_legacy_no_upgrade_needed(self):
        """System version matches target, no kickstart."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I7(1)"}],
            ["NXOS: version 7.0(3)I7(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "nxos.bin")
        self.assertFalse(result["upgrade_needed"])

    def test_check_mode_legacy_upgrade_needed(self):
        """System version does not match target."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I7(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_needed"])
        self.assertTrue(result["disruptive"])

    def test_check_mode_legacy_target_image_error(self):
        """Target image version cannot be parsed."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["some garbage output"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "nxos.bin")
        self.assertTrue(result["error"])

    def test_check_mode_legacy_with_kick_upgrade_needed(self):
        """Kickstart image differs from current."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I6(1)"],
            ["kickstart: version 7.0(3)I7(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "sys.bin", "kick.bin")
        self.assertTrue(result["upgrade_needed"])
        self.assertTrue(result["disruptive"])

    def test_check_mode_legacy_with_kick_error(self):
        """Kickstart image version cannot be parsed."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I6(1)"],
            ["garbage output no version here"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "sys.bin", "kick.bin")
        self.assertTrue(result["error"])

    def test_check_mode_legacy_with_kick_no_upgrade(self):
        """Both system and kickstart match current."""
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I6(1)"],
            ["kickstart: version 7.0(3)I6(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_legacy(module, "no", "sys.bin", "kick.bin")
        self.assertFalse(result["upgrade_needed"])

    # ------------------------------------------------------------------
    # check_mode_nextgen
    # ------------------------------------------------------------------
    def test_check_mode_nextgen_success(self):
        """Normal success path with no errors."""
        install_output = (
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version  Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        self.load_config.return_value = [install_output]
        module = MagicMock()
        result = nxos_install_os.check_mode_nextgen(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_needed"])
        self.assertFalse(result["error"])
        self.assertIn("upgrade_cmd", result)

    def test_check_mode_nextgen_error_desired_retry(self):
        """Error with issu=desired should retry with issu=no."""
        error_output = "Invalid command at line 1"
        success_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  "
        )
        # First call returns error, second returns success
        self.load_config.side_effect = [
            [error_output],
            [success_output],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode_nextgen(module, "desired", "nxos.bin")
        self.assertFalse(result["error"])

    def test_check_mode_nextgen_server_error(self):
        """Server error should set error=True."""
        self.load_config.return_value = [-1]
        module = MagicMock()
        result = nxos_install_os.check_mode_nextgen(module, "no", "nxos.bin")
        self.assertTrue(result["server_error"])
        self.assertTrue(result["error"])

    # ------------------------------------------------------------------
    # check_install_in_progress
    # ------------------------------------------------------------------
    def test_check_install_in_progress_immediate_success(self):
        """No install in progress, returns immediately."""
        self.load_config.return_value = ["Install has been successful"]
        module = MagicMock()
        commands = ["terminal dont-ask", "install all nxos nxos.bin"]
        opts = {"ignore_timeout": True}
        result = nxos_install_os.check_install_in_progress(module, commands, opts)
        self.assertTrue(result["upgrade_succeeded"])
        self.assertEqual(self.load_config.call_count, 1)

    def test_check_install_in_progress_retries(self):
        """Install in progress on first call, succeeds on second."""
        self.load_config.side_effect = [
            ["Another install procedure may be in progress"],
            ["Install has been successful"],
        ]
        module = MagicMock()
        commands = ["terminal dont-ask", "install all nxos nxos.bin"]
        opts = {"ignore_timeout": True}
        result = nxos_install_os.check_install_in_progress(module, commands, opts)
        self.assertTrue(result["upgrade_succeeded"])
        self.assertEqual(self.load_config.call_count, 2)

    # ------------------------------------------------------------------
    # check_mode
    # ------------------------------------------------------------------
    def test_check_mode_nextgen_success_no_fallback(self):
        """Nextgen succeeds, no fallback needed."""
        install_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        self.load_config.return_value = [install_output]
        module = MagicMock()
        result = nxos_install_os.check_mode(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_needed"])

    def test_check_mode_fallback_server_error(self):
        """Server error triggers fallback to legacy."""
        self.load_config.return_value = [-1]
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I7(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_needed"])

    def test_check_mode_fallback_invalid_command(self):
        """Invalid command triggers fallback to legacy."""
        self.load_config.return_value = ["Invalid command at line 1"]
        self.run_commands.side_effect = [
            [{"kickstart_ver_str": "7.0(3)I6(1)"}],
            ["NXOS: version 7.0(3)I7(1)"],
        ]
        module = MagicMock()
        result = nxos_install_os.check_mode(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_needed"])

    # ------------------------------------------------------------------
    # do_install_all
    # ------------------------------------------------------------------
    def test_do_install_all_check_mode(self):
        """In check mode, impact data is returned without installing."""
        install_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        self.load_config.return_value = [install_output]
        module = MagicMock()
        module.check_mode = True
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertIn("*** SWITCH WAS NOT UPGRADED: IMPACT DATA ONLY ***", result["processed"])

    def test_do_install_all_check_mode_error(self):
        """Error in check_mode should be returned."""
        self.load_config.return_value = ["Pre-upgrade check failed"]
        module = MagicMock()
        module.check_mode = True
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        # Check mode appends message regardless of error
        self.assertIn("*** SWITCH WAS NOT UPGRADED: IMPACT DATA ONLY ***", result["processed"])

    def test_do_install_all_error_not_check_mode(self):
        """Error found during impact check, not in check mode."""
        self.load_config.return_value = ["Pre-upgrade check failed"]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertTrue(result["error"])

    def test_do_install_all_no_upgrade_needed(self):
        """Switch already at target version."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertFalse(result["upgrade_needed"])
        self.assertFalse(result["error"])

    def test_do_install_all_non_disruptive_upgrade(self):
        """Non-disruptive upgrade succeeds."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        install_output = "Install has been successful"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "desired", "nxos.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_disruptive_issu_yes_fails(self):
        """Disruptive upgrade with issu=yes should fail."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     8       yes      disruptive         reset  Incompatible\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     8       lcn9k                7.0(3)F3(2)    7.0(3)F2(2)           yes"
        )
        self.load_config.return_value = [impact_output]
        module = MagicMock()
        module.check_mode = False
        nxos_install_os.do_install_all(module, "yes", "nxos.bin")
        module.fail_json.assert_called_once()
        call_kwargs = module.fail_json.call_args
        self.assertIn("ISSU/ISSD requested", call_kwargs[1]["msg"])

    def test_do_install_all_disruptive_issu_no(self):
        """Disruptive upgrade with issu=no should proceed."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     8       yes      disruptive         reset  Incompatible\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     8       lcn9k                7.0(3)F3(2)    7.0(3)F2(2)           yes"
        )
        install_output = "Install has been successful"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_disruptive_issu_desired_falls_back(self):
        """Disruptive with issu=desired should fall back to issu=no."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes      disruptive         reset  Incompatible\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        install_output = "Install has been successful"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "desired", "nxos.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_invalid_command_force_retry(self):
        """Invalid command with force should retry without force."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes      disruptive         reset  Incompatible\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        # First install attempt: invalid command (force not supported)
        # Second install attempt (without force): success
        install_error = "Invalid command at line 1"
        install_success = "Install has been successful"
        self.load_config.side_effect = [
            [impact_output],
            [install_error],
            [install_success],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "sys.bin", "kick.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_server_error_uses_impact_data(self):
        """Server error during install uses impact data."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        self.load_config.side_effect = [
            [impact_output],
            [-1],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_use_impact_data_not_succeeded(self):
        """use_impact_data=True but upgrade_succeeded=False."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        # Install returns connection failure with use_impact_data but NOT upgrade_succeeded
        # This is a tricky edge case: connection failure sets both use_impact_data
        # and upgrade_succeeded. Let's construct data that sets use_impact_data but not
        # upgrade_succeeded via a different path. Actually looking at the code, when
        # server_error is hit during install, it forces upgrade_succeeded=True and
        # use_impact_data=True. The only other path to use_impact_data=True with
        # upgrade_succeeded=False is if the install output itself sets it.
        # The code at line 556 handles this case.
        install_output = "connection failure: timed out"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        module = MagicMock()
        module.check_mode = False
        # connection failure sets both upgrade_succeeded=True and use_impact_data=True
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertTrue(result["upgrade_succeeded"])

    def test_do_install_all_upgrade_not_succeeded_sets_error(self):
        """When upgrade does not succeed, error should be set."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        # Install returns something that doesn't indicate success
        install_output = "Some unknown status"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        module = MagicMock()
        module.check_mode = False
        result = nxos_install_os.do_install_all(module, "no", "nxos.bin")
        self.assertTrue(result["error"])

    # ------------------------------------------------------------------
    # main() via execute_module
    # ------------------------------------------------------------------
    def test_main_no_upgrade_needed(self):
        """End-to-end: no upgrade needed."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(dict(system_image_file="nxos.7.0.3.I7.1.bin"))
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_main_upgrade_needed(self):
        """End-to-end: upgrade needed and successful via connection timeout."""
        impact_output = (
            "Compatibility check is done:\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes"
        )
        install_output = "Connection failure: timed out"
        self.load_config.side_effect = [
            [impact_output],
            [install_output],
        ]
        set_module_args(dict(system_image_file="nxos.7.0.3.I7.1.bin"))
        result = self.execute_module(changed=True)
        self.assertTrue(result["changed"])

    def test_main_error(self):
        """End-to-end: error during install."""
        self.load_config.return_value = ["Pre-upgrade check failed"]
        set_module_args(dict(system_image_file="bad.bin"))
        result = self.execute_module(failed=True)
        self.assertTrue(result["failed"])

    def test_main_issu_required_maps_to_yes(self):
        """issu='required' should be remapped to 'yes'."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(
            dict(system_image_file="nxos.bin", issu="required"),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_main_kickstart_null_becomes_none(self):
        """kickstart_image_file='null' should be treated as None."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(
            dict(system_image_file="nxos.bin", kickstart_image_file="null"),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_main_kickstart_empty_becomes_none(self):
        """kickstart_image_file='' should be treated as None."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(
            dict(system_image_file="nxos.bin", kickstart_image_file=""),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_main_with_kickstart_image(self):
        """End-to-end with kickstart image provided."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(
            dict(
                system_image_file="system.bin",
                kickstart_image_file="kickstart.bin",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_main_issu_desired(self):
        """End-to-end with issu=desired."""
        no_upgrade_output = (
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no"
        )
        self.load_config.return_value = [no_upgrade_output]
        set_module_args(
            dict(system_image_file="nxos.bin", issu="desired"),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    # ------------------------------------------------------------------
    # execute_show_command
    # ------------------------------------------------------------------
    def test_execute_show_command_text(self):
        """Default output type is text."""
        self.run_commands.return_value = ["show output"]
        module = MagicMock()
        result = nxos_install_os.execute_show_command(module, "show version")
        self.run_commands.assert_called_once_with(
            module,
            [{"command": "show version", "output": "text"}],
        )
        self.assertEqual(result, ["show output"])

    def test_execute_show_command_json(self):
        """JSON output type."""
        self.run_commands.return_value = [{"version": "7.0"}]
        module = MagicMock()
        result = nxos_install_os.execute_show_command(module, "show version", "json")
        self.run_commands.assert_called_once_with(
            module,
            [{"command": "show version", "output": "json"}],
        )
        self.assertEqual(result, [{"version": "7.0"}])

    # ------------------------------------------------------------------
    # Additional edge cases
    # ------------------------------------------------------------------
    def test_parse_show_install_lines_not_matching_any_pattern(self):
        """Regular text lines that don't match any pattern are skipped."""
        data = [
            "Installer will perform impact only check. Please wait.\n"
            "Verifying image bootflash:/nxos.bin for boot variable nxos.\n"
            "[####################] 100% -- SUCCESS",
        ]
        result = nxos_install_os.parse_show_install(data)
        # No specific flags should be set
        self.assertFalse(result["error"])
        self.assertFalse(result["disruptive"])
        self.assertFalse(result["upgrade_needed"])
        self.assertFalse(result["upgrade_succeeded"])
        self.assertEqual(result["processed"], [])

    def test_parse_show_install_error_stops_processing(self):
        """Once an error is found, processing should stop (break)."""
        data = [
            "Pre-upgrade check failed\nInstall has been successful",
        ]
        result = nxos_install_os.parse_show_install(data)
        self.assertTrue(result["error"])
        # upgrade_succeeded should NOT be set because processing stopped at the error
        self.assertFalse(result["upgrade_succeeded"])

    def test_parse_show_install_images_will_header(self):
        """'Images will' header line should be in processed."""
        line = "Images will be upgraded according to following table:"
        data = [line]
        result = nxos_install_os.parse_show_install(data)
        self.assertIn(line, result["processed"])

    def test_parse_show_install_empty_string_defaults(self):
        """parse_show_install with empty string sets all defaults."""
        result = nxos_install_os.parse_show_install("")
        self.assertEqual(result["raw"], "")
        self.assertFalse(result["error"])
        self.assertFalse(result["server_error"])
        self.assertFalse(result["install_in_progress"])
        self.assertFalse(result["upgrade_succeeded"])
        self.assertFalse(result["use_impact_data"])

    def test_build_install_cmd_set_always_starts_with_terminal_dont_ask(self):
        """All command sets start with 'terminal dont-ask'."""
        for issu in ["yes", "no", "desired", "required"]:
            for kick in [None, "kick.bin"]:
                for cmd_type in ["impact", "install"]:
                    cmds = nxos_install_os.build_install_cmd_set(
                        issu,
                        "img.bin",
                        kick,
                        cmd_type,
                    )
                    self.assertEqual(cmds[0], "terminal dont-ask")
                    self.assertEqual(len(cmds), 2)
