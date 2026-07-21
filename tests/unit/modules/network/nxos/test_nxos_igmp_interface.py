#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosIgmpInterfaceModule(TestNxosModule):
    module = nxos_igmp_interface

    def setUp(self):
        super(TestNxosIgmpInterfaceModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()
        self.get_interface_mode.return_value = "layer3"

        self.mock_get_igmp_interface = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.get_igmp_interface",
        )
        self.get_igmp_interface = self.mock_get_igmp_interface.start()

    def tearDown(self):
        super(TestNxosIgmpInterfaceModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_interface_type.stop()
        self.mock_get_interface_mode.stop()
        self.mock_get_igmp_interface.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_igmp_interface_no_change(self):
        self.get_igmp_interface.return_value = {
            "version": "2",
            "startup_query_interval": "31",
            "startup_query_count": "2",
            "robustness": "2",
            "querier_timeout": "255",
            "query_mrt": "10",
            "query_interval": "125",
            "last_member_qrt": "1",
            "last_member_query_count": "2",
            "group_timeout": "260",
            "report_llg": False,
            "immediate_leave": False,
            "oif_routemap": None,
            "oif_prefix_source": [],
        }
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="2",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])
