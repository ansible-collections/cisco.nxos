# (c) 2022 Red Hat Inc.
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

from ansible_collections.cisco.nxos.plugins.modules import nxos_hostname

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosHostnameModule(TestNxosModule):
    module = nxos_hostname

    def setUp(self):
        super(TestNxosHostnameModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.hostname.hostname.HostnameFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosHostnameModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_hostname_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(config=dict(hostname="NXOSv-9k"), state="merged"),
            ignore_provider_arg,
        )
        commands = ["hostname NXOSv-9k"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_hostname_linear_merged_idempotent(self):
        # test merged for linear attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(
            dict(config=dict(hostname="NXOSv-9k"), state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_hostname_linear_merged_2(self):
        # test merged for linear attributes - 2
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(
            dict(config=dict(hostname="NXOSv"), state="merged"),
            ignore_provider_arg,
        )
        commands = ["hostname NXOSv"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_hostname_linear_replaced(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(
            dict(config=dict(hostname="NXOSv"), state="replaced"),
            ignore_provider_arg,
        )
        commands = ["hostname NXOSv"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_hostname_linear_overridden(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(
            dict(config=dict(hostname="NXOSv"), state="overridden"),
            ignore_provider_arg,
        )
        commands = ["hostname NXOSv"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_hostname_deleted(self):
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = ["no hostname NXOSv-9k"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_hostname_rendered(self):
        set_module_args(
            dict(config=dict(hostname="NXOSv-9k"), state="rendered"),
            ignore_provider_arg,
        )
        commands = ["hostname NXOSv-9k"]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    def test_nxos_hostname_parsed(self):
        # test parsed
        cfg = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        parsed = {"hostname": "NXOSv-9k"}
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_hostname_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            hostname NXOSv-9k
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = {"hostname": "NXOSv-9k"}
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)
