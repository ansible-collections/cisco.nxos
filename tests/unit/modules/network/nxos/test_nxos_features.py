# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for the nxos_features Ansible module.

This module tests the behavior of nxos_features including:
- Merged, replaced, overridden and deleted state
- Idempotency of each state
- Rendered, gathered and parsed state
- Feature names with a space or a special character, and the no feature lines of default-off features
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_features

from .nxos_module import TestNxosModule, set_module_args


RUNNING = dedent(
    """\
    feature ssh
    no feature nxapi
    no feature bash-shell
    feature tacacs+
    feature bgp
    feature interface-vlan
    feature vn-segment-vlan-based
    feature nv overlay
    feature password encryption aes
    """,
)

RUNNING_CONFIG = [
    {"name": "bash-shell", "enabled": False},
    {"name": "bgp", "enabled": True},
    {"name": "interface-vlan", "enabled": True},
    {"name": "nv overlay", "enabled": True},
    {"name": "nxapi", "enabled": False},
    {"name": "password encryption aes", "enabled": True},
    {"name": "ssh", "enabled": True},
    {"name": "tacacs+", "enabled": True},
    {"name": "vn-segment-vlan-based", "enabled": True},
]


class TestNxosFeaturesModule(TestNxosModule):
    """Unit tests for the nxos_features."""

    module = nxos_features

    def setUp(self):
        """Set up test fixtures before each test method."""

        super().setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base."
            "resource_module_base.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.features."
            "features.FeaturesFacts.get_features_data",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        """Clean up after each test method."""

        super().tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()

    def _run(self, args, have="", changed=True):
        """Run the module with the given arguments against the given running configuration."""

        self.get_config.return_value = have
        set_module_args(args)
        return self.execute_module(changed=changed)

    # merged

    def test_nxos_features_merged_empty(self):
        """Test state merged on a device without feature lines."""

        result = self._run(
            {
                "config": [
                    {"name": "nv overlay", "enabled": True},
                    {"name": "vn-segment-vlan-based", "enabled": True},
                    {"name": "tacacs+", "enabled": True},
                ],
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            ["feature nv overlay", "feature vn-segment-vlan-based", "feature tacacs+"],
        )

    def test_nxos_features_merged_enabled_defaults_to_true(self):
        """Test that a feature without the enabled option is enabled."""

        result = self._run({"config": [{"name": "bgp"}], "state": "merged"})
        self.assertEqual(result["commands"], ["feature bgp"])

    def test_nxos_features_merged_idempotent(self):
        """Test idempotency of state merged."""

        self._run({"config": RUNNING_CONFIG, "state": "merged"}, have=RUNNING, changed=False)

    def test_nxos_features_merged_keeps_other_features(self):
        """Test that state merged removes nothing."""

        result = self._run(
            {"config": [{"name": "lacp", "enabled": True}], "state": "merged"},
            have=RUNNING,
        )
        self.assertEqual(result["commands"], ["feature lacp"])

    def test_nxos_features_merged_enables_before_disables(self):
        """Test that the commands that enable a feature come first."""

        result = self._run(
            {
                "config": [
                    {"name": "interface-vlan", "enabled": False},
                    {"name": "bgp", "enabled": False},
                    {"name": "lacp", "enabled": True},
                    {"name": "bfd", "enabled": True},
                ],
                "state": "merged",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            ["feature lacp", "feature bfd", "no feature interface-vlan", "no feature bgp"],
        )

    def test_nxos_features_merged_disable_idempotent(self):
        """Test that disabling a feature that is off, or has no line, changes nothing."""

        self._run(
            {
                "config": [
                    {"name": "nxapi", "enabled": False},
                    {"name": "ldap", "enabled": False},
                ],
                "state": "merged",
            },
            have=RUNNING,
            changed=False,
        )

    def test_nxos_features_merged_enable_default_off_feature(self):
        """Test that a feature with a no feature line is enabled."""

        result = self._run(
            {"config": [{"name": "bash-shell", "enabled": True}], "state": "merged"},
            have=RUNNING,
        )
        self.assertEqual(result["commands"], ["feature bash-shell"])

    def test_nxos_features_conflicting_duplicate(self):
        """Test that a feature given twice with different values fails."""

        set_module_args(
            {
                "config": [{"name": "bgp", "enabled": True}, {"name": "bgp", "enabled": False}],
                "state": "merged",
            },
        )
        self.get_config.return_value = ""
        result = self.execute_module(failed=True)
        self.assertIn("both enabled true and false", result["msg"])

    # replaced

    def test_nxos_features_replaced(self):
        """Test that state replaced behaves like merged."""

        config = [{"name": "lacp", "enabled": True}, {"name": "bgp", "enabled": False}]
        result = self._run({"config": config, "state": "replaced"}, have=RUNNING)
        self.assertEqual(result["commands"], ["feature lacp", "no feature bgp"])

    def test_nxos_features_replaced_idempotent(self):
        """Test idempotency of state replaced."""

        self._run({"config": RUNNING_CONFIG, "state": "replaced"}, have=RUNNING, changed=False)

    # overridden

    def test_nxos_features_overridden(self):
        """Test that state overridden disables the features that are not listed, after the enables."""

        result = self._run(
            {
                "config": [
                    {"name": "lacp", "enabled": True},
                    {"name": "bgp", "enabled": True},
                    {"name": "ssh", "enabled": True},
                ],
                "state": "overridden",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "feature lacp",
                "no feature interface-vlan",
                "no feature nv overlay",
                "no feature password encryption aes",
                "no feature tacacs+",
                "no feature vn-segment-vlan-based",
            ],
        )

    def test_nxos_features_overridden_idempotent(self):
        """Test idempotency of state overridden."""

        self._run({"config": RUNNING_CONFIG, "state": "overridden"}, have=RUNNING, changed=False)

    def test_nxos_features_overridden_skips_features_that_are_off(self):
        """Test that a no feature line is not disabled again."""

        self._run(
            {"config": [{"name": "ssh", "enabled": True}], "state": "overridden"},
            have="feature ssh\nno feature nxapi\n",
            changed=False,
        )

    # deleted

    def test_nxos_features_deleted_listed(self):
        """Test that state deleted disables the listed features whatever the value of enabled."""

        result = self._run(
            {
                "config": [
                    {"name": "bgp", "enabled": True},
                    {"name": "nxapi"},
                    {"name": "interface-vlan", "enabled": False},
                ],
                "state": "deleted",
            },
            have=RUNNING,
        )
        self.assertEqual(result["commands"], ["no feature bgp", "no feature interface-vlan"])

    def test_nxos_features_deleted_all(self):
        """Test that state deleted without config disables every enabled feature."""

        result = self._run({"state": "deleted"}, have=RUNNING)
        self.assertEqual(
            result["commands"],
            [
                "no feature bgp",
                "no feature interface-vlan",
                "no feature nv overlay",
                "no feature password encryption aes",
                "no feature ssh",
                "no feature tacacs+",
                "no feature vn-segment-vlan-based",
            ],
        )

    def test_nxos_features_deleted_idempotent(self):
        """Test idempotency of state deleted."""

        self._run(
            {"config": [{"name": "nxapi"}], "state": "deleted"},
            have=RUNNING,
            changed=False,
        )
        self._run({"state": "deleted"}, have="no feature nxapi\n", changed=False)

    # rendered, gathered, parsed

    def test_nxos_features_rendered(self):
        """Test state rendered."""

        set_module_args(
            {
                "config": [
                    {"name": "bgp", "enabled": True},
                    {"name": "bash-shell", "enabled": False},
                    {"name": "nv overlay"},
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            ["feature bgp", "feature nv overlay", "no feature bash-shell"],
        )

    def test_nxos_features_gathered(self):
        """Test state gathered, with spaces and special characters in the names."""

        result = self._run({"state": "gathered"}, have=RUNNING, changed=False)
        self.assertEqual(result["gathered"], RUNNING_CONFIG)

    def test_nxos_features_gathered_empty(self):
        """Test state gathered on a device without feature lines."""

        result = self._run({"state": "gathered"}, have="", changed=False)
        self.assertEqual(result["gathered"], [])

    def test_nxos_features_parsed(self):
        """Test state parsed, also with other lines in the running configuration."""

        set_module_args(
            {
                "running_config": "hostname sw1\n"
                + RUNNING
                + "interface Ethernet1/1\n  no shutdown\n",
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], RUNNING_CONFIG)
