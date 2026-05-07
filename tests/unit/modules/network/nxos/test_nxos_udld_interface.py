from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_udld_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosUdldInterfaceModule(TestNxosModule):
    module = nxos_udld_interface

    def setUp(self):
        super(TestNxosUdldInterfaceModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_udld_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosUdldInterfaceModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()

    def test_nxos_udld_interface_aggressive(self):
        self.run_commands.return_value = ["udld enable"]
        set_module_args(dict(interface="Ethernet1/1", mode="aggressive", state="present"))
        result = self.execute_module(changed=True)

    def test_nxos_udld_interface_no_change(self):
        self.run_commands.return_value = ["udld aggressive"]
        set_module_args(dict(interface="Ethernet1/1", mode="aggressive", state="present"))
        result = self.execute_module(changed=False)

    def test_nxos_udld_interface_disabled(self):
        self.run_commands.return_value = ["udld aggressive"]
        set_module_args(dict(interface="Ethernet1/1", mode="disabled", state="present"))
        result = self.execute_module(changed=True)
