from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_snapshot

from .nxos_module import TestNxosModule, set_module_args


class TestNxosSnapshotModule(TestNxosModule):
    module = nxos_snapshot

    def setUp(self):
        super(TestNxosSnapshotModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_snapshot.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_snapshot.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosSnapshotModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def _snapshot_output(self, *names):
        lines = []
        for name in names:
            lines.append(
                "{0}  Mon May 06 05:30:22 2026  test snapshot".format(name),
            )
        return ["\n".join(lines)]

    def test_nxos_snapshot_create(self):
        self.run_commands.return_value = [""]
        set_module_args(
            dict(action="create", snapshot_name="test_snap", description="test snapshot"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_snapshot_create_already_exists(self):
        self.run_commands.return_value = self._snapshot_output("test_snap")
        set_module_args(
            dict(action="create", snapshot_name="test_snap", description="test snapshot"),
        )
        result = self.execute_module(changed=False)

    def test_nxos_snapshot_delete(self):
        self.run_commands.return_value = self._snapshot_output("test_snap")
        set_module_args(dict(action="delete", snapshot_name="test_snap"))
        result = self.execute_module(changed=True)

    def test_nxos_snapshot_delete_nonexistent(self):
        self.run_commands.return_value = [""]
        set_module_args(dict(action="delete", snapshot_name="test_snap"))
        result = self.execute_module(changed=False)

    def test_nxos_snapshot_delete_all(self):
        self.run_commands.return_value = self._snapshot_output("snap1", "snap2")
        set_module_args(dict(action="delete_all"))
        result = self.execute_module(changed=True)

    def test_nxos_snapshot_delete_all_empty(self):
        self.run_commands.return_value = [""]
        set_module_args(dict(action="delete_all"))
        result = self.execute_module(changed=False)
