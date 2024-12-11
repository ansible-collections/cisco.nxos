# (c) 2024 Red Hat Inc.
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

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_interfaces

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfInterfacesModule(TestNxosModule):
    """Test the  nxos_vrf_interfaces module."""

    module = nxos_vrf_interfaces

    def setUp(self):
        """Set up for nxos_vrf_interfaces module tests"""
        super(TestNxosVrfInterfacesModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vrf_interfaces.vrf_interfaces."
            "Vrf_interfacesFacts.get_device_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosVrfInterfacesModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_vrf_interfaces_merged_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member test
            interface Ethernet1/6
             no switchport
             speed 1000
             vrf member test2
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "test"},
                    {"name": "Ethernet1/6", "vrf_name": "test2"},
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_vrf_interfaces_merged(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
            interface Ethernet1/6
             no switchport
             speed 1000
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "test"},
                    {"name": "Ethernet1/6", "vrf_name": "test2"},
                ],
                state="merged",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "vrf member test",
            "interface Ethernet1/6",
            "vrf member test2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_interfaces_replaced(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
            interface Ethernet1/6
             no switchport
             speed 1000
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "VRF8"},
                    {"name": "Ethernet1/6", "vrf_name": "VRF6"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "vrf member VRF8",
            "interface Ethernet1/6",
            "vrf member VRF6",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_interfaces_deleted(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member test
            interface Ethernet1/6
             no switchport
             vrf member test2
             speed 1000
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2"},
                    {"name": "Ethernet1/3"},
                    {"name": "Ethernet1/6"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "no vrf member test",
            "interface Ethernet1/6",
            "no vrf member test2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_interfaces_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    interface Ethernet1/1
                    interface Ethernet1/2
                      no switchport
                      vrf member VRF1
                    interface Ethernet1/6
                      no switchport
                      speed 1000
                      vrf member TEST_VRF

                    """,
                ),
                state="parsed",
            ),
        )
        parsed_list = [
            {"name": "Ethernet1/1"},
            {"name": "Ethernet1/2", "vrf_name": "VRF1"},
            {"name": "Ethernet1/6", "vrf_name": "TEST_VRF"},
        ]
        result = self.execute_module(changed=False)

        self.assertEqual(result["parsed"], parsed_list)

    def test_nxos_vrf_interfaces_overridden(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member VRF1
            interface Ethernet1/6
             no switchport
             speed 1000
             vrf member TEST_VRF
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "test"},
                    {"name": "Ethernet1/6", "vrf_name": "test_vrf"},
                ],
                state="replaced",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "vrf member test",
            "interface Ethernet1/6",
            "vrf member test_vrf",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_vrf_interfaces_replaced_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member test_vrf1
            interface Ethernet1/6
             no switchport
             speed 1000
             vrf member test_vrf2
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "test_vrf1"},
                    {"name": "Ethernet1/6", "vrf_name": "test_vrf2"},
                ],
                state="replaced",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vrf_interfaces_overridden_idempotent(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member VRF1
            interface Ethernet1/6
             no switchport
             speed 1000
             vrf member TEST_VRF
            """,
        )
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "VRF1"},
                    {"name": "Ethernet1/6", "vrf_name": "TEST_VRF"},
                ],
                state="overridden",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vrf_interfaces_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            interface Ethernet1/1
            interface Ethernet1/2
             no switchport
             vrf member VRF1
            interface Ethernet1/3
            interface Ethernet1/4
            interface Ethernet1/5
            interface Ethernet1/6
             no switchport
             speed 1000
             vrf member TEST_VRF
            """,
        )
        set_module_args(dict(state="gathered"))
        gathered_list = [
            {"name": "Ethernet1/1"},
            {"name": "Ethernet1/2", "vrf_name": "VRF1"},
            {"name": "Ethernet1/3"},
            {"name": "Ethernet1/4"},
            {"name": "Ethernet1/5"},
            {"name": "Ethernet1/6", "vrf_name": "TEST_VRF"},
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered_list)

    def test_nxos_vrf_interfaces_rendered(self):
        self.execute_show_command.return_value = None
        set_module_args(
            dict(
                config=[
                    {"name": "Ethernet1/1"},
                    {"name": "Ethernet1/2", "vrf_name": "test"},
                    {"name": "Ethernet1/6", "vrf_name": "test2"},
                ],
                state="rendered",
            ),
        )
        commands = [
            "interface Ethernet1/2",
            "vrf member test",
            "interface Ethernet1/6",
            "vrf member test2",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["rendered"]), sorted(commands))
