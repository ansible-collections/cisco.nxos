#
# (c) 2019, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.cisco.nxos.plugins.modules import nxos_acls
from ansible_collections.cisco.nxos.tests.unit.compat.mock import (
    patch,
    MagicMock,
)
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    set_module_args,
)
from .nxos_module import TestNxosModule
from textwrap import dedent


class TestNxosAclsModule(TestNxosModule):

    module = nxos_acls

    def setUp(self):
        super(TestNxosAclsModule, self).setUp()

        self.mock_get_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_load_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network.Config.load_config"
        )
        self.load_config = self.mock_load_config.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection"
        )
        self.get_resource_connection_config = (
            self.mock_get_resource_connection_config.start()
        )

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection"
        )
        self.get_resource_connection_facts = (
            self.mock_get_resource_connection_facts.start()
        )

        self.mock_edit_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.acls.acls.Acls.edit_config"
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.acls.acls.AclsFacts.get_device_data"
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
                                        protocol_options=dict(
                                            tcp=dict(ack=True)
                                        ),
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
                                        destination=dict(
                                            prefix="2002:2:2:2::/64"
                                        ),
                                        source=dict(prefix="2002:1:1:1::/64"),
                                        sequence=30,
                                        protocol="icmp",
                                        protocol_options=dict(
                                            icmp=dict(echo_request=True)
                                        ),
                                    ),
                                ],
                            )
                        ],
                    ),
                    dict(afi="ipv6", acls=[dict(name="ACL2v6")]),
                ],
                state="merged",
            )
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
                            )
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
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="merged",
            )
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
                                            icmp=dict(
                                                administratively_prohibited=True
                                            )
                                        ),
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="replaced",
            )
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
                            )
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
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="replaced",
            )
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
                                            icmp=dict(
                                                administratively_prohibited=True
                                            )
                                        ),
                                    ),
                                    dict(remark="Overridden ACL"),
                                ],
                            )
                        ],
                    )
                ],
                state="overridden",
            )
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
                            )
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
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="overridden",
            )
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
                            )
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
                                    )
                                ],
                            )
                        ],
                    ),
                ],
                state="rendered",
            )
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
            sorted(result["rendered"]), sorted(commands), result["rendered"]
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
                    """
                ),
                state="parsed",
            )
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
                    }
                ],
            }
        ]
        self.assertEqual(result["parsed"], compare_list, result["parsed"])

    def test_nxos_acls_gathered(self):
        set_module_args(dict(config=[], state="gathered"))
        result = self.execute_module(changed=False)
        compare_list = [
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "destination": {"any": True},
                                "sequence": 10,
                                "protocol": "sctp",
                                "source": {"any": True},
                                "grant": "permit",
                            }
                        ],
                        "name": "ACL1v6",
                    }
                ],
                "afi": "ipv6",
            },
            {
                "acls": [
                    {
                        "aces": [
                            {
                                "destination": {"any": True},
                                "sequence": 10,
                                "protocol": "ip",
                                "source": {"any": True},
                                "grant": "permit",
                            },
                            {
                                "destination": {"any": True},
                                "sequence": 20,
                                "protocol": "udp",
                                "source": {"any": True},
                                "grant": "deny",
                            },
                        ],
                        "name": "ACL1v4",
                    }
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
            """
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
                            )
                        ],
                    )
                ],
                state="replaced",
            )
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
            """
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
                                    )
                                ],
                            )
                        ],
                    )
                ],
                state="merged",
            )
        )

        result = self.execute_module(failed=True)
        failure_msg = "Cannot update existing ACE 99 of ACL 10 with state merged. Please use state replaced or overridden."
        self.assertEqual(result["msg"], failure_msg)

    def test_nxos_acls_parse_remark(self):
        self.execute_show_command.return_value = dedent(
            """\
              ip access-list TEST_RESEQUENCE
                10 permit ip 10.0.0.0/24 any
                20 deny udp any any eq domain
                30 remark for resetting to default run resequence ip access-list TEST_RESEQUENCE 2 3
              ipv6 access-list TEST_RESEQUENCE_ipv6
                10 permit udp any any
                20 deny tcp any any
                30 remark for resetting to default run resequence ip access-list TEST_RESEQUENCE_ipv6 2 3
            """
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
                    }
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
                                "sequence": 20,
                                "grant": "deny",
                                "protocol": "udp",
                                "source": {"any": True},
                                "destination": {
                                    "any": True,
                                    "port_protocol": {"eq": "domain"},
                                },
                            },
                            {
                                "sequence": 30,
                                "remark": "for resetting to default run resequence ip access-list TEST_RESEQUENCE 2 3",
                            },
                        ],
                    }
                ],
                "afi": "ipv4",
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)
