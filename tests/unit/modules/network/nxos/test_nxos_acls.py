#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_acls
from ansible_collections.cisco.nxos.tests.unit.modules.utils import set_module_args

from .nxos_module import TestNxosModule


class TestNxosAclsModule(TestNxosModule):
    module = nxos_acls

    def setUp(self):
        super(TestNxosAclsModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config",
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config",
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.acls.acls.Acls.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.acls.acls.AclsFacts.get_device_data",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

        v4 = """\nip access-list ACL1v4\n 10 permit ip any any\n 20 deny udp any any"""
        v6 = """\nipv6 access-list ACL1v6\n 10 permit sctp any any"""
        self.execute_show_command.return_value = dedent(v4 + v6)

    def tearDown(self):
        super(TestNxosAclsModule, self).tearDown()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_config.stop()
        self.mock_load_config.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_acls_merged(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL2v4",
                                aces=[
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        fragments=True,
                                        sequence=20,
                                        protocol="tcp",
                                        protocol_options=dict(tcp=dict(ack=True)),
                                    ),
                                    dict(
                                        destination=dict(
                                            address="1.2.2.2",
                                            wildcard_bits="0.0.255.255",
                                        ),
                                        dscp="31",
                                        grant="permit",
                                        protocol="ip",
                                        sequence="25",
                                        source=dict(
                                            address="1.1.1.1",
                                            wildcard_bits="0.0.0.255",
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(prefix="2002:2:2:2::/64"),
                                        source=dict(prefix="2002:1:1:1::/64"),
                                        sequence=30,
                                        protocol="icmp",
                                        protocol_options=dict(
                                            icmp=dict(echo_request=True),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(afi="ipv6", acls=[dict(name="ACL2v6")]),
                ],
                state="merged",
            ),
        )
        commands = [
            "ip access-list ACL2v4",
            "20 deny tcp any any ack fragments",
            "25 permit ip 1.1.1.1 0.0.0.255 1.2.2.2 0.0.255.255 dscp 31",
            "30 deny icmp 2002:1:1:1::/64 2002:2:2:2::/64 echo-request",
            "ipv6 access-list ACL2v6",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_acls_merged_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL1v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=20,
                                        protocol="udp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="ACL1v6",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="sctp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_acls_replaced(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL1v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(host="192.0.2.28"),
                                        source=dict(any=True),
                                        log=True,
                                        sequence=50,
                                        protocol="icmp",
                                        protocol_options=dict(
                                            icmp=dict(administratively_prohibited=True),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        commands = [
            "ip access-list ACL1v4",
            "no 20 deny udp any any",
            "no 10 permit ip any any",
            "50 permit icmp any host 192.0.2.28 administratively-prohibited log",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_acls_replaced_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL1v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=20,
                                        protocol="udp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="ACL1v6",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="sctp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_acls_overridden(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL2v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(host="192.0.2.28"),
                                        source=dict(any=True),
                                        log=True,
                                        sequence=50,
                                        protocol="icmp",
                                        protocol_options=dict(
                                            icmp=dict(administratively_prohibited=True),
                                        ),
                                    ),
                                    dict(remark="Overridden ACL"),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        commands = [
            "no ip access-list ACL1v4",
            "no ipv6 access-list ACL1v6",
            "ip access-list ACL2v4",
            "50 permit icmp any host 192.0.2.28 administratively-prohibited log",
            "remark Overridden ACL",
        ]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_acls_overridden_idempotent(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL1v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=20,
                                        protocol="udp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="ACL1v6",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="sctp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_acls_deletedafi(self):
        set_module_args(dict(config=[dict(afi="ipv4")], state="deleted"))
        commands = ["no ip access-list ACL1v4"]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_acls_deletedall(self):
        set_module_args(dict(config=[], state="deleted"))
        commands = ["no ipv6 access-list ACL1v6", "no ip access-list ACL1v4"]
        self.execute_module(changed=True, commands=commands)

    def test_nxos_acls_rendered(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="ACL1v4",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=20,
                                        protocol="udp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="ACL1v6",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=10,
                                        protocol="sctp",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
        )
        commands = [
            "ip access-list ACL1v4",
            "10 permit ip any any",
            "20 deny udp any any",
            "ipv6 access-list ACL1v6",
            "10 permit sctp any any",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(
            sorted(result["rendered"]),
            sorted(commands),
            result["rendered"],
        )

    def test_nxos_acls_parsed(self):
        set_module_args(
            dict(
                running_config=dedent(
                    """
                    ip access-list ACL1v4
                      statistics per-entry
                      10 permit ip any any
                      20 deny udp any any dscp AF23 precedence critical
                    """,
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "afi": "ipv4",
                "acls": [
                    {
                        "name": "ACL1v4",
                        "aces": [
                            {
                                "grant": "permit",
                                "sequence": 10,
                                "protocol": "ip",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "grant": "deny",
                                "sequence": 20,
                                "protocol": "udp",
                                "source": {"any": True},
                                "destination": {"any": True},
                                "dscp": "AF23",
                                "precedence": "critical",
                            },
                        ],
                    },
                ],
            },
        ]
        self.assertEqual(result["parsed"], compare_list, result["parsed"])

    def test_nxos_acls_gathered(self):
        self.execute_show_command.return_value = dedent(
            """\
            ip access-list ACL1v4
                10 permit ip any any
                20 deny udp any any
            ip access-list ComplicatedAcl
                10 permit tcp any range 1024 65500 192.168.0.0 0.0.0.255 eq 1700
            ipv6 access-list ACL1v6
                10 permit sctp any any
            """,
        )
        set_module_args(dict(config=[], state="gathered"))
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "acls": [
                    {
                        "name": "ACL1v6",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "sctp",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                        ],
                    },
                ],
                "afi": "ipv6",
            },
            {
                "acls": [
                    {
                        "name": "ACL1v4",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "ip",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 20,
                                "grant": "deny",
                                "protocol": "udp",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                        ],
                    },
                    {
                        "name": "ComplicatedAcl",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {
                                    "any": True,
                                    "port_protocol": {"range": {"start": "1024", "end": "65500"}},
                                },
                                "destination": {
                                    "address": "192.168.0.0",
                                    "wildcard_bits": "0.0.0.255",
                                    "port_protocol": {"eq": "1700"},
                                },
                            },
                        ],
                    },
                ],
                "afi": "ipv4",
            },
        ]
        self.assertEqual(result["gathered"], compare_list, result["gathered"])

    def test_nxos_acls_replaced_2(self):
        self.execute_show_command.return_value = dedent(
            """\
              ip access-list 99
                10 remark TEST-COMMENT-1
                20 permit ip 192.0.2.4/32 any
                30 permit ip 192.0.2.5/32 any
                40 remark TEST-COMMENT-2
                50 permit ip 198.51.100.6/32 any
                60 permit ip 198.51.100.7/32 any
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="99",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.1"),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.2"),
                                        sequence=20,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.3"),
                                        sequence=30,
                                        protocol="ip",
                                    ),
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.1"),
                                        sequence=40,
                                        protocol="ip",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
        )

        commands = [
            "ip access-list 99",
            "no 10 remark TEST-COMMENT-1",
            "no 20 permit ip host 192.0.2.4 any",
            "no 30 permit ip host 192.0.2.5 any",
            "no 40 remark TEST-COMMENT-2",
            "no 50 permit ip host 198.51.100.6 any",
            "no 60 permit ip host 198.51.100.7 any",
            "10 permit ip host 192.0.2.1 any",
            "20 permit ip host 192.0.2.2 any",
            "30 permit ip host 192.0.2.3 any",
            "40 permit ip host 192.0.2.1 any",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_nxos_acls_merged_failure(self):
        self.execute_show_command.return_value = dedent(
            """\
              ip access-list 99
                10 remark TEST-COMMENT-1
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="99",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.1"),
                                        sequence=10,
                                        protocol="ip",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )

        result = self.execute_module(failed=True)
        failure_msg = "Cannot update existing ACE 99 of ACL 10 with state merged. Please use state replaced or overridden."
        self.assertEqual(result["msg"], failure_msg)

    def test_nxos_acls_parse_remark(self):
        self.execute_show_command.return_value = dedent(
            """\
              ip access-list TEST_RESEQUENCE
                10 permit ip 10.0.0.0/24 any
                11 permit tcp 1.1.1.1/32 range 7111 9111 192.168.0.0/24 established
                20 deny tcp any eq ftp-data any eq domain
                25 permit icmp any any echo-reply
                27 permit icmp any any port-unreachable
                30 remark for resetting to default run resequence ip access-list TEST_RESEQUENCE 2 3
              ipv6 access-list TEST_RESEQUENCE_ipv6
                10 permit udp any any
                20 deny tcp any any
                30 remark for resetting to default run resequence ip access-list TEST_RESEQUENCE_ipv6 2 3
              ipv6 access-list TEST_PREFIX_HOST
                10 permit ipv6 fd00:976a::/32 any
                20 permit ipv6 2001:db8:85a3::8a2e:370:7334/128 any
              ipv6 access-list TEST_ICMPv6
                10 permit icmp any any nd-na
                20 deny icmp any any nd-ns telemetry_path
            """,
        )
        set_module_args(dict(state="gathered"))

        gathered = [
            {
                "acls": [
                    {
                        "name": "TEST_RESEQUENCE_ipv6",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "udp",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 20,
                                "grant": "deny",
                                "protocol": "tcp",
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 30,
                                "remark": "for resetting to default run resequence ip access-list TEST_RESEQUENCE_ipv6 2 3",
                            },
                        ],
                    },
                    {
                        "name": "TEST_PREFIX_HOST",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "ipv6",
                                "source": {"prefix": "fd00:976a::/32"},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "protocol": "ipv6",
                                "source": {"host": "2001:db8:85a3::8a2e:370:7334"},
                                "destination": {"any": True},
                            },
                        ],
                    },
                    {
                        "name": "TEST_ICMPv6",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "icmpv6",
                                "protocol_options": {
                                    "icmpv6": {
                                        "nd_na": True,
                                    },
                                },
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 20,
                                "grant": "deny",
                                "protocol": "icmpv6",
                                "protocol_options": {
                                    "icmpv6": {
                                        "nd_ns": True,
                                        "telemetry_path": True,
                                    },
                                },
                                "source": {"any": True},
                                "destination": {"any": True},
                            },
                        ],
                    },
                ],
                "afi": "ipv6",
            },
            {
                "acls": [
                    {
                        "name": "TEST_RESEQUENCE",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "ip",
                                "source": {"prefix": "10.0.0.0/24"},
                                "destination": {"any": True},
                            },
                            {
                                "sequence": 11,
                                "grant": "permit",
                                "protocol": "tcp",
                                "protocol_options": {"tcp": {"established": True}},
                                "source": {
                                    "host": "1.1.1.1",
                                    "port_protocol": {
                                        "range": {"end": "9111", "start": "7111"},
                                    },
                                },
                                "destination": {"prefix": "192.168.0.0/24"},
                            },
                            {
                                "sequence": 20,
                                "grant": "deny",
                                "protocol": "tcp",
                                "source": {
                                    "any": True,
                                    "port_protocol": {"eq": "ftp-data"},
                                },
                                "destination": {
                                    "any": True,
                                    "port_protocol": {"eq": "domain"},
                                },
                            },
                            {
                                "sequence": 25,
                                "grant": "permit",
                                "protocol": "icmp",
                                "protocol_options": {
                                    "icmp": {
                                        "echo_reply": True,
                                    },
                                },
                                "source": {
                                    "any": True,
                                },
                                "destination": {
                                    "any": True,
                                },
                            },
                            {
                                "sequence": 27,
                                "grant": "permit",
                                "protocol": "icmp",
                                "protocol_options": {
                                    "icmp": {
                                        "port_unreachable": True,
                                    },
                                },
                                "source": {
                                    "any": True,
                                },
                                "destination": {
                                    "any": True,
                                },
                            },
                            {
                                "sequence": 30,
                                "remark": "for resetting to default run resequence ip access-list TEST_RESEQUENCE 2 3",
                            },
                        ],
                    },
                ],
                "afi": "ipv4",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_acls_icmpv6_1(self):
        self.execute_show_command.return_value = dedent(
            """\
              ipv6 access-list TEST_ICMPv6
                20 deny icmp any any nd-ns telemetry_path
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv6",
                        acls=[
                            dict(
                                name="TEST_ICMPv6",
                                aces=[
                                    dict(
                                        grant="permit",
                                        destination=dict(any=True),
                                        source=dict(host="192.0.2.1"),
                                        sequence=10,
                                        protocol="icmpv6",
                                        protocol_options=dict(
                                            icmpv6=dict(
                                                nd_na=True,
                                            ),
                                        ),
                                    ),
                                    dict(
                                        grant="deny",
                                        destination=dict(any=True),
                                        source=dict(any=True),
                                        sequence=20,
                                        protocol="icmpv6",
                                        protocol_options=dict(
                                            icmpv6=dict(
                                                nd_ns=True,
                                                telemetry_path=True,
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )

        commands = [
            "ipv6 access-list TEST_ICMPv6",
            "10 permit icmp host 192.0.2.1 any nd-na",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_acls_ranges(self):
        self.execute_show_command.return_value = dedent(
            """\
              ip access-list acl1
                10 permit tcp any any range ftp-data ftp
                20 permit tcp any range ftp-data ftp any range telnet time
                30 permit tcp any range ftp-data ftp any
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
        )

        gathered = [
            {
                "acls": [
                    {
                        "name": "acl1",
                        "aces": [
                            {
                                "sequence": 10,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {
                                    "any": True,
                                },
                                "destination": {
                                    "any": True,
                                    "port_protocol": {
                                        "range": {
                                            "start": "ftp-data",
                                            "end": "ftp",
                                        },
                                    },
                                },
                            },
                            {
                                "sequence": 20,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {
                                    "any": True,
                                    "port_protocol": {
                                        "range": {
                                            "start": "ftp-data",
                                            "end": "ftp",
                                        },
                                    },
                                },
                                "destination": {
                                    "any": True,
                                    "port_protocol": {
                                        "range": {
                                            "start": "telnet",
                                            "end": "time",
                                        },
                                    },
                                },
                            },
                            {
                                "sequence": 30,
                                "grant": "permit",
                                "protocol": "tcp",
                                "source": {
                                    "any": True,
                                    "port_protocol": {
                                        "range": {
                                            "start": "ftp-data",
                                            "end": "ftp",
                                        },
                                    },
                                },
                                "destination": {
                                    "any": True,
                                },
                            },
                        ],
                    },
                ],
                "afi": "ipv4",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_acls_protocol_conversion(self):
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        acls=[
                            dict(
                                name="SIPS_Automation_Test_ACL_Create",
                                aces=[
                                    dict(
                                        sequence=17,
                                        grant="permit",
                                        protocol="tcp",
                                        source=dict(any=True),
                                        destination=dict(
                                            prefix="10.247.12.0/24",
                                            port_protocol=dict(
                                                range=dict(
                                                    start="ftp-data",
                                                    end=23,
                                                ),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
        )
        commands = [
            "ip access-list SIPS_Automation_Test_ACL_Create",
            "17 permit tcp any 10.247.12.0/24 range ftp-data telnet",
        ]
        self.execute_module(changed=True, commands=commands)
