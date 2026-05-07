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
        json_body = {
            "enabled": "true",
            "grepsup": "true",
            "glinklocalgrpsup": "true",
            "gv3repsup": "false",
        }
        text_body = "  Group timeout configured: 300\n"
        self.run_commands.side_effect = [[json_body], [text_body]]
        self.load_config.return_value = None

    def test_nxos_igmp_snooping_idempotent(self):
        set_module_args(dict(snooping=True, state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_igmp_snooping_enable_v3_report(self):
        set_module_args(dict(v3_report_supp=True, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("ip igmp snooping v3-report-suppression", result["commands"])

    def test_nxos_igmp_snooping_disable(self):
        set_module_args(dict(snooping=False, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip igmp snooping", result["commands"])

    def test_nxos_igmp_snooping_group_timeout(self):
        set_module_args(dict(group_timeout="500", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("ip igmp snooping group-timeout 500", result["commands"])

    def test_nxos_igmp_snooping_default(self):
        json_body = {
            "enabled": "true",
            "grepsup": "false",
            "glinklocalgrpsup": "false",
            "gv3repsup": "true",
        }
        text_body = "  Group timeout configured: 300\n"
        self.run_commands.side_effect = [[json_body], [text_body]]
        set_module_args(dict(state="default"))
        result = self.execute_module(changed=True)

    def test_nxos_igmp_snooping_check_mode(self):
        set_module_args(dict(v3_report_supp=True, state="present", _ansible_check_mode=True))
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()
