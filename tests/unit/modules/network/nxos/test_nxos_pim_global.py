# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for the nxos_pim_global Ansible module.

This module tests the behavior of nxos_pim_global including:
- Merged, replaced, overridden and deleted state
- Idempotency of each state
- Rendered, gathered and parsed state
- The special cases of the NX-OS configuration: the SSM range that is one line with a hidden default,
  the group list that is stored for a static RP without one, and the bidir keyword.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_pim_global

from .nxos_module import TestNxosModule, set_module_args


RUNNING = dedent(
    """\
    ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
    ip pim rp-address 192.0.2.3 prefix-list PL_RP3
    ip pim rp-address 192.0.2.4 route-map RM_RP4
    ip pim ssm range 232.0.0.0/8 239.255.250.0/24
    ip pim log-neighbor-changes
    ip pim register-rate-limit 100
    ip pim flush-routes
    ip pim bfd
    ip pim anycast-rp 192.0.2.10 192.0.2.11
    ip pim anycast-rp 192.0.2.10 192.0.2.12
    """,
)

RUNNING_CONFIG = {
    "bfd": True,
    "log_neighbor_changes": True,
    "flush_routes": True,
    "register_rate_limit": 100,
    "ssm_range": ["232.0.0.0/8", "239.255.250.0/24"],
    "rp_addresses": [
        {"rp_address": "192.0.2.1", "group_list": "239.255.0.0/16"},
        {"rp_address": "192.0.2.2", "group_list": "239.254.0.0/16", "bidir": True},
        {"rp_address": "192.0.2.3", "prefix_list": "PL_RP3"},
        {"rp_address": "192.0.2.4", "route_map": "RM_RP4"},
    ],
    "anycast_rps": [{"anycast_rp": "192.0.2.10", "members": ["192.0.2.11", "192.0.2.12"]}],
}


class TestNxosPimGlobalModule(TestNxosModule):
    """Unit tests for the nxos_pim_global."""

    module = nxos_pim_global

    def setUp(self):
        """Set up test fixtures before each test method."""

        super().setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base."
            "resource_module_base.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.pim_global."
            "pim_global.Pim_globalFacts.get_pim_global_data",
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

    def test_nxos_pim_global_merged_empty(self):
        """Test state merged on a device without global PIM configuration."""

        result = self._run(
            {
                "config": RUNNING_CONFIG,
                "state": "merged",
            },
        )
        self.assertEqual(
            result["commands"],
            [
                "ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16",
                "ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir",
                "ip pim rp-address 192.0.2.3 prefix-list PL_RP3",
                "ip pim rp-address 192.0.2.4 route-map RM_RP4",
                "ip pim anycast-rp 192.0.2.10 192.0.2.11",
                "ip pim anycast-rp 192.0.2.10 192.0.2.12",
                "ip pim bfd",
                "ip pim log-neighbor-changes",
                "ip pim flush-routes",
                "ip pim register-rate-limit 100",
                "ip pim ssm range 232.0.0.0/8 239.255.250.0/24",
            ],
        )

    def test_nxos_pim_global_merged_idempotent(self):
        """Test idempotency of state merged."""

        self._run({"config": RUNNING_CONFIG, "state": "merged"}, have=RUNNING, changed=False)

    def test_nxos_pim_global_merged_keeps_existing(self):
        """Test that state merged adds to the existing configuration and removes nothing."""

        result = self._run(
            {
                "config": {
                    "rp_addresses": [{"rp_address": "192.0.2.1", "group_list": "239.253.0.0/16"}],
                    "anycast_rps": [{"anycast_rp": "192.0.2.10", "members": ["192.0.2.13"]}],
                },
                "state": "merged",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "ip pim rp-address 192.0.2.1 group-list 239.253.0.0/16",
                "ip pim anycast-rp 192.0.2.10 192.0.2.13",
            ],
        )

    def test_nxos_pim_global_merged_rp_without_group_list(self):
        """Test that a static RP without a group list is the RP of all groups."""

        have = "ip pim rp-address 192.0.2.5 group-list 224.0.0.0/4\n"
        config = {"rp_addresses": [{"rp_address": "192.0.2.5"}]}
        self._run({"config": config, "state": "merged"}, have=have, changed=False)
        result = self._run({"config": config, "state": "merged"})
        self.assertEqual(result["commands"], ["ip pim rp-address 192.0.2.5 group-list 224.0.0.0/4"])

    def test_nxos_pim_global_merged_bidir_change(self):
        """Test that a changed bidir keyword replaces the line."""

        have = "ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16\n"
        result = self._run(
            {
                "config": {
                    "rp_addresses": [
                        {"rp_address": "192.0.2.1", "group_list": "239.255.0.0/16", "bidir": True},
                    ],
                },
                "state": "merged",
            },
            have=have,
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16",
                "ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16 bidir",
            ],
        )

    def test_nxos_pim_global_merged_ssm_range_replaces_default(self):
        """Test that a range replaces the hidden default as NX-OS does."""

        result = self._run({"config": {"ssm_range": ["239.255.250.0/24"]}, "state": "merged"})
        self.assertEqual(result["commands"], ["ip pim ssm range 239.255.250.0/24"])

    def test_nxos_pim_global_merged_ssm_range_extends(self):
        """Test that state merged extends the configured SSM range."""

        have = "ip pim ssm range 239.255.250.0/24\n"
        result = self._run(
            {"config": {"ssm_range": ["239.255.251.0/24", "239.255.250.0/24"]}, "state": "merged"},
            have=have,
        )
        self.assertEqual(
            result["commands"],
            ["ip pim ssm range 239.255.250.0/24 239.255.251.0/24"],
        )

    def test_nxos_pim_global_merged_ssm_range_order_is_not_a_change(self):
        """Test that the order of the SSM ranges is not a change."""

        have = "ip pim ssm range 239.255.250.0/24 232.0.0.0/8\n"
        self._run(
            {"config": {"ssm_range": ["232.0.0.0/8", "239.255.250.0/24"]}, "state": "merged"},
            have=have,
            changed=False,
        )

    def test_nxos_pim_global_merged_ssm_range_none(self):
        """Test the keyword none, which replaces all ranges."""

        have = "ip pim ssm range 239.255.250.0/24\n"
        result = self._run({"config": {"ssm_range": ["none"]}, "state": "merged"}, have=have)
        self.assertEqual(result["commands"], ["ip pim ssm range none"])
        self._run(
            {"config": {"ssm_range": ["none"]}, "state": "merged"},
            have="ip pim ssm range none\n",
            changed=False,
        )

    def test_nxos_pim_global_merged_ssm_range_from_none(self):
        """Test that a range replaces the keyword none."""

        result = self._run(
            {"config": {"ssm_range": ["239.255.250.0/24"]}, "state": "merged"},
            have="ip pim ssm range none\n",
        )
        self.assertEqual(result["commands"], ["ip pim ssm range 239.255.250.0/24"])

    def test_nxos_pim_global_merged_flag_false(self):
        """Test that a flag that is false is removed in every state and not sent when absent."""

        result = self._run(
            {"config": {"log_neighbor_changes": False, "bfd": False}, "state": "merged"},
            have="ip pim log-neighbor-changes\n",
        )
        self.assertEqual(result["commands"], ["no ip pim log-neighbor-changes"])
        self._run(
            {"config": {"log_neighbor_changes": False}, "state": "merged"},
            have="",
            changed=False,
        )

    def test_nxos_pim_global_merged_register_rate_limit(self):
        """Test a change of the register rate limit."""

        result = self._run(
            {"config": {"register_rate_limit": 200}, "state": "merged"},
            have="ip pim register-rate-limit 100\n",
        )
        self.assertEqual(result["commands"], ["ip pim register-rate-limit 200"])

    # replaced and overridden

    def test_nxos_pim_global_replaced(self):
        """Test state replaced removes what is not given."""

        result = self._run(
            {
                "config": {
                    "rp_addresses": [
                        {"rp_address": "192.0.2.1", "group_list": "239.255.0.0/16"},
                        {"rp_address": "192.0.2.5", "group_list": "239.253.0.0/16"},
                    ],
                    "anycast_rps": [{"anycast_rp": "192.0.2.10", "members": ["192.0.2.11"]}],
                    "register_rate_limit": 100,
                },
                "state": "replaced",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir",
                "no ip pim rp-address 192.0.2.3 prefix-list PL_RP3",
                "no ip pim rp-address 192.0.2.4 route-map RM_RP4",
                "no ip pim anycast-rp 192.0.2.10 192.0.2.12",
                "no ip pim bfd",
                "no ip pim log-neighbor-changes",
                "no ip pim flush-routes",
                "no ip pim ssm range 232.0.0.0/8",
                "ip pim rp-address 192.0.2.5 group-list 239.253.0.0/16",
            ],
        )

    def test_nxos_pim_global_replaced_idempotent(self):
        """Test idempotency of state replaced."""

        self._run({"config": RUNNING_CONFIG, "state": "replaced"}, have=RUNNING, changed=False)

    def test_nxos_pim_global_overridden(self):
        """Test state overridden, which behaves as replaced for the global configuration."""

        result = self._run(
            {
                "config": {"ssm_range": ["232.0.0.0/8", "239.255.250.0/24"]},
                "state": "overridden",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16",
                "no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir",
                "no ip pim rp-address 192.0.2.3 prefix-list PL_RP3",
                "no ip pim rp-address 192.0.2.4 route-map RM_RP4",
                "no ip pim anycast-rp 192.0.2.10 192.0.2.11",
                "no ip pim anycast-rp 192.0.2.10 192.0.2.12",
                "no ip pim bfd",
                "no ip pim log-neighbor-changes",
                "no ip pim flush-routes",
                "no ip pim register-rate-limit",
            ],
        )

    def test_nxos_pim_global_replaced_ssm_range_to_default(self):
        """Test that the default range resets the line."""

        result = self._run(
            {"config": {"ssm_range": ["232.0.0.0/8"]}, "state": "replaced"},
            have="ip pim ssm range 239.255.250.0/24\n",
        )
        self.assertEqual(result["commands"], ["no ip pim ssm range 239.255.250.0/24"])
        self._run(
            {"config": {"ssm_range": ["232.0.0.0/8"]}, "state": "replaced"},
            have="",
            changed=False,
        )

    def test_nxos_pim_global_replaced_ssm_range_from_none(self):
        """Test that the keyword none is removed to get the default."""

        result = self._run(
            {"config": {"bfd": True, "ssm_range": ["232.0.0.0/8"]}, "state": "replaced"},
            have="ip pim ssm range none\nip pim bfd\n",
        )
        self.assertEqual(result["commands"], ["no ip pim ssm range none"])

    def test_nxos_pim_global_replaced_ssm_range_not_given(self):
        """Test that a SSM range that is not given is removed."""

        result = self._run(
            {"config": {"bfd": True}, "state": "replaced"},
            have="ip pim bfd\nip pim ssm range 239.255.250.0/24\n",
        )
        self.assertEqual(result["commands"], ["no ip pim ssm range 239.255.250.0/24"])

    # deleted

    def test_nxos_pim_global_deleted_all(self):
        """Test state deleted without config."""

        result = self._run({"state": "deleted"}, have=RUNNING)
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "no ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16",
                    "no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir",
                    "no ip pim rp-address 192.0.2.3 prefix-list PL_RP3",
                    "no ip pim rp-address 192.0.2.4 route-map RM_RP4",
                    "no ip pim anycast-rp 192.0.2.10 192.0.2.11",
                    "no ip pim anycast-rp 192.0.2.10 192.0.2.12",
                    "no ip pim bfd",
                    "no ip pim log-neighbor-changes",
                    "no ip pim flush-routes",
                    "no ip pim register-rate-limit",
                    "no ip pim ssm range 232.0.0.0/8",
                ],
            ),
        )

    def test_nxos_pim_global_deleted_idempotent(self):
        """Test idempotency of state deleted."""

        self._run({"state": "deleted"}, have="", changed=False)

    def test_nxos_pim_global_deleted_listed(self):
        """Test that state deleted removes only what is listed."""

        result = self._run(
            {
                "config": {
                    "rp_addresses": [{"rp_address": "192.0.2.3", "prefix_list": "PL_RP3"}],
                    "anycast_rps": [{"anycast_rp": "192.0.2.10", "members": ["192.0.2.12"]}],
                    "bfd": True,
                    "register_rate_limit": 100,
                    "ssm_range": ["239.255.250.0/24"],
                },
                "state": "deleted",
            },
            have=RUNNING,
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip pim rp-address 192.0.2.3 prefix-list PL_RP3",
                "no ip pim anycast-rp 192.0.2.10 192.0.2.12",
                "no ip pim bfd",
                "no ip pim register-rate-limit",
                "no ip pim ssm range 232.0.0.0/8",
            ],
        )

    def test_nxos_pim_global_deleted_listed_not_present(self):
        """Test that state deleted does nothing for configuration that is not on the device."""

        self._run(
            {
                "config": {
                    "rp_addresses": [{"rp_address": "192.0.2.99", "group_list": "239.1.0.0/16"}],
                },
                "state": "deleted",
            },
            have=RUNNING,
            changed=False,
        )

    # rendered, gathered and parsed

    def test_nxos_pim_global_rendered(self):
        """Test state rendered."""

        set_module_args(
            {
                "config": {
                    "bfd": True,
                    "rp_addresses": [{"rp_address": "192.0.2.1"}],
                    "ssm_range": ["none"],
                },
                "state": "rendered",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "ip pim rp-address 192.0.2.1 group-list 224.0.0.0/4",
                "ip pim bfd",
                "ip pim ssm range none",
            ],
        )

    def test_nxos_pim_global_gathered(self):
        """Test state gathered."""

        self.get_config.return_value = RUNNING
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], RUNNING_CONFIG)

    def test_nxos_pim_global_gathered_empty(self):
        """Test state gathered without PIM configuration."""

        self.get_config.return_value = ""
        set_module_args({"state": "gathered"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})

    def test_nxos_pim_global_parsed(self):
        """Test state parsed."""

        set_module_args({"running_config": RUNNING, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], RUNNING_CONFIG)

    def test_nxos_pim_global_parsed_ssm_none_and_whitespace(self):
        """Test parsing of the keyword none, of an RP for all groups and of trailing whitespace."""

        running = (
            "ip pim ssm range none  \n"
            "ip pim rp-address 192.0.2.5 group-list 224.0.0.0/4   \n"
            "ip pim anycast-rp 192.0.2.10 192.0.2.11\t\n"
            "ip pim sparse-mode\n"
        )
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "ssm_range": ["none"],
                "rp_addresses": [{"rp_address": "192.0.2.5", "group_list": "224.0.0.0/4"}],
                "anycast_rps": [{"anycast_rp": "192.0.2.10", "members": ["192.0.2.11"]}],
            },
        )

    # validation

    def test_nxos_pim_global_rp_group_sources_are_exclusive(self):
        """Test that the group list, prefix list and route map are mutually exclusive."""

        set_module_args(
            {
                "config": {
                    "rp_addresses": [
                        {
                            "rp_address": "192.0.2.1",
                            "group_list": "239.1.0.0/16",
                            "prefix_list": "PL",
                        },
                    ],
                },
                "state": "merged",
            },
        )
        result = self.execute_module(failed=True)
        self.assertIn("mutually exclusive", result["msg"])
