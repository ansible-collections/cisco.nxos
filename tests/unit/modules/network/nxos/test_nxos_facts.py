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

    def test_nxos_facts_ipv6_interface_no_table_addr(self):
        """Test that IPv6 interfaces without TABLE_addr don't cause KeyError."""
        from unittest.mock import MagicMock

        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.legacy.base import (
            Interfaces,
        )

        # Create a mock module
        module = MagicMock()

        # Create Interfaces instance
        interfaces_obj = Interfaces(module)

        # Pre-populate interfaces dict (simulating show interface output)
        interfaces_obj.facts = {
            "interfaces": {
                "Vlan100": {
                    "state": "up",
                    "macaddress": "5254.0014.c104",
                    "mtu": "1500",
                },
            },
            "all_ipv4_addresses": [],
            "all_ipv6_addresses": [],
        }

        # Mock data with IPv6 interface that has no TABLE_addr (only prefix)
        ipv6_data = {
            "TABLE_intf": {
                "ROW_intf": {
                    "intf-name": "Vlan100",
                    "prefix": "2001:db8::/64",
                    "forwarding-enabled": "enabled",
                },
            },
        }

        # This should not raise KeyError
        interfaces_obj.populate_structured_ipv6_interfaces(ipv6_data)

        # Verify that all_ipv6_addresses is still empty (no address was added)
        self.assertEqual(len(interfaces_obj.facts["all_ipv6_addresses"]), 0)

        # Verify that ipv6 key was added to the interface with prefix info
        self.assertIn("ipv6", interfaces_obj.facts["interfaces"]["Vlan100"])
        self.assertEqual(
            interfaces_obj.facts["interfaces"]["Vlan100"]["ipv6"]["subnet"],
            "2001:db8::/64",
        )

    def test_nxos_facts_ipv6_multiple_vlan_interfaces(self):
        # Test for multiple VLAN interfaces with IPv6 addresses
        import json
        import os
        from unittest.mock import MagicMock

        from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.legacy.base import (
            Interfaces,
        )

        module = MagicMock()
        interfaces_obj = Interfaces(module)

        # Setup interfaces dict with two VLAN interfaces
        interfaces_obj.facts = {
            "interfaces": {
                "Vlan101": {
                    "state": "up",
                    "macaddress": "5254.0014.c104",
                    "mtu": "1500",
                },
                "Vlan102": {
                    "state": "up",
                    "macaddress": "5254.0014.c105",
                    "mtu": "1500",
                },
            },
            "all_ipv4_addresses": [],
            "all_ipv6_addresses": [],
        }

        # Load fixture with two VLAN interfaces
        fixture_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "nxos_facts",
            "show_ipv6_interface_vrf_all_two_vlans",
        )
        with open(fixture_path) as f:
            ipv6_data = json.load(f)

        # This should collect both IPv6 addresses
        interfaces_obj.populate_structured_ipv6_interfaces(ipv6_data)

        # Verify that both IPv6 addresses are collected
        self.assertEqual(len(interfaces_obj.facts["all_ipv6_addresses"]), 2)
        self.assertIn("2001:db8:101::1/64", interfaces_obj.facts["all_ipv6_addresses"])
        self.assertIn("2001:db8:102::1/64", interfaces_obj.facts["all_ipv6_addresses"])
