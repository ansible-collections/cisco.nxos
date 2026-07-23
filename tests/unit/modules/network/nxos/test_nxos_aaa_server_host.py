#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
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

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_aaa_server_host_no_change(self):
        self.run_commands.return_value = [
            "radius-server host 10.0.0.1\n",
        ]
        set_module_args(
            dict(
                server_type="radius",
                address="10.0.0.1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])
