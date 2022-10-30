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

from ansible_collections.cisco.nxos.plugins.modules import nxos_route_maps
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import AnsibleFailJson

from .nxos_module import TestNxosModule, load_fixture, set_module_args


ignore_provider_arg = True


class TestNxosRouteMapsModule(TestNxosModule):

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

    module = nxos_route_maps

    def setUp(self):
        super(TestNxosRouteMapsModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.route_maps.route_maps.Route_mapsFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosRouteMapsModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_route_maps_linear_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                description="rmap1-permit-10",
                                continue_sequence=30,
                            ),
                            dict(
                                action="deny",
                                sequence=40,
                                description="rmap1-deny-40",
                                set=dict(
                                    as_path=dict(prepend=dict(last_as=10), tag=True),
                                    comm_list="comm1",
                                    dampening=dict(
                                        half_life=10,
                                        start_reuse_route=20,
                                        start_suppress_route=30,
                                        max_suppress_time=80,
                                    ),
                                    extcomm_list="extcomm1",
                                    forwarding_address=True,
                                ),
                            ),
                        ],
                    ),
                    dict(
                        route_map="rmap2",
                        entries=[
                            dict(
                                sequence=10,
                                action="permit",
                                set=dict(
                                    null_interface="null0",
                                    ip=dict(
                                        address=dict(prefix_list="prefixlist1"),
                                        precedence="critical",
                                    ),
                                    ipv6=dict(
                                        address=dict(prefix_list="prefixlist2"),
                                        precedence="immediate",
                                    ),
                                    label_index=20,
                                    level="level-1",
                                    local_preference=200,
                                    metric=dict(
                                        bandwidth=1000,
                                        igrp_delay_metric=90,
                                        igrp_reliability_metric=80,
                                        igrp_effective_bandwidth_metric=100,
                                        igrp_mtu=900,
                                    ),
                                    metric_type="external",
                                    nssa_only=True,
                                    origin="egp",
                                    path_selection="all",
                                    tag=10,
                                    weight=40,
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "route-map rmap1 permit 10",
            "description rmap1-permit-10",
            "continue 30",
            "route-map rmap1 deny 40",
            "description rmap1-deny-40",
            "set as-path prepend last-as 10",
            "set as-path tag",
            "set comm-list comm1 delete",
            "set dampening 10 20 30 80",
            "set extcomm-list extcomm1 delete",
            "set forwarding-address",
            "route-map rmap2 permit 10",
            "set interface null0",
            "set ip address prefix-list prefixlist1",
            "set ip precedence critical",
            "set ipv6 address prefix-list prefixlist2",
            "set ipv6 precedence immediate",
            "set label-index 20",
            "set level level-1",
            "set local-preference 200",
            "set metric 1000 90 80 100 900",
            "set metric-type external",
            "set nssa-only",
            "set origin egp",
            "set path-selection all advertise",
            "set tag 10",
            "set weight 40",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_linear_merged_idempotent(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
              set comm-list comm1 delete
              set dampening 10 20 30 80
              set extcomm-list extcomm1 delete
              set forwarding-address
            route-map rmap2 permit 10
              description rmap1-deny-40
              set interface null0
              set ip address prefix-list prefixlist1
              set ip precedence critical
              set ipv6 address prefix-list prefixlist2
              set ipv6 precedence immediate
              set label-index 20
              set level level-1
              set local-preference 200
              set metric 1000 90 80 100 900
              set metric-type external
              set nssa-only
              set origin egp
              set path-selection all advertise
              set tag 10
              set weight 40
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                description="rmap1-permit-10",
                                continue_sequence=30,
                            ),
                            dict(
                                action="deny",
                                sequence=40,
                                description="rmap1-deny-40",
                                set=dict(
                                    as_path=dict(prepend=dict(last_as=10), tag=True),
                                    comm_list="comm1",
                                    dampening=dict(
                                        half_life=10,
                                        start_reuse_route=20,
                                        start_suppress_route=30,
                                        max_suppress_time=80,
                                    ),
                                    extcomm_list="extcomm1",
                                    forwarding_address=True,
                                ),
                            ),
                        ],
                    ),
                    dict(
                        route_map="rmap2",
                        entries=[
                            dict(
                                sequence=10,
                                action="permit",
                                set=dict(
                                    null_interface="null0",
                                    ip=dict(
                                        address=dict(prefix_list="prefixlist1"),
                                        precedence="critical",
                                    ),
                                    ipv6=dict(
                                        address=dict(prefix_list="prefixlist2"),
                                        precedence="immediate",
                                    ),
                                    label_index=20,
                                    level="level-1",
                                    local_preference=200,
                                    metric=dict(
                                        bandwidth=1000,
                                        igrp_delay_metric=90,
                                        igrp_reliability_metric=80,
                                        igrp_effective_bandwidth_metric=100,
                                        igrp_mtu=900,
                                    ),
                                    metric_type="external",
                                    nssa_only=True,
                                    origin="egp",
                                    path_selection="all",
                                    tag=10,
                                    weight=40,
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], commands)

    def test_nxos_route_maps_linear_replaced(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
              set comm-list comm1 delete
              set dampening 10 20 30 80
              set extcomm-list extcomm1 delete
              set forwarding-address
            route-map rmap2 permit 10
              description rmap1-deny-40
              set interface null0
              set ip address prefix-list prefixlist1
              set ip precedence critical
              set ipv6 address prefix-list prefixlist2
              set ipv6 precedence immediate
              set label-index 20
              set level level-1
              set local-preference 200
              set metric 1000 90 80 100 900
              set metric-type external
              set nssa-only
              set origin egp
              set path-selection all advertise
              set tag 10
              set weight 40
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                description="rmap1-permit-10",
                                continue_sequence=40,
                            ),
                            dict(
                                action="deny",
                                sequence=40,
                                description="rmap1-deny-40-2",
                                set=dict(
                                    extcomm_list="extcomm2",
                                    forwarding_address=True,
                                ),
                            ),
                        ],
                    ),
                    dict(route_map="rmap2"),
                    dict(
                        route_map="rmap3",
                        entries=[
                            dict(
                                sequence=11,
                                action="deny",
                                set=dict(
                                    ip=dict(
                                        address=dict(prefix_list="prefixlist1"),
                                        precedence="critical",
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no route-map rmap2 permit 10",
            "route-map rmap1 permit 10",
            "continue 40",
            "route-map rmap1 deny 40",
            "description rmap1-deny-40-2",
            "no set as-path prepend last-as 10",
            "no set as-path tag",
            "no set comm-list comm1 delete",
            "no set dampening 10 20 30 80",
            "set extcomm-list extcomm2 delete",
            "route-map rmap3 deny 11",
            "set ip address prefix-list prefixlist1",
            "set ip precedence critical",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_parsed(self):
        # test parsed
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    route-map rmap1 permit 10
                      description rmap1-permit-10
                      continue 30
                    route-map rmap1 deny 40
                      description rmap1-deny-40
                      set as-path prepend last-as 10
                      set as-path tag
                    route-map rmap2 permit 10
                      description rmap1-deny-40
                      set interface null0
                      set ip address prefix-list prefixlist1
                      set ip precedence critical
                      set ipv6 address prefix-list prefixlist2
                      set ipv6 precedence immediate
                    """,
                ),
                state="parsed",
            ),
            ignore_provider_arg,
        )

        parsed = [
            dict(
                route_map="rmap1",
                entries=[
                    dict(
                        action="permit",
                        sequence=10,
                        description="rmap1-permit-10",
                        continue_sequence=30,
                    ),
                    dict(
                        action="deny",
                        sequence=40,
                        description="rmap1-deny-40",
                        set=dict(as_path=dict(prepend=dict(last_as=10), tag=True)),
                    ),
                ],
            ),
            dict(
                route_map="rmap2",
                entries=[
                    dict(
                        sequence=10,
                        action="permit",
                        set=dict(
                            null_interface="null0",
                            ip=dict(
                                address=dict(prefix_list="prefixlist1"),
                                precedence="critical",
                            ),
                            ipv6=dict(
                                address=dict(prefix_list="prefixlist2"),
                                precedence="immediate",
                            ),
                        ),
                    ),
                ],
            ),
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(set(result["parsed"][0]), set(parsed[0]))
        self.assertEqual(set(result["parsed"][1]), set(parsed[1]))

    def test_nxos_route_maps_gathered(self):
        # test parsed
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
            route-map rmap2 permit 10
              description rmap1-deny-40
              set interface null0
              set ip address prefix-list prefixlist1
              set ip precedence critical
              set ipv6 address prefix-list prefixlist2
              set ipv6 precedence immediate
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)

        gathered = [
            dict(
                route_map="rmap1",
                entries=[
                    dict(
                        action="permit",
                        sequence=10,
                        description="rmap1-permit-10",
                        continue_sequence=30,
                    ),
                    dict(
                        action="deny",
                        sequence=40,
                        description="rmap1-deny-40",
                        set=dict(as_path=dict(prepend=dict(last_as=10), tag=True)),
                    ),
                ],
            ),
            dict(
                route_map="rmap2",
                entries=[
                    dict(
                        sequence=10,
                        action="permit",
                        set=dict(
                            null_interface="null0",
                            ip=dict(
                                address=dict(prefix_list="prefixlist1"),
                                precedence="critical",
                            ),
                            ipv6=dict(
                                address=dict(prefix_list="prefixlist2"),
                                precedence="immediate",
                            ),
                        ),
                    ),
                ],
            ),
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(set(result["gathered"][0]), set(gathered[0]))
        self.assertEqual(set(result["gathered"][1]), set(gathered[1]))

    def test_nxos_route_maps_rendered(self):
        # test rendered
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                description="rmap1-permit-10",
                                continue_sequence=40,
                            ),
                            dict(
                                action="deny",
                                sequence=40,
                                description="rmap1-deny-40-2",
                                set=dict(
                                    extcomm_list="extcomm2",
                                    forwarding_address=True,
                                ),
                            ),
                        ],
                    ),
                    dict(
                        route_map="rmap3",
                        entries=[
                            dict(
                                sequence=11,
                                action="deny",
                                set=dict(
                                    ip=dict(
                                        address=dict(prefix_list="prefixlist1"),
                                        precedence="critical",
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="rendered",
            ),
            ignore_provider_arg,
        )
        rendered = [
            "route-map rmap1 permit 10",
            "description rmap1-permit-10",
            "continue 40",
            "route-map rmap1 deny 40",
            "description rmap1-deny-40-2",
            "set extcomm-list extcomm2 delete",
            "set forwarding-address",
            "route-map rmap3 deny 11",
            "set ip address prefix-list prefixlist1",
            "set ip precedence critical",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(set(result["rendered"]), set(rendered))

    def test_nxos_route_maps_overridden(self):
        # test overridden
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
            route-map rmap2 permit 10
              description rmap2-permit-10
              set interface null0
            route-map rmap2 permit 11
              description rmap2-permit-11
            route-map rmap3 permit 21
              description rmap3-permit-21
            route-map rmap3 permit 22
              description rmap3-permit-21
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                description="rmap1-permit-10",
                                continue_sequence=30,
                            ),
                            dict(
                                action="deny",
                                sequence=40,
                                description="rmap1-deny-40",
                                set=dict(
                                    ipv6=dict(
                                        address=dict(prefix_list="prefixlist2"),
                                        precedence="immediate",
                                    ),
                                ),
                            ),
                        ],
                    ),
                    dict(
                        route_map="rmap2",
                        entries=[
                            dict(
                                sequence=10,
                                action="permit",
                                description="rmap2-permit-10",
                                set=dict(null_interface="null0"),
                            ),
                        ],
                    ),
                ],
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no route-map rmap3 permit 21",
            "no route-map rmap3 permit 22",
            "no route-map rmap2 permit 11",
            "route-map rmap1 deny 40",
            "no set as-path prepend last-as 10",
            "no set as-path tag",
            "set ipv6 address prefix-list prefixlist2",
            "set ipv6 precedence immediate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_deleted_1(self):
        # test deleted - single route-map
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
            route-map rmap2 permit 10
              description rmap2-permit-10
              set interface null0
            route-map rmap2 permit 11
              description rmap2-permit-11
            route-map rmap3 permit 21
              description rmap3-permit-21
            route-map rmap3 permit 22
              description rmap3-permit-21
            """,
        )
        set_module_args(
            dict(config=[dict(route_map="rmap1")], state="deleted"),
            ignore_provider_arg,
        )
        commands = [
            "no route-map rmap1 permit 10",
            "no route-map rmap1 deny 40",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_deleted_2(self):
        # test deleted - all route-maps
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              description rmap1-permit-10
              continue 30
            route-map rmap1 deny 40
              description rmap1-deny-40
              set as-path prepend last-as 10
              set as-path tag
            route-map rmap2 permit 10
              description rmap2-permit-10
              set interface null0
            route-map rmap2 permit 11
              description rmap2-permit-11
            route-map rmap3 permit 21
              description rmap3-permit-21
            route-map rmap3 permit 22
              description rmap3-permit-21
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "no route-map rmap1 permit 10",
            "no route-map rmap1 deny 40",
            "no route-map rmap2 permit 10",
            "no route-map rmap2 permit 11",
            "no route-map rmap3 permit 21",
            "no route-map rmap3 permit 22",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_complex_merged(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                match=dict(
                                    as_number=dict(
                                        asn=["64455", "65546"],
                                        as_path_list=["acl1", "acl2"],
                                    ),
                                    as_path=["65565", "65578", "65590"],
                                    community=dict(community_list=["comm1", "comm2"]),
                                    evpn=dict(route_types=["1", "2-mac-ip"]),
                                    extcommunity=dict(
                                        extcommunity_list=[
                                            "extcomm1",
                                            "extcomm2",
                                        ],
                                    ),
                                    interfaces=["Ethernet1/1", "Ethernet1/2"],
                                    ip=dict(
                                        address=dict(
                                            access_list="acl1",
                                            prefix_lists=["pl1", "pl2", "pl3"],
                                        ),
                                        multicast=dict(
                                            group=dict(prefix="239.0.0.1/24"),
                                            rp=dict(
                                                prefix="209.165.201.0/27",
                                                rp_type="Bidir",
                                            ),
                                            source="192.168.1.0/24",
                                        ),
                                        next_hop=dict(prefix_lists=["pl1", "pl2"]),
                                        route_source=dict(prefix_lists=["pl3", "pl4"]),
                                    ),
                                    mac_list=["mac1", "mac2"],
                                    metric=[100, 200],
                                    ospf_area=[200, 300],
                                    route_types=["external", "inter-area"],
                                    source_protocol=["eigrp", "ospf"],
                                    tags=[10, 200],
                                ),
                            ),
                            dict(
                                action="permit",
                                sequence=20,
                                match=dict(
                                    ipv6=dict(
                                        address=dict(
                                            access_list="acl1",
                                            prefix_lists=["pl1", "pl2", "pl3"],
                                        ),
                                        multicast=dict(
                                            group=dict(prefix="239.0.0.1/24"),
                                            rp=dict(
                                                prefix="209.165.201.0/27",
                                                rp_type="Bidir",
                                            ),
                                            source="192.168.1.0/24",
                                        ),
                                        next_hop=dict(prefix_lists=["pl1", "pl2"]),
                                        route_source=dict(prefix_lists=["pl3", "pl4"]),
                                    ),
                                ),
                            ),
                            dict(
                                sequence=40,
                                action="permit",
                                set=dict(
                                    as_path=dict(prepend=dict(as_number=["65546", "78878"])),
                                    distance=dict(
                                        igp_ebgp_routes=10,
                                        internal_routes=20,
                                        local_routes=90,
                                    ),
                                    evpn=dict(gateway_ip=dict(ip="192.168.1.1")),
                                ),
                            ),
                            dict(
                                sequence=52,
                                action="permit",
                                set=dict(
                                    evpn=dict(gateway_ip=dict(use_nexthop=True)),
                                    community=dict(
                                        internet=True,
                                        number=["655:10", "655:20"],
                                        no_export=True,
                                        no_advertise=True,
                                        local_as=True,
                                        graceful_shutdown=True,
                                        additive=True,
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "route-map rmap1 permit 10",
            "match as-number as-path-list acl1 acl2",
            "match as-number 64455, 65546",
            "match as-path 65565 65578 65590",
            "match community comm1 comm2",
            "match evpn route-type 1 2-mac-ip",
            "match extcommunity extcomm1 extcomm2",
            "match interface Ethernet1/1 Ethernet1/2",
            "match ip address acl1",
            "match ip address prefix-list pl1 pl2 pl3",
            "match ip multicast source 192.168.1.0/24 group 239.0.0.1/24 rp 209.165.201.0/27 rp-type Bidir",
            "match ip next-hop prefix-list pl1 pl2",
            "match ip route-source prefix-list pl3 pl4",
            "match mac-list mac1 mac2",
            "match metric 100 200",
            "match ospf-area 200 300",
            "match route-type external inter-area",
            "match source-protocol eigrp ospf",
            "match tag 10 200",
            "route-map rmap1 permit 20",
            "match ipv6 address acl1",
            "match ipv6 address prefix-list pl1 pl2 pl3",
            "match ipv6 multicast source 192.168.1.0/24 group 239.0.0.1/24 rp 209.165.201.0/27 rp-type Bidir",
            "match ipv6 next-hop prefix-list pl1 pl2",
            "match ipv6 route-source prefix-list pl3 pl4",
            "route-map rmap1 permit 40",
            "set as-path prepend 65546 78878",
            "set distance 10 20 90",
            "set evpn gateway-ip 192.168.1.1",
            "route-map rmap1 permit 52",
            "set community internet 655:10 655:20 no-export no-advertise local-AS graceful-shutdown additive",
            "set evpn gateway-ip use-nexthop",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_complex_merged_2(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                match=dict(
                                    ip=dict(
                                        multicast=dict(
                                            group_range=dict(
                                                first="239.0.0.1",
                                                last="239.255.255.255",
                                            ),
                                            rp=dict(
                                                prefix="209.165.201.0/27",
                                                rp_type="Bidir",
                                            ),
                                            source="192.168.1.0/24",
                                        ),
                                    ),
                                    ipv6=dict(
                                        multicast=dict(
                                            group_range=dict(
                                                first="fd00:80::",
                                                last="fd00:ff:ffff:ffff::",
                                            ),
                                            rp=dict(
                                                prefix="fd00:280::/25",
                                                rp_type="Bidir",
                                            ),
                                            source="2001:db8:2000::/36",
                                        ),
                                    ),
                                ),
                                set=dict(
                                    metric=dict(
                                        bandwidth=1000,
                                        igrp_delay_metric=90,
                                        igrp_reliability_metric=80,
                                        igrp_effective_bandwidth_metric=100,
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "route-map rmap1 permit 10",
            "match ip multicast source 192.168.1.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 209.165.201.0/27 rp-type Bidir",
            "match ipv6 multicast source 2001:db8:2000::/36 group-range fd00:80:: to fd00:ff:ffff:ffff:: rp fd00:280::/25 rp-type Bidir",
            "set metric 1000 90 80 100",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_complex_replaced(self):
        # test replaced for complex attributes
        self.get_config.return_value = dedent(
            """\
            route-map rmap1 permit 10
              match ip address prefix-list pl1 pl2 pl3
              match ip multicast source 192.168.1.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 209.165.201.0/27 rp-type Bidir
              match ipv6 multicast source 2001:db8:2000::/36 group-range fd00:80:: to fd00:ff:ffff:ffff:: rp fd00:280::/25 rp-type Bidir
            """,
        )
        set_module_args(
            dict(
                config=[
                    dict(
                        route_map="rmap1",
                        entries=[
                            dict(
                                action="permit",
                                sequence=10,
                                match=dict(
                                    ip=dict(
                                        address=dict(prefix_lists=["pl4"]),
                                        multicast=dict(
                                            group=dict(prefix="239.0.0.1/24"),
                                            rp=dict(
                                                prefix="209.165.201.0/27",
                                                rp_type="Bidir",
                                            ),
                                            source="192.168.1.0/24",
                                        ),
                                    ),
                                    ipv6=dict(
                                        multicast=dict(
                                            group_range=dict(
                                                first="fd00:80::",
                                                last="fd00:ff:ffff:ffff::",
                                            ),
                                            rp=dict(
                                                prefix="fd00:280::/25",
                                                rp_type="Bidir",
                                            ),
                                            source="2001:db8:2000::/36",
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "route-map rmap1 permit 10",
            "no match ip multicast source 192.168.1.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 209.165.201.0/27 rp-type Bidir",
            "match ip multicast source 192.168.1.0/24 group 239.0.0.1/24 rp 209.165.201.0/27 rp-type Bidir",
            "no match ip address prefix-list pl1 pl2 pl3",
            "match ip address prefix-list pl4",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_route_maps_gathered_empty(self):
        # test gathered for empty config
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], [])
