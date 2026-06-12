from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_udld

from .nxos_module import TestNxosModule, set_module_args


class TestNxosUdldModule(TestNxosModule):
    module = nxos_udld

    def setUp(self):
        super(TestNxosUdldModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosUdldModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def _set_udld(self, aggressive="disabled", msg_time="15"):
        mode = "enabled-aggressive" if aggressive == "enabled" else "disabled"
        self.run_commands.return_value = [
            {"udld-global-mode": mode, "message-interval": msg_time},
        ]

    def test_nxos_udld_aggressive_enable(self):
        self._set_udld(aggressive="disabled")
        set_module_args(dict(aggressive="enabled", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("udld aggressive", result["updates"])

    def test_nxos_udld_msg_time(self):
        self._set_udld()
        set_module_args(dict(msg_time="20", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("udld message-time 20", result["updates"])

    def test_nxos_udld_no_change(self):
        self._set_udld()
        set_module_args(dict(aggressive="disabled", state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_udld_absent(self):
        self._set_udld(aggressive="enabled", msg_time="20")
        set_module_args(dict(state="absent"))
        result = self.execute_module(changed=True)
        self.assertIn("no udld aggressive", result["updates"])

    def test_nxos_udld_reset_with_absent_fails(self):
        self._set_udld()
        set_module_args(dict(reset=True, state="absent"))
        result = self.execute_module(failed=True)

    def test_nxos_udld_reset_present(self):
        self._set_udld()
        set_module_args(dict(aggressive="enabled", reset=True, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("udld reset", result["updates"])

    def test_nxos_udld_msg_time_default(self):
        self._set_udld(msg_time="20")
        set_module_args(dict(msg_time="default", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("no udld message-time", result["updates"])
