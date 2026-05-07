from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vtp_version

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVtpVersionModule(TestNxosModule):
    module = nxos_vtp_version

    def setUp(self):
        super(TestNxosVtpVersionModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_version.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_version.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_version.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {"network_os_model": "Nexus 9000"},
        }

    def tearDown(self):
        super(TestNxosVtpVersionModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None, device=""):
        vtp_status = "VTP version running  : 1\nVTP Domain Name  : testing\n"
        vtp_password = {"passwd": "secret"}
        self.run_commands.side_effect = [[vtp_status], [vtp_password], [vtp_status], [vtp_password]]
        self.load_config.return_value = None

    def test_nxos_vtp_version_change(self):
        set_module_args(dict(version="2"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["updates"], ["vtp version 2"])

    def test_nxos_vtp_version_no_change(self):
        set_module_args(dict(version="1"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])

    def test_nxos_vtp_version_check_mode(self):
        set_module_args(dict(version="3", _ansible_check_mode=True))
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()
