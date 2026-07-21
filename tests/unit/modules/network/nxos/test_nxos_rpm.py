#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_rpm

from .nxos_module import TestNxosModule, set_module_args


class TestNxosRpmModule(TestNxosModule):
    module = nxos_rpm

    def setUp(self):
        super(TestNxosRpmModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_rpm.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_remote_file_exists = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_rpm.remote_file_exists",
        )
        self.remote_file_exists = self.mock_remote_file_exists.start()

        self.mock_install_remove_rpm = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_rpm.install_remove_rpm",
        )
        self.install_remove_rpm = self.mock_install_remove_rpm.start()

    def tearDown(self):
        super(TestNxosRpmModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_remote_file_exists.stop()
        self.mock_install_remove_rpm.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_rpm_present_already_installed(self):
        self.remote_file_exists.return_value = True
        self.install_remove_rpm.return_value = []
        set_module_args(
            dict(
                pkg="test_pkg",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
