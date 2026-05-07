from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_rollback

from .nxos_module import TestNxosModule, set_module_args


class TestNxosRollbackModule(TestNxosModule):
    module = nxos_rollback

    def setUp(self):
        super(TestNxosRollbackModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_rollback.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()
        self.run_commands.return_value = [None]

    def tearDown(self):
        super(TestNxosRollbackModule, self).tearDown()
        self.mock_run_commands.stop()

    def test_nxos_rollback_checkpoint(self):
        set_module_args(dict(checkpoint_file="backup.cfg"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["filename"], "backup.cfg")
        self.assertEqual(result["status"], "checkpoint file created")
        self.run_commands.assert_called_once()

    def test_nxos_rollback_rollback_to(self):
        set_module_args(dict(rollback_to="backup.cfg"))
        result = self.execute_module(changed=True)
        self.assertEqual(result["filename"], "backup.cfg")
        self.assertEqual(result["status"], "rollback executed")
        self.run_commands.assert_called_once()

    def test_nxos_rollback_no_args(self):
        set_module_args(dict())
        result = self.execute_module(changed=True)
        self.assertIsNone(result["status"])
        self.assertIsNone(result["filename"])
