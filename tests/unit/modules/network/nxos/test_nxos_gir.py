from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_gir

from .nxos_module import TestNxosModule, set_module_args


class TestNxosGirModule(TestNxosModule):
    module = nxos_gir

    def setUp(self):
        super(TestNxosGirModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosGirModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def test_nxos_gir_maintenance_mode(self):
        self.run_commands.return_value = ["System is in Normal mode"]
        set_module_args(dict(system_mode_maintenance=True, state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_gir_already_in_maintenance(self):
        self.run_commands.return_value = ["System is in Maintenance mode"]
        set_module_args(dict(system_mode_maintenance=True, state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_gir_normal_mode(self):
        self.run_commands.return_value = ["System is in Maintenance mode"]
        set_module_args(dict(system_mode_maintenance=False, state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_gir_already_in_normal(self):
        self.run_commands.return_value = ["System is in Normal mode"]
        set_module_args(dict(system_mode_maintenance=False, state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_gir_shutdown_mode(self):
        self.run_commands.return_value = ["System is in Normal mode"]
        set_module_args(dict(system_mode_maintenance_shutdown=True, state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_gir_check_mode(self):
        self.run_commands.return_value = ["System is in Normal mode"]
        set_module_args(
            dict(system_mode_maintenance=True, state="present", _ansible_check_mode=True),
        )
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()

    def test_nxos_gir_timeout_present(self):
        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show system mode" in cmd:
                return ["System is in Normal mode"]
            elif "show maintenance timeout" in cmd:
                return ["Maintenance mode timeout value: 30 minutes"]
            return [""]

        self.run_commands.side_effect = side_effect
        set_module_args(dict(system_mode_maintenance_timeout="60", state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_gir_timeout_no_change(self):
        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show system mode" in cmd:
                return ["System is in Normal mode"]
            elif "show maintenance timeout" in cmd:
                return ["Maintenance mode timeout value: 30 minutes"]
            return [""]

        self.run_commands.side_effect = side_effect
        set_module_args(dict(system_mode_maintenance_timeout="30", state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_gir_reset_reason_present(self):
        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show system mode" in cmd:
                return ["System is in Normal mode"]
            elif "show maintenance on-reload reset-reasons" in cmd:
                return ["Reset Reasons: hw_error"]
            return [""]

        self.run_commands.side_effect = side_effect
        set_module_args(
            dict(
                system_mode_maintenance_on_reload_reset_reason="manual_reload",
                state="present",
            ),
        )
        result = self.execute_module(changed=True)
