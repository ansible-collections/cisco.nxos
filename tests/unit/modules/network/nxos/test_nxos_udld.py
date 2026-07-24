#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_udld

from .nxos_module import TestNxosModule, set_module_args


class TestNxosUdldModule(TestNxosModule):
    module = nxos_udld

    def setUp(self):
        super(TestNxosUdldModule, self).setUp()
        self.mock_get_udld_global = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld.get_udld_global",
        )
        self.get_udld_global = self.mock_get_udld_global.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosUdldModule, self).tearDown()
        self.mock_get_udld_global.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_udld_no_change(self):
        self.get_udld_global.return_value = {
            "aggressive": "enabled",
            "msg_time": "10",
        }
        set_module_args(
            dict(
                aggressive="enabled",
                msg_time="10",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
