from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vtp_domain

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVtpDomainModule(TestNxosModule):
    module = nxos_vtp_domain

    def setUp(self):
        super(TestNxosVtpDomainModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_domain.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_domain.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_domain.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {"network_os_model": "Nexus 9000"},
        }

    def tearDown(self):
        super(TestNxosVtpDomainModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None, device=""):
        vtp_status = "VTP version running  : 2\nVTP Domain Name  : testing\n"
        vtp_password = {"passwd": "secret"}
        self.run_commands.side_effect = [[vtp_status], [vtp_password], [vtp_status], [vtp_password]]
        self.load_config.return_value = None

    def test_nxos_vtp_domain_change(self):
        set_module_args(dict(domain="ntc"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["updates"], ["vtp domain ntc"])

    def test_nxos_vtp_domain_no_change(self):
        set_module_args(dict(domain="testing"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])

    def test_nxos_vtp_domain_check_mode(self):
        set_module_args(dict(domain="ntc", _ansible_check_mode=True))
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()
