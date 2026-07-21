#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfInterfaceModule(TestNxosModule):
    module = nxos_vrf_interface

    def setUp(self):
        super(TestNxosVrfInterfaceModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_normalize_interface = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.normalize_interface",
        )
        self.normalize_interface = self.mock_normalize_interface.start()
        self.normalize_interface.side_effect = lambda x: x

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_get_vrf_list = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_vrf_list",
        )
        self.get_vrf_list = self.mock_get_vrf_list.start()

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()

        self.mock_get_interface_info = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_info",
        )
        self.get_interface_info = self.mock_get_interface_info.start()

    def tearDown(self):
        super(TestNxosVrfInterfaceModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_normalize_interface.stop()
        self.mock_get_interface_type.stop()
        self.mock_get_vrf_list.stop()
        self.mock_get_interface_mode.stop()
        self.mock_get_interface_info.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_vrf_interface_no_change(self):
        self.get_vrf_list.return_value = ["default", "management"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "management"
        set_module_args(
            dict(
                vrf="management",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
