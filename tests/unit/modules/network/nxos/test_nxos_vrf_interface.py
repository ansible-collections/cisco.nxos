#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Tests generated with AI assistance (Claude)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfInterfaceModule(TestNxosModule):
    module = nxos_vrf_interface

    def setUp(self):
        super(TestNxosVrfInterfaceModule, self).setUp()
        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_normalize_interface = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.normalize_interface",
        )
        self.normalize_interface = self.mock_normalize_interface.start()
        self.normalize_interface.side_effect = lambda x: x

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_get_vrf_list = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_vrf_list",
        )
        self.get_vrf_list = self.mock_get_vrf_list.start()

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()

        self.mock_get_interface_info = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_info",
        )
        self.get_interface_info = self.mock_get_interface_info.start()

    def tearDown(self):
        super(TestNxosVrfInterfaceModule, self).tearDown()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_normalize_interface.stop()
        self.mock_get_interface_type.stop()
        self.mock_get_vrf_list.stop()
        self.mock_get_interface_mode.stop()
        self.mock_get_interface_info.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    # ------------------------------------------------------------------ #
    #  Integration tests exercising main() via execute_module             #
    # ------------------------------------------------------------------ #

    def test_nxos_vrf_interface_no_change(self):
        self.get_vrf_list.return_value = ["default", "management"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "management"
        set_module_args(
            dict(
                vrf="management",
                interface="Ethernet1/1",
                state="present",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])

    def test_vrf_interface_present_vrf_changed(self):
        """When the interface already has a different VRF, switch to the new one."""
        self.get_vrf_list.return_value = ["management", "ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "management"
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="present"),
        )
        result = self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "vrf member ntc"],
            sort=False,
        )
        self.load_config.assert_called_once()

    def test_vrf_interface_present_no_existing_vrf(self):
        """When no VRF is assigned to the interface, assign the requested one."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = ""
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="present"),
        )
        result = self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "vrf member ntc"],
            sort=False,
        )

    def test_vrf_interface_absent_vrf_matches(self):
        """Remove the VRF when existing VRF matches the requested VRF."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "ntc"
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="absent"),
        )
        result = self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "no vrf member ntc"],
            sort=False,
        )
        self.load_config.assert_called_once()

    def test_vrf_interface_absent_vrf_mismatch_fail(self):
        """Fail when trying to remove a VRF that differs from what is configured."""
        self.get_vrf_list.return_value = ["ntc", "other"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "other"
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="absent"),
        )
        result = self.execute_module(failed=True)
        self.assertIn("does not exist on that interface", result["msg"])

    def test_vrf_interface_absent_no_existing_vrf(self):
        """No change when state=absent and interface has no VRF assigned."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = ""
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="absent"),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_vrf_interface_vrf_not_in_current_vrfs_warning(self):
        """A warning is emitted when the VRF is not in the device VRF list."""
        self.get_vrf_list.return_value = ["default"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = ""
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="present"),
        )
        with patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.emit_warnings",
        ):
            result = self.execute_module(
                changed=True,
                commands=["interface Ethernet1/1", "vrf member ntc"],
                sort=False,
            )
            self.assertIn(
                "The VRF is not present/active on the device. Use nxos_vrf to fix this.",
                result["warnings"],
            )

    def test_vrf_interface_layer2_fail(self):
        """Fail when the interface is in Layer 2 mode."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer2"
        set_module_args(
            dict(vrf="ntc", interface="Ethernet1/1", state="present"),
        )
        result = self.execute_module(failed=True)
        self.assertIn("Layer 3 port", result["msg"])

    def test_vrf_interface_dne_interface_fail(self):
        """Fail when a non-ethernet interface does not exist (cliconf)."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_type.return_value = "loopback"
        set_module_args(
            dict(vrf="ntc", interface="loopback10", state="present"),
        )
        with patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.is_default",
            return_value="DNE",
        ):
            result = self.execute_module(failed=True)
        self.assertIn("interface does not exist", result["msg"])

    def test_vrf_interface_check_mode_present(self):
        """Check mode returns commands without applying configuration."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = ""
        set_module_args(
            dict(
                vrf="ntc",
                interface="Ethernet1/1",
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/1", "vrf member ntc"],
        )
        self.load_config.assert_not_called()

    def test_vrf_interface_check_mode_absent(self):
        """Check mode for state=absent returns commands without applying."""
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = "ntc"
        set_module_args(
            dict(
                vrf="ntc",
                interface="Ethernet1/1",
                state="absent",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/1", "no vrf member ntc"],
        )
        self.load_config.assert_not_called()

    def test_vrf_interface_nxapi_skips_dne_check(self):
        """Non-ethernet interface with nxapi does not trigger DNE check."""
        self.get_capabilities.return_value = {"network_api": "nxapi"}
        self.get_vrf_list.return_value = ["ntc"]
        self.get_interface_type.return_value = "loopback"
        self.get_interface_mode.return_value = "layer3"
        self.get_interface_info.return_value = ""
        set_module_args(
            dict(vrf="ntc", interface="loopback10", state="present"),
        )
        result = self.execute_module(
            changed=True,
            commands=["interface loopback10", "vrf member ntc"],
            sort=False,
        )

    # ------------------------------------------------------------------ #
    #  Direct helper function tests                                       #
    #                                                                     #
    #  The setUp patches shadow the module-level functions.  Each helper  #
    #  test temporarily stops the relevant mock so the real function runs #
    #  with a patched run_commands underneath.                            #
    # ------------------------------------------------------------------ #

    def test_get_interface_mode_ethernet_layer3(self):
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {"TABLE_interface": {"ROW_interface": {"eth_mode": "layer3"}}},
                ]
                mode = nxos_vrf_interface.get_interface_mode(
                    "Ethernet1/1",
                    "ethernet",
                    None,
                )
                self.assertEqual(mode, "layer3")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_ethernet_layer2_access(self):
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {"TABLE_interface": {"ROW_interface": {"eth_mode": "access"}}},
                ]
                mode = nxos_vrf_interface.get_interface_mode(
                    "Ethernet1/1",
                    "ethernet",
                    None,
                )
                self.assertEqual(mode, "layer2")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_ethernet_layer2_trunk(self):
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {"TABLE_interface": {"ROW_interface": {"eth_mode": "trunk"}}},
                ]
                mode = nxos_vrf_interface.get_interface_mode(
                    "Ethernet1/1",
                    "ethernet",
                    None,
                )
                self.assertEqual(mode, "layer2")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_ethernet_no_eth_mode_defaults_layer3(self):
        """When eth_mode key is absent but dict is non-empty, defaults to 'layer3'."""
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {"TABLE_interface": {"ROW_interface": {"admin_state": "up"}}},
                ]
                mode = nxos_vrf_interface.get_interface_mode(
                    "Ethernet1/1",
                    "ethernet",
                    None,
                )
                self.assertEqual(mode, "layer3")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_ethernet_key_error(self):
        """Returns 'unknown' when body lacks expected keys."""
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [{}]
                mode = nxos_vrf_interface.get_interface_mode(
                    "Ethernet1/1",
                    "ethernet",
                    None,
                )
                self.assertEqual(mode, "unknown")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_loopback(self):
        self.mock_get_interface_mode.stop()
        try:
            mode = nxos_vrf_interface.get_interface_mode(
                "loopback0",
                "loopback",
                None,
            )
            self.assertEqual(mode, "layer3")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_svi(self):
        self.mock_get_interface_mode.stop()
        try:
            mode = nxos_vrf_interface.get_interface_mode(
                "Vlan10",
                "svi",
                None,
            )
            self.assertEqual(mode, "layer3")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_interface_mode_portchannel(self):
        self.mock_get_interface_mode.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {"TABLE_interface": {"ROW_interface": {"eth_mode": "layer3"}}},
                ]
                mode = nxos_vrf_interface.get_interface_mode(
                    "port-channel1",
                    "portchannel",
                    None,
                )
                self.assertEqual(mode, "layer3")
        finally:
            self.get_interface_mode = self.mock_get_interface_mode.start()

    def test_get_vrf_list_success(self):
        self.mock_get_vrf_list.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    {
                        "TABLE_vrf": {
                            "ROW_vrf": [
                                {"vrf_name": "default"},
                                {"vrf_name": "management"},
                            ],
                        },
                    },
                ]
                result = nxos_vrf_interface.get_vrf_list(None)
                self.assertEqual(result, ["default", "management"])
        finally:
            self.get_vrf_list = self.mock_get_vrf_list.start()

    def test_get_vrf_list_empty(self):
        """Returns empty list when body has no TABLE_vrf key."""
        self.mock_get_vrf_list.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [{}]
                result = nxos_vrf_interface.get_vrf_list(None)
                self.assertEqual(result, [])
        finally:
            self.get_vrf_list = self.mock_get_vrf_list.start()

    def test_get_interface_info_with_vrf(self):
        self.mock_get_interface_info.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    "interface Ethernet1/1\n  vrf member ntc\n  ip address 10.0.0.1/24",
                ]
                result = nxos_vrf_interface.get_interface_info("Ethernet1/1", None)
                self.assertEqual(result, "ntc")
        finally:
            self.get_interface_info = self.mock_get_interface_info.start()

    def test_get_interface_info_no_vrf(self):
        """Returns empty string when no vrf member line is present."""
        self.mock_get_interface_info.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    "interface Ethernet1/1\n  ip address 10.0.0.1/24",
                ]
                result = nxos_vrf_interface.get_interface_info("Ethernet1/1", None)
                self.assertEqual(result, "")
        finally:
            self.get_interface_info = self.mock_get_interface_info.start()

    def test_get_interface_info_loopback_prefix(self):
        """Loopback interfaces are not capitalized."""
        self.mock_get_interface_info.stop()
        try:
            with patch(
                "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
            ) as mock_run:
                mock_run.return_value = [
                    "interface loopback0\n  vrf member ntc",
                ]
                result = nxos_vrf_interface.get_interface_info("loopback0", None)
                self.assertEqual(result, "ntc")
                cmd_arg = mock_run.call_args[0][1][0]["command"]
                self.assertIn("loopback0", cmd_arg)
        finally:
            self.get_interface_info = self.mock_get_interface_info.start()

    def test_is_default_true(self):
        """Returns True when interface config has only the interface line."""
        with patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
        ) as mock_run:
            mock_run.return_value = ["interface Ethernet1/1"]
            result = nxos_vrf_interface.is_default("Ethernet1/1", None)
            self.assertTrue(result)

    def test_is_default_false(self):
        """Returns False when interface has additional configuration."""
        with patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
        ) as mock_run:
            mock_run.return_value = [
                "interface Ethernet1/1\n  ip address 10.0.0.1/24",
            ]
            result = nxos_vrf_interface.is_default("Ethernet1/1", None)
            self.assertFalse(result)

    def test_is_default_dne(self):
        """Returns 'DNE' when run_commands raises IndexError."""
        with patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
        ) as mock_run:
            mock_run.return_value = []
            result = nxos_vrf_interface.is_default("Ethernet1/1", None)
            self.assertEqual(result, "DNE")
