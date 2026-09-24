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

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vpc_interface

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosVpcInterfaceModule(TestNxosModule):
    module = nxos_vpc_interface

    def setUp(self):
        super(TestNxosVpcInterfaceModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vpc_interfaces.vpc_interfaces.Vpc_interfacesFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosVpcInterfaceModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    # merged

    def test_nxos_vpc_interface_merged(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              switchport
            interface port-channel20
              switchport
            interface Ethernet1/3
              switchport
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(name="port-channel10", vpc="100"),
                    dict(name="port-channel20", peer_link=True),
                    dict(name="Ethernet1/3", orphan_port_suspend=True),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel10",
                "vpc 100",
                "interface port-channel20",
                "vpc peer-link",
                "interface Ethernet1/3",
                "vpc orphan-port suspend",
            ],
        )

    def test_nxos_vpc_interface_merged_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            interface Ethernet1/3
              vpc orphan-port suspend
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(name="port-channel10", vpc="100"),
                    dict(name="port-channel20", peer_link=True),
                    dict(name="Ethernet1/3", orphan_port_suspend=True),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_interface_merged_change_vpc_id(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10", vpc="200")], state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel10", "no vpc", "vpc 200"],
        )

    def test_nxos_vpc_interface_merged_peer_link_false(self):
        # merged must be able to turn the peer-link off
        self.get_config.return_value = dedent(
            """\
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel20", peer_link=False)], state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel20", "no vpc peer-link"],
        )

    def test_nxos_vpc_interface_merged_orphan_port_suspend_false(self):
        # merged must be able to turn orphan-port suspend off
        self.get_config.return_value = dedent(
            """\
            interface Ethernet1/3
              vpc orphan-port suspend
            """,
        )
        set_module_args(
            dict(
                config=[dict(name="Ethernet1/3", orphan_port_suspend=False)],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/3", "no vpc orphan-port suspend"],
        )

    def test_nxos_vpc_interface_merged_peer_link_over_vpc_id(self):
        # asking for the peer-link clears a conflicting VPC ID on the device
        self.get_config.return_value = dedent(
            """\
            interface port-channel20
              vpc 100
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel20", peer_link=True)], state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel20", "no vpc", "vpc peer-link"],
        )

    def test_nxos_vpc_interface_merged_vpc_id_over_peer_link(self):
        # asking for a VPC ID clears a conflicting peer-link on the device
        self.get_config.return_value = dedent(
            """\
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel20", vpc="100")], state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel20", "no vpc peer-link", "vpc 100"],
        )

    def test_nxos_vpc_interface_merged_retains_unmentioned(self):
        # merged leaves attributes the playbook does not mention alone
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
              vpc orphan-port suspend
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10", vpc="100")], state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_interface_vpc_and_peer_link_mutually_exclusive(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[dict(name="port-channel20", vpc="100", peer_link=True)],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(failed=True)
        self.assertIn("mutually exclusive", result["msg"])

    # replaced

    def test_nxos_vpc_interface_replaced(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
              vpc orphan-port suspend
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10", vpc="200")], state="replaced"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel10",
                "no vpc",
                "vpc 200",
                "no vpc orphan-port suspend",
            ],
        )

    def test_nxos_vpc_interface_replaced_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10", vpc="100")], state="replaced"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_interface_replaced_removes_peer_link(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel20")], state="replaced"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel20", "no vpc peer-link"],
        )

    # overridden

    def test_nxos_vpc_interface_overridden(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            interface port-channel30
              vpc 300
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(name="port-channel10", vpc="100"),
                    dict(name="port-channel20", peer_link=True),
                ],
                state="overridden",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface port-channel30", "no vpc"],
        )

    def test_nxos_vpc_interface_overridden_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10", vpc="100")], state="overridden"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # deleted

    def test_nxos_vpc_interface_deleted(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(
            dict(config=[dict(name="port-channel10")], state="deleted"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface port-channel10", "no vpc"])

    def test_nxos_vpc_interface_deleted_all(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            interface Ethernet1/3
              vpc orphan-port suspend
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface port-channel10",
                "no vpc",
                "interface port-channel20",
                "no vpc peer-link",
                "interface Ethernet1/3",
                "no vpc orphan-port suspend",
            ],
        )

    def test_nxos_vpc_interface_deleted_empty_have(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              switchport
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # rendered

    def test_nxos_vpc_interface_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(name="port-channel10", vpc="100"),
                    dict(name="port-channel20", peer_link=True),
                    dict(name="Ethernet1/3", orphan_port_suspend=True),
                ],
                state="rendered",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "interface port-channel10",
                "vpc 100",
                "interface port-channel20",
                "vpc peer-link",
                "interface Ethernet1/3",
                "vpc orphan-port suspend",
            ],
        )

    # parsed

    def test_nxos_vpc_interface_parsed(self):
        cfg = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            interface Ethernet1/3
              vpc orphan-port suspend
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            [
                {"name": "port-channel10", "vpc": "100"},
                {"name": "port-channel20", "peer_link": True},
                {"name": "Ethernet1/3", "orphan_port_suspend": True},
            ],
        )

    def test_nxos_vpc_interface_parsed_no_vpc_config(self):
        cfg = dedent(
            """\
            interface port-channel10
              switchport
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], [])

    # gathered

    def test_nxos_vpc_interface_gathered(self):
        self.get_config.return_value = dedent(
            """\
            interface port-channel10
              vpc 100
            interface port-channel20
              vpc peer-link
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["gathered"],
            [
                {"name": "port-channel10", "vpc": "100"},
                {"name": "port-channel20", "peer_link": True},
            ],
        )

    def test_nxos_vpc_interface_gathered_empty(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], [])
