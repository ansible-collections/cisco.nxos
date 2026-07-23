#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_gir_profile_management

from .nxos_module import TestNxosModule, set_module_args


class TestNxosGirProfileManagementModule(TestNxosModule):
    module = nxos_gir_profile_management

    def setUp(self):
        super(TestNxosGirProfileManagementModule, self).setUp()
        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir_profile_management.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir_profile_management.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosGirProfileManagementModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_gir_profile_no_change(self):
        self.get_config.return_value = ""
        set_module_args(
            dict(
                mode="maintenance",
                state="absent",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
