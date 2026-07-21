#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_install_os

from .nxos_module import TestNxosModule, set_module_args


class TestNxosInstallOsModule(TestNxosModule):
    module = nxos_install_os

    def setUp(self):
        super(TestNxosInstallOsModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_install_os.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_install_os.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_do_install_all = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_install_os.do_install_all",
        )
        self.do_install_all = self.mock_do_install_all.start()

    def tearDown(self):
        super(TestNxosInstallOsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_do_install_all.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_install_os_no_upgrade_needed(self):
        self.do_install_all.return_value = {
            "error": False,
            "processed": [{"module": "nxos", "running": "9.3(7)", "status": "Success"}],
            "upgrade_needed": False,
            "list_data": [],
            "upgrade_cmd": "",
        }
        set_module_args(
            dict(
                system_image_file="nxos.9.3.7.bin",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_nxos_install_os_upgrade_needed(self):
        self.do_install_all.return_value = {
            "error": False,
            "processed": [{"module": "nxos", "running": "9.3(8)", "status": "Success"}],
            "upgrade_needed": True,
            "list_data": [],
            "upgrade_cmd": "install all nxos nxos.9.3.8.bin",
        }
        set_module_args(
            dict(
                system_image_file="nxos.9.3.8.bin",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertTrue(result["changed"])

    def test_nxos_install_os_error(self):
        self.do_install_all.return_value = {
            "error": True,
            "processed": [],
            "upgrade_needed": False,
            "list_data": ["Some error output"],
            "upgrade_cmd": "install all nxos bad.bin",
        }
        set_module_args(
            dict(
                system_image_file="bad.bin",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertTrue(result["failed"])
