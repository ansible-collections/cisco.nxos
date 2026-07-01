from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp

from .nxos_module import TestNxosModule, set_module_args


class TestNxosIgmpModule(TestNxosModule):
    module = nxos_igmp

    def setUp(self):
        super(TestNxosIgmpModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosIgmpModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def test_nxos_igmp_enable_flush_routes(self):
        self.run_commands.return_value = [""]
        set_module_args(dict(flush_routes=True, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("ip igmp flush-routes", result["updates"])

    def test_nxos_igmp_enable_enforce_rtr_alert(self):
        self.run_commands.return_value = [""]
        set_module_args(dict(enforce_rtr_alert=True, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("ip igmp enforce-router-alert", result["updates"])

    def test_nxos_igmp_idempotent(self):
        self.run_commands.return_value = [
            "ip igmp flush-routes\nip igmp enforce-router-alert\n",
        ]
        set_module_args(dict(flush_routes=True, enforce_rtr_alert=True, state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_igmp_default(self):
        self.run_commands.return_value = [
            "ip igmp flush-routes\nip igmp enforce-router-alert\n",
        ]
        set_module_args(dict(state="default"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip igmp flush-routes", result["updates"])
        self.assertIn("no ip igmp enforce-router-alert", result["updates"])

    def test_nxos_igmp_default_nothing_set(self):
        self.run_commands.return_value = [""]
        set_module_args(dict(state="default"))
        result = self.execute_module(changed=False)

    def test_nxos_igmp_disable_flush_routes(self):
        self.run_commands.return_value = ["ip igmp flush-routes\n"]
        set_module_args(dict(flush_routes=False, state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip igmp flush-routes", result["updates"])
