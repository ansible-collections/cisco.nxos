#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
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

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_reboot_no_confirm(self):
        set_module_args(dict(confirm=False))
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_nxos_reboot_confirm(self):
        set_module_args(dict(confirm=True))
        result = self.execute_module(changed=True)
        self.assertTrue(result["changed"])
