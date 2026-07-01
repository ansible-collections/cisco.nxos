from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_aaa_server_host

from .nxos_module import TestNxosModule, set_module_args


class TestNxosAaaServerHostModule(TestNxosModule):
    module = nxos_aaa_server_host

    def setUp(self):
        super(TestNxosAaaServerHostModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_aaa_server_host.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_aaa_server_host.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_aaa_server_host.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

    def tearDown(self):
        super(TestNxosAaaServerHostModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()

    def test_nxos_aaa_server_host_radius_new(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(server_type="radius", address="1.2.3.4", host_timeout="10", state="present"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_aaa_server_host_tacacs(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(server_type="tacacs", address="5.6.7.8", tacacs_port="89", state="present"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_aaa_server_host_absent(self):
        self.run_commands.side_effect = [
            ["radius-server host 1.2.3.4 auth-port 1812 acct-port 1813"],
            [""],
        ]
        set_module_args(
            dict(server_type="radius", address="1.2.3.4", state="absent"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_aaa_server_host_tacacs_port_with_radius(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(server_type="radius", address="1.2.3.4", tacacs_port="89", state="present"),
        )
        result = self.execute_module(failed=True)

    def test_nxos_aaa_server_host_auth_port_with_tacacs(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(server_type="tacacs", address="5.6.7.8", auth_port="2084", state="present"),
        )
        result = self.execute_module(failed=True)

    def test_nxos_aaa_server_host_encrypt_without_key(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(server_type="radius", address="1.2.3.4", encrypt_type="7", state="present"),
        )
        result = self.execute_module(failed=True)
