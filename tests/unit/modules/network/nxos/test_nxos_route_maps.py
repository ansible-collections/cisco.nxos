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
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_route_maps

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
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.route_maps.route_maps.Route_mapsFacts.get_config"
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
            """
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
                                    as_path=dict(
                                        prepend=dict(last_as=10), tag=True
                                    ),
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
                                        address=dict(
                                            prefix_list="prefixlist1"
                                        ),
                                        precedence="critical",
                                    ),
                                    ipv6=dict(
                                        address=dict(
                                            prefix_list="prefixlist2"
                                        ),
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
                            )
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
            """
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
                                    as_path=dict(
                                        prepend=dict(last_as=10), tag=True
                                    ),
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
                                        address=dict(
                                            prefix_list="prefixlist1"
                                        ),
                                        precedence="critical",
                                    ),
                                    ipv6=dict(
                                        address=dict(
                                            prefix_list="prefixlist2"
                                        ),
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
                            )
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
            """
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
                                        address=dict(
                                            prefix_list="prefixlist1"
                                        ),
                                        precedence="critical",
                                    )
                                ),
                            )
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
                    """
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
                        set=dict(
                            as_path=dict(prepend=dict(last_as=10), tag=True)
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
                        ),
                    )
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
            """
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
                        set=dict(
                            as_path=dict(prepend=dict(last_as=10), tag=True)
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
                        ),
                    )
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
                                        address=dict(
                                            prefix_list="prefixlist1"
                                        ),
                                        precedence="critical",
                                    )
                                ),
                            )
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
            """
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
                                        address=dict(
                                            prefix_list="prefixlist2"
                                        ),
                                        precedence="immediate",
                                    )
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
                            )
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
            """
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
            """
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
