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

from ansible_collections.cisco.nxos.plugins.modules import nxos_prefix_lists

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosPrefixListsModule(TestNxosModule):
    # Testing strategy
    # ------------------
    # (a) The unit tests cover `merged` and `replaced` for every attribute.
    #     Since `overridden` is essentially `replaced` but at a larger
    #     scale, these indirectly cover `overridden` as well.
    # (b) For linear attributes replaced is not valid and hence, those tests
    #     delete the attributes from the config subsection.
    # (c) The argspec for VRFs is same as the top-level spec and the config logic
    #     is re-used. Hence, those attributes are not explictly covered. However, a
    #     combination of VRF + top-level spec + AF is tested.

    module = nxos_prefix_lists

    def setUp(self):
        super(TestNxosPrefixListsModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.prefix_lists.prefix_lists.Prefix_listsFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosPrefixListsModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_prefix_lists_linear_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                description="Test plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.1.0/24",
                                    ),
                                    dict(
                                        sequence=20,
                                        action="deny",
                                        prefix="192.168.2.0/24",
                                        mask="255.255.255.0",
                                    ),
                                ],
                            ),
                            dict(
                                name="plist2",
                                entries=[
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="10.0.0.0/8",
                                        eq=8,
                                    ),
                                    dict(
                                        sequence=50,
                                        action="deny",
                                        prefix="10.0.0.8/24",
                                        ge=25,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                name="plist3",
                                description="Test plist3",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="deny",
                                        prefix="2001:db8:1000::/36",
                                        le=36,
                                    ),
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="2001:db8:2000::/36",
                                    ),
                                ],
                            ),
                            dict(
                                name="plist4",
                                entries=[
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="2001:db8:3000::/36",
                                    ),
                                    dict(
                                        sequence=50,
                                        action="deny",
                                        prefix="2001:db8:4000::/36",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "ip prefix-list plist1 description Test plist1",
            "ip prefix-list plist1 seq 10 permit 192.168.1.0/24",
            "ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0",
            "ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8",
            "ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25",
            "ipv6 prefix-list plist3 description Test plist3",
            "ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36",
            "ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36",
            "ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36",
            "ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_linear_merged_idempotent(self):
        # test merged for linear attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                description="Test plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.1.0/24",
                                    ),
                                    dict(
                                        sequence=20,
                                        action="deny",
                                        prefix="192.168.2.0/24",
                                        mask="255.255.255.0",
                                    ),
                                ],
                            ),
                            dict(
                                name="plist2",
                                entries=[
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="10.0.0.0/8",
                                        eq=8,
                                    ),
                                    dict(
                                        sequence=50,
                                        action="deny",
                                        prefix="10.0.0.8/24",
                                        ge=25,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dict(
                        afi="ipv6",
                        prefix_lists=[
                            dict(
                                name="plist3",
                                description="Test plist3",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="deny",
                                        prefix="2001:db8:1000::/36",
                                        le=36,
                                    ),
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="2001:db8:2000::/36",
                                    ),
                                ],
                            ),
                            dict(
                                name="plist4",
                                entries=[
                                    dict(
                                        sequence=20,
                                        action="permit",
                                        prefix="2001:db8:3000::/36",
                                    ),
                                    dict(
                                        sequence=50,
                                        action="deny",
                                        prefix="2001:db8:4000::/36",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_prefix_lists_merged_update(self):
        # test existing sequence with merged (should fail)
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                description="Test plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.8.0/24",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "Cannot update existing sequence 10 of prefix list plist1 with state merged."
            " Please use state replaced or overridden.",
        )

    def test_nxos_prefix_lists_replaced_update(self):
        # test existing sequence with replaced
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                description="Test plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.8.0/24",
                                    ),
                                    dict(
                                        sequence=20,
                                        action="deny",
                                        prefix="192.168.2.0/24",
                                        mask="255.255.255.0",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ip prefix-list plist1 seq 10 permit 192.168.1.0/24",
            "ip prefix-list plist1 seq 10 permit 192.168.8.0/24",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_replaced(self):
        # test replaced
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.8.0/24",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ip prefix-list plist1 description Test plist1",
            "no ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0",
            "no ip prefix-list plist1 seq 10 permit 192.168.1.0/24",
            "ip prefix-list plist1 seq 10 permit 192.168.8.0/24",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_overridden(self):
        # test overridden
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        afi="ipv4",
                        prefix_lists=[
                            dict(
                                name="plist1",
                                entries=[
                                    dict(
                                        sequence=10,
                                        action="permit",
                                        prefix="192.168.8.0/24",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no ip prefix-list plist1 description Test plist1",
            "no ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0",
            "no ip prefix-list plist1 seq 10 permit 192.168.1.0/24",
            "ip prefix-list plist1 seq 10 permit 192.168.8.0/24",
            "no ipv6 prefix-list plist4",
            "no ip prefix-list plist2",
            "no ipv6 prefix-list plist3",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_deleted_afi(self):
        # test deleted (AFI)
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(config=[dict(afi="ipv4")], state="deleted"),
            ignore_provider_arg,
        )
        commands = ["no ip prefix-list plist1", "no ip prefix-list plist2"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_deleted_prefix_list(self):
        # test deleted (prefix-list)
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(
            dict(
                config=[dict(afi="ipv6", prefix_lists=[dict(name="plist3")])],
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = ["no ipv6 prefix-list plist3"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_deleted_all(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 10 permit 192.168.1.0/24
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ip prefix-list plist2 seq 20 permit 10.0.0.0/8 eq 8
              ip prefix-list plist2 seq 50 deny 10.0.0.8/24 ge 25
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 10 deny 2001:db8:1000::/36 le 36
              ipv6 prefix-list plist3 seq 20 permit 2001:db8:2000::/36
              ipv6 prefix-list plist4 seq 20 permit 2001:db8:3000::/36
              ipv6 prefix-list plist4 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "no ip prefix-list plist1",
            "no ip prefix-list plist2",
            "no ipv6 prefix-list plist3",
            "no ipv6 prefix-list plist4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_prefix_lists_parsed(self):
        # test parsed
        cfg = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ipv6 prefix-list plist3 description Test plist3
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        parsed = [
            {
                "afi": "ipv4",
                "prefix_lists": [{"name": "plist1", "description": "Test plist1"}],
            },
            {
                "afi": "ipv6",
                "prefix_lists": [{"name": "plist3", "description": "Test plist3"}],
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_prefix_lists_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
              ip prefix-list plist1 description Test plist1
              ip prefix-list plist1 seq 20 deny 192.168.2.0/24 mask 255.255.255.0
              ipv6 prefix-list plist3 description Test plist3
              ipv6 prefix-list plist3 seq 50 deny 2001:db8:4000::/36
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = [
            {
                "afi": "ipv4",
                "prefix_lists": [
                    {
                        "name": "plist1",
                        "description": "Test plist1",
                        "entries": [
                            {
                                "sequence": 20,
                                "action": "deny",
                                "prefix": "192.168.2.0/24",
                                "mask": "255.255.255.0",
                            },
                        ],
                    },
                ],
            },
            {
                "afi": "ipv6",
                "prefix_lists": [
                    {
                        "name": "plist3",
                        "description": "Test plist3",
                        "entries": [
                            {
                                "sequence": 50,
                                "action": "deny",
                                "prefix": "2001:db8:4000::/36",
                            },
                        ],
                    },
                ],
            },
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)
