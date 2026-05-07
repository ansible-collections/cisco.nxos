from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrrp

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrrpModule(TestNxosModule):
    module = nxos_vrrp

    def setUp(self):
        super(TestNxosVrrpModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vrrp.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

    def tearDown(self):
        super(TestNxosVrrpModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_capabilities.stop()
        self.mock_get_interface_type.stop()

    def _setup_no_existing(self):
        show_interface = {
            "TABLE_interface": {
                "ROW_interface": {
                    "interface": "Ethernet1/1",
                    "eth_mode": "layer3",
                },
            },
        }

        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show interface" in cmd:
                return [show_interface]
            elif "show vrrp detail" in cmd:
                return [None]
            elif "show run" in cmd:
                return [""]
            return [{}]

        self.run_commands.side_effect = side_effect

    def _setup_with_existing(self):
        show_interface = {
            "TABLE_interface": {
                "ROW_interface": {
                    "interface": "Ethernet1/1",
                    "eth_mode": "layer3",
                },
            },
        }
        show_vrrp_detail = {
            "TABLE_vrrp_group": {
                "ROW_vrrp_group": {
                    "sh_group_id": "100",
                    "sh_vip_addr": "10.1.100.1",
                    "sh_priority": "100",
                    "sh_group_preempt": "Enable",
                    "sh_auth_text": "",
                    "sh_adv_interval": "1",
                },
            },
        }

        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd = cmd["command"]
            if "show interface" in cmd:
                return [show_interface]
            elif "show vrrp detail" in cmd:
                return [show_vrrp_detail]
            elif "show run" in cmd:
                return ["vrrp 100\n  shutdown\n"]
            return [{}]

        self.run_commands.side_effect = side_effect

    def test_nxos_vrrp_present_new(self):
        self._setup_no_existing()
        set_module_args(
            dict(interface="Ethernet1/1", group="100", vip="10.1.100.1", state="present"),
        )
        result = self.execute_module(changed=True)
        self.assertIn("interface ethernet1/1", result["commands"])
        self.assertIn("vrrp 100", result["commands"])
        self.assertIn("address 10.1.100.1", result["commands"])

    def test_nxos_vrrp_present_no_vip(self):
        self._setup_no_existing()
        set_module_args(dict(interface="Ethernet1/1", group="100", state="present"))
        result = self.execute_module(failed=True)

    def test_nxos_vrrp_absent_no_existing(self):
        self._setup_no_existing()
        set_module_args(
            dict(interface="Ethernet1/1", group="100", vip="10.1.100.1", state="absent"),
        )
        result = self.execute_module(changed=False)

    def test_nxos_vrrp_absent_with_existing(self):
        self._setup_with_existing()
        set_module_args(
            dict(interface="Ethernet1/1", group="100", vip="10.1.100.1", state="absent"),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no vrrp 100", result["commands"])
