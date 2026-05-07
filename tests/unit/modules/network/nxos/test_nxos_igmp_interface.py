from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp_interface

from .nxos_module import TestNxosModule, set_module_args


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
        self.load_config.return_value = None

        self.mock_get_interface_type = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_igmp_interface.get_interface_type",
        )
        self.get_interface_type = self.mock_get_interface_type.start()
        self.get_interface_type.return_value = "ethernet"

    def tearDown(self):
        super(TestNxosIgmpInterfaceModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_interface_type.stop()

    def _setup_json_data(self, version="2"):
        json_body = {
            "TABLE_vrf": {
                "ROW_vrf": {
                    "TABLE_if": {
                        "ROW_if": {
                            "if-name": "Ethernet1/1",
                            "if-status": "up",
                            "IGMPVersion": version,
                            "ConfiguredQueryInterval": "125",
                            "ConfiguredQueryMaxResponseTime": "10",
                            "StartupQueryInterval": "31",
                            "StartupQueryCount": "2",
                            "LastMemberMTR": "1",
                            "LastMemberQueryCount": "2",
                            "ConfiguredGroupTimeout": "260",
                            "ConfiguredRobustnessVariable": "2",
                            "ReportingForLinkLocal": "disabled",
                            "ImmediateLeave": "disabled",
                        },
                    },
                },
            },
        }
        text_body = ""
        intf_mode = {
            "TABLE_interface": {
                "ROW_interface": {"interface": "Ethernet1/1", "eth_mode": "layer3"},
            },
        }

        def side_effect(module, cmds):
            cmd = cmds[0] if isinstance(cmds, list) else cmds
            if isinstance(cmd, dict):
                cmd_str = cmd.get("command", "")
                output = cmd.get("output", "text")
            else:
                cmd_str = str(cmd)
                output = "text"

            if "show ip igmp interface" in cmd_str:
                if output == "json" or "json" in cmd_str:
                    return [json_body]
                return [text_body]
            elif "show interface" in cmd_str:
                return [intf_mode]
            return [""]

        self.run_commands.side_effect = side_effect

    def test_nxos_igmp_interface_version_change(self):
        self._setup_json_data(version="2")
        set_module_args(dict(interface="Ethernet1/1", version="3", state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_igmp_interface_idempotent(self):
        self._setup_json_data(version="2")
        set_module_args(dict(interface="Ethernet1/1", version="2", state="present"))
        result = self.execute_module(changed=False)
