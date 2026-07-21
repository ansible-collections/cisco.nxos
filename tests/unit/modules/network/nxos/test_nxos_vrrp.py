#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrrp

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrrpModule(TestNxosModule):
    module = nxos_vrrp

    def setUp(self):
        super(TestNxosVrrpModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()
        self.get_interface_mode.return_value = ("layer3", "Ethernet1/1")

        self.mock_get_existing_vrrp = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_existing_vrrp",
        )
        self.get_existing_vrrp = self.mock_get_existing_vrrp.start()

    def tearDown(self):
        super(TestNxosVrrpModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_get_interface_type.stop()
        self.mock_get_interface_mode.stop()
        self.mock_get_existing_vrrp.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_vrrp_no_change(self):
        self.get_existing_vrrp.return_value = {
            "group": "10",
            "vip": "192.0.2.1",
            "priority": "100",
            "preempt": False,
            "authentication": "",
            "interval": "1",
            "admin_state": "shutdown",
        }
        set_module_args(
            dict(
                group="10",
                interface="Ethernet1/1",
                vip="192.0.2.1",
                priority="100",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
