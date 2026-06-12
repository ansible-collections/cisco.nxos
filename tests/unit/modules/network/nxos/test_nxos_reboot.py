from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_reboot

from .nxos_module import TestNxosModule, set_module_args


class TestNxosRebootModule(TestNxosModule):
    module = nxos_reboot

    def setUp(self):
        super(TestNxosRebootModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_reboot.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosRebootModule, self).tearDown()
        self.mock_load_config.stop()

    def test_nxos_reboot_confirm_true(self):
        set_module_args(dict(confirm=True))
        result = self.execute_module(changed=True)
        self.load_config.assert_called_once()

    def test_nxos_reboot_confirm_false(self):
        set_module_args(dict(confirm=False))
        result = self.execute_module(changed=False)
        self.load_config.assert_not_called()

    def test_nxos_reboot_check_mode(self):
        set_module_args(dict(confirm=True, _ansible_check_mode=True))
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()
