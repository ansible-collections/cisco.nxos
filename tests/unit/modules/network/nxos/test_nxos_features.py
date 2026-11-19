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

# Features that are enabled by default are in the all view, but not in the plain running configuration.
DEFAULT_ON = {"ssh"}

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

        self.mock_get_plain = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.features."
            "features.Features.get_plain_features",
        )
        self.get_plain = self.mock_get_plain.start()

    def tearDown(self):
        """Clean up after each test method."""

        super().tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()
        self.mock_get_plain.stop()

    def _run(self, args, have="", changed=True, plain=None):
        """
        Run the module with the given arguments against the given running configuration.

        have is the output of the all view. The plain running configuration is the same without
        the features that are enabled by default, unless plain is given.
        """

        self.get_config.return_value = have
        if plain is None:
            plain = "".join(
                line + "\n"
                for line in have.splitlines()
                if line.startswith("feature ") and line.split(" ", 1)[1] not in DEFAULT_ON
            )
        self.get_plain.return_value = plain
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
            ["feature lacp", "feature bfd", "no feature bgp", "no feature interface-vlan"],
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

    # errors and empty configuration

    def _fails(self, args):
        """Run the module with the given arguments and return the failure."""

        self.get_config.return_value = ""
        set_module_args(args)
        return self.execute_module(failed=True)

    def test_nxos_features_config_required(self):
        """Test that the states that change or render features need a configuration."""

        for state in ("merged", "replaced", "overridden", "rendered"):
            with self.subTest(state=state):
                result = self._fails({"state": state})
                self.assertIn("state is {0} but all of the following".format(state), result["msg"])
                self.assertIn("config", result["msg"])

    def test_nxos_features_empty_config_list(self):
        """Test that an empty list of features is rejected by the states that need features."""

        for state in ("merged", "replaced", "overridden", "rendered"):
            with self.subTest(state=state):
                result = self._fails({"config": [], "state": state})
                self.assertEqual(
                    result["msg"],
                    "value of config parameter must not be empty for state {0}".format(state),
                )

    def test_nxos_features_deleted_empty_config_list(self):
        """Test that state deleted with an empty list disables every enabled feature."""

        result = self._run(
            {"config": [], "state": "deleted"},
            have="feature bgp\nno feature nxapi\nfeature lacp\n",
        )
        self.assertEqual(result["commands"], ["no feature bgp", "no feature lacp"])

    def test_nxos_features_parsed_requires_running_config(self):
        """Test that state parsed fails without a running configuration."""

        result = self._fails({"state": "parsed"})
        self.assertIn("running_config", result["msg"])

        result = self._fails({"running_config": "", "state": "parsed"})
        self.assertEqual(
            result["msg"],
            "value of running_config parameter must not be empty for state parsed",
        )

    def test_nxos_features_parsed_without_feature_lines(self):
        """Test that state parsed returns nothing for text without feature lines."""

        result = self._run(
            {
                "running_config": "hostname sw1\ninterface Ethernet1/1\n  no shutdown\n",
                "state": "parsed",
            },
            changed=False,
        )
        self.assertEqual(result["parsed"], [])
        self.assertNotIn("commands", result)

    def test_nxos_features_config_and_running_config_are_exclusive(self):
        """Test that config and running_config cannot be given together."""

        result = self._fails(
            {
                "config": [{"name": "bgp"}],
                "running_config": "feature bgp",
                "state": "parsed",
            },
        )
        self.assertIn("mutually exclusive", result["msg"])

    def test_nxos_features_name_is_required(self):
        """Test that a feature without a name is rejected."""

        result = self._fails({"config": [{"enabled": True}], "state": "merged"})
        self.assertIn("name", result["msg"])

    def test_nxos_features_unknown_option(self):
        """Test that an unknown option of a feature is rejected."""

        result = self._fails(
            {"config": [{"name": "bgp", "state": "enabled"}], "state": "merged"},
        )
        self.assertIn("Unsupported parameters", result["msg"])

    def test_nxos_features_enabled_must_be_boolean(self):
        """Test that a value for enabled that is not a boolean is rejected."""

        result = self._fails(
            {"config": [{"name": "bgp", "enabled": "sometimes"}], "state": "merged"},
        )
        self.assertIn("boolean", result["msg"])

    def test_nxos_features_state_must_be_known(self):
        """Test that an unknown state is rejected."""

        result = self._fails({"config": [{"name": "bgp"}], "state": "present"})
        self.assertIn("value of state must be one of", result["msg"])

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
        self.assertEqual(result["commands"], ["no feature interface-vlan", "no feature bgp"])

    def test_nxos_features_deleted_all(self):
        """Test that state deleted without config disables the features with a feature line."""

        result = self._run({"state": "deleted"}, have=RUNNING)
        self.assertEqual(
            result["commands"],
            [
                "no feature bgp",
                "no feature interface-vlan",
                "no feature nv overlay",
                "no feature password encryption aes",
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

    # features that are enabled by default, and the order of the disables

    def test_nxos_features_overridden_leaves_default_features_alone(self):
        """Test that state overridden does not disable ssh, it has no feature line."""

        result = self._run(
            {"config": [{"name": "bgp", "enabled": True}], "state": "overridden"},
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "no feature interface-vlan",
                "no feature nv overlay",
                "no feature password encryption aes",
                "no feature tacacs+",
                "no feature vn-segment-vlan-based",
            ],
        )
        self.assertNotIn("no feature ssh", result["commands"])

    def test_nxos_features_overridden_default_features_idempotent(self):
        """Test that the features with a feature line, listed without ssh, change nothing."""

        config = [item for item in RUNNING_CONFIG if item["name"] != "ssh"]
        self._run({"config": config, "state": "overridden"}, have=RUNNING, changed=False)

    def test_nxos_features_overridden_disables_default_feature_with_a_line(self):
        """Test that a feature with a feature line is disabled, also if ssh is its name."""

        result = self._run(
            {"config": [{"name": "bgp", "enabled": True}], "state": "overridden"},
            have="feature ssh\nfeature bgp\n",
            plain="feature ssh\nfeature bgp\n",
        )
        self.assertEqual(result["commands"], ["no feature ssh"])

    def test_nxos_features_overridden_listed_default_feature_is_disabled(self):
        """Test that a listed feature that is enabled by default is disabled when asked."""

        result = self._run(
            {"config": [{"name": "ssh", "enabled": False}], "state": "overridden"},
            have="feature ssh\n",
            plain="",
        )
        self.assertEqual(result["commands"], ["no feature ssh"])

    def test_nxos_features_merged_listed_default_feature_is_disabled(self):
        """Test that state merged disables a feature that is enabled by default when asked."""

        result = self._run(
            {"config": [{"name": "ssh", "enabled": False}], "state": "merged"},
            have=RUNNING,
        )
        self.assertEqual(result["commands"], ["no feature ssh"])

    def test_nxos_features_deleted_listed_default_feature_is_disabled(self):
        """Test that state deleted with config disables a listed feature that is on by default."""

        result = self._run(
            {"config": [{"name": "ssh"}], "state": "deleted"},
            have=RUNNING,
        )
        self.assertEqual(result["commands"], ["no feature ssh"])

    def test_nxos_features_deleted_all_only_default_features_changes_nothing(self):
        """Test that state deleted without config does nothing when only default features are on."""

        self._run({"state": "deleted"}, have="feature ssh\nno feature nxapi\n", changed=False)

    def test_nxos_features_plain_config_is_only_read_when_needed(self):
        """Test that the plain running configuration is read for overridden and deleted without config."""

        self._run({"config": RUNNING_CONFIG, "state": "merged"}, have=RUNNING, changed=False)
        self._run({"config": RUNNING_CONFIG, "state": "replaced"}, have=RUNNING, changed=False)
        self._run(
            {"config": [{"name": "bgp"}], "state": "deleted"},
            have=RUNNING,
        )
        self.get_plain.assert_not_called()
        self._run({"state": "deleted"}, have=RUNNING)
        self.assertEqual(self.get_plain.call_count, 1)
        self._run({"config": RUNNING_CONFIG, "state": "overridden"}, have=RUNNING, changed=False)
        self.assertEqual(self.get_plain.call_count, 2)

    def test_nxos_features_disables_in_reverse_order_of_the_config(self):
        """Test that the disables come in the reverse order of the config, for dependencies."""

        config = [
            {"name": "nv overlay", "enabled": False},
            {"name": "vn-segment-vlan-based", "enabled": False},
            {"name": "interface-vlan", "enabled": False},
        ]
        for state in ("merged", "replaced"):
            result = self._run({"config": config, "state": state}, have=RUNNING)
            self.assertEqual(
                result["commands"],
                [
                    "no feature interface-vlan",
                    "no feature vn-segment-vlan-based",
                    "no feature nv overlay",
                ],
            )

    def test_nxos_features_overridden_listed_disables_before_the_unlisted_ones(self):
        """Test that overridden disables the listed features in reverse order, then the others."""

        result = self._run(
            {
                "config": [
                    {"name": "nv overlay", "enabled": False},
                    {"name": "vn-segment-vlan-based", "enabled": False},
                    {"name": "bgp", "enabled": True},
                ],
                "state": "overridden",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "no feature vn-segment-vlan-based",
                "no feature nv overlay",
                "no feature interface-vlan",
                "no feature password encryption aes",
                "no feature tacacs+",
            ],
        )

    def test_nxos_features_deleted_listed_in_reverse_order(self):
        """Test that state deleted with config disables the features in the reverse order."""

        result = self._run(
            {
                "config": [{"name": "nv overlay"}, {"name": "vn-segment-vlan-based"}],
                "state": "deleted",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            ["no feature vn-segment-vlan-based", "no feature nv overlay"],
        )

    def test_nxos_features_rendered_disables_in_reverse_order(self):
        """Test that state rendered puts the no feature lines in the reverse order."""

        set_module_args(
            {
                "config": [
                    {"name": "nv overlay", "enabled": False},
                    {"name": "vn-segment-vlan-based", "enabled": False},
                ],
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            ["no feature vn-segment-vlan-based", "no feature nv overlay"],
        )

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
