# (c) 2019 Red Hat Inc.
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

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_l2_interfaces
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule


ignore_provider_arg = True


class TestNxosL2InterfacesModule(TestNxosModule):
    module = nxos_l2_interfaces

    def setUp(self):
        super(TestNxosL2InterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.l2_interfaces.l2_interfaces."
            "L2_interfacesFacts._get_interface_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        self.maxDiff = None

    def tearDown(self):
        super(TestNxosL2InterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_l2_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """
            interface Ethernet1/6
             switchport
             switchport mode trunk
             switchport access vlan 20
             switchport trunk native vlan 40
             switchport trunk allowed vlan 30-45,47
            interface Ethernet1/2
              switchport mode trunk
              switchport trunk native vlan 20
              switchport trunk allowed vlan 10,20,30
            interface Ethernet1/4
             speed 1000
             service-policy type qos output test-policy
             no shutdown
            """
        )

        set_module_args(
            dict(
                state="gathered",
            )
        )

        expected = [
            {
                'access': {'vlan': 20}, 
                'mode': 'trunk', 
                'name': 'Ethernet1/6', 
                'trunk': {
                    'allowed_vlans': '30-45,47', 
                    'native_vlan': 40
                }
            }, 
            {
                'mode': 'trunk', 
                'name': 'Ethernet1/2', 
                'trunk': {
                    'allowed_vlans': '10,20,30', 
                    'native_vlan': 20
                }
            }
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], expected)

