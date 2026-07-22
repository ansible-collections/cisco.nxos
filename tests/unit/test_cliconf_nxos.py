# Generated with AI assistance: Claude Code (Anthropic)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

from unittest import TestCase
from unittest.mock import MagicMock, patch

from ansible.errors import AnsibleConnectionFailure

from ansible_collections.cisco.nxos.plugins.cliconf.nxos import Cliconf


def make_cliconf():
    conn = MagicMock()
    conn.get_prompt.return_value = b"switch#"
    cliconf = Cliconf.__new__(Cliconf)
    cliconf._module_context = {}
    cliconf._device_info = {}
    cliconf._connection = conn
    return cliconf, conn


class TestCliconfNxosModuleContext(TestCase):
    def test_save_and_read_module_context(self):
        cliconf, _conn = make_cliconf()
        cliconf.save_module_context("test_key", {"data": "value"})
        result = cliconf.read_module_context("test_key")
        self.assertEqual(result, {"data": "value"})

    def test_read_module_context_missing_key(self):
        cliconf, _conn = make_cliconf()
        result = cliconf.read_module_context("nonexistent")
        self.assertIsNone(result)


class TestCliconfNxosDeviceInfo(TestCase):
    def test_get_device_info_system_version(self):
        cliconf, conn = make_cliconf()

        show_version_output = (
            "Cisco Nexus Operating System (NX-OS) Software\n"
            "Hardware\n"
            "  cisco Nexus9000 C9300v Chassis\n"
            "  Device name: nxos-switch\n"
            "  system:  version 9.3(7)\n"
            "  system image file is: bootflash:///nxos.9.3.7.bin\n"
        )
        show_inventory_output = (
            'NAME: "Chassis",   DESCR: "Nexus9000 C9300v Chassis"\nPID: N9K-C9300v\n'
        )

        def mock_get(cmd, *args, **kwargs):
            if "show version" in cmd:
                return show_version_output
            if "show inventory" in cmd:
                return show_inventory_output
            return ""

        cliconf.get = mock_get
        info = cliconf.get_device_info()
        self.assertEqual(info["network_os"], "nxos")
        self.assertEqual(info["network_os_version"], "9.3(7)")
        self.assertEqual(info["network_os_hostname"], "nxos-switch")
        self.assertIn("Nexus9000", info["network_os_model"])
        self.assertEqual(info["network_os_platform"], "N9K-C9300v")
        self.assertIn("nxos.9.3.7.bin", info["network_os_image"])

    def test_get_device_info_kickstart_version(self):
        cliconf, conn = make_cliconf()

        show_version_output = (
            "Cisco Nexus Operating System (NX-OS) Software\n"
            "Hardware\n"
            "  cisco Nexus7000 Chassis\n"
            "  Device name: n7k-switch\n"
            "  kickstart:  version 8.2(1)\n"
            "  kickstart image file is: bootflash:///n7000-s2-kickstart.8.2.1.bin\n"
        )
        show_inventory_output = 'NAME: "Chassis",   DESCR: "Nexus7000 Chassis"\nPID: N7K-C7009\n'

        def mock_get(cmd, *args, **kwargs):
            if "show version" in cmd:
                return show_version_output
            if "show inventory" in cmd:
                return show_inventory_output
            return ""

        cliconf.get = mock_get
        info = cliconf.get_device_info()
        self.assertEqual(info["network_os_version"], "8.2(1)")
        self.assertIn("n7000-s2-kickstart", info["network_os_image"])

    def test_get_device_info_nxos_version(self):
        cliconf, conn = make_cliconf()

        show_version_output = (
            "Cisco Nexus Operating System (NX-OS) Software\n"
            "Hardware\n"
            "  cisco Nexus 9000 Chassis\n"
            "  Device name: leaf1\n"
            "  NXOS:  version 10.2(3)\n"
            "  NXOS image file is: bootflash:///nxos64-cs.10.2.3.M.bin\n"
        )
        show_inventory_output = 'NAME: "Chassis",   DESCR: "Nexus 9000"\nPID: N9K-C93180YC-FX\n'

        def mock_get(cmd, *args, **kwargs):
            if "show version" in cmd:
                return show_version_output
            if "show inventory" in cmd:
                return show_inventory_output
            return ""

        cliconf.get = mock_get
        info = cliconf.get_device_info()
        self.assertEqual(info["network_os_version"], "10.2(3)")
        self.assertIn("nxos64-cs", info["network_os_image"])

    def test_get_device_info_cached(self):
        cliconf, conn = make_cliconf()
        cliconf._device_info = {"network_os": "nxos", "network_os_version": "cached"}
        info = cliconf.get_device_info()
        self.assertEqual(info["network_os_version"], "cached")


class TestCliconfNxosGetConfig(TestCase):
    def test_get_config_running(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="running config output")
        result = cliconf.get_config(source="running")
        self.assertEqual(result, "running config output")
        cliconf.send_command.assert_called_once_with("show running-config")

    def test_get_config_startup(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="startup config output")
        result = cliconf.get_config(source="startup")
        self.assertEqual(result, "startup config output")
        cliconf.send_command.assert_called_once_with("show startup-config")

    def test_get_config_with_flags(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="config output")
        result = cliconf.get_config(source="running", flags=["interface Ethernet1/1"])
        cliconf.send_command.assert_called_once_with(
            "show running-config interface Ethernet1/1",
        )

    def test_get_config_json_format(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="{}")
        result = cliconf.get_config(source="running", format="json")
        cliconf.send_command.assert_called_once_with("show running-config | json")

    def test_get_config_invalid_source(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.get_config(source="candidate")

    def test_get_config_invalid_format(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.get_config(source="running", format="xml")


class TestCliconfNxosRestore(TestCase):
    def test_restore_with_filename(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="ok")
        cliconf.restore(filename="backup.cfg")
        cliconf.send_command.assert_called_once_with(
            "configure replace backup.cfg best-effort",
        )

    def test_restore_with_path(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="ok")
        cliconf.restore(filename="backup.cfg", path="bootflash:/")
        cliconf.send_command.assert_called_once_with(
            "configure replace bootflash:/backup.cfg best-effort",
        )

    def test_restore_without_filename_raises(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.restore()


class TestCliconfNxosGetDiff(TestCase):
    def test_get_diff_no_candidate_raises(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.get_diff(candidate=None)

    def test_get_diff_invalid_match(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.get_diff(candidate="line1", diff_match="invalid")

    def test_get_diff_invalid_replace(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.get_diff(candidate="line1", diff_replace="invalid")

    def test_get_diff_with_candidate_only(self):
        cliconf, conn = make_cliconf()
        result = cliconf.get_diff(candidate="interface Ethernet1/1\n  no shutdown")
        self.assertIn("config_diff", result)

    def test_get_diff_with_running(self):
        cliconf, conn = make_cliconf()
        result = cliconf.get_diff(
            candidate="interface Ethernet1/1\n  description test",
            running="interface Ethernet1/1\n  no shutdown",
        )
        self.assertIn("config_diff", result)

    def test_get_diff_match_none(self):
        cliconf, conn = make_cliconf()
        result = cliconf.get_diff(
            candidate="interface Ethernet1/1\n  description test",
            running="interface Ethernet1/1\n  no shutdown",
            diff_match="none",
        )
        self.assertIn("config_diff", result)


class TestCliconfNxosEditConfig(TestCase):
    def test_edit_config_basic(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        result = cliconf.edit_config(candidate=["interface Ethernet1/1", "no shutdown"])
        self.assertIn("request", result)
        self.assertIn("response", result)
        self.assertEqual(result["request"], ["interface Ethernet1/1", "no shutdown"])

    def test_edit_config_skips_end_command(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        result = cliconf.edit_config(candidate=["interface Ethernet1/1", "end"])
        self.assertEqual(result["request"], ["interface Ethernet1/1"])

    def test_edit_config_no_commit_raises(self):
        cliconf, conn = make_cliconf()
        cliconf.check_edit_config_capability = MagicMock()
        with self.assertRaises(ValueError):
            cliconf.edit_config(candidate=["test"], commit=False)

    def test_edit_config_with_replace(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        result = cliconf.edit_config(
            candidate="config replace bootflash:/backup.cfg",
            replace="bootflash:/backup.cfg",
        )
        self.assertIn("request", result)

    def test_edit_config_diff_warning(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        result = cliconf.edit_config(candidate=["test cmd"], diff=True)
        conn.queue_message.assert_called()

    def test_edit_config_with_err_responses(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        conn._get_terminal_std_re.return_value = []
        result = cliconf.edit_config(
            candidate=["interface Ethernet1/1"],
            err_responses=["custom error pattern"],
        )
        self.assertIn("request", result)

    def test_edit_config_with_dict_command(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        cliconf.check_edit_config_capability = MagicMock()
        result = cliconf.edit_config(
            candidate=[{"command": "interface Ethernet1/1"}],
        )
        self.assertEqual(result["request"], ["interface Ethernet1/1"])


class TestCliconfNxosRunCommands(TestCase):
    def test_run_commands_none_raises(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf.run_commands(commands=None)

    def test_run_commands_basic(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="output text")
        result = cliconf.run_commands(commands=["show version"])
        self.assertEqual(result, ["output text"])

    def test_run_commands_json_output(self):
        cliconf, conn = make_cliconf()
        json_data = json.dumps({"version": "9.3(7)"})
        cliconf.send_command = MagicMock(return_value=json_data)
        cliconf._get_command_with_output = MagicMock(
            return_value="show version | json",
        )
        result = cliconf.run_commands(
            commands=[{"command": "show version", "output": "json"}],
        )
        self.assertEqual(result, [{"version": "9.3(7)"}])

    def test_run_commands_connection_failure_check_rc_true(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(
            side_effect=AnsibleConnectionFailure("connection lost"),
        )
        with self.assertRaises(AnsibleConnectionFailure):
            cliconf.run_commands(commands=["show version"], check_rc=True)

    def test_run_commands_connection_failure_check_rc_false(self):
        cliconf, conn = make_cliconf()
        err = AnsibleConnectionFailure("connection lost")
        err.err = "error output"
        cliconf.send_command = MagicMock(side_effect=err)
        result = cliconf.run_commands(commands=["show version"], check_rc=False)
        self.assertEqual(result, ["error output"])


class TestCliconfNxosGetCommandWithOutput(TestCase):
    def test_json_output_appended(self):
        cliconf, conn = make_cliconf()
        cliconf._device_info = {
            "network_os_model": "Nexus9000",
            "network_os_platform": "N9K-C9300v",
        }
        result = cliconf._get_command_with_output("show version", "json")
        self.assertEqual(result, "show version | json")

    def test_json_already_present(self):
        cliconf, conn = make_cliconf()
        result = cliconf._get_command_with_output("show version | json", "json")
        self.assertEqual(result, "show version | json")

    def test_text_output_strips_json(self):
        cliconf, conn = make_cliconf()
        result = cliconf._get_command_with_output("show version | json", "text")
        self.assertEqual(result, "show version ")

    def test_text_output_no_change(self):
        cliconf, conn = make_cliconf()
        result = cliconf._get_command_with_output("show version", "text")
        self.assertEqual(result, "show version")

    def test_invalid_output_raises(self):
        cliconf, conn = make_cliconf()
        with self.assertRaises(ValueError):
            cliconf._get_command_with_output("show version", "xml")

    def test_json_pretty_output(self):
        cliconf, conn = make_cliconf()
        cliconf._device_info = {
            "network_os_model": "Nexus9000",
            "network_os_platform": "N9K-C9300v",
        }
        result = cliconf._get_command_with_output("show version", "json-pretty")
        self.assertEqual(result, "show version | json-pretty")

    def test_mds_platform_uses_json_native(self):
        cliconf, conn = make_cliconf()
        cliconf._device_info = {
            "network_os_model": "MDS 9148S",
            "network_os_platform": "DS-C9148S-K9",
        }
        result = cliconf._get_command_with_output("show version", "json")
        self.assertEqual(result, "show version | json native")


class TestCliconfNxosGet(TestCase):
    def test_get_basic(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="output")
        result = cliconf.get("show version")
        self.assertEqual(result, "output")

    def test_get_with_output(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="json output")
        cliconf._get_command_with_output = MagicMock(
            return_value="show version | json",
        )
        result = cliconf.get("show version", output="json")
        cliconf._get_command_with_output.assert_called_once_with(
            "show version",
            "json",
        )


class TestCliconfNxosDeviceOperations(TestCase):
    def test_get_device_operations(self):
        cliconf, conn = make_cliconf()
        ops = cliconf.get_device_operations()
        self.assertTrue(ops["supports_diff_replace"])
        self.assertFalse(ops["supports_commit"])
        self.assertTrue(ops["supports_generate_diff"])
        self.assertTrue(ops["supports_replace"])

    def test_get_option_values(self):
        cliconf, conn = make_cliconf()
        vals = cliconf.get_option_values()
        self.assertIn("text", vals["format"])
        self.assertIn("json", vals["format"])
        self.assertIn("line", vals["diff_match"])
        self.assertIn("json-pretty", vals["output"])

    def test_get_capabilities(self):
        cliconf, conn = make_cliconf()
        cliconf.send_command = MagicMock(return_value="")
        with patch.object(
            type(cliconf).__bases__[0],
            "get_capabilities",
            return_value={"rpc": ["edit_config", "get_config"], "network_api": "cliconf"},
        ):
            result_str = cliconf.get_capabilities()
            result = json.loads(result_str)
            self.assertIn("get_diff", result["rpc"])
            self.assertIn("run_commands", result["rpc"])
            self.assertIn("device_operations", result)
            self.assertIn("format", result)


class TestCliconfNxosSetCliPromptContext(TestCase):
    def test_already_in_exec_mode(self):
        cliconf, conn = make_cliconf()
        conn.connected = True
        conn.get_prompt.return_value = b"switch#"
        cliconf.set_cli_prompt_context()

    def test_in_config_mode_exits(self):
        cliconf, conn = make_cliconf()
        conn.connected = True
        conn.get_prompt.side_effect = [b"switch(config)#", b"switch#"]
        conn.send_command = MagicMock()
        cliconf.set_cli_prompt_context()
        conn.send_command.assert_called_with("exit")

    def test_prompt_none_raises(self):
        cliconf, conn = make_cliconf()
        conn.connected = True
        conn.get_prompt.return_value = None
        conn._last_recv_window = b"some window"
        with self.assertRaises(AnsibleConnectionFailure):
            cliconf.set_cli_prompt_context()

    def test_maint_mode_prompt_not_exited(self):
        cliconf, conn = make_cliconf()
        conn.connected = True
        conn.get_prompt.return_value = b"switch(maint-mode)#"
        cliconf.set_cli_prompt_context()
        conn.send_command.assert_not_called()


class TestCliconfNxosPullFile(TestCase):
    def test_pull_file_success(self):
        cliconf, conn = make_cliconf()
        conn._get_terminal_std_re.return_value = []
        cliconf.send_command = MagicMock(return_value="Copy complete")
        result = cliconf.pull_file("copy scp://user@host/file bootflash:")
        self.assertTrue(result)

    def test_pull_file_with_overwrite_prompt(self):
        cliconf, conn = make_cliconf()
        conn._get_terminal_std_re.return_value = []
        cliconf.send_command = MagicMock(
            side_effect=[
                "file existing with this name",
                "Copy complete",
            ],
        )
        result = cliconf.pull_file("copy scp://user@host/file bootflash:")
        self.assertTrue(result)

    def test_pull_file_with_ssh_prompt(self):
        cliconf, conn = make_cliconf()
        conn._get_terminal_std_re.return_value = []
        cliconf.send_command = MagicMock(
            side_effect=[
                "sure you want to continue connecting",
                "Password: ",
                "Copy complete",
            ],
        )
        result = cliconf.pull_file(
            "copy scp://user@host/file bootflash:",
            remotepassword="secret",
        )
        self.assertTrue(result)

    def test_pull_file_failure_max_retries(self):
        cliconf, conn = make_cliconf()
        conn._get_terminal_std_re.return_value = []
        cliconf.send_command = MagicMock(return_value="still copying...")
        result = cliconf.pull_file("copy scp://user@host/file bootflash:")
        self.assertFalse(result)
