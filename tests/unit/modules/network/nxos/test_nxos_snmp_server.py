# (c) 2021 Red Hat Inc.
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
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.plugins.modules import nxos_snmp_server

from .nxos_module import TestNxosModule, set_module_args

ignore_provider_arg = True


class TestNxosSnmpServerModule(TestNxosModule):

    module = nxos_snmp_server

    def setUp(self):
        super(TestNxosSnmpServerModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.snmp_server.snmp_server.Snmp_serverFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosSnmpServerModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_snmp_server_linear_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36000),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1800)),
                    drop=dict(unknown_engine_id=True, unknown_user=True),
                    engine_id=dict(
                        local="'00:00:00:63:00:01:00:10:20:15:10:03'"
                    ),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(
                        community_map=dict(
                            community="public", context="public1"
                        )
                    ),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(
                        informs="Ethernet1/1", traps="Ethernet1/2"
                    ),
                    system_shutdown=True,
                    tcp_session=dict(auth=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server globalEnforcePriv",
            "snmp-server tcp-session auth",
            "snmp-server packetsize 484",
            "snmp-server drop unknown-user",
            "snmp-server source-interface informs Ethernet1/1",
            "snmp-server context public vrf siteA",
            "snmp-server protocol enable",
            "snmp-server system-shutdown",
            "snmp-server aaa-user cache-timeout 36000",
            "snmp-server engineID local '00:00:00:63:00:01:00:10:20:15:10:03'",
            "snmp-server contact testswitch@localhost",
            "snmp-server drop unknown-engine-id",
            "snmp-server location lab",
            "snmp-server mib community-map public context public1",
            "snmp-server source-interface traps Ethernet1/2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_linear_merged_idempotent(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            snmp-server globalEnforcePriv
            snmp-server tcp-session auth
            snmp-server packetsize 484
            snmp-server drop unknown-user
            snmp-server source-interface informs Ethernet1/1
            snmp-server context public vrf siteA
            snmp-server protocol enable
            snmp-server system-shutdown
            snmp-server aaa-user cache-timeout 36000
            snmp-server engineID local 00:00:00:63:00:01:00:10:20:15:10:03
            snmp-server contact testswitch@localhost
            snmp-server drop unknown-engine-id
            snmp-server location lab
            snmp-server mib community-map public context public1
            snmp-server source-interface traps Ethernet1/2
            """
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36000),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1800)),
                    drop=dict(unknown_engine_id=True, unknown_user=True),
                    engine_id=dict(
                        local="00:00:00:63:00:01:00:10:20:15:10:03"
                    ),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(
                        community_map=dict(
                            community="public", context="public1"
                        )
                    ),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(
                        informs="Ethernet1/1", traps="Ethernet1/2"
                    ),
                    system_shutdown=True,
                    tcp_session=dict(auth=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
