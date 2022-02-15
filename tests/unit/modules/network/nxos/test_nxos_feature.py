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

import json

from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.plugins.modules import nxos_feature
from .nxos_module import TestNxosModule, load_fixture, set_module_args


class TestNxosFeatureModule(TestNxosModule):

    module = nxos_feature

    def setUp(self):
        super(TestNxosFeatureModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.run_commands"
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.get_capabilities"
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {"network_api": "cliconf"}

    def tearDown(self):
        super(TestNxosFeatureModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_config.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None, device=""):
        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for item in commands:
                try:
                    obj = json.loads(item["command"])
                    command = obj["command"]
                except ValueError:
                    command = item["command"]
            filename = "%s.txt" % str(command).replace(" ", "_")
            output.append(load_fixture("nxos_feature", filename))
            return output

        self.run_commands.side_effect = load_from_file
        self.get_config.return_value = ""
        self.load_config.return_value = None

    def test_nxos_feature_enable(self):
        set_module_args(dict(feature="nve", state="enabled"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"], ["terminal dont-ask", "feature nv overlay"]
        )

    def test_nxos_feature_disable(self):
        set_module_args(dict(feature="ospf", state="disabled"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"], ["terminal dont-ask", "no feature ospf"]
        )


class TestNxosFeatureModuleMDS(TestNxosModule):

    module = nxos_feature

    def setUp(self):
        super(TestNxosFeatureModuleMDS, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.run_commands"
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_feature.get_capabilities"
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {
                "network_os_platform": "DS-C9396T-K9",
                "network_os_version": "8.4(2)",
            },
            "network_api": "cliconf",
        }

    def tearDown(self):
        super(TestNxosFeatureModuleMDS, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_load_config.stop()
        self.mock_get_config.stop()
        self.mock_get_capabilities.stop()

    def load_fixtures(self, commands=None, device=""):
        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for item in commands:
                try:
                    obj = json.loads(item["command"])
                    command = obj["command"]
                except ValueError:
                    command = item["command"]
            filename = "%s_mds.txt" % str(command).replace(" ", "_")
            output.append(load_fixture("nxos_feature", filename))
            return output

        self.run_commands.side_effect = load_from_file
        self.get_config.return_value = ""
        self.load_config.return_value = None

    def test_nxos_feature_enable(self):
        set_module_args(dict(feature="fcrxbbcredit", state="enabled"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"], ["terminal dont-ask", "feature fcrxbbcredit"]
        )

    def test_nxos_feature_disable(self):
        set_module_args(dict(feature="port-track", state="disabled"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"], ["terminal dont-ask", "no feature port-track"]
        )

    def test_nxos_feature_enable_already_enabled(self):
        set_module_args(dict(feature="analytics", state="enabled"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_feature_disable_already_disabled(self):
        set_module_args(dict(feature="sftp-server", state="disabled"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
