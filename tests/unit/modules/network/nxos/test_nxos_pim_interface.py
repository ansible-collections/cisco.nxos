# Generated with AI assistance: Claude Code (Anthropic)
# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_pim_interface

from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosIPInterfaceModule(TestNxosModule):
    module = nxos_pim_interface

    def setUp(self):
        super(TestNxosIPInterfaceModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestNxosIPInterfaceModule, self).tearDown()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None, device=""):
        module_name = self.module.__name__.rsplit(".", 1)[1]

        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for command in commands:
                if isinstance(command, dict):
                    command = command["command"]
                filename = str(command).split(" | ", 1)[0].replace(" ", "_").replace("/", "_")
                output.append(load_fixture(module_name, filename))
            return output

        self.get_config.return_value = load_fixture(module_name, "config.cfg")
        self.load_config.return_value = None
        self.run_commands.side_effect = load_from_file

    def test_nxos_pim_interface_present(self):
        set_module_args(
            dict(
                interface="eth2/1",
                dr_prio=10,
                hello_interval=40,
                sparse=True,
                border=False,
            ),
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface eth2/1",
                "ip pim dr-priority 10",
                "ip pim hello-interval 40000",
                "ip pim sparse-mode",
            ],
        )

    def test_nxos_pim_interface_jp(self):
        set_module_args(
            dict(
                interface="eth2/1",
                jp_policy_in="JPIN",
                jp_policy_out="JPOUT",
                jp_type_in="routemap",
                jp_type_out="routemap",
            ),
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface eth2/1",
                "ip pim jp-policy JPOUT out",
                "ip pim jp-policy JPIN in",
            ],
        )

    def test_nxos_pim_interface_default(self):
        set_module_args(dict(interface="eth2/1", state="default"))
        self.execute_module(changed=False, commands=[])

    def test_nxos_pim_interface_ip_absent(self):
        set_module_args(dict(interface="eth2/1", state="absent"))
        self.execute_module(changed=False, commands=[])


class TestNxosPimInterfaceBfdModule(TestNxosModule):
    module = nxos_pim_interface

    def setUp(self):
        super(TestNxosPimInterfaceBfdModule, self).setUp()

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestNxosPimInterfaceBfdModule, self).tearDown()
        self.mock_get_interface_mode.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_bfd_1(self):
        # default (None) -> enable
        self.get_config.return_value = None
        set_module_args(dict(interface="eth2/1", bfd="enable"))
        self.execute_module(changed=True, commands=["interface eth2/1", "ip pim bfd-instance"])

        # default (None) -> disable
        set_module_args(dict(interface="eth2/1", bfd="disable"))
        self.execute_module(
            changed=True,
            commands=["interface eth2/1", "ip pim bfd-instance disable"],
        )

        # default (None) -> default (None) (idempotence)
        set_module_args(dict(interface="eth2/1", bfd="default"))
        self.execute_module(changed=False)

        # default (None) -> interface state 'default'
        set_module_args(dict(interface="Ethernet9/3", state="default"))
        self.execute_module(changed=False)

        # default (None) -> interface state 'absent'
        set_module_args(dict(interface="Ethernet9/3", state="absent"))
        self.execute_module(changed=False)

    def test_bfd_2(self):
        # From disable
        self.get_config.return_value = """
            interface Ethernet9/2
              ip pim bfd-instance disable
        """
        # disable -> enable
        set_module_args(dict(interface="Ethernet9/2", bfd="enable"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/2", "ip pim bfd-instance"],
        )

        # disable -> disable (idempotence)
        set_module_args(dict(interface="Ethernet9/2", bfd="disable"))
        self.execute_module(changed=False)

        # disable -> default (None)
        set_module_args(dict(interface="Ethernet9/2", bfd="default"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/2", "no ip pim bfd-instance"],
        )
        # disable -> interface state 'default'
        set_module_args(dict(interface="Ethernet9/3", state="default"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "no ip pim bfd-instance"],
        )

        # disable -> interface state 'absent'
        set_module_args(dict(interface="Ethernet9/3", state="absent"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "no ip pim bfd-instance"],
        )

    def test_bfd_3(self):
        # From enable
        self.get_config.return_value = """
            interface Ethernet9/2
              ip pim bfd-instance
        """
        # enable -> disabled
        set_module_args(dict(interface="Ethernet9/3", bfd="disable"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "ip pim bfd-instance disable"],
        )

        # enable -> enable (idempotence)
        set_module_args(dict(interface="Ethernet9/3", bfd="enable"))
        self.execute_module(changed=False)

        # enable -> default (None)
        set_module_args(dict(interface="Ethernet9/3", bfd="default"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "no ip pim bfd-instance"],
        )

        # enable -> interface state 'default'
        set_module_args(dict(interface="Ethernet9/3", state="default"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "no ip pim bfd-instance"],
        )

        # enable -> interface state 'absent'
        set_module_args(dict(interface="Ethernet9/3", state="absent"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/3", "no ip pim bfd-instance"],
        )

    def test_bfd_4(self):
        self.get_config.return_value = """
            interface Ethernet9/2
              ip pim hello-interval 1000
        """
        # update hello-interval (as milliseconds)
        set_module_args(
            dict(
                interface="Ethernet9/2",
                hello_interval=1,
                hello_interval_ms=True,
            ),
        )
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/2", "ip pim hello-interval 1"],
        )

        # idempotent (as milliseconds)
        set_module_args(
            dict(
                interface="Ethernet9/2",
                hello_interval=1000,
                hello_interval_ms=True,
            ),
        )
        self.execute_module(changed=False, commands=[])

        # update hello-interval (default seconds)
        set_module_args(dict(interface="Ethernet9/2", hello_interval=2))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet9/2", "ip pim hello-interval 2000"],
        )

        # idempotent (default seconds)
        set_module_args(dict(interface="Ethernet9/2", hello_interval=1))
        self.execute_module(changed=False, commands=[])


class TestNxosPimInterfaceValidationModule(TestNxosModule):
    module = nxos_pim_interface

    def setUp(self):
        super(TestNxosPimInterfaceValidationModule, self).setUp()

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestNxosPimInterfaceValidationModule, self).tearDown()
        self.mock_get_interface_mode.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_layer2_interface_rejected(self):
        self.get_interface_mode.return_value = "layer2"
        self.get_config.return_value = None
        set_module_args(dict(interface="Ethernet1/1", sparse=True))
        result = self.execute_module(failed=True)
        self.assertIn("Layer 3", result["msg"])

    def test_jp_policy_in_without_type_fails(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                jp_policy_in="TESTPOLICY",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertIn("jp_type_in", result["msg"])

    def test_jp_policy_out_without_type_fails(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                jp_policy_out="TESTPOLICY",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertIn("jp_type_out", result["msg"])

    def test_neighbor_policy_without_type_fails(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                neighbor_policy="NBPOLICY",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertIn("neighbor_type", result["msg"])

    def test_neighbor_policy_prefix(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                neighbor_policy="NBPOLICY",
                neighbor_type="prefix",
            ),
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface Ethernet1/1",
                "ip pim neighbor-policy prefix-list NBPOLICY",
            ],
        )

    def test_neighbor_policy_routemap(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                neighbor_policy="NBPOLICY",
                neighbor_type="routemap",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("ip pim neighbor-policy NBPOLICY", result["commands"])

    def test_jp_policy_prefix_type(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                jp_policy_in="JPIN",
                jp_type_in="prefix",
                jp_policy_out="JPOUT",
                jp_type_out="prefix",
            ),
        )
        self.execute_module(
            changed=True,
            commands=[
                "interface Ethernet1/1",
                "ip pim jp-policy prefix-list JPOUT out",
                "ip pim jp-policy prefix-list JPIN in",
            ],
        )

    def test_sparse_mode_present(self):
        self.get_config.return_value = None
        set_module_args(dict(interface="Ethernet1/1", sparse=True))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "ip pim sparse-mode"],
        )

    def test_border_enable(self):
        self.get_config.return_value = None
        set_module_args(dict(interface="Ethernet1/1", border=True))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "ip pim border"],
        )

    def test_dr_prio_change(self):
        self.get_config.return_value = None
        set_module_args(dict(interface="Ethernet1/1", dr_prio="50"))
        self.execute_module(
            changed=True,
            commands=["interface Ethernet1/1", "ip pim dr-priority 50"],
        )

    def test_check_mode(self):
        self.get_config.return_value = None
        set_module_args(
            dict(
                interface="Ethernet1/1",
                sparse=True,
                _ansible_check_mode=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertTrue(result["changed"])
        self.load_config.assert_not_called()


class TestNxosPimInterfaceExistingConfig(TestNxosModule):
    module = nxos_pim_interface

    def setUp(self):
        super(TestNxosPimInterfaceExistingConfig, self).setUp()

        self.mock_get_interface_mode = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_interface_mode",
        )
        self.get_interface_mode = self.mock_get_interface_mode.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_pim_interface.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestNxosPimInterfaceExistingConfig, self).tearDown()
        self.mock_get_interface_mode.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_default_with_existing_neighbor_policy(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim neighbor-policy prefix-list NBPOL
              ip pim sparse-mode
              ip pim dr-priority 5
        """
        set_module_args(dict(interface="Ethernet1/1", state="default"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip pim neighbor-policy", result["commands"])

    def test_default_with_existing_jp_prefix_out(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim jp-policy prefix-list JPOUT out
        """
        set_module_args(dict(interface="Ethernet1/1", state="default"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip pim jp-policy prefix-list JPOUT out", result["commands"])

    def test_default_with_existing_jp_routemap_in(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim jp-policy JPIN in
        """
        set_module_args(dict(interface="Ethernet1/1", state="default"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip pim jp-policy JPIN in", result["commands"])

    def test_absent_with_existing_sparse_and_border(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim sparse-mode
              ip pim border
        """
        set_module_args(dict(interface="Ethernet1/1", state="absent"))
        result = self.execute_module(changed=True)
        self.assertIn("no ip pim border", result["commands"])
        self.assertIn("no ip pim sparse-mode", result["commands"])

    def test_jp_bidir_replace(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim jp-policy BIDIR
        """
        set_module_args(
            dict(
                interface="Ethernet1/1",
                jp_policy_in="NEWIN",
                jp_type_in="routemap",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("no ip pim jp-policy BIDIR", result["commands"])
        self.assertIn("ip pim jp-policy NEWIN in", result["commands"])

    def test_existing_neighbor_policy_routemap_change_policy_name(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim neighbor-policy NBPOL
        """
        set_module_args(
            dict(
                interface="Ethernet1/1",
                neighbor_policy="NEWNBPOL",
                neighbor_type="routemap",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("ip pim neighbor-policy NEWNBPOL", result["commands"])

    def test_hello_auth_key_removal(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim hello-authentication ah-md5 existingkey
        """
        set_module_args(
            dict(
                interface="Ethernet1/1",
                sparse=True,
            ),
        )
        result = self.execute_module(changed=True)
        self.assertIn("ip pim sparse-mode", result["commands"])

    def test_sparse_removal_goes_last(self):
        self.get_config.return_value = """
            interface Ethernet1/1
              ip pim sparse-mode
              ip pim dr-priority 5
              ip pim border
        """
        set_module_args(dict(interface="Ethernet1/1", state="absent"))
        result = self.execute_module(changed=True)
        cmds = result["commands"]
        sparse_idx = None
        for i, c in enumerate(cmds):
            if c == "no ip pim sparse-mode":
                sparse_idx = i
        if sparse_idx is not None:
            self.assertEqual(sparse_idx, len(cmds) - 1)


class TestPimInterfaceHelpers(TestNxosModule):
    module = nxos_pim_interface

    def setUp(self):
        super(TestPimInterfaceHelpers, self).setUp()

    def tearDown(self):
        super(TestPimInterfaceHelpers, self).tearDown()

    def load_fixtures(self, commands=None, device=""):
        pass

    def test_get_pim_interface_defaults(self):
        defaults = nxos_pim_interface.get_pim_interface_defaults()
        self.assertEqual(defaults["dr_prio"], "1")
        self.assertEqual(defaults["hello_interval"], "30000")
        self.assertFalse(defaults["sparse"])
        self.assertFalse(defaults["border"])
        self.assertEqual(defaults["bfd"], "default")

    def test_flatten_list_mixed(self):
        result = nxos_pim_interface.flatten_list([["a", "b"], "c", ["d"]])
        self.assertEqual(result, ["a", "b", "c", "d"])

    def test_flatten_list_empty(self):
        result = nxos_pim_interface.flatten_list([])
        self.assertEqual(result, [])

    def test_local_existing_with_jp_bidir_and_isauth(self):
        existing = {
            "jp_bidir": True,
            "isauth": True,
            "sparse": True,
            "dr_prio": "1",
        }
        result, jp_bidir, isauth = nxos_pim_interface.local_existing(existing)
        self.assertTrue(jp_bidir)
        self.assertTrue(isauth)
        self.assertNotIn("jp_bidir", result)
        self.assertNotIn("isauth", result)

    def test_local_existing_without_jp_bidir(self):
        existing = {"sparse": True, "dr_prio": "1"}
        result, jp_bidir, isauth = nxos_pim_interface.local_existing(existing)
        self.assertFalse(jp_bidir)
        self.assertFalse(isauth)

    def test_local_existing_none(self):
        result, jp_bidir, isauth = nxos_pim_interface.local_existing(None)
        self.assertFalse(jp_bidir)
        self.assertFalse(isauth)

    def test_fix_delta_removes_defaults_when_existing_is_none(self):
        delta = {"dr_prio": "1", "hello_interval": "30000", "sparse": False, "border": False}
        existing = {}
        result = nxos_pim_interface.fix_delta(delta, existing)
        self.assertEqual(result, {})

    def test_fix_delta_keeps_non_default_values(self):
        delta = {"dr_prio": "10", "hello_interval": "5000"}
        existing = {}
        result = nxos_pim_interface.fix_delta(delta, existing)
        self.assertEqual(result, {"dr_prio": "10", "hello_interval": "5000"})

    def test_config_pim_interface_with_hello_auth_key(self):
        delta = {"hello_auth_key": "mysecret"}
        existing = {}
        commands = nxos_pim_interface.config_pim_interface(delta, existing, False, False)
        self.assertIn("ip pim hello-authentication ah-md5 mysecret", commands)

    def test_config_pim_interface_remove_hello_auth_key(self):
        delta = {"hello_auth_key": False}
        existing = {}
        commands = nxos_pim_interface.config_pim_interface(delta, existing, False, True)
        self.assertIn("no ip pim hello-authentication ah-md5", commands)

    def test_config_pim_interface_bfd_enable(self):
        delta = {"bfd": "enable"}
        existing = {"bfd": "default"}
        commands = nxos_pim_interface.config_pim_interface(delta, existing, False, False)
        self.assertIn("ip pim bfd-instance", commands)

    def test_config_pim_interface_bfd_disable(self):
        delta = {"bfd": "disable"}
        existing = {"bfd": "default"}
        commands = nxos_pim_interface.config_pim_interface(delta, existing, False, False)
        self.assertIn("ip pim bfd-instance disable", commands)

    def test_config_pim_interface_bfd_none(self):
        delta = {"bfd": None}
        existing = {"bfd": "enable"}
        commands = nxos_pim_interface.config_pim_interface(delta, existing, False, False)
        self.assertEqual(commands, [])

    def test_default_pim_interface_policies_jp_bidir(self):
        existing = {
            "jp_policy_in": "BIDIR",
            "jp_policy_out": "BIDIR",
            "jp_type_in": "prefix",
            "jp_type_out": "prefix",
        }
        commands = nxos_pim_interface.default_pim_interface_policies(existing, True)
        self.assertIn("no ip pim jp-policy prefix-list BIDIR", commands)

    def test_default_pim_interface_policies_no_bidir_prefix(self):
        existing = {
            "jp_policy_in": "JPIN",
            "jp_policy_out": "JPOUT",
            "jp_type_in": "prefix",
            "jp_type_out": "prefix",
        }
        commands = nxos_pim_interface.default_pim_interface_policies(existing, False)
        self.assertIn("no ip pim jp-policy prefix-list JPIN in", commands)
        self.assertIn("no ip pim jp-policy prefix-list JPOUT out", commands)

    def test_default_pim_interface_policies_no_bidir_routemap(self):
        existing = {
            "jp_policy_in": "JPIN",
            "jp_policy_out": "JPOUT",
            "jp_type_in": "routemap",
            "jp_type_out": "routemap",
        }
        commands = nxos_pim_interface.default_pim_interface_policies(existing, False)
        self.assertIn("no ip pim jp-policy JPIN in", commands)
        self.assertIn("no ip pim jp-policy JPOUT out", commands)

    def test_default_pim_interface_policies_with_neighbor_policy(self):
        existing = {
            "neighbor_policy": "NBPOL",
        }
        commands = nxos_pim_interface.default_pim_interface_policies(existing, False)
        self.assertIn("no ip pim neighbor-policy", commands)

    def test_normalize_proposed_values_hello_interval_seconds(self):
        from unittest.mock import MagicMock

        module = MagicMock()
        module.params = {"hello_interval_ms": False}
        proposed = {"hello_interval": 30}
        nxos_pim_interface.normalize_proposed_values(proposed, module)
        self.assertEqual(proposed["hello_interval"], "30000")

    def test_normalize_proposed_values_hello_interval_ms(self):
        from unittest.mock import MagicMock

        module = MagicMock()
        module.params = {"hello_interval_ms": True}
        proposed = {"hello_interval": 5000}
        nxos_pim_interface.normalize_proposed_values(proposed, module)
        self.assertEqual(proposed["hello_interval"], "5000")

    def test_normalize_proposed_values_bfd(self):
        from unittest.mock import MagicMock

        module = MagicMock()
        module.params = {}
        proposed = {"bfd": "ENABLE"}
        nxos_pim_interface.normalize_proposed_values(proposed, module)
        self.assertEqual(proposed["bfd"], "enable")
