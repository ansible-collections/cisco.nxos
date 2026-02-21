# (c) 2020 Red Hat Inc.
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

from ansible_collections.cisco.nxos.plugins.modules import nxos_lag_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosLacpInterfacesModule(TestNxosModule):
    module = nxos_lag_interfaces

    def setUp(self):
        super(TestNxosLacpInterfacesModule, self).setUp()

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
        super(TestNxosLacpInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()

    # ---------------------------
    # Lag_interfaces Test Cases
    # ---------------------------

    SHOW_CMD = "show running-config | section ^interface"

    def test_lag_no_change(self):
        # basic tests
        existing = dedent(
            """\
          interface port-channel1
            switchport
          interface Ethernet1/1
            channel-group 1 mode active
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        playbook = dict(
            config=[
                dict(
                    name="port-channel1",
                    members=[
                        dict(
                            member="Ethernet1/1",
                            mode="active",
                        ),
                    ],
                ),
            ],
        )
        # Expected result commands for each 'state'
        merged = []

        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=False, commands=merged)

    def test_lag_add_additional_interface(self):
        # basic tests
        existing = dedent(
            """\
          interface port-channel1
            switchport
          interface Ethernet1/1
            channel-group 1 mode active
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        playbook = dict(
            config=[
                dict(
                    name="port-channel1",
                    members=[
                        dict(
                            member="Ethernet1/1",
                            mode="active",
                        ),
                        dict(
                            member="Ethernet1/2",
                            mode="active",
                        ),
                    ],
                ),
            ],
        )
        # Expected result commands for each 'state'
        merged = [
            "interface Ethernet1/2",
            "channel-group 1 mode active",
        ]

        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

    def test_lag_replace_lag_with_no_existing_members(self):
        # basic tests
        existing = dedent(
            """\
          interface port-channel1
            switchport
        """,
        )
        self.get_resource_connection_facts.return_value = {self.SHOW_CMD: existing}
        playbook = dict(
            config=[
                dict(
                    name="port-channel1",
                    members=[
                        dict(
                            member="Ethernet1/1",
                            mode="active",
                        ),
                        dict(
                            member="Ethernet1/2",
                            mode="active",
                        ),
                    ],
                ),
            ],
        )
        # Expected result commands for each 'state'
        merged = [
            "interface Ethernet1/1",
            "channel-group 1 mode active",
            "interface Ethernet1/2",
            "channel-group 1 mode active",
        ]

        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)
