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
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_snmp_server

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosSnmpServerModule(TestNxosModule):
    module = nxos_snmp_server

    def setUp(self):
        super(TestNxosSnmpServerModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.snmp_server.snmp_server.Snmp_serverFacts.get_config",
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
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36000),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA", instance="test"),
                    counter=dict(cache=dict(timeout=1800)),
                    drop=dict(unknown_engine_id=True, unknown_user=True),
                    engine_id=dict(local="'00:00:00:63:00:01:00:10:20:15:10:03'"),
                    communities=[
                        dict(name="private", group="network-admin"),
                        dict(community="public", use_ipv4acl="myacl"),
                    ],
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(community_map=dict(community="public", context="public1")),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(informs="Ethernet1/1", traps="Ethernet1/2"),
                    system_shutdown=True,
                    tcp_session=dict(auth=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server community private group network-admin",
            "snmp-server community public use-ipv4acl myacl",
            "snmp-server globalEnforcePriv",
            "snmp-server tcp-session auth",
            "snmp-server counter cache timeout 1800",
            "snmp-server packetsize 484",
            "snmp-server drop unknown-user",
            "snmp-server source-interface informs Ethernet1/1",
            "snmp-server context public instance test vrf siteA",
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
            snmp-server counter cache timeout 1800
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
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36000),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1800)),
                    drop=dict(unknown_engine_id=True, unknown_user=True),
                    engine_id=dict(local="00:00:00:63:00:01:00:10:20:15:10:03"),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(community_map=dict(community="public", context="public1")),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(informs="Ethernet1/1", traps="Ethernet1/2"),
                    system_shutdown=True,
                    tcp_session=dict(auth=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_snmp_server_linear_replaced(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            snmp-server globalEnforcePriv
            snmp-server tcp-session auth
            snmp-server counter cache timeout 1800
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
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36500),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1860)),
                    engine_id=dict(local="00:00:00:63:00:01:00:10:20:15:10:03"),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(community_map=dict(community="public", context="public1")),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(informs="Ethernet1/3", traps="Ethernet1/2"),
                    tcp_session=dict(auth=True),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server counter cache timeout 1860",
            "no snmp-server drop unknown-user",
            "no snmp-server drop unknown-engine-id",
            "snmp-server source-interface informs Ethernet1/3",
            "no snmp-server system-shutdown",
            "snmp-server aaa-user cache-timeout 36500",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_linear_overridden(self):
        # test overridden for linear attributes
        self.get_config.return_value = dedent(
            """\
            snmp-server globalEnforcePriv
            snmp-server tcp-session auth
            snmp-server counter cache timeout 1800
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
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36500),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1860)),
                    engine_id=dict(local="00:00:00:63:00:01:00:10:20:15:10:03"),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(community_map=dict(community="public", context="public1")),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(informs="Ethernet1/3", traps="Ethernet1/2"),
                    tcp_session=dict(auth=True),
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server counter cache timeout 1860",
            "no snmp-server drop unknown-user",
            "no snmp-server drop unknown-engine-id",
            "snmp-server source-interface informs Ethernet1/3",
            "no snmp-server system-shutdown",
            "snmp-server aaa-user cache-timeout 36500",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_location_spaces(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            snmp-server contact testswitch@localhost
            snmp-server location lab
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    contact="test-switch @t localhost",
                    location="long/and.(complicated) address",
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server contact test-switch @t localhost",
            "snmp-server location long/and.(complicated) address",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_traps_merged(self):
        # test merged for traps
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    traps=dict(
                        aaa=dict(server_state_change=True),
                        bridge=dict(enable=True),
                        callhome=dict(event_notify=True, smtp_send_fail=True),
                        bgp=dict(enable=True),
                        ospf=dict(enable=True),
                        ospfv3=dict(enable=True),
                    ),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server enable traps aaa server-state-change",
            "snmp-server enable traps bridge newroot",
            "snmp-server enable traps bridge topologychange",
            "snmp-server enable traps callhome event-notify",
            "snmp-server enable traps callhome smtp-send-fail",
            "snmp-server enable traps bgp",
            "snmp-server enable traps ospf",
            "snmp-server enable traps ospfv3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_traps_merged_idempotent(self):
        # test merged for traps (idempotent)
        self.get_config.return_value = dedent(
            """\
            snmp-server enable traps aaa server-state-change
            snmp-server enable traps bridge newroot
            snmp-server enable traps bridge topologychange
            snmp-server enable traps callhome event-notify
            snmp-server enable traps callhome smtp-send-fail
            snmp-server enable traps bgp
            snmp-server enable traps ospf
            snmp-server enable traps ospfv3
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    traps=dict(
                        aaa=dict(server_state_change=True),
                        bridge=dict(enable=True),
                        callhome=dict(event_notify=True, smtp_send_fail=True),
                        bgp=dict(enable=True),
                        ospf=dict(enable=True),
                        ospfv3=dict(enable=True),
                    ),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_snmp_server_traps_replaced(self):
        # test replaced for traps
        self.get_config.return_value = dedent(
            """\
            snmp-server enable traps aaa server-state-change
            snmp-server enable traps bridge newroot
            snmp-server enable traps bridge topologychange
            snmp-server enable traps callhome event-notify
            snmp-server enable traps callhome smtp-send-fail
            snmp-server enable traps link cisco-xcvr-mon-status-chg
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    traps=dict(
                        aaa=dict(server_state_change=True),
                        bridge=dict(enable=True),
                        cfs=dict(merge_failure=True),
                        link=dict(cisco_xcvr_mon_status_chg=False),
                    ),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no snmp-server enable traps callhome event-notify",
            "no snmp-server enable traps callhome smtp-send-fail",
            "snmp-server enable traps cfs merge-failure",
            "no snmp-server enable traps link cisco-xcvr-mon-status-chg",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_traps_replaced_1(self):
        # test replaced for traps
        self.get_config.return_value = dedent(
            """\
            snmp-server enable traps aaa server-state-change
            snmp-server enable traps bridge newroot
            snmp-server enable traps bridge topologychange
            snmp-server enable traps callhome event-notify
            snmp-server enable traps callhome smtp-send-fail
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    traps=dict(
                        aaa=dict(server_state_change=True),
                        bridge=dict(enable=True),
                        cfs=dict(merge_failure=True),
                    ),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no snmp-server enable traps callhome event-notify",
            "no snmp-server enable traps callhome smtp-send-fail",
            "snmp-server enable traps cfs merge-failure",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_hosts_merged(self):
        # test merged for hosts
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    hosts=[
                        dict(
                            host="192.168.1.1",
                            version="2c",
                            community="public",
                            traps=True,
                        ),
                        dict(host="192.168.1.1", source_interface="Ethernet1/1"),
                        dict(
                            host="192.168.2.1",
                            version="1",
                            community="private",
                            traps=True,
                        ),
                        dict(
                            host="192.168.2.1",
                            version="2c",
                            community="private",
                            informs=True,
                        ),
                        dict(
                            host="192.168.3.1",
                            version="3",
                            auth="private",
                            informs=True,
                            udp_port=65550,
                        ),
                        dict(
                            host="192.168.4.1",
                            version="3",
                            priv="private",
                            informs=True,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server host 192.168.2.1 informs version 2c private",
            "snmp-server host 192.168.1.1 traps version 2c public",
            "snmp-server host 192.168.4.1 informs version 3 priv private",
            "snmp-server host 192.168.1.1 source-interface Ethernet1/1",
            "snmp-server host 192.168.2.1 traps version 1 private",
            "snmp-server host 192.168.3.1 informs version 3 auth private udp-port 65550",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_hosts_merged_1(self):
        # test merged for hosts
        self.get_config.return_value = dedent(
            """\
            snmp-server host 192.168.2.1 informs version 2c private
            snmp-server host 192.168.1.1 traps version 2c public
            snmp-server host 192.168.4.1 informs version 3 priv private
            snmp-server host 192.168.1.1 source-interface Ethernet1/1
            snmp-server host 192.168.2.1 traps version 1 private
            snmp-server host 192.168.3.1 informs version 3 auth private udp-port 65550
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    hosts=[
                        dict(
                            host="192.168.1.1",
                            version="2c",
                            community="public",
                            traps=True,
                        ),
                        dict(host="192.168.1.1", source_interface="Ethernet1/1"),
                        dict(
                            host="192.168.2.1",
                            version="1",
                            community="private",
                            traps=True,
                        ),
                        dict(
                            host="192.168.2.1",
                            version="2c",
                            community="private",
                            informs=True,
                        ),
                        dict(
                            host="192.168.3.1",
                            version="3",
                            auth="private",
                            informs=True,
                            udp_port=65550,
                        ),
                        dict(
                            host="192.168.4.1",
                            version="3",
                            priv="private",
                            informs=True,
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_snmp_server_hosts_replaced(self):
        # test replaced for hosts
        self.get_config.return_value = dedent(
            """\
            snmp-server host 192.168.2.1 informs version 2c private
            snmp-server host 192.168.1.1 traps version 2c public
            snmp-server host 192.168.4.1 informs version 3 priv private
            snmp-server host 192.168.1.1 source-interface Ethernet1/1
            snmp-server host 192.168.2.1 traps version 1 private
            snmp-server host 192.168.3.1 informs version 3 auth private udp-port 65550
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    hosts=[
                        dict(
                            host="192.168.1.1",
                            version="2c",
                            community="public",
                            traps=True,
                        ),
                        dict(host="192.168.1.1", source_interface="Ethernet1/1"),
                        dict(
                            host="192.168.2.1",
                            version="1",
                            community="private",
                            traps=True,
                        ),
                        dict(
                            host="192.168.2.1",
                            version="2c",
                            community="private",
                            informs=True,
                        ),
                        dict(host="192.168.2.1", filter_vrf="siteA"),
                        dict(host="192.168.4.1", use_vrf="siteB"),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no snmp-server host 192.168.4.1 informs version 3 priv private",
            "no snmp-server host 192.168.3.1 informs version 3 auth private udp-port 65550",
            "snmp-server host 192.168.2.1 filter-vrf siteA",
            "snmp-server host 192.168.4.1 use-vrf siteB",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_users_merged_1(self):
        # test merged for users
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    users=dict(
                        auth=[
                            dict(
                                user="snmp_user_1",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af26281e1d0f1",
                                    engine_id="1:1:1:1:1",
                                    localized_key=True,
                                ),
                            ),
                            dict(
                                user="snmp_user_2",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af26281e1d0f1",
                                    engine_id="2:2:2:2:2",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af26281e1d0f1",
                                    ),
                                    localizedv2_key=True,
                                ),
                            ),
                            dict(
                                user="snmp_user_3",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af26281e1d0f1",
                                    engine_id="3:3:3:3:3",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af26281e1d0f1",
                                        aes_128=True,
                                    ),
                                    localized_key=True,
                                ),
                            ),
                            dict(
                                user="snmp_user_4",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="sha-256",
                                    password="0x5632724fb8ac3699296af26281e1d0f1",
                                    engine_id="4:4:4:4:4",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af26281e1d0f1",
                                        aes_128=True,
                                    ),
                                    localized_key=True,
                                ),
                            ),
                        ],
                    ),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server user snmp_user_2 network-admin auth md5 0x5632724fb8ac3699296af26281e1d0f1 priv 0x5632724fb8ac3699296af26281e1d0f1"
            " localizedV2key engineID 2:2:2:2:2",
            "snmp-server user snmp_user_3 network-admin auth md5 0x5632724fb8ac3699296af26281e1d0f1 priv aes-128"
            " 0x5632724fb8ac3699296af26281e1d0f1 localizedkey engineID 3:3:3:3:3",
            "snmp-server user snmp_user_1 network-admin auth md5 0x5632724fb8ac3699296af26281e1d0f1"
            " localizedkey engineID 1:1:1:1:1",
            "snmp-server user snmp_user_4 network-admin auth sha-256 0x5632724fb8ac3699296af26281e1d0f1 priv aes-128"
            " 0x5632724fb8ac3699296af26281e1d0f1 localizedkey engineID 4:4:4:4:4",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_users_merged_2(self):
        # test merged for users
        self.get_config.return_value = dedent(
            """\
            snmp-server user user2 network-admin auth md5 0x5632724fb8ac3699296af262 priv 0x5632724fb8ac3699296af262 localizedV2key engineID 2:2:2:2:2
            snmp-server user user3 network-admin auth md5 0x5632724fb8ac3699296af262 priv aes-128 0x5632724fb8ac3699296af262 localizedkey engineID 3:3:3:3:3
            snmp-server user user1 network-admin auth md5 0x5632724fb8ac3699296af262 localizedkey engineID 1:1:1:1:1
            snmp-server user user4 network-admin auth sha-256 0x5632724fb8ac3699296af262 priv aes-128 0x5632724fb8ac3699296af262 localizedkey engineID 4:4:4:4:4
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    users=dict(
                        auth=[
                            dict(
                                user="user1",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="1:1:1:1:1",
                                    localized_key=True,
                                ),
                            ),
                            dict(
                                user="user2",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="2:2:2:2:2",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af262",
                                    ),
                                    localizedv2_key=True,
                                ),
                            ),
                            dict(
                                user="user3",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="3:3:3:3:3",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af262",
                                        aes_128=True,
                                    ),
                                    localized_key=True,
                                ),
                            ),
                            dict(
                                user="user4",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="sha-256",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="4:4:4:4:4",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af262",
                                        aes_128=True,
                                    ),
                                    localized_key=True,
                                ),
                            ),
                        ],
                    ),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_snmp_server_users_replaced(self):
        # test replaced for users
        self.get_config.return_value = dedent(
            """\
            snmp-server user user2 network-admin auth md5 0x5632724fb8ac3699296af262 priv 0x5632724fb8ac3699296af262 localizedkey engineID 2:2:2:2:2
            snmp-server user user3 network-admin auth md5 0x5632724fb8ac3699296af262 priv aes-128 0x5632724fb8ac3699296af262 localizedkey engineID 3:3:3:3:3
            snmp-server user user1 network-admin auth md5 0x5632724fb8ac3699296af262 localizedkey engineID 1:1:1:1:1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    users=dict(
                        auth=[
                            dict(
                                user="user1",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="1:1:1:1:1",
                                    localized_key=True,
                                ),
                            ),
                            dict(
                                user="user4",
                                group="network-admin",
                                authentication=dict(
                                    algorithm="md5",
                                    password="0x5632724fb8ac3699296af262",
                                    engine_id="3:3:3:3:3",
                                    priv=dict(
                                        privacy_password="0x5632724fb8ac3699296af262",
                                        aes_128=True,
                                    ),
                                    localized_key=True,
                                ),
                            ),
                        ],
                    ),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no snmp-server user user2",
            "no snmp-server user user3",
            "snmp-server user user4 network-admin auth md5 0x5632724fb8ac3699296af262 priv aes-128"
            " 0x5632724fb8ac3699296af262 localizedkey engineID 3:3:3:3:3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_deleted(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
            snmp-server globalEnforcePriv
            snmp-server tcp-session auth
            snmp-server counter cache timeout 1800
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
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "no snmp-server globalEnforcePriv",
            "no snmp-server tcp-session auth",
            "no snmp-server counter cache timeout 1800",
            "no snmp-server packetsize 484",
            "no snmp-server drop unknown-user",
            "no snmp-server source-interface informs Ethernet1/1",
            "no snmp-server context public vrf siteA",
            "no snmp-server protocol enable",
            "no snmp-server system-shutdown",
            "no snmp-server aaa-user cache-timeout 36000",
            "no snmp-server engineID local 00:00:00:63:00:01:00:10:20:15:10:03",
            "no snmp-server contact testswitch@localhost",
            "no snmp-server drop unknown-engine-id",
            "no snmp-server location lab",
            "no snmp-server mib community-map public context public1",
            "no snmp-server source-interface traps Ethernet1/2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_snmp_server_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    snmp-server community private group network-admin
                    snmp-server community public use-ipv4acl myacl use-ipv6acl myaclv6
                    snmp-server globalEnforcePriv
                    snmp-server tcp-session auth
                    snmp-server counter cache timeout 1800
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
                    snmp-server user 1234 network-admin auth md5 0x7d425fbf09417c44bca69e1d9e9ce889 priv 0x7d425fbf09417c44bca69e1d9e9ce889 localizedkey
                    snmp-server user snmp_user_1 network-operator auth md5 0x5632724fb8ac3699296af26281e1d0f1 localizedkey
                    """,
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )

        parsed = dict(
            aaa_user=dict(cache_timeout=36000),
            contact="testswitch@localhost",
            communities=[
                dict(name="private", group="network-admin"),
                dict(name="public", use_ipv4acl="myacl", use_ipv6acl="myaclv6"),
            ],
            context=dict(name="public", vrf="siteA"),
            counter=dict(cache=dict(timeout=1800)),
            drop=dict(unknown_engine_id=True, unknown_user=True),
            engine_id=dict(local="00:00:00:63:00:01:00:10:20:15:10:03"),
            global_enforce_priv=True,
            location="lab",
            mib=dict(community_map=dict(community="public", context="public1")),
            packetsize=484,
            protocol=dict(enable=True),
            source_interface=dict(informs="Ethernet1/1", traps="Ethernet1/2"),
            system_shutdown=True,
            tcp_session=dict(auth=True),
            users=dict(
                auth=[
                    dict(
                        user="1234",
                        group="network-admin",
                        authentication=dict(
                            algorithm="md5",
                            password="0x7d425fbf09417c44bca69e1d9e9ce889",
                            localized_key=True,
                            priv=dict(
                                privacy_password="0x7d425fbf09417c44bca69e1d9e9ce889",
                            ),
                        ),
                    ),
                    dict(
                        user="snmp_user_1",
                        group="network-operator",
                        authentication=dict(
                            algorithm="md5",
                            password="0x5632724fb8ac3699296af26281e1d0f1",
                            localized_key=True,
                        ),
                    ),
                ],
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_snmp_server_rendered(self):
        # test rendered
        set_module_args(
            dict(
                config=dict(
                    aaa_user=dict(cache_timeout=36000),
                    contact="testswitch@localhost",
                    context=dict(name="public", vrf="siteA"),
                    counter=dict(cache=dict(timeout=1800)),
                    communities=[
                        dict(name="private", group="network-admin"),
                        dict(name="public", use_ipv4acl="myacl", use_ipv6acl="myaclv6"),
                    ],
                    drop=dict(unknown_engine_id=True, unknown_user=True),
                    engine_id=dict(local="'00:00:00:63:00:01:00:10:20:15:10:03'"),
                    global_enforce_priv=True,
                    location="lab",
                    mib=dict(community_map=dict(community="public", context="public1")),
                    packetsize=484,
                    protocol=dict(enable=True),
                    source_interface=dict(informs="Ethernet1/1", traps="Ethernet1/2"),
                    system_shutdown=True,
                    tcp_session=dict(auth=True),
                ),
                state="rendered",
            ),
            ignore_provider_arg,
        )
        rendered = [
            "snmp-server globalEnforcePriv",
            "snmp-server tcp-session auth",
            "snmp-server counter cache timeout 1800",
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
            "snmp-server community private group network-admin",
            "snmp-server community public use-ipv4acl myacl use-ipv6acl myaclv6",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(rendered))

    def test_nxos_snmp_server_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            snmp-server globalEnforcePriv
            snmp-server tcp-session auth
            snmp-server counter cache timeout 1800
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
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)

        gathered = dict(
            aaa_user=dict(cache_timeout=36000),
            contact="testswitch@localhost",
            context=dict(name="public", vrf="siteA"),
            counter=dict(cache=dict(timeout=1800)),
            drop=dict(unknown_engine_id=True, unknown_user=True),
            engine_id=dict(local="00:00:00:63:00:01:00:10:20:15:10:03"),
            global_enforce_priv=True,
            location="lab",
            mib=dict(community_map=dict(community="public", context="public1")),
            packetsize=484,
            protocol=dict(enable=True),
            source_interface=dict(informs="Ethernet1/1", traps="Ethernet1/2"),
            system_shutdown=True,
            tcp_session=dict(auth=True),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_snmp_server_gathered_empty(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)

        gathered = {}
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_snmp_server_traps_merged_820(self):
        # test merged for traps, related to #820
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    traps=dict(
                        entity=dict(
                            entity_fan_status_change=True,
                            entity_mib_change=True,
                            entity_module_inserted=True,
                            entity_module_removed=True,
                            entity_module_status_change=True,
                            entity_power_out_change=True,
                            entity_power_status_change=True,
                            entity_unrecognised_module=True,
                            entity_sensor=True,
                        ),
                    ),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "snmp-server enable traps entity entity_fan_status_change",
            "snmp-server enable traps entity entity_mib_change",
            "snmp-server enable traps entity entity_module_inserted",
            "snmp-server enable traps entity entity_module_status_change",
            "snmp-server enable traps entity entity_power_out_change",
            "snmp-server enable traps entity entity_power_status_change",
            "snmp-server enable traps entity entity_sensor",
            "snmp-server enable traps entity entity_unrecognised_module",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
