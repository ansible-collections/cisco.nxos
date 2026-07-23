#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
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

    def tearDown(self):
        super(TestNxosAaaServerModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_aaa_server_no_change(self):
        self.run_commands.side_effect = [
            ["deadtime:10\ntimeout:5\n"],
            ["enabled"],
            [""],
        ]
        set_module_args(
            dict(
                server_type="radius",
                deadtime="10",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_aaa_server_change(self):
        self.run_commands.side_effect = [
            ["deadtime:0\ntimeout:5\n"],
            ["disabled"],
            [""],
            ["deadtime:10\ntimeout:5\n"],
            ["disabled"],
            [""],
        ]
        set_module_args(
            dict(
                server_type="radius",
                deadtime="10",
                state="present",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertNotEqual(result["commands"], [])
