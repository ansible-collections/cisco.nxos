from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.cisco.nxos.plugins.modules.nxos_install_os import (
    build_install_cmd_set,
    massage_install_data,
    parse_show_install,
    parse_show_version,
)


class TestNxosInstallOsParseFunctions(unittest.TestCase):

    def _install_data(self, text):
        return [text]

    def test_parse_show_install_disruptive(self):
        text = (
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes      disruptive         reset  Incompatible image for ISSU\n"
            "\n"
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version   Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes\n"
        )
        result = parse_show_install(self._install_data(text))
        self.assertTrue(result["disruptive"])
        self.assertTrue(result["upgrade_needed"])
        self.assertFalse(result["error"])

    def test_parse_show_install_non_disruptive(self):
        text = (
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "\n"
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version   Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I6(1)    7.0(3)I7(1)           yes\n"
        )
        result = parse_show_install(self._install_data(text))
        self.assertFalse(result["disruptive"])
        self.assertTrue(result["upgrade_needed"])

    def test_parse_show_install_no_upgrade(self):
        text = (
            "Compatibility check is done:\n"
            "Module  bootable          Impact  Install-type  Reason\n"
            "------  --------  --------------  ------------  ------\n"
            "     1       yes  non-disruptive         reset  \n"
            "\n"
            "Images will be upgraded according to following table:\n"
            "Module       Image  Running-Version(pri:alt)    New-Version   Upg-Required\n"
            "------  ----------  ----------------------------------------  ------------\n"
            "     1        nxos                7.0(3)I7(1)    7.0(3)I7(1)            no\n"
        )
        result = parse_show_install(self._install_data(text))
        self.assertFalse(result["upgrade_needed"])

    def test_parse_show_install_error(self):
        result = parse_show_install(self._install_data("Pre-upgrade check failed.\n"))
        self.assertTrue(result["error"])

    def test_parse_show_install_invalid_command(self):
        result = parse_show_install(self._install_data("Invalid command at '^' marker.\n"))
        self.assertTrue(result["invalid_command"])
        self.assertTrue(result["error"])

    def test_parse_show_install_in_progress(self):
        result = parse_show_install(
            self._install_data("Another install procedure may be in progress\n"),
        )
        self.assertTrue(result["install_in_progress"])

    def test_parse_show_install_server_error_int(self):
        result = parse_show_install([-1])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_500(self):
        result = parse_show_install([500])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_32603(self):
        result = parse_show_install([-32603])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_server_error_1(self):
        result = parse_show_install([1])
        self.assertTrue(result["server_error"])

    def test_parse_show_install_upgrade_succeeded(self):
        result = parse_show_install(self._install_data("Install has been successful.\n"))
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_finishing(self):
        result = parse_show_install(
            self._install_data("Finishing the upgrade, switch will reboot in 10 seconds.\n"),
        )
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_switchover(self):
        result = parse_show_install(self._install_data("Switching over onto standby\n"))
        self.assertTrue(result["upgrade_succeeded"])

    def test_parse_show_install_timeout_upgrade(self):
        result = parse_show_install(
            self._install_data("timeout 120 trying to send command: install all\n"),
        )
        self.assertTrue(result["upgrade_succeeded"])
        self.assertTrue(result["use_impact_data"])

    def test_parse_show_install_connection_failure(self):
        result = parse_show_install(self._install_data("Connection failure: timed out\n"))
        self.assertTrue(result["server_error"] or result["upgrade_succeeded"])

    def test_parse_show_install_backend_error(self):
        result = parse_show_install(self._install_data("Backend processing error\n"))
        self.assertTrue(result["server_error"])

    def test_parse_show_install_timed_out(self):
        result = parse_show_install(self._install_data("timed out\n"))
        self.assertTrue(result["server_error"])

    def test_massage_install_data_single_item(self):
        result = massage_install_data(["test data"])
        self.assertEqual(result, "test data")

    def test_massage_install_data_two_items(self):
        result = massage_install_data(["header", "actual data"])
        self.assertEqual(result, "actual data")

    def test_massage_install_data_empty(self):
        result = massage_install_data([])
        self.assertEqual(result, "No install all data found")

    def test_build_install_cmd_set_no_issu(self):
        cmds = build_install_cmd_set("no", "nxos.bin", None, "impact")
        self.assertTrue(len(cmds) > 0)

    def test_build_install_cmd_set_with_kick(self):
        cmds = build_install_cmd_set("no", "nxos.bin", "kick.bin", "impact")
        self.assertTrue(len(cmds) > 0)

    def test_build_install_cmd_set_issu_yes(self):
        cmds = build_install_cmd_set("yes", "nxos.bin", None, "impact")
        cmd_str = " ".join(str(c) for c in cmds)
        self.assertIn("non-disruptive", cmd_str)

    def test_parse_show_version(self):
        data = [
            "Cisco Nexus Operating System (NX-OS) Software\n"
            "  BIOS: version 08.36\n"
            "  NXOS: version 7.0(3)I7(1)\n"
            "  System version: 7.0(3)I7(1)\n",
        ]
        result = parse_show_version(data)
        self.assertEqual(result["version"], "7.0(3)I7(1)")
        self.assertFalse(result["error"])

    def test_parse_show_version_no_match(self):
        data = ["No version info found\n"]
        result = parse_show_version(data)
        self.assertTrue(result["error"])
        self.assertEqual(result["version"], "")

    def test_parse_show_install_no_data(self):
        result = parse_show_install(self._install_data(""))
        self.assertFalse(result["error"])

    def test_parse_show_install_no_install_data(self):
        result = parse_show_install(self._install_data("No install all data found\n"))
        self.assertTrue(result["error"])
