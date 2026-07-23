#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_gir

from .nxos_module import TestNxosModule, set_module_args


class TestNxosGirModule(TestNxosModule):
    module = nxos_gir

    def setUp(self):
        super(TestNxosGirModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosGirModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_gir_maintenance_no_change(self):
        self.run_commands.return_value = [
            "      System Mode: Maintenance\n",
        ]
        set_module_args(
            dict(
                system_mode_maintenance=True,
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
