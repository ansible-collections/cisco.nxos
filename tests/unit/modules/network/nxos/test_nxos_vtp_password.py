from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vtp_password

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVtpPasswordModule(TestNxosModule):
    module = nxos_vtp_password

    def setUp(self):
        super(TestNxosVtpPasswordModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_password.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_password.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_password.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {"network_os_model": "Nexus 9000"},
        }

    def tearDown(self):
        super(TestNxosVtpPasswordModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()

    def _set_existing(self, domain="testing", version="2", password="oldpass"):
        vtp_status = "VTP version running  : {0}\nVTP Domain Name  : {1}\n".format(
            version, domain,
        )
        vtp_password = {"passwd": password}
        self.run_commands.side_effect = [
            [vtp_status], [vtp_password], [vtp_status], [vtp_password],
        ]

    def test_nxos_vtp_password_set(self):
        self._set_existing(password="oldpass")
        set_module_args(dict(vtp_password="newpass", state="present"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["updates"], ["vtp password newpass"])

    def test_nxos_vtp_password_no_change(self):
        self._set_existing(password="oldpass")
        set_module_args(dict(vtp_password="oldpass", state="present"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])

    def test_nxos_vtp_password_remove(self):
        self._set_existing(password="oldpass")
        set_module_args(dict(vtp_password="oldpass", state="absent"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["updates"], ["no vtp password"])

    def test_nxos_vtp_password_remove_mismatch(self):
        self._set_existing(password="oldpass")
        set_module_args(dict(vtp_password="wrongpass", state="absent"))
        result = self.execute_module(failed=True)

    def test_nxos_vtp_password_absent_no_password(self):
        self._set_existing(password="")
        set_module_args(dict(state="absent"))
        result = self.execute_module(changed=False)
