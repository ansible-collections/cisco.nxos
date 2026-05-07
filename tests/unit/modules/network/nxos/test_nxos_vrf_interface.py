from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfInterfaceModule(TestNxosModule):
    module = nxos_vrf_interface

    def setUp(self):
        super(TestNxosVrfInterfaceModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

        self.mock_normalize_interface = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrf_interface.normalize_interface",
        )
        self.normalize_interface = self.mock_normalize_interface.start()
        self.normalize_interface.return_value = "Ethernet1/1"

    def tearDown(self):
        super(TestNxosVrfInterfaceModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_get_interface_type.stop()
        self.mock_normalize_interface.stop()

    def _setup_no_vrf(self):
        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show vrf all" in cmd:
                return [{"TABLE_vrf": {"ROW_vrf": [{"vrf_name": "ntc"}]}}]
            elif "show interface" in cmd:
                return [
                    {
                        "TABLE_interface": {
                            "ROW_interface": {"interface": "Ethernet1/1", "eth_mode": "layer3"}
                        }
                    }
                ]
            elif "show run interface" in cmd:
                return ["interface Ethernet1/1\n"]
            return [""]

        self.run_commands.side_effect = side_effect

    def _setup_with_vrf(self):
        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show vrf all" in cmd:
                return [{"TABLE_vrf": {"ROW_vrf": [{"vrf_name": "ntc"}]}}]
            elif "show interface" in cmd:
                return [
                    {
                        "TABLE_interface": {
                            "ROW_interface": {"interface": "Ethernet1/1", "eth_mode": "layer3"}
                        }
                    }
                ]
            elif "show run interface" in cmd:
                return ["interface Ethernet1/1\n  vrf member ntc\n"]
            return [""]

        self.run_commands.side_effect = side_effect

    def test_nxos_vrf_interface_present(self):
        self._setup_no_vrf()
        set_module_args(dict(vrf="ntc", interface="Ethernet1/1", state="present"))
        result = self.execute_module(changed=True)
        self.assertIn("vrf member ntc", result["commands"])

    def test_nxos_vrf_interface_present_already_set(self):
        self._setup_with_vrf()
        set_module_args(dict(vrf="ntc", interface="Ethernet1/1", state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_vrf_interface_absent(self):
        self._setup_with_vrf()
        set_module_args(dict(vrf="ntc", interface="Ethernet1/1", state="absent"))
        result = self.execute_module(changed=True)
        self.assertIn("no vrf member ntc", result["commands"])
