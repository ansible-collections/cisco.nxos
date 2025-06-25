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

from ansible_collections.cisco.nxos.plugins.modules import nxos_facts
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule, load_fixture


class TestNxosFactsModule(TestNxosModule):
    module = nxos_facts

    def setUp(self):
        super(TestNxosFactsModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.legacy.base.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_capabilities = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.legacy.base.get_capabilities",
        )
        self.get_capabilities = self.mock_get_capabilities.start()
        self.get_capabilities.return_value = {
            "device_info": {
                "network_os": "nxos",
                "network_os_hostname": "nxos9k",
                "network_os_image": "bootflash:///nxos64-cs.10.3.1.F.bin",
                "network_os_model": "9WQOE7E35N3",
                "network_os_version": "10.3(1)",
            },
            "network_api": "cliconf",
        }
        self.mock_connection = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_facts.Connection",
        )
        self.connection = self.mock_connection.start()
        self.connection_instance = self.connection.return_value

    def load_fixtures(self, commands=None, device=""):
        def load_from_file(*args, **kwargs):
            module, commands = args
            output = list()

            for command in commands:
                if isinstance(command, dict):
                    command = command["command"]
                filename = str(command).split(" | ", 1)[0].replace(" ", "_")
                output.append(load_fixture("nxos_facts", filename))
            return output

        self.run_commands.side_effect = load_from_file

    def tearDown(self):
        super(TestNxosFactsModule, self).tearDown()
        self.mock_run_commands.stop()
        self.mock_get_capabilities.stop()

    def test_nxos_facts_interface(self):
        set_module_args(dict(gather_subset="interfaces"))
        result = self.execute_module()
        self.assertEqual(
            result["ansible_facts"]["ansible_net_all_ipv4_addresses"][0],
            "192.168.255.115",
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_all_ipv6_addresses"][0],
            "2001:db8:8086:5554::1/31",
        )
        self.assertEqual(
            result["ansible_facts"]["ansible_net_interfaces"]["Ethernet1/1"]["macaddress"],
            "5254.0014.c104",
        )
