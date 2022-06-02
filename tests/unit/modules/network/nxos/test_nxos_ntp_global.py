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

from ansible_collections.cisco.nxos.plugins.modules import nxos_ntp_global
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import AnsibleFailJson

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosNtpGlobalModule(TestNxosModule):

    module = nxos_ntp_global

    def setUp(self):
        super(TestNxosNtpGlobalModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ntp_global.ntp_global.Ntp_globalFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosNtpGlobalModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_ntp_global_linear_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="PeerAcl1"),
                            dict(access_list="PeerAcl2"),
                        ],
                        serve=[
                            dict(access_list="ServeAcl1"),
                            dict(access_list="ServeAcl2"),
                        ],
                        query_only=[
                            dict(access_list="QueryAcl1"),
                            dict(access_list="QueryAcl2"),
                        ],
                        serve_only=[
                            dict(access_list="ServeOnlyAcl1"),
                            dict(access_list="ServeOnlyAcl2"),
                        ],
                    ),
                    allow=dict(control=dict(rate_limit=400), private=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp access-group peer PeerAcl1",
            "ntp access-group peer PeerAcl2",
            "ntp access-group serve ServeAcl1",
            "ntp access-group serve ServeAcl2",
            "ntp access-group query-only QueryAcl1",
            "ntp access-group query-only QueryAcl2",
            "ntp access-group serve-only ServeOnlyAcl1",
            "ntp access-group serve-only ServeOnlyAcl2",
            "ntp allow control rate-limit 400",
            "ntp allow private",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_linear_merged_idempotent(self):
        # test merged for linear attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
            ntp access-group peer PeerAcl1
            ntp access-group peer PeerAcl2
            ntp access-group serve ServeAcl1
            ntp access-group serve ServeAcl2
            ntp access-group query-only QueryAcl1
            ntp access-group query-only QueryAcl2
            ntp access-group serve-only ServeOnlyAcl1
            ntp access-group serve-only ServeOnlyAcl2
            ntp allow control rate-limit 400
            ntp allow private
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[
                            dict(access_list="PeerAcl1"),
                            dict(access_list="PeerAcl2"),
                        ],
                        serve=[
                            dict(access_list="ServeAcl1"),
                            dict(access_list="ServeAcl2"),
                        ],
                        query_only=[
                            dict(access_list="QueryAcl1"),
                            dict(access_list="QueryAcl2"),
                        ],
                        serve_only=[
                            dict(access_list="ServeOnlyAcl1"),
                            dict(access_list="ServeOnlyAcl2"),
                        ],
                    ),
                    allow=dict(control=dict(rate_limit=400), private=True),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ntp_global_linear_replaced_idempotent(self):
        # test merged for linear attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
            ntp access-group peer PeerAcl1
            ntp access-group peer PeerAcl2
            ntp access-group serve ServeAcl1
            ntp access-group serve ServeAcl2
            ntp access-group query-only QueryAcl1
            ntp access-group query-only QueryAcl2
            ntp access-group serve-only ServeOnlyAcl1
            ntp access-group serve-only ServeOnlyAcl2
            ntp allow control rate-limit 400
            ntp allow private
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    access_group=dict(
                        peer=[dict(access_list="PeerAcl1")],
                        serve=[
                            dict(access_list="ServeAcl1"),
                            dict(access_list="ServeAcl2"),
                            dict(access_list="ServeAcl3"),
                        ],
                        query_only=[
                            dict(access_list="QueryAcl1"),
                            dict(access_list="QueryAcl2"),
                        ],
                    ),
                    allow=dict(control=dict(rate_limit=400)),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ntp allow private",
            "no ntp access-group peer PeerAcl2",
            "ntp access-group serve ServeAcl3",
            "no ntp access-group serve-only ServeOnlyAcl1",
            "no ntp access-group serve-only ServeOnlyAcl2",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_merged(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    authenticate=True,
                    authentication_keys=[
                        dict(id=1, key="testPass", encryption=0),
                        dict(id=2, key="vagwwtKfkv", encryption=7),
                        dict(id=3, key="secretPass", encryption=0),
                    ],
                    logging=True,
                    master=dict(stratum=2),
                    passive=True,
                    source="192.168.1.1",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp authenticate",
            "ntp authentication-key 1 md5 testPass 0",
            "ntp authentication-key 2 md5 vagwwtKfkv 7",
            "ntp authentication-key 3 md5 secretPass 0",
            "ntp logging",
            "ntp master 2",
            "ntp passive",
            "ntp source 192.168.1.1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_merged_idempotent(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            ntp authenticate
            ntp authentication-key 1 md5 testPass 0
            ntp authentication-key 2 md5 vagwwtKfkv 7
            ntp authentication-key 3 md5 secretPass 0
            ntp logging
            ntp master 2
            ntp passive
            ntp source 192.168.1.1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    authenticate=True,
                    authentication_keys=[
                        dict(id=1, key="testPass", encryption=0),
                        dict(id=2, key="vagwwtKfkv", encryption=7),
                        dict(id=3, key="secretPass", encryption=0),
                    ],
                    logging=True,
                    master=dict(stratum=2),
                    passive=True,
                    source="192.168.1.1",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ntp_global_complex_merged_idempotent(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            ntp authenticate
            ntp authentication-key 1 md5 testPass 0
            ntp authentication-key 2 md5 vagwwtKfkv 7
            ntp authentication-key 3 md5 secretPass 0
            ntp logging
            ntp master 2
            ntp passive
            ntp source 192.168.1.1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    authentication_keys=[
                        dict(id=1, key="testPass", encryption=0),
                        dict(id=2, key="vagwwtKfkvb", encryption=7),
                    ],
                    logging=True,
                    master=dict(stratum=3),
                    source="192.168.1.1",
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp authentication-key 2 md5 vagwwtKfkvb 7",
            "no ntp authentication-key 3 md5 secretPass 0",
            "ntp master 3",
            "no ntp authenticate",
            "no ntp passive",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_2_merged(self):
        # test merged for complex attributes - 2
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    peers=[
                        dict(
                            peer="192.168.1.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            use_vrf="siteA",
                            prefer=True,
                        ),
                        dict(peer="192.168.1.2", key_id=3, use_vrf="siteB"),
                        dict(peer="192.168.1.3", maxpoll=10, use_vrf="default"),
                    ],
                    servers=[
                        dict(
                            server="203.0.113.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            use_vrf="siteA",
                            prefer=True,
                        ),
                        dict(server="203.0.113.2", key_id=3, use_vrf="siteB"),
                        dict(server="203.0.113.3", maxpoll=10, use_vrf="default"),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp peer 192.168.1.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15",
            "ntp peer 192.168.1.2 use-vrf siteB key 3",
            "ntp peer 192.168.1.3 use-vrf default maxpoll 10",
            "ntp server 203.0.113.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15",
            "ntp server 203.0.113.2 use-vrf siteB key 3",
            "ntp server 203.0.113.3 use-vrf default maxpoll 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_2_merged_idempotent(self):
        # test merged for complex attributes - 2 (idempotent)
        self.get_config.return_value = dedent(
            """\
            ntp peer 192.168.1.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15
            ntp peer 192.168.1.2 use-vrf siteB key 3
            ntp peer 192.168.1.3 use-vrf default maxpoll 10
            ntp server 203.0.113.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15
            ntp server 203.0.113.2 use-vrf siteB key 3
            ntp server 203.0.113.3 use-vrf default maxpoll 10
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    peers=[
                        dict(
                            peer="192.168.1.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            vrf="siteA",
                            prefer=True,
                        ),
                        dict(peer="192.168.1.2", key_id=3, vrf="siteB"),
                        dict(peer="192.168.1.3", maxpoll=10, vrf="default"),
                    ],
                    servers=[
                        dict(
                            server="203.0.113.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            vrf="siteA",
                            prefer=True,
                        ),
                        dict(server="203.0.113.2", key_id=3, vrf="siteB"),
                        dict(server="203.0.113.3", maxpoll=10, vrf="default"),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ntp_global_complex_2_replaced(self):
        # test replaced for complex attributes - 2
        self.get_config.return_value = dedent(
            """\
            ntp peer 192.168.1.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15
            ntp peer 192.168.1.2 use-vrf siteB key 3
            ntp peer 192.168.1.3 use-vrf default maxpoll 10
            ntp server 203.0.113.1 prefer use-vrf siteA key 2 minpoll 5 maxpoll 15
            ntp server 203.0.113.2 use-vrf siteB key 3
            ntp server 203.0.113.3 use-vrf default maxpoll 10
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    peers=[
                        dict(
                            peer="192.168.1.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            vrf="siteA",
                            prefer=True,
                        ),
                        dict(peer="192.168.1.2", vrf="siteB"),
                    ],
                    servers=[
                        dict(
                            server="203.0.113.1",
                            key_id=2,
                            minpoll=5,
                            maxpoll=15,
                            vrf="siteA",
                            prefer=True,
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ntp peer 192.168.1.2 use-vrf siteB key 3",
            "ntp peer 192.168.1.2 use-vrf siteB",
            "no ntp peer 192.168.1.3 use-vrf default maxpoll 10",
            "no ntp server 203.0.113.2 use-vrf siteB key 3",
            "no ntp server 203.0.113.3 use-vrf default maxpoll 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_3_merged(self):
        # test merged for complex attributes - 3
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    trusted_keys=[
                        dict(key_id=1001),
                        dict(key_id=1002),
                        dict(key_id=1003),
                    ],
                    source_interface="Ethernet1/1",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp trusted-key 1001",
            "ntp trusted-key 1002",
            "ntp trusted-key 1003",
            "ntp source-interface Ethernet1/1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_complex_3_merged_idempotent(self):
        # test merged for complex attributes - 3 (idempotent)
        self.get_config.return_value = dedent(
            """\
            ntp trusted-key 1001
            ntp trusted-key 1002
            ntp trusted-key 1003
            ntp source-interface  Ethernet1/1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    trusted_keys=[
                        dict(key_id=1001),
                        dict(key_id=1002),
                        dict(key_id=1003),
                    ],
                    source_interface="Ethernet1/1",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ntp_global_source_interface_merged_idempotent(self):
        # test merged for complex attributes - 3 (idempotent)
        self.get_config.return_value = dedent(
            """\
            ntp trusted-key 1001
            ntp trusted-key 1002
            ntp trusted-key 1003
            ntp source-interface Ethernet1/1
            """,
        )
        set_module_args(
            dict(config=dict(source_interface="Ethernet1/1"), state="merged"),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_ntp_global_complex_3_replaced(self):
        # test replaced for complex attributes - 3
        self.get_config.return_value = dedent(
            """\
            ntp trusted-key 1001
            ntp trusted-key 1002
            ntp trusted-key 1003
            ntp source-interface 192.168.1.100
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    trusted_keys=[
                        dict(key_id=1001),
                        dict(key_id=1002),
                        dict(key_id=1004),
                    ],
                    source_interface="192.168.1.101",
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ntp trusted-key 1003",
            "ntp trusted-key 1004",
            "ntp source-interface 192.168.1.101",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_gathered_empty(self):
        set_module_args(dict(running_config="", state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})

    def test_nxos_ntp_global_gathered(self):
        self.get_config.return_value = dedent(
            """\
            ntp trusted-key 1001
            ntp trusted-key 1002
            ntp trusted-key 1003
            ntp source-interface 192.168.1.100
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = {
            "trusted_keys": [
                {"key_id": 1001},
                {"key_id": 1002},
                {"key_id": 1003},
            ],
            "source_interface": "192.168.1.100",
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_ntp_global_parsed(self):
        cfg = dedent(
            """\
            ntp trusted-key 1001
            ntp trusted-key 1002
            ntp trusted-key 1003
            ntp source-interface 192.168.1.100
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        parsed = {
            "trusted_keys": [
                {"key_id": 1001},
                {"key_id": 1002},
                {"key_id": 1003},
            ],
            "source_interface": "192.168.1.100",
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_ntp_global_linear_deleted(self):
        self.get_config.return_value = dedent(
            """\
            ntp access-group peer PeerAcl1
            ntp access-group peer PeerAcl2
            ntp access-group serve ServeAcl1
            ntp access-group serve ServeAcl2
            ntp access-group query-only QueryAcl1
            ntp access-group query-only QueryAcl2
            ntp access-group serve-only ServeOnlyAcl1
            ntp access-group serve-only ServeOnlyAcl2
            ntp allow control rate-limit 400
            ntp allow private
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "no ntp access-group peer PeerAcl1",
            "no ntp access-group peer PeerAcl2",
            "no ntp access-group serve ServeAcl1",
            "no ntp access-group serve ServeAcl2",
            "no ntp access-group query-only QueryAcl1",
            "no ntp access-group query-only QueryAcl2",
            "no ntp access-group serve-only ServeOnlyAcl1",
            "no ntp access-group serve-only ServeOnlyAcl2",
            "no ntp allow control rate-limit 400",
            "no ntp allow private",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_alias(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    servers=[
                        dict(
                            server="1.1.1.1",
                            vrf="management",
                        ),
                        dict(
                            server="1.1.1.3",
                            use_vrf="v200",
                        ),
                    ],
                    peers=[
                        dict(
                            peer="192.168.1.1",
                            vrf="default",
                        ),
                        dict(
                            peer="192.168.1.2",
                            use_vrf="v200",
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ntp server 1.1.1.1 use-vrf management",
            "ntp server 1.1.1.3 use-vrf v200",
            "ntp peer 192.168.1.1 use-vrf default",
            "ntp peer 192.168.1.2 use-vrf v200",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_ntp_global_alias_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            ntp server 1.1.1.1 use-vrf management
            ntp server 1.1.1.3 use-vrf v200
            ntp peer 192.168.1.1 use-vrf default
            ntp peer 192.168.1.2 use-vrf v200
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    servers=[
                        dict(
                            server="1.1.1.1",
                            vrf="management",
                        ),
                        dict(
                            server="1.1.1.3",
                            use_vrf="v200",
                        ),
                    ],
                    peers=[
                        dict(
                            peer="192.168.1.1",
                            vrf="default",
                        ),
                        dict(
                            peer="192.168.1.2",
                            use_vrf="v200",
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        self.execute_module(changed=False)
