#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_file_copy

from .nxos_module import TestNxosModule, set_module_args


class TestNxosFileCopyModule(TestNxosModule):
    module = nxos_file_copy

    def setUp(self):
        super(TestNxosFileCopyModule, self).setUp()
        self.mock_get_resource_connection = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_file_copy.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        mock_conn = MagicMock()
        mock_conn.run_commands.return_value = [""]
        mock_conn.get_file.return_value = None
        self.get_resource_connection.return_value = mock_conn

    def tearDown(self):
        super(TestNxosFileCopyModule, self).tearDown()
        self.mock_get_resource_connection.stop()

    def load_fixtures(self, commands=None, device=""):
        pass

    def test_nxos_file_copy_file_pull_check_mode(self):
        set_module_args(
            dict(
                file_pull=True,
                remote_file="/test_file.bin",
                remote_scp_server="10.0.0.1",
                remote_scp_server_user="admin",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertTrue(result["changed"])
