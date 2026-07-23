# (c) 2026 Red Hat Inc.
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
from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_lag_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosLagInterfacesModule(TestNxosModule):
    module = nxos_lag_interfaces

    def setUp(self):
        super(TestNxosLagInterfacesModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS",
        )
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

    def tearDown(self):
        super(TestNxosLagInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()

    def load_fixtures(self, commands=None, device=""):
        self.mock_FACT_LEGACY_SUBSETS.return_value = dict()
        conn = MagicMock()
        conn.edit_config.return_value = {}
        self.get_resource_connection_config.return_value = conn

    SHOW_CMD = "show running-config | section ^interface"

    def test_replaced_empty_port_channel_no_members(self):
        """Regression for #819: replaced on port-channel with no members."""
        existing = dedent(
            """\
          interface port-channel100
          interface Ethernet1/1
          interface Ethernet1/2
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        set_module_args(
            dict(
                config=[
                    dict(
                        name="port-channel100",
                        members=[
                            dict(member="Ethernet1/1", mode="active"),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "channel-group 100 mode active",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_replaced_with_existing_members(self):
        existing = dedent(
            """\
          interface port-channel10
          interface Ethernet1/1
            channel-group 10
          interface Ethernet1/2
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        set_module_args(
            dict(
                config=[
                    dict(
                        name="port-channel10",
                        members=[
                            dict(member="Ethernet1/2", mode="active"),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/2",
            "channel-group 10 mode active",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_replaced_empty_port_channel_idempotent(self):
        existing = dedent(
            """\
          interface port-channel100
          interface Ethernet1/1
            channel-group 100 mode active
          interface Ethernet1/2
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        set_module_args(
            dict(
                config=[
                    dict(
                        name="port-channel100",
                        members=[
                            dict(member="Ethernet1/1", mode="active"),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        self.execute_module(changed=False, commands=[])

    def test_merged_empty_port_channel(self):
        existing = dedent(
            """\
          interface port-channel11
          interface Ethernet1/1
          interface Ethernet1/2
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        set_module_args(
            dict(
                config=[
                    dict(
                        name="port-channel11",
                        members=[
                            dict(member="Ethernet1/1"),
                            dict(member="Ethernet1/2", mode="active"),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Ethernet1/1",
            "channel-group 11",
            "interface Ethernet1/2",
            "channel-group 11 mode active",
        ]
        self.execute_module(changed=True, commands=commands)
