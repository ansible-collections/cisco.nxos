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

from ansible_collections.cisco.nxos.plugins.modules import nxos_bgp_templates

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosBgpTemplatesModule(TestNxosModule):
    module = nxos_bgp_templates

    def setUp(self):
        super(TestNxosBgpTemplatesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bgp_templates.bgp_templates.Bgp_templatesFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosBgpTemplatesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_bgp_templates_merged(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            description="test-neighbor-template",
                            bfd=dict(
                                singlehop=True,
                                multihop=dict(
                                    interval=dict(
                                        tx_interval=300,
                                        min_rx_interval=258,
                                        multiplier=12,
                                    ),
                                ),
                            ),
                            bmp_activate_server=12,
                            capability=dict(
                                suppress_4_byte_as=True,
                            ),
                            disable_connected_check=True,
                            dont_capability_negotiate=True,
                            dscp="cs1",
                            dynamic_capability=True,
                            ebgp_multihop=5,
                            graceful_shutdown=dict(
                                activate=dict(
                                    route_map="rmap1",
                                ),
                            ),
                            inherit=dict(peer_session="peer_sess_1"),
                            local_as="65535",
                            log_neighbor_changes=dict(
                                disable=True,
                            ),
                            low_memory=dict(
                                exempt=True,
                            ),
                            password=dict(
                                encryption=7,
                                key="095C4F1A0A1218000F",
                            ),
                            path_attribute=[
                                dict(
                                    action="discard",
                                    type=10,
                                ),
                                dict(
                                    action="treat-as-withdraw",
                                    range=dict(
                                        start=10,
                                        end=15,
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            name="tmplt_2",
                            bfd=dict(
                                set=True,
                            ),
                            remote_as="65534",
                            remove_private_as=dict(
                                replace_as=True,
                            ),
                            shutdown=True,
                            timers=dict(
                                keepalive=200,
                                holdtime=300,
                            ),
                            transport=dict(connection_mode=dict(passive=True)),
                            ttl_security=dict(
                                hops=10,
                            ),
                            update_source="Ethernet1/1",
                        ),
                        dict(
                            name="tmplt_3",
                            bfd=dict(
                                multihop=dict(
                                    set=True,
                                ),
                            ),
                            address_family=[
                                dict(
                                    afi="l2vpn",
                                    safi="evpn",
                                    send_community="both",
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "template peer tmplt_1",
            "bfd singlehop",
            "bfd multihop interval 300 min_rx 258 multiplier 12",
            "bmp-activate-server 12",
            "capability suppress 4-byte-as",
            "description test-neighbor-template",
            "disable-connected-check",
            "dont-capability-negotiate",
            "dscp cs1",
            "dynamic-capability",
            "ebgp-multihop 5",
            "graceful-shutdown activate route-map rmap1",
            "inherit peer-session peer_sess_1",
            "local-as 65535",
            "log-neighbor-changes disable",
            "low-memory exempt",
            "password 7 095C4F1A0A1218000F",
            "path-attribute discard 10 in",
            "path-attribute treat-as-withdraw range 10 15 in",
            "template peer tmplt_2",
            "bfd",
            "remote-as 65534",
            "remove-private-as replace-as",
            "shutdown",
            "timers 200 300",
            "transport connection-mode passive",
            "ttl-security hops 10",
            "update-source Ethernet1/1",
            "template peer tmplt_3",
            "bfd multihop",
            "address-family l2vpn evpn",
            "send-community",
            "send-community extended",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_templates_merged_idempotent(self):
        self.get_config.return_value = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                  bmp-activate-server 12
                  capability suppress 4-byte-as
                  description test-neighbor-template
                  disable-connected-check
                  dont-capability-negotiate
                  dscp cs1
                  dynamic-capability
                  ebgp-multihop 5
                  graceful-shutdown activate route-map rmap1
                  inherit peer-session peer_sess_1
                  local-as 65535
                  log-neighbor-changes disable
                  low-memory exempt
                  password 7 095C4F1A0A1218000F
                  path-attribute discard 10 in
                  path-attribute treat-as-withdraw range 10 15 in
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
                  shutdown
                  timers 200 300
                  transport connection-mode passive
                  ttl-security hops 10
                  update-source Ethernet1/1
                template peer tmplt_3
                  bfd multihop
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            description="test-neighbor-template",
                            bfd=dict(
                                singlehop=True,
                                multihop=dict(
                                    interval=dict(
                                        tx_interval=300,
                                        min_rx_interval=258,
                                        multiplier=12,
                                    ),
                                ),
                            ),
                            bmp_activate_server=12,
                            capability=dict(
                                suppress_4_byte_as=True,
                            ),
                            disable_connected_check=True,
                            dont_capability_negotiate=True,
                            dscp="cs1",
                            dynamic_capability=True,
                            ebgp_multihop=5,
                            graceful_shutdown=dict(
                                activate=dict(
                                    route_map="rmap1",
                                ),
                            ),
                            inherit=dict(peer_session="peer_sess_1"),
                            local_as="65535",
                            log_neighbor_changes=dict(
                                disable=True,
                            ),
                            low_memory=dict(
                                exempt=True,
                            ),
                            password=dict(
                                encryption=7,
                                key="095C4F1A0A1218000F",
                            ),
                            path_attribute=[
                                dict(
                                    action="discard",
                                    type=10,
                                ),
                                dict(
                                    action="treat-as-withdraw",
                                    range=dict(
                                        start=10,
                                        end=15,
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            name="tmplt_2",
                            bfd=dict(
                                set=True,
                            ),
                            remote_as="65534",
                            remove_private_as=dict(
                                replace_as=True,
                            ),
                            shutdown=True,
                            timers=dict(
                                keepalive=200,
                                holdtime=300,
                            ),
                            transport=dict(connection_mode=dict(passive=True)),
                            ttl_security=dict(
                                hops=10,
                            ),
                            update_source="Ethernet1/1",
                        ),
                        dict(
                            name="tmplt_3",
                            bfd=dict(
                                multihop=dict(
                                    set=True,
                                ),
                            ),
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_templates_deleted_single(self):
        self.get_config.return_value = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                  bmp-activate-server 12
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
            """,
        )
        set_module_args(
            dict(
                config=dict(as_number="65536", neighbor=[dict(name="tmplt_1")]),
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "no template peer tmplt_1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_templates_deleted_all(self):
        self.get_config.return_value = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                  bmp-activate-server 12
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
            """,
        )
        set_module_args(
            dict(
                state="deleted",
            ),
            ignore_provider_arg,
        )
        commands = ["router bgp 65536", "no template peer tmplt_1", "no template peer tmplt_2"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_templates_overridden(self):
        self.get_config.return_value = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
                  path-attribute discard 10 in
                  path-attribute treat-as-withdraw range 10 15 in
                template peer tmplt_3
                  remote-as 65533
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            bfd=dict(
                                singlehop=True,
                                multihop=dict(
                                    interval=dict(
                                        tx_interval=300,
                                        min_rx_interval=258,
                                        multiplier=12,
                                    ),
                                ),
                            ),
                        ),
                        dict(
                            name="tmplt_2",
                            remote_as="65534",
                            path_attribute=[
                                dict(
                                    action="discard",
                                    type=10,
                                ),
                            ],
                        ),
                    ],
                ),
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "no template peer tmplt_3",
            "template peer tmplt_2",
            "no bfd",
            "no remove-private-as replace-as",
            "no path-attribute treat-as-withdraw range 10 15 in",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_templates_gathered(self):
        self.get_config.return_value = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
                  path-attribute discard 10 in
            """,
        )
        set_module_args(
            dict(
                state="gathered",
            ),
            ignore_provider_arg,
        )
        gathered = dict(
            as_number="65536",
            neighbor=[
                dict(
                    name="tmplt_1",
                    bfd=dict(
                        singlehop=True,
                        multihop=dict(
                            interval=dict(
                                tx_interval=300,
                                min_rx_interval=258,
                                multiplier=12,
                            ),
                        ),
                    ),
                ),
                dict(
                    name="tmplt_2",
                    bfd=dict(
                        set=True,
                    ),
                    remote_as="65534",
                    path_attribute=[
                        dict(
                            action="discard",
                            type=10,
                        ),
                    ],
                    remove_private_as=dict(
                        replace_as=True,
                    ),
                ),
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_bgp_templates_parsed(self):
        run_cfg = dedent(
            """\
              router bgp 65536
                template peer tmplt_1
                  bfd singlehop
                  bfd multihop interval 300 min_rx 258 multiplier 12
                template peer tmplt_2
                  bfd
                  remote-as 65534
                  remove-private-as replace-as
                  path-attribute discard 10 in
            """,
        )
        set_module_args(
            dict(
                running_config=run_cfg,
                state="parsed",
            ),
            ignore_provider_arg,
        )
        parsed = dict(
            as_number="65536",
            neighbor=[
                dict(
                    name="tmplt_1",
                    bfd=dict(
                        singlehop=True,
                        multihop=dict(
                            interval=dict(
                                tx_interval=300,
                                min_rx_interval=258,
                                multiplier=12,
                            ),
                        ),
                    ),
                ),
                dict(
                    name="tmplt_2",
                    bfd=dict(
                        set=True,
                    ),
                    remote_as="65534",
                    path_attribute=[
                        dict(
                            action="discard",
                            type=10,
                        ),
                    ],
                    remove_private_as=dict(
                        replace_as=True,
                    ),
                ),
            ],
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_bgp_templates_af(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            description="test-neighbor-template",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    advertise_map=dict(
                                        route_map="rmap1",
                                        exist_map="rmap2",
                                    ),
                                    advertisement_interval=100,
                                    allowas_in=dict(
                                        max_occurences=10,
                                    ),
                                    as_override=True,
                                    capability=dict(
                                        additional_paths=dict(
                                            receive="disable",
                                            send="disable",
                                        ),
                                    ),
                                    default_originate=dict(
                                        route_map="rmap1",
                                    ),
                                    disable_peer_as_check=True,
                                    filter_list=dict(
                                        inbound="flist1",
                                        outbound="flist2",
                                    ),
                                    inherit=dict(
                                        peer_policy="tmplt_policy_1",
                                    ),
                                ),
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    maximum_prefix=dict(
                                        max_prefix_limit=10,
                                        generate_warning_threshold=80,
                                        restart_interval=60,
                                        warning_only=True,
                                    ),
                                    next_hop_self=dict(
                                        all_routes=True,
                                    ),
                                    next_hop_third_party=True,
                                    prefix_list=dict(
                                        inbound="plist1",
                                        outbound="plist2",
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            name="tmplt_2",
                            description="test-neighbor-template-2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    route_map=dict(
                                        inbound="rmap1",
                                        outbound="rmap2",
                                    ),
                                    route_reflector_client=True,
                                    soft_reconfiguration_inbound=dict(
                                        always=True,
                                    ),
                                    soo="test",
                                    suppress_inactive=True,
                                    unsuppress_map="rmap1",
                                    weight=2,
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "template peer tmplt_1",
            "description test-neighbor-template",
            "address-family ipv4 unicast",
            "advertise-map rmap1 exist-map rmap2",
            "advertisement-interval 100",
            "allowas-in 10",
            "as-override",
            "capability additional-paths receive disable",
            "capability additional-paths send disable",
            "default-originate route-map rmap1",
            "disable-peer-as-check",
            "filter-list flist1 in",
            "filter-list flist2 out",
            "inherit peer-policy tmplt_policy_1",
            "address-family ipv4 multicast",
            "maximum-prefix 10 80 restart 60 warning-only",
            "next-hop-self all",
            "next-hop-third-party",
            "prefix-list plist1 in",
            "prefix-list plist2 out",
            "template peer tmplt_2",
            "description test-neighbor-template-2",
            "address-family ipv4 unicast",
            "route-map rmap1 in",
            "route-map rmap2 out",
            "route-reflector-client",
            "soft-reconfiguration inbound always",
            "soo test",
            "suppress-inactive",
            "unsuppress-map rmap1",
            "weight 2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_templates_af_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
            template peer tmplt_1
              description test-neighbor-template
              address-family ipv4 unicast
                advertise-map rmap1 exist-map rmap2
                advertisement-interval 100
                allowas-in 10
                as-override
                capability additional-paths receive disable
                capability additional-paths send disable
                default-originate route-map rmap1
                disable-peer-as-check
                filter-list flist1 in
                filter-list flist2 out
                inherit peer-policy tmplt_policy_1
              address-family ipv4 multicast
                maximum-prefix 10 80 restart 60 warning-only
                next-hop-self all
                no next-hop-third-party
                prefix-list plist1 in
                prefix-list plist2 out
            template peer tmplt_2
              description test-neighbor-template-2
              address-family ipv4 unicast
                route-map rmap1 in
                route-map rmap2 out
                route-reflector-client
                soft-reconfiguration inbound always
                soo test
                suppress-inactive
                unsuppress-map rmap1
                weight 2
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            description="test-neighbor-template",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    advertise_map=dict(
                                        route_map="rmap1",
                                        exist_map="rmap2",
                                    ),
                                    advertisement_interval=100,
                                    allowas_in=dict(
                                        max_occurences=10,
                                    ),
                                    as_override=True,
                                    capability=dict(
                                        additional_paths=dict(
                                            receive="disable",
                                            send="disable",
                                        ),
                                    ),
                                    default_originate=dict(
                                        route_map="rmap1",
                                    ),
                                    disable_peer_as_check=True,
                                    filter_list=dict(
                                        inbound="flist1",
                                        outbound="flist2",
                                    ),
                                    inherit=dict(
                                        peer_policy="tmplt_policy_1",
                                    ),
                                ),
                                dict(
                                    afi="ipv4",
                                    safi="multicast",
                                    maximum_prefix=dict(
                                        max_prefix_limit=10,
                                        generate_warning_threshold=80,
                                        restart_interval=60,
                                        warning_only=True,
                                    ),
                                    next_hop_self=dict(
                                        all_routes=True,
                                    ),
                                    next_hop_third_party=False,
                                    prefix_list=dict(
                                        inbound="plist1",
                                        outbound="plist2",
                                    ),
                                ),
                            ],
                        ),
                        dict(
                            name="tmplt_2",
                            description="test-neighbor-template-2",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    route_map=dict(
                                        inbound="rmap1",
                                        outbound="rmap2",
                                    ),
                                    route_reflector_client=True,
                                    soft_reconfiguration_inbound=dict(
                                        always=True,
                                    ),
                                    soo="test",
                                    suppress_inactive=True,
                                    unsuppress_map="rmap1",
                                    weight=2,
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_templates_send_comm(self):
        self.get_config.return_value = dedent(
            """\
            router bgp 65536
            template peer tmplt_1
              address-family ipv4 unicast
                send-community
                send-community extended
            template peer tmplt_2
              address-family l2vpn evpn
                send-community extended
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    neighbor=[
                        dict(
                            name="tmplt_1",
                            address_family=[
                                dict(
                                    afi="ipv4",
                                    safi="unicast",
                                    send_community="both",
                                ),
                            ],
                        ),
                        dict(
                            name="tmplt_2",
                            address_family=[
                                dict(
                                    afi="l2vpn",
                                    safi="evpn",
                                    send_community="standard",
                                ),
                            ],
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "template peer tmplt_2",
            "address-family l2vpn evpn",
            "no send-community extended",
            "send-community",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
