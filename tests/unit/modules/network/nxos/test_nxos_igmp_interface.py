#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# AI-generated unit tests for nxos_igmp_interface module.
# Generated to increase coverage from 54.34% by testing state transitions,
# oif_ps/oif_routemap handling, config helpers, error paths, and check mode.
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp_interface
from ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface import (
    apply_key_map,
    config_default_igmp_interface,
    config_igmp_interface,
    config_remove_oif,
    flatten_list,
    get_igmp_interface,
    get_interface_mode,
)

from .nxos_module import TestNxosModule, set_module_args


def _default_existing():
    """Return a baseline existing IGMP interface config dict."""
    return {
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

    # ------------------------------------------------------------------
    # No-change baseline
    # ------------------------------------------------------------------

    def test_nxos_igmp_interface_no_change(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="2",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["updates"], [])

    # ------------------------------------------------------------------
    # state=present with changes
    # ------------------------------------------------------------------

    def test_present_version_change(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(interface="Ethernet1/1", version="3", state="present"),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp version 3", result["updates"])
        self.load_config.assert_called_once()

    def test_present_startup_query_interval_change(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                startup_query_interval="60",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp startup-query-interval 60", result["updates"])

    def test_present_report_llg_true(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(interface="Ethernet1/1", report_llg=True, state="present"),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp report-link-local-groups", result["updates"])

    def test_present_immediate_leave_true(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(interface="Ethernet1/1", immediate_leave=True, state="present"),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp immediate-leave", result["updates"])

    def test_present_multiple_params_change(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="3",
                robustness="5",
                query_mrt="20",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        updates = result["updates"]
        self.assertIn("ip igmp version 3", updates)
        self.assertIn("ip igmp robustness-variable 5", updates)
        self.assertIn("ip igmp query-max-response-time 20", updates)

    # ------------------------------------------------------------------
    # oif_ps handling
    # ------------------------------------------------------------------

    def test_present_oif_ps_add_new_prefix(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_ps=[{"prefix": "238.2.2.6"}],
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp static-oif 238.2.2.6", result["updates"])

    def test_present_oif_ps_add_prefix_with_source(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_ps=[{"prefix": "238.2.2.5", "source": "192.168.0.1"}],
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn(
            "ip igmp static-oif 238.2.2.5 source 192.168.0.1 ",
            result["updates"],
        )

    def test_present_oif_ps_remove_stale_entries(self):
        existing = _default_existing()
        existing["oif_prefix_source"] = [{"prefix": "238.1.1.1"}]
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_ps=[{"prefix": "238.2.2.6"}],
                state="present",
            ),
        )
        result = self.changed(changed=True)
        updates = result["updates"]
        self.assertIn("ip igmp static-oif 238.2.2.6", updates)
        self.assertIn("no ip igmp static-oif 238.1.1.1", updates)

    def test_present_oif_ps_default_removes_all(self):
        existing = _default_existing()
        existing["oif_prefix_source"] = [{"prefix": "238.1.1.1"}]
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_ps="default",
                state="present",
            ),
        )
        # oif_ps='default' sets delta["oif_ps"] = [] and then
        # config_igmp_interface removes all existing prefix/source entries
        result = self.changed(changed=True)
        self.assertIn("no ip igmp static-oif 238.1.1.1", result["updates"])

    # ------------------------------------------------------------------
    # oif_routemap handling
    # ------------------------------------------------------------------

    def test_present_oif_routemap_set(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_routemap="MY_RMAP",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn(
            "ip igmp static-oif route-map MY_RMAP",
            result["updates"],
        )

    def test_present_oif_routemap_default_removes(self):
        existing = _default_existing()
        existing["oif_routemap"] = "OLD_MAP"
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_routemap="default",
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn(
            "no ip igmp static-oif route-map OLD_MAP",
            result["updates"],
        )

    # ------------------------------------------------------------------
    # state=default
    # ------------------------------------------------------------------

    def test_state_default_resets_params(self):
        existing = _default_existing()
        existing["version"] = "3"
        existing["robustness"] = "5"
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(interface="Ethernet1/1", state="default"),
        )
        result = self.changed(changed=True)
        updates = result["updates"]
        self.assertIn("ip igmp version 2", updates)
        self.assertIn("ip igmp robustness-variable 2", updates)

    def test_state_default_no_change_when_already_default(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(interface="Ethernet1/1", state="default"),
        )
        result = self.changed(changed=False)
        self.assertEqual(result["updates"], [])

    # ------------------------------------------------------------------
    # state=absent
    # ------------------------------------------------------------------

    def test_state_absent_removes_oif_routemap(self):
        existing = _default_existing()
        existing["oif_routemap"] = "SOME_MAP"
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(interface="Ethernet1/1", state="absent"),
        )
        result = self.changed(changed=True)
        self.assertIn(
            "no ip igmp static-oif route-map SOME_MAP",
            result["updates"],
        )

    def test_state_absent_removes_oif_prefix_source(self):
        existing = _default_existing()
        existing["oif_prefix_source"] = [
            {"prefix": "238.2.2.6"},
            {"prefix": "238.2.2.5", "source": "192.168.0.1"},
        ]
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(interface="Ethernet1/1", state="absent"),
        )
        result = self.changed(changed=True)
        updates = result["updates"]
        self.assertIn("no ip igmp static-oif 238.2.2.6", updates)
        self.assertIn(
            "no ip igmp static-oif 238.2.2.5 source 192.168.0.1 ",
            updates,
        )

    # ------------------------------------------------------------------
    # Error cases
    # ------------------------------------------------------------------

    def test_layer2_interface_rejected(self):
        self.get_interface_mode.return_value = "layer2"
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(interface="Ethernet1/1", version="3", state="present"),
        )
        result = self.failed()
        self.assertIn("Layer 3", result["msg"])

    def test_pim_not_enabled_no_version(self):
        existing = _default_existing()
        existing["version"] = ""
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(interface="Ethernet1/1", version="3", state="present"),
        )
        result = self.failed()
        self.assertIn("pim", result["msg"].lower())

    def test_oif_routemap_with_existing_prefix_conflict(self):
        existing = _default_existing()
        existing["oif_prefix_source"] = [{"prefix": "238.2.2.6"}]
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_routemap="MY_RMAP",
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("route", result["msg"].lower())

    def test_oif_ps_with_existing_routemap_conflict(self):
        existing = _default_existing()
        existing["oif_routemap"] = "EXISTING_MAP"
        self.get_igmp_interface.return_value = existing
        set_module_args(
            dict(
                interface="Ethernet1/1",
                oif_ps=[{"prefix": "238.2.2.6"}],
                state="present",
            ),
        )
        result = self.failed()
        self.assertIn("route-map", result["msg"].lower())

    def test_state_absent_with_cannot_absent_params(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="3",
                state="absent",
            ),
        )
        result = self.failed()
        self.assertIn("oif_ps", result["msg"])

    # ------------------------------------------------------------------
    # Check mode
    # ------------------------------------------------------------------

    def test_check_mode_returns_commands_without_load(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="3",
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp version 3", result["commands"])
        self.load_config.assert_not_called()

    # ------------------------------------------------------------------
    # Direct helper: config_igmp_interface()
    # ------------------------------------------------------------------

    def test_config_igmp_interface_version(self):
        delta = {"version": "3"}
        existing = _default_existing()
        cmds = config_igmp_interface(delta, existing, [])
        self.assertIn("ip igmp version 3", cmds)

    def test_config_igmp_interface_report_llg_false(self):
        delta = {"report_llg": False}
        existing = _default_existing()
        existing["report_llg"] = True
        cmds = config_igmp_interface(delta, existing, [])
        self.assertTrue(
            any("no" in c and "report-link-local-groups" in c for c in cmds),
        )

    def test_config_igmp_interface_immediate_leave_false(self):
        delta = {"immediate_leave": False}
        existing = _default_existing()
        existing["immediate_leave"] = True
        cmds = config_igmp_interface(delta, existing, [])
        self.assertTrue(
            any("no" in c and "immediate-leave" in c for c in cmds),
        )

    def test_config_igmp_interface_default_value_no_change(self):
        """When value is 'default' and existing already matches default, no command."""
        delta = {"version": "default"}
        existing = _default_existing()  # version is already "2" which is the default
        cmds = config_igmp_interface(delta, existing, [])
        self.assertEqual(cmds, [])

    def test_config_igmp_interface_default_value_with_change(self):
        """When value is 'default' but existing differs, emit reset command."""
        delta = {"version": "default"}
        existing = _default_existing()
        existing["version"] = "3"
        cmds = config_igmp_interface(delta, existing, [])
        self.assertIn("ip igmp version 2", cmds)

    def test_config_igmp_interface_oif_routemap_default_with_existing(self):
        delta = {"oif_routemap": "default"}
        existing = _default_existing()
        existing["oif_routemap"] = "OLD_MAP"
        cmds = config_igmp_interface(delta, existing, [])
        self.assertIn("no ip igmp static-oif route-map OLD_MAP", cmds)

    def test_config_igmp_interface_oif_routemap_default_without_existing(self):
        delta = {"oif_routemap": "default"}
        existing = _default_existing()
        cmds = config_igmp_interface(delta, existing, [])
        self.assertEqual(cmds, [])

    def test_config_igmp_interface_oif_ps_new_and_stale(self):
        delta = {"oif_ps": [{"prefix": "238.2.2.6"}]}
        existing = _default_existing()
        existing_oif = [{"prefix": "238.1.1.1"}]
        cmds = config_igmp_interface(delta, existing, existing_oif)
        self.assertIn("ip igmp static-oif 238.2.2.6", cmds)
        self.assertIn("no ip igmp static-oif 238.1.1.1", cmds)

    def test_config_igmp_interface_oif_ps_stale_with_source(self):
        delta = {"oif_ps": [{"prefix": "238.2.2.6"}]}
        existing = _default_existing()
        existing_oif = [{"prefix": "238.1.1.1", "source": "10.0.0.1"}]
        cmds = config_igmp_interface(delta, existing, existing_oif)
        self.assertIn("ip igmp static-oif 238.2.2.6", cmds)
        self.assertIn(
            "no ip igmp static-oif 238.1.1.1 source 10.0.0.1 ",
            cmds,
        )

    def test_config_igmp_interface_oif_ps_no_stale_when_matching(self):
        """Existing prefix/source already in proposed: no remove, no add."""
        entry = {"prefix": "238.2.2.6"}
        delta = {"oif_ps": [entry]}
        existing = _default_existing()
        existing_oif = [{"prefix": "238.2.2.6"}]
        cmds = config_igmp_interface(delta, existing, existing_oif)
        # No add (already present), no remove (still wanted)
        oif_cmds = [c for c in cmds if "static-oif" in c]
        self.assertEqual(oif_cmds, [])

    # ------------------------------------------------------------------
    # Direct helper: config_remove_oif()
    # ------------------------------------------------------------------

    def test_config_remove_oif_routemap(self):
        existing = {"oif_routemap": "MY_MAP"}
        cmds = config_remove_oif(existing, [])
        self.assertEqual(cmds, ["no ip igmp static-oif route-map MY_MAP"])

    def test_config_remove_oif_prefix_source_entries(self):
        existing = {"oif_routemap": None}
        oif_ps = [
            {"prefix": "238.2.2.6"},
            {"prefix": "238.2.2.5", "source": "192.168.0.1"},
        ]
        cmds = config_remove_oif(existing, oif_ps)
        self.assertIn("no ip igmp static-oif 238.2.2.6", cmds)
        self.assertIn(
            "no ip igmp static-oif 238.2.2.5 source 192.168.0.1 ",
            cmds,
        )

    def test_config_remove_oif_empty(self):
        existing = {"oif_routemap": None}
        cmds = config_remove_oif(existing, [])
        self.assertEqual(cmds, [])

    # ------------------------------------------------------------------
    # Direct helper: config_default_igmp_interface()
    # ------------------------------------------------------------------

    def test_config_default_igmp_interface_with_diff(self):
        # The function does set(proposed.items()).difference(existing.items())
        # so existing must not contain unhashable values like lists.
        # In the real module flow, oif_prefix_source is popped before this
        # function is called.
        existing = _default_existing()
        existing.pop("oif_prefix_source", None)
        existing.pop("oif_routemap", None)
        existing["version"] = "3"
        existing["robustness"] = "7"
        cmds = config_default_igmp_interface(existing, {})
        self.assertIn("ip igmp version 2", cmds)
        self.assertIn("ip igmp robustness-variable 2", cmds)

    def test_config_default_igmp_interface_no_diff(self):
        existing = _default_existing()
        existing.pop("oif_prefix_source", None)
        existing.pop("oif_routemap", None)
        cmds = config_default_igmp_interface(existing, {})
        self.assertEqual(cmds, [])

    # ------------------------------------------------------------------
    # Direct helpers: flatten_list() and apply_key_map()
    # ------------------------------------------------------------------

    def test_flatten_list_with_nested(self):
        result = flatten_list([["a", "b"], "c", ["d"]])
        self.assertEqual(result, ["a", "b", "c", "d"])

    def test_flatten_list_empty(self):
        result = flatten_list([])
        self.assertEqual(result, [])

    def test_apply_key_map_none_value(self):
        key_map = {"Key": "new_key"}
        table = {"Key": None}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"new_key": None})

    # ------------------------------------------------------------------
    # Restart flag
    # ------------------------------------------------------------------

    def test_present_with_restart(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                version="3",
                restart=True,
                state="present",
            ),
        )
        result = self.changed(changed=True)
        self.assertIn("ip igmp version 3", result["updates"])
        # run_commands should have been called for the restart action
        self.run_commands.assert_called()

    def test_present_restart_only_no_config_change(self):
        self.get_igmp_interface.return_value = _default_existing()
        set_module_args(
            dict(
                interface="Ethernet1/1",
                restart=True,
                state="present",
            ),
        )
        result = self.changed(changed=False)
        self.assertEqual(result["updates"], [])
        # restart still fires via run_commands even without config change
        self.run_commands.assert_called()


def _igmp_json_body(report_llg="true", immediate_leave="disabled"):
    """Build a standard IGMP JSON response body for helper tests."""
    return {
        "TABLE_vrf": {
            "ROW_vrf": {
                "TABLE_if": {
                    "ROW_if": {
                        "IGMPVersion": "2",
                        "ConfiguredStartupQueryInterval": "31",
                        "StartupQueryCount": "2",
                        "RobustnessVariable": "2",
                        "ConfiguredQuerierTimeout": "255",
                        "ConfiguredMaxResponseTime": "10",
                        "ConfiguredQueryInterval": "125",
                        "LastMemberMTR": "1",
                        "LastMemberQueryCount": "2",
                        "ConfiguredGroupTimeout": "260",
                        "ReportingForLinkLocal": report_llg,
                        "ImmediateLeave": immediate_leave,
                    },
                },
            },
        },
    }


class TestNxosIgmpInterfaceHelpers(unittest.TestCase):
    """Tests for device-interaction helper functions in nxos_igmp_interface."""

    def setUp(self):
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()
        self.module = MagicMock()

    def tearDown(self):
        self.mock_run_commands.stop()

    # ------------------------------------------------------------------
    # get_interface_mode
    # ------------------------------------------------------------------

    def test_get_interface_mode_ethernet_layer3(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/1",
                        "eth_mode": "routed",
                    },
                },
            },
        ]
        mode = get_interface_mode("Ethernet1/1", "ethernet", self.module)
        self.assertEqual(mode, "routed")

    def test_get_interface_mode_ethernet_access_is_layer2(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/2",
                        "eth_mode": "access",
                    },
                },
            },
        ]
        mode = get_interface_mode("Ethernet1/2", "ethernet", self.module)
        self.assertEqual(mode, "layer2")

    def test_get_interface_mode_ethernet_trunk_is_layer2(self):
        self.run_commands.return_value = [
            {
                "TABLE_interface": {
                    "ROW_interface": {
                        "interface": "Ethernet1/3",
                        "eth_mode": "trunk",
                    },
                },
            },
        ]
        mode = get_interface_mode("Ethernet1/3", "ethernet", self.module)
        self.assertEqual(mode, "layer2")

    def test_get_interface_mode_loopback_is_layer3(self):
        mode = get_interface_mode("loopback0", "loopback", self.module)
        self.assertEqual(mode, "layer3")
        self.run_commands.assert_not_called()

    def test_get_interface_mode_svi_is_layer3(self):
        mode = get_interface_mode("Vlan10", "svi", self.module)
        self.assertEqual(mode, "layer3")
        self.run_commands.assert_not_called()

    def test_get_interface_mode_unknown_type(self):
        mode = get_interface_mode("mgmt0", "management", self.module)
        self.assertEqual(mode, "unknown")

    # ------------------------------------------------------------------
    # apply_key_map (IGMP-specific key map)
    # ------------------------------------------------------------------

    def test_apply_key_map_igmp_fields(self):
        key_map = {
            "IGMPVersion": "version",
            "ConfiguredStartupQueryInterval": "startup_query_interval",
            "RobustnessVariable": "robustness",
        }
        table = {
            "IGMPVersion": "2",
            "ConfiguredStartupQueryInterval": "31",
            "RobustnessVariable": "2",
            "UnmappedField": "ignored",
        }
        result = apply_key_map(key_map, table)
        self.assertEqual(
            result,
            {"version": "2", "startup_query_interval": "31", "robustness": "2"},
        )

    def test_apply_key_map_falsy_value_preserved(self):
        key_map = {"Key": "mapped"}
        table = {"Key": ""}
        result = apply_key_map(key_map, table)
        self.assertEqual(result, {"mapped": ""})

    # ------------------------------------------------------------------
    # get_igmp_interface
    # ------------------------------------------------------------------

    def test_get_igmp_interface_normal_json_report_true_leave_disabled(self):
        json_body = _igmp_json_body(report_llg="true", immediate_leave="disabled")
        self.run_commands.side_effect = [
            [json_body],
            [""],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertEqual(result["version"], "2")
        self.assertEqual(result["startup_query_interval"], "31")
        self.assertEqual(result["robustness"], "2")
        self.assertTrue(result["report_llg"])
        self.assertFalse(result["immediate_leave"])
        self.assertIsNone(result["oif_routemap"])
        self.assertEqual(result["oif_prefix_source"], [])

    def test_get_igmp_interface_report_false_leave_enabled(self):
        json_body = _igmp_json_body(report_llg="false", immediate_leave="enabled")
        self.run_commands.side_effect = [
            [json_body],
            [""],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertFalse(result["report_llg"])
        self.assertTrue(result["immediate_leave"])

    def test_get_igmp_interface_not_running_returns_empty(self):
        self.run_commands.side_effect = [
            ["IGMP is not running on this interface"],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertEqual(result, {})

    def test_get_igmp_interface_oif_routemap(self):
        json_body = _igmp_json_body()
        oif_text = "  ip igmp static-oif route-map MY_ROUTE_MAP\n"
        self.run_commands.side_effect = [
            [json_body],
            [oif_text],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertEqual(result["oif_routemap"], "MY_ROUTE_MAP")
        self.assertEqual(result["oif_prefix_source"], [])

    def test_get_igmp_interface_oif_prefix_with_source(self):
        json_body = _igmp_json_body()
        oif_text = "  ip igmp static-oif 238.2.2.5 source 192.168.0.1\n"
        self.run_commands.side_effect = [
            [json_body],
            [oif_text],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertIsNone(result["oif_routemap"])
        self.assertEqual(len(result["oif_prefix_source"]), 1)
        self.assertEqual(result["oif_prefix_source"][0]["prefix"], "238.2.2.5")
        self.assertEqual(result["oif_prefix_source"][0]["source"], "192.168.0.1")

    def test_get_igmp_interface_oif_prefix_only_no_source(self):
        json_body = _igmp_json_body()
        oif_text = "  ip igmp static-oif 238.2.2.6\n"
        self.run_commands.side_effect = [
            [json_body],
            [oif_text],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertIsNone(result["oif_routemap"])
        self.assertEqual(len(result["oif_prefix_source"]), 1)
        self.assertEqual(result["oif_prefix_source"][0]["prefix"], "238.2.2.6")
        self.assertNotIn("source", result["oif_prefix_source"][0])

    def test_get_igmp_interface_multiple_oif_entries(self):
        json_body = _igmp_json_body()
        oif_text = "  ip igmp static-oif route-map MY_MAP\n  ip igmp static-oif 238.2.2.6\n"
        self.run_commands.side_effect = [
            [json_body],
            [oif_text],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        # More than one entry: goes to oif_prefix_source, not oif_routemap
        self.assertIsNone(result["oif_routemap"])
        self.assertEqual(len(result["oif_prefix_source"]), 2)

    def test_get_igmp_interface_empty_oif_body(self):
        json_body = _igmp_json_body()
        self.run_commands.side_effect = [
            [json_body],
            [""],
        ]
        result = get_igmp_interface(self.module, "Ethernet1/1")
        self.assertIsNone(result["oif_routemap"])
        self.assertEqual(result["oif_prefix_source"], [])
