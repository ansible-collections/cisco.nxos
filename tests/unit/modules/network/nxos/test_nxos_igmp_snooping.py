#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp_snooping

from .nxos_module import TestNxosModule, set_module_args


class TestNxosIgmpSnoopingModule(TestNxosModule):
    module = nxos_igmp_snooping

    def setUp(self):
        super(TestNxosIgmpSnoopingModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_snooping.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_snooping.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosIgmpSnoopingModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_igmp_snooping_no_change(self):
        self.run_commands.side_effect = [
            [
                {
                    "enabled": "true",
                    "grepsup": "false",
                    "gv3repsup": "false",
                    "glinklocalgrpsup": "false",
                },
            ],
            ["ip igmp snooping\n  Group timeout configured: \n"],
        ]
        set_module_args(
            dict(
                snooping=True,
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
