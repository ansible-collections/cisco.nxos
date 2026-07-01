from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_aaa_server

from .nxos_module import TestNxosModule, set_module_args


class TestNxosAaaServerModule(TestNxosModule):
    module = nxos_aaa_server

    def setUp(self):
        super(TestNxosAaaServerModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_aaa_server.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_aaa_server.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosAaaServerModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def _set_default_existing(self):
        self.run_commands.side_effect = [
            ["timeout:5\ndeadtime:0\n"],
            ["disabled"],
            [""],
        ]

    def test_nxos_aaa_server_deadtime(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", deadtime="20", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("radius-server deadtime 20", result["commands"])

    def test_nxos_aaa_server_timeout(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", server_timeout="10", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("radius-server timeout 10", result["commands"])

    def test_nxos_aaa_server_directed_request(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", directed_request="enabled", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("radius-server directed-request", result["commands"])

    def test_nxos_aaa_server_no_change(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", deadtime="0", state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_aaa_server_encrypt_without_key(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", encrypt_type="7", state="present"))
        result = self.execute_module(failed=True)

    def test_nxos_aaa_server_invalid_deadtime(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", deadtime="9999", state="present"))
        result = self.execute_module(failed=True)

    def test_nxos_aaa_server_invalid_timeout(self):
        self._set_default_existing()
        set_module_args(dict(server_type="radius", server_timeout="999", state="present"))
        result = self.execute_module(failed=True)

    def test_nxos_aaa_server_default(self):
        self.run_commands.side_effect = [
            ["timeout:10\ndeadtime:20\n"],
            ["enabled"],
            ['radius-server key 7 "secretkey"'],
        ]
        set_module_args(
            dict(
                server_type="radius",
                deadtime="default",
                server_timeout="default",
                directed_request="default",
                state="default",
            ),
        )
        result = self.execute_module(changed=True)

    def test_nxos_aaa_server_tacacs(self):
        self._set_default_existing()
        set_module_args(dict(server_type="tacacs", deadtime="10", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("tacacs-server deadtime 10", result["commands"])
