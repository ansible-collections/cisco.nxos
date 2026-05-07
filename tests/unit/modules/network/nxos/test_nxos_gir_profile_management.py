from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_gir_profile_management

from .nxos_module import TestNxosModule, set_module_args


class TestNxosGirProfileManagementModule(TestNxosModule):
    module = nxos_gir_profile_management

    def setUp(self):
        super(TestNxosGirProfileManagementModule, self).setUp()
        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir_profile_management.get_config",
        )
        self.get_config = self.mock_get_config.start()
        self.get_config.return_value = ""

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_gir_profile_management.load_config",
        )
        self.load_config = self.mock_load_config.start()
        self.load_config.return_value = None

    def tearDown(self):
        super(TestNxosGirProfileManagementModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()

    def test_nxos_gir_profile_present_maintenance(self):
        set_module_args(
            dict(mode="maintenance", commands=["router eigrp 11", "isolate"], state="present"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_gir_profile_present_normal(self):
        set_module_args(
            dict(mode="normal", commands=["router eigrp 11", "isolate"], state="present"),
        )
        result = self.execute_module(changed=True)

    def test_nxos_gir_profile_absent_no_existing(self):
        set_module_args(dict(mode="maintenance", state="absent"))
        result = self.execute_module(changed=False)

    def test_nxos_gir_profile_absent_with_existing(self):
        self.get_config.return_value = (
            "configure maintenance profile maintenance-mode\n"
            "  router eigrp 11\n"
            "  isolate\n"
        )
        set_module_args(dict(mode="maintenance", state="absent"))
        result = self.execute_module(changed=True)

    def test_nxos_gir_profile_absent_with_commands_fails(self):
        set_module_args(
            dict(mode="maintenance", commands=["router eigrp 11"], state="absent"),
        )
        result = self.execute_module(failed=True)

    def test_nxos_gir_profile_idempotent(self):
        self.get_config.return_value = (
            "configure maintenance profile maintenance-mode\n"
            "  router eigrp 11\n"
            "  isolate\n"
        )
        set_module_args(
            dict(mode="maintenance", commands=["router eigrp 11", "isolate"], state="present"),
        )
        result = self.execute_module(changed=False)

    def test_nxos_gir_profile_check_mode(self):
        set_module_args(
            dict(
                mode="maintenance",
                commands=["router eigrp 11", "isolate"],
                state="present",
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.load_config.assert_not_called()
