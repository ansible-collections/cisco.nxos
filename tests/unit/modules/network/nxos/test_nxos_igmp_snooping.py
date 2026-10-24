# (c) 2026 Red Hat Inc.
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
from unittest import TestCase
from unittest.mock import MagicMock, patch

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.igmp_snooping.igmp_snooping import (
    Igmp_snoopingFacts,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_igmp_snooping

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

DEFAULTS = dict(
    snooping=True,
    link_local_groups_suppression=True,
    report_suppression=True,
    v3_report_suppression=False,
    vxlan=False,
    disable_nve_static_router_port=False,
    max_gq_miss=3,
    syslog_threshold=90,
    holddown_timer=210,
)

# the settings at their defaults are not shown by the device
BASE = dedent(
    """\
    ip igmp snooping vxlan
    ip igmp snooping v3-report-suppression
    no ip igmp snooping report-suppression
    ip igmp snooping group-timeout 300
    vlan configuration 100
      ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
      ip igmp snooping static-group 233.252.0.10 interface port-channel20
      ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface port-channel20
    vlan configuration 200
      ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20
    vlan configuration 300
    """,
)

BASE_NO_ORPHAN = BASE.replace("vlan configuration 300\n", "")

# what `include "^ip igmp snooping|^no ip igmp snooping"` prints on top of the globals: the indented
# lines of the blocks, without their headers
INCLUDE_OUTPUT = dedent(
    """\
    ip igmp snooping vxlan
      ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    """,
)

SECTION_OUTPUT = dedent(
    """\
    vlan configuration 100
      ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    """,
)

GROUP_10 = dict(group="233.252.0.10", interfaces=["Ethernet1/10", "port-channel20"])
GROUP_11 = dict(group="233.252.0.11", source="192.0.2.10", interfaces=["port-channel20"])
GROUP_20 = dict(group="233.252.0.20", interfaces=["Ethernet1/20"])
BASE_VLANS = [
    dict(vlan_id=100, static_groups=[GROUP_10, GROUP_11]),
    dict(vlan_id=200, static_groups=[GROUP_20]),
    dict(vlan_id=300),
]
BASE_GLOBALS = dict(
    v3_report_suppression=True,
    report_suppression=False,
    vxlan=True,
    group_timeout="300",
)
BASE_FACTS = dict(DEFAULTS, vlans=BASE_VLANS, **BASE_GLOBALS)

NO_VLAN_200 = "no vlan configuration 200"
NO_VLAN_300 = "no vlan configuration 300"
VLAN_100 = "vlan configuration 100"
GROUP_10_ETH = "ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10"
GROUP_10_PO = "ip igmp snooping static-group 233.252.0.10 interface port-channel20"
GROUP_11_PO = (
    "ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface port-channel20"
)
GROUP_TIMEOUT_300 = "ip igmp snooping group-timeout 300"
NO_GROUP_TIMEOUT_300 = "no ip igmp snooping group-timeout 300"


FULL_VLAN_CLI = dedent(
    """\
    vlan configuration 100
      no ip igmp snooping
      no ip igmp snooping explicit-tracking
      no ip igmp snooping link-local-groups-suppression
      no ip igmp snooping report-suppression
      ip igmp snooping v3-report-suppression
      ip igmp snooping fast-leave
      ip igmp snooping group-timeout 300
      ip igmp snooping proxy general-queries mrt 8
      ip igmp snooping proxy-leave use-group-address
      ip igmp snooping querier 192.0.2.1
      ip igmp snooping querier-timeout 300
      ip igmp snooping query-interval 200
      ip igmp snooping query-max-response-time 15
      ip igmp snooping startup-query-count 4
      ip igmp snooping startup-query-interval 100
      ip igmp snooping robustness-variable 3
      ip igmp snooping last-member-query-interval 2
      ip igmp snooping version 2
      ip igmp snooping mrouter interface port-channel20
      ip igmp snooping mrouter interface Ethernet1/10
      ip igmp snooping report-flood all
      ip igmp snooping report-flood interface port-channel20
      ip igmp snooping report-policy route-map RM_ONE interface port-channel20
      ip igmp snooping report-policy prefix-list PL_ONE interface Ethernet1/10
      ip igmp snooping access-group RM_TWO
      ip igmp snooping access-group prefix-list PL_TWO interface Ethernet1/11
      ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    """,
)
FULL_VLAN_FACTS = dict(
    vlan_id=100,
    snooping=False,
    explicit_tracking=False,
    link_local_groups_suppression=False,
    report_suppression=False,
    v3_report_suppression=True,
    fast_leave=True,
    group_timeout="300",
    proxy=dict(general_queries=True, mrt=8),
    proxy_leave_use_group_address=True,
    querier="192.0.2.1",
    querier_timeout=300,
    query_interval=200,
    query_max_response_time=15,
    startup_query_count=4,
    startup_query_interval=100,
    robustness_variable=3,
    last_member_query_interval=2,
    version=2,
    mrouter_interfaces=["Ethernet1/10", "port-channel20"],
    report_flood=dict(all=True, interfaces=["port-channel20"]),
    report_policy=[
        dict(policy_type="prefix_list", name="PL_ONE", interface="Ethernet1/10"),
        dict(policy_type="route_map", name="RM_ONE", interface="port-channel20"),
    ],
    access_group=[
        dict(policy_type="prefix_list", name="PL_TWO", interface="Ethernet1/11"),
        dict(policy_type="route_map", name="RM_TWO"),
    ],
    static_groups=[dict(group="233.252.0.10", interfaces=["Ethernet1/10"])],
)
FULL_GLOBAL_CLI = dedent(
    """\
    ip igmp snooping max-gq-miss 4
    ip igmp snooping syslog-threshold 70
    ip igmp snooping holddown-timer 100
    ip igmp snooping proxy general-queries
    """,
)


def _vlan(vlan_id, group, interfaces, source=None):
    entry = dict(group=group, interfaces=interfaces)
    if source:
        entry["source"] = source
    return dict(vlan_id=vlan_id, static_groups=[entry])


class TestNxosIgmpSnoopingModule(TestNxosModule):
    module = nxos_igmp_snooping
    maxDiff = None

    def setUp(self):
        super(TestNxosIgmpSnoopingModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.igmp_snooping.igmp_snooping.Igmp_snoopingFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosIgmpSnoopingModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    def _fail(self, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(failed=True)

    # facts

    def test_nxos_igmp_snooping_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_igmp_snooping_parsed_full_running_config(self):
        """Lines of other sections and of the global include output are not credited to a VLAN."""
        full = (
            "hostname sw\n"
            "interface Ethernet1/1\n"
            "  no shutdown\n"
            "  ip igmp snooping static-group 233.252.0.99 interface Ethernet1/1\n"
            + BASE
            + "vlan configuration 5-7\n"
            "  ip igmp snooping static-group 233.252.0.98 interface Ethernet1/5\n"
            "router bgp 65000\n"
            "  ip igmp snooping static-group 233.252.0.97 interface Ethernet1/6\n"
        )
        result = self._run(False, running_config=full, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_igmp_snooping_parsed_defaults(self):
        result = self._run(False, running_config="hostname sw\n", state="parsed")
        self.assertEqual(result["parsed"], DEFAULTS)

    def test_nxos_igmp_snooping_parsed_explicit_default_forms(self):
        cfg = dedent(
            """\
            ip igmp snooping
            ip igmp snooping link-local-groups-suppression
            no ip igmp snooping vxlan
            ip igmp snooping group-timeout never
            ip igmp snooping disable-nve-static-router-port
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(DEFAULTS, group_timeout="never", disable_nve_static_router_port=True),
        )

    def test_nxos_igmp_snooping_parsed_snooping_disabled(self):
        result = self._run(False, running_config="no ip igmp snooping\n", state="parsed")
        self.assertEqual(result["parsed"], dict(DEFAULTS, snooping=False))

    def test_nxos_igmp_snooping_gathered(self):
        self.get_config.return_value = BASE
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)

    def test_nxos_igmp_snooping_gathered_defaults(self):
        self.get_config.return_value = ""
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], DEFAULTS)

    # rendered

    def test_nxos_igmp_snooping_rendered(self):
        result = self._run(
            False,
            config=dict(
                snooping=True,
                link_local_groups_suppression=False,
                v3_report_suppression=True,
                vxlan=True,
                disable_nve_static_router_port=True,
                group_timeout="never",
                vlans=[
                    dict(
                        vlan_id=100,
                        static_groups=[
                            dict(group="233.252.0.10", interfaces=["Eth1/10", "Po20"]),
                            dict(
                                group="233.252.0.11",
                                source="192.0.2.10",
                                interfaces=["port-channel20"],
                            ),
                        ],
                    ),
                ],
            ),
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            [
                "ip igmp snooping",
                "no ip igmp snooping link-local-groups-suppression",
                "ip igmp snooping v3-report-suppression",
                "ip igmp snooping vxlan",
                "ip igmp snooping disable-nve-static-router-port",
                "ip igmp snooping group-timeout never",
                VLAN_100,
                GROUP_10_ETH,
                GROUP_10_PO,
                GROUP_11_PO,
            ],
        )

    def test_nxos_igmp_snooping_rendered_false_values(self):
        result = self._run(False, config=dict(snooping=False, vxlan=False), state="rendered")
        self.assertEqual(result["rendered"], ["no ip igmp snooping", "no ip igmp snooping vxlan"])

    def test_nxos_igmp_snooping_rendered_vlan_without_groups(self):
        result = self._run(False, config=dict(vlans=[dict(vlan_id=100)]), state="rendered")
        self.assertEqual(result["rendered"], [])

    def test_nxos_igmp_snooping_rendered_group_timeout_with_snooping_disabled(self):
        result = self._run(False, config=dict(snooping=False, group_timeout="10"), state="rendered")
        self.assertEqual(
            result["rendered"],
            ["ip igmp snooping group-timeout 10", "no ip igmp snooping"],
        )

    # merged

    def test_nxos_igmp_snooping_merged_from_default(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                vxlan=True,
                v3_report_suppression=True,
                group_timeout="300",
                vlans=[_vlan(100, "233.252.0.10", ["Eth1/10"])],
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "ip igmp snooping v3-report-suppression",
                "ip igmp snooping vxlan",
                GROUP_TIMEOUT_300,
                VLAN_100,
                GROUP_10_ETH,
            ],
        )

    def test_nxos_igmp_snooping_merged_idempotent_explicit_have(self):
        self.get_config.return_value = BASE
        result = self._run(False, config=dict(BASE_GLOBALS, vlans=BASE_VLANS), state="merged")
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_merged_idempotent_default_have(self):
        """Default values on a default device are a no-op and no context is entered."""
        self.get_config.return_value = ""
        result = self._run(False, config=dict(DEFAULTS, vlans=[dict(vlan_id=100)]), state="merged")
        self.assertEqual(result["commands"], [])
        self.assertNotIn("after", result)

    def test_nxos_igmp_snooping_merged_idempotent_name_variants(self):
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=dict(vlans=[_vlan(100, "233.252.0.10", ["ethernet1/10", "Po20", "Eth1/10"])]),
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_merged_adds_only(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                snooping=True,
                link_local_groups_suppression=False,
                vlans=[
                    dict(
                        vlan_id=100,
                        static_groups=[
                            dict(group="233.252.0.10", interfaces=["Eth1/11"]),
                            dict(
                                group="233.252.0.11",
                                source="192.0.2.10",
                                interfaces=["Ethernet1/10"],
                            ),
                        ],
                    ),
                    _vlan(400, "233.252.0.40", ["Po40"]),
                ],
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip igmp snooping link-local-groups-suppression",
                VLAN_100,
                "ip igmp snooping static-group 233.252.0.10 interface Ethernet1/11",
                "ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10",
                "vlan configuration 400",
                "ip igmp snooping static-group 233.252.0.40 interface port-channel40",
            ],
        )

    def test_nxos_igmp_snooping_merged_source_variant_is_distinct(self):
        """The same group with and without a source are different entries."""
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(vlans=[_vlan(100, "233.252.0.11", ["port-channel20"])]),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [VLAN_100, "ip igmp snooping static-group 233.252.0.11 interface port-channel20"],
        )

    def test_nxos_igmp_snooping_merged_duplicate_vlan_entries(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                vlans=[
                    _vlan(100, "233.252.0.10", ["Eth1/10"]),
                    _vlan(100, "233.252.0.10", ["Eth1/10", "Eth1/11"]),
                ],
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                VLAN_100,
                GROUP_10_ETH,
                "ip igmp snooping static-group 233.252.0.10 interface Ethernet1/11",
            ],
        )

    def test_nxos_igmp_snooping_merged_group_timeout_is_last(self):
        self.get_config.return_value = "no ip igmp snooping\n"
        result = self._run(
            True,
            config=dict(snooping=True, group_timeout="never", vxlan=True),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["ip igmp snooping", "ip igmp snooping vxlan", "ip igmp snooping group-timeout never"],
        )

    def test_nxos_igmp_snooping_merged_group_timeout_change(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=dict(group_timeout="500"), state="merged")
        self.assertEqual(result["commands"], ["ip igmp snooping group-timeout 500"])

    def test_nxos_igmp_snooping_merged_check_mode_sends_nothing(self):
        self.get_config.return_value = ""
        set_module_args(
            dict(config=dict(vxlan=True), state="merged", _ansible_check_mode=True),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["ip igmp snooping vxlan"])
        self.get_resource_connection.return_value.edit_config.assert_not_called()

    def test_nxos_igmp_snooping_merged_sends_commands(self):
        self.get_config.return_value = ""
        self._run(True, config=dict(vxlan=True), state="merged")
        self.get_resource_connection.return_value.edit_config.assert_called_once_with(
            candidate=["ip igmp snooping vxlan"],
        )

    # group-timeout dependency and option validation

    def test_nxos_igmp_snooping_group_timeout_with_snooping_false(self):
        self.get_config.return_value = ""
        result = self._run(True, config=dict(snooping=False, group_timeout="10"), state="merged")
        self.assertEqual(
            result["commands"],
            ["ip igmp snooping group-timeout 10", "no ip igmp snooping"],
        )

    def test_nxos_igmp_snooping_group_timeout_with_snooping_disabled_on_device(self):
        self.get_config.return_value = "no ip igmp snooping\n"
        result = self._run(True, config=dict(group_timeout="never"), state="merged")
        self.assertEqual(result["commands"], ["ip igmp snooping group-timeout never"])

    def test_nxos_igmp_snooping_group_timeout_snooping_enabled_by_want(self):
        self.get_config.return_value = "no ip igmp snooping\n"
        result = self._run(True, config=dict(snooping=True, group_timeout="10"), state="merged")
        self.assertEqual(
            result["commands"],
            ["ip igmp snooping", "ip igmp snooping group-timeout 10"],
        )

    def test_nxos_igmp_snooping_group_timeout_invalid_values(self):
        self.get_config.return_value = ""
        for value in ("0", "10081", "abc", "-5", "1.5"):
            result = self._fail(config=dict(group_timeout=value), state="merged")
            self.assertIn(
                "group_timeout must be 'never' or a number in the range 1-10080",
                result["msg"],
            )

    def test_nxos_igmp_snooping_group_timeout_normalised(self):
        self.get_config.return_value = ""
        result = self._run(True, config=dict(group_timeout=" Never "), state="merged")
        self.assertEqual(result["commands"], ["ip igmp snooping group-timeout never"])
        result = self._run(True, config=dict(group_timeout="0300"), state="merged")
        self.assertEqual(result["commands"], [GROUP_TIMEOUT_300])

    def test_nxos_igmp_snooping_vlan_id_out_of_range(self):
        self.get_config.return_value = ""
        for vlan_id in (0, 4095):
            result = self._fail(
                config=dict(vlans=[_vlan(vlan_id, "233.252.0.1", ["Eth1/1"])]),
                state="merged",
            )
            self.assertIn("vlan_id must be in the range 1-4094", result["msg"])

    def test_nxos_igmp_snooping_group_must_be_multicast(self):
        self.get_config.return_value = ""
        result = self._fail(
            config=dict(vlans=[_vlan(100, "192.0.2.1", ["Eth1/1"])]),
            state="merged",
        )
        self.assertEqual(result["msg"], "group must be a multicast address, got '192.0.2.1'")

    def test_nxos_igmp_snooping_group_must_be_ipv4(self):
        self.get_config.return_value = ""
        result = self._fail(config=dict(vlans=[_vlan(100, "ff02::1", ["Eth1/1"])]), state="merged")
        self.assertEqual(result["msg"], "group must be an IPv4 address, got 'ff02::1'")

    def test_nxos_igmp_snooping_source_must_be_ipv4(self):
        self.get_config.return_value = ""
        result = self._fail(
            config=dict(vlans=[_vlan(100, "233.252.0.1", ["Eth1/1"], source="host")]),
            state="merged",
        )
        self.assertEqual(result["msg"], "source must be an IPv4 address, got 'host'")

    def test_nxos_igmp_snooping_empty_config(self):
        for state in ("merged", "replaced", "overridden", "rendered"):
            result = self._fail(config=dict(), state=state)
            self.assertEqual(
                result["msg"],
                "value of config parameter must not be empty for state {0}".format(state),
            )

    def test_nxos_igmp_snooping_parsed_requires_running_config(self):
        result = self._fail(state="parsed")
        self.assertIn("running_config", result["msg"])

    # replaced

    def test_nxos_igmp_snooping_replaced_resets_unlisted_globals(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(vxlan=True, vlans=BASE_VLANS[:2]),
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "ip igmp snooping report-suppression",
                "no ip igmp snooping v3-report-suppression",
                NO_GROUP_TIMEOUT_300,
            ],
        )

    def test_nxos_igmp_snooping_replaced_vlan_groups(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                BASE_GLOBALS,
                vlans=[
                    dict(
                        vlan_id=100,
                        static_groups=[
                            dict(group="233.252.0.10", interfaces=["Eth1/10", "Eth1/12"]),
                            dict(group="233.252.0.12", interfaces=["Po20"]),
                        ],
                    ),
                ],
            ),
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                VLAN_100,
                "no " + GROUP_10_PO,
                "no " + GROUP_11_PO,
                "ip igmp snooping static-group 233.252.0.10 interface Ethernet1/12",
                "ip igmp snooping static-group 233.252.0.12 interface port-channel20",
            ],
        )

    def test_nxos_igmp_snooping_replaced_keeps_unlisted_vlans(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(BASE_GLOBALS, vlans=[_vlan(400, "233.252.0.40", ["Eth1/40"])]),
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "vlan configuration 400",
                "ip igmp snooping static-group 233.252.0.40 interface Ethernet1/40",
            ],
        )

    def test_nxos_igmp_snooping_replaced_vlan_without_groups_removes_block(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                BASE_GLOBALS,
                vlans=[dict(vlan_id=300), dict(vlan_id=200), dict(vlan_id=999)],
            ),
            state="replaced",
        )
        self.assertEqual(result["commands"], [NO_VLAN_300, NO_VLAN_200])

    def test_nxos_igmp_snooping_replaced_idempotent(self):
        self.get_config.return_value = BASE_NO_ORPHAN
        result = self._run(False, config=dict(BASE_GLOBALS, vlans=BASE_VLANS[:2]), state="replaced")
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_replaced_default_have_is_idempotent(self):
        """The defaults are what replaced resets to, so nothing is sent on a default device."""
        self.get_config.return_value = ""
        result = self._run(
            False,
            config=dict(snooping=True, vlans=[dict(vlan_id=100)]),
            state="replaced",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_replaced_snooping_off_removes_group_timeout_first(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(snooping=False, vxlan=True, v3_report_suppression=True),
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                NO_GROUP_TIMEOUT_300,
                "no ip igmp snooping",
                "ip igmp snooping report-suppression",
            ],
        )

    # overridden

    def test_nxos_igmp_snooping_overridden_removes_unlisted_vlans(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(BASE_GLOBALS, vlans=[BASE_VLANS[0]]),
            state="overridden",
        )
        self.assertEqual(result["commands"], [NO_VLAN_200, NO_VLAN_300])

    def test_nxos_igmp_snooping_overridden_without_vlans_removes_all_blocks(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=dict(BASE_GLOBALS), state="overridden")
        self.assertEqual(
            result["commands"],
            ["no vlan configuration 100", NO_VLAN_200, NO_VLAN_300],
        )

    def test_nxos_igmp_snooping_overridden_orphan_block(self):
        self.get_config.return_value = "vlan configuration 2990\n  ip igmp snooping static-group 233.252.0.9 interface Ethernet1/9\n"
        result = self._run(True, config=dict(vxlan=True), state="overridden")
        self.assertEqual(
            result["commands"],
            ["ip igmp snooping vxlan", "no vlan configuration 2990"],
        )

    def test_nxos_igmp_snooping_overridden_idempotent(self):
        self.get_config.return_value = BASE_NO_ORPHAN
        result = self._run(
            False,
            config=dict(BASE_GLOBALS, vlans=BASE_VLANS[:2]),
            state="overridden",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_overridden_gathered_orphan_block_is_removed(self):
        """Feeding the gathered facts back drops the block that has no static groups."""
        self.get_config.return_value = BASE
        result = self._run(True, config=BASE_FACTS, state="overridden")
        self.assertEqual(result["commands"], [NO_VLAN_300])

    def test_nxos_igmp_snooping_overridden_empty_diff_emits_nothing(self):
        self.get_config.return_value = ""
        result = self._run(False, config=dict(snooping=True), state="overridden")
        self.assertEqual(result["commands"], [])

    # deleted

    def test_nxos_igmp_snooping_deleted_everything(self):
        self.get_config.return_value = BASE
        result = self._run(True, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "ip igmp snooping report-suppression",
                "no ip igmp snooping v3-report-suppression",
                "no ip igmp snooping vxlan",
                NO_GROUP_TIMEOUT_300,
                "no vlan configuration 100",
                NO_VLAN_200,
                NO_VLAN_300,
            ],
        )

    def test_nxos_igmp_snooping_deleted_restores_snooping_before_group_timeout(self):
        self.get_config.return_value = "no ip igmp snooping\nip igmp snooping group-timeout 300\n"
        result = self._run(True, state="deleted")
        self.assertEqual(result["commands"], ["ip igmp snooping", NO_GROUP_TIMEOUT_300])

    def test_nxos_igmp_snooping_deleted_restore_to_default_is_idempotent(self):
        self.get_config.return_value = ""
        result = self._run(False, state="deleted")
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_deleted_listed_globals(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(vxlan=True, group_timeout="300", snooping=True),
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no ip igmp snooping vxlan", NO_GROUP_TIMEOUT_300])

    def test_nxos_igmp_snooping_deleted_vlan_block(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(vlans=[dict(vlan_id=200), dict(vlan_id=999)]),
            state="deleted",
        )
        self.assertEqual(result["commands"], [NO_VLAN_200])

    def test_nxos_igmp_snooping_deleted_listed_static_groups(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                vlans=[
                    dict(
                        vlan_id=100,
                        static_groups=[
                            dict(group="233.252.0.10", interfaces=["Po20", "Eth1/11"]),
                            dict(group="233.252.0.11", interfaces=["Po20"]),
                        ],
                    ),
                ],
            ),
            state="deleted",
        )
        self.assertEqual(result["commands"], [VLAN_100, "no " + GROUP_10_PO])

    def test_nxos_igmp_snooping_deleted_static_groups_not_present_emits_nothing(self):
        """Removing what is not there must not create the context (the nxos_config pitfall)."""
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=dict(
                vlans=[
                    _vlan(100, "233.252.0.99", ["Eth1/1"]),
                    _vlan(999, "233.252.0.10", ["Eth1/10"]),
                ],
            ),
            state="deleted",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_igmp_snooping_deleted_source_group(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(vlans=[_vlan(100, "233.252.0.11", ["Po20"], source="192.0.2.10")]),
            state="deleted",
        )
        self.assertEqual(result["commands"], [VLAN_100, "no " + GROUP_11_PO])

    # full option surface

    def test_full_vlan_parsed(self):
        result = self._run(False, running_config=FULL_VLAN_CLI, state="parsed")
        self.assertEqual(result["parsed"], dict(DEFAULTS, vlans=[FULL_VLAN_FACTS]))

    def test_full_vlan_gathered_round_trip_is_idempotent(self):
        self.get_config.return_value = FULL_VLAN_CLI
        for state in ["merged", "replaced", "overridden"]:
            self._run(False, config=dict(vlans=[FULL_VLAN_FACTS]), state=state)

    def test_vlan_group_timeout_is_not_global(self):
        cfg = "vlan configuration 100\n  ip igmp snooping group-timeout 300\n  ip igmp snooping proxy general-queries\n"
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                DEFAULTS,
                vlans=[dict(vlan_id=100, group_timeout="300", proxy=dict(general_queries=True))],
            ),
        )

    def test_full_global_parsed(self):
        result = self._run(False, running_config=FULL_GLOBAL_CLI, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                DEFAULTS,
                max_gq_miss=4,
                syslog_threshold=70,
                holddown_timer=100,
                proxy=dict(general_queries=True),
            ),
        )

    def test_full_global_idempotent(self):
        self.get_config.return_value = FULL_GLOBAL_CLI
        config = dict(
            max_gq_miss=4,
            syslog_threshold=70,
            holddown_timer=100,
            proxy=dict(general_queries=True),
        )
        self._run(False, config=config, state="merged")
        self._run(False, config=config, state="replaced")

    def test_global_merged_commands(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                max_gq_miss=5,
                syslog_threshold=50,
                holddown_timer=300,
                proxy=dict(general_queries=True, mrt=8),
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "ip igmp snooping max-gq-miss 5",
                "ip igmp snooping syslog-threshold 50",
                "ip igmp snooping holddown-timer 300",
                "ip igmp snooping proxy general-queries mrt 8",
            ],
        )

    def test_global_default_value_removes_the_line(self):
        self.get_config.return_value = FULL_GLOBAL_CLI
        result = self._run(
            True,
            config=dict(max_gq_miss=3, holddown_timer=210, proxy=dict(general_queries=False)),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "no ip igmp snooping max-gq-miss 4",
                "no ip igmp snooping holddown-timer 100",
                "no ip igmp snooping proxy general-queries",
            ],
        )

    def test_global_replaced_resets_unlisted(self):
        self.get_config.return_value = FULL_GLOBAL_CLI
        result = self._run(True, config=dict(syslog_threshold=70), state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "no ip igmp snooping max-gq-miss 4",
                "no ip igmp snooping holddown-timer 100",
                "no ip igmp snooping proxy general-queries",
            ],
        )

    def test_global_deleted_resets_everything(self):
        self.get_config.return_value = FULL_GLOBAL_CLI
        result = self._run(True, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "no ip igmp snooping max-gq-miss 4",
                "no ip igmp snooping syslog-threshold 70",
                "no ip igmp snooping holddown-timer 100",
                "no ip igmp snooping proxy general-queries",
            ],
        )

    def test_global_proxy_mrt_change(self):
        self.get_config.return_value = "ip igmp snooping proxy general-queries mrt 8\n"
        result = self._run(
            True,
            config=dict(proxy=dict(general_queries=True, mrt=10)),
            state="merged",
        )
        self.assertEqual(result["commands"], ["ip igmp snooping proxy general-queries mrt 10"])

    def test_vlan_merged_from_nothing(self):
        self.get_config.return_value = ""
        result = self._run(True, config=dict(vlans=[FULL_VLAN_FACTS]), state="merged")
        self.assertEqual(
            result["commands"],
            [
                VLAN_100,
                GROUP_10_ETH,
                "ip igmp snooping mrouter interface Ethernet1/10",
                "ip igmp snooping mrouter interface port-channel20",
                "ip igmp snooping report-flood all",
                "ip igmp snooping report-flood interface port-channel20",
                "ip igmp snooping report-policy prefix-list PL_ONE interface Ethernet1/10",
                "ip igmp snooping report-policy route-map RM_ONE interface port-channel20",
                "ip igmp snooping access-group prefix-list PL_TWO interface Ethernet1/11",
                "ip igmp snooping access-group RM_TWO",
                "no ip igmp snooping",
                "no ip igmp snooping link-local-groups-suppression",
                "no ip igmp snooping report-suppression",
                "ip igmp snooping v3-report-suppression",
                "no ip igmp snooping explicit-tracking",
                "ip igmp snooping fast-leave",
                "ip igmp snooping proxy-leave use-group-address",
                "ip igmp snooping querier-timeout 300",
                "ip igmp snooping query-interval 200",
                "ip igmp snooping query-max-response-time 15",
                "ip igmp snooping startup-query-count 4",
                "ip igmp snooping startup-query-interval 100",
                "ip igmp snooping robustness-variable 3",
                "ip igmp snooping last-member-query-interval 2",
                "ip igmp snooping version 2",
                "ip igmp snooping querier 192.0.2.1",
                "ip igmp snooping group-timeout 300",
                "ip igmp snooping proxy general-queries mrt 8",
            ],
        )

    def test_vlan_values_at_defaults_create_no_block(self):
        self.get_config.return_value = ""
        result = self._run(
            False,
            config=dict(
                vlans=[
                    dict(
                        vlan_id=100,
                        snooping=True,
                        explicit_tracking=True,
                        fast_leave=False,
                        version=3,
                        querier_timeout=255,
                        query_interval=125,
                        robustness_variable=2,
                    ),
                ],
            ),
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_vlan_default_value_removes_the_line(self):
        self.get_config.return_value = FULL_VLAN_CLI
        result = self._run(
            True,
            config=dict(
                vlans=[
                    dict(
                        vlan_id=100,
                        snooping=True,
                        explicit_tracking=True,
                        fast_leave=False,
                        version=3,
                        query_interval=125,
                        querier="192.0.2.1",
                    ),
                ],
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                VLAN_100,
                "ip igmp snooping",
                "ip igmp snooping explicit-tracking",
                "no ip igmp snooping fast-leave",
                "no ip igmp snooping query-interval 200",
                "no ip igmp snooping version 2",
            ],
        )

    def test_vlan_merged_changes_value(self):
        self.get_config.return_value = FULL_VLAN_CLI
        result = self._run(
            True,
            config=dict(vlans=[dict(vlan_id=100, query_interval=300, querier="192.0.2.2")]),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [VLAN_100, "ip igmp snooping query-interval 300", "ip igmp snooping querier 192.0.2.2"],
        )

    def test_vlan_replaced_resets_unlisted(self):
        self.get_config.return_value = FULL_VLAN_CLI
        result = self._run(
            True,
            config=dict(vlans=[dict(vlan_id=100, mrouter_interfaces=["Po20"], version=2)]),
            state="replaced",
        )
        commands = result["commands"]
        self.assertEqual(commands[0], VLAN_100)
        self.assertIn("no ip igmp snooping mrouter interface Ethernet1/10", commands)
        self.assertNotIn("no ip igmp snooping mrouter interface port-channel20", commands)
        self.assertIn("no ip igmp snooping report-flood all", commands)
        self.assertIn("no ip igmp snooping report-flood interface port-channel20", commands)
        self.assertIn(
            "no ip igmp snooping report-policy route-map RM_ONE interface port-channel20",
            commands,
        )
        self.assertIn("no ip igmp snooping access-group RM_TWO", commands)
        self.assertIn(
            "no ip igmp snooping access-group prefix-list PL_TWO interface Ethernet1/11",
            commands,
        )
        self.assertIn(
            "no ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10",
            commands,
        )
        self.assertIn("ip igmp snooping", commands)
        self.assertIn("no ip igmp snooping group-timeout 300", commands)
        self.assertIn("no ip igmp snooping proxy general-queries", commands)
        self.assertIn("no ip igmp snooping proxy-leave use-group-address", commands)
        self.assertIn("no ip igmp snooping querier 192.0.2.1", commands)
        self.assertIn("no ip igmp snooping startup-query-count 4", commands)
        self.assertNotIn("ip igmp snooping version 2", commands)
        self.assertNotIn("no ip igmp snooping version 2", commands)

    def test_vlan_deleted_listed_values_and_items(self):
        self.get_config.return_value = FULL_VLAN_CLI
        result = self._run(
            True,
            config=dict(
                vlans=[
                    dict(
                        vlan_id=100,
                        fast_leave=True,
                        querier="192.0.2.1",
                        mrouter_interfaces=["Po20", "Eth1/99"],
                        proxy=dict(general_queries=True),
                    ),
                ],
            ),
            state="deleted",
        )
        self.assertEqual(
            result["commands"],
            [
                VLAN_100,
                "no ip igmp snooping mrouter interface port-channel20",
                "no ip igmp snooping fast-leave",
                "no ip igmp snooping querier 192.0.2.1",
                "no ip igmp snooping proxy general-queries",
            ],
        )

    def test_vlan_only_vlan_id_with_content_in_have_is_kept_by_merged(self):
        self.get_config.return_value = FULL_VLAN_CLI
        result = self._run(False, config=dict(vlans=[dict(vlan_id=100)]), state="merged")
        self.assertEqual(result["commands"], [])

    def test_vlan_validation(self):
        cases = [
            (dict(query_interval=0), "query_interval must be in the range 1-18000"),
            (dict(version=1), "version must be in the range 2-3"),
            (dict(querier="not-an-address"), "querier must be an IPv4 address"),
            (dict(querier_timeout=70000), "querier_timeout must be in the range"),
            (dict(proxy=dict(general_queries=True, mrt=30)), "proxy mrt must be in the range 1-25"),
            (dict(proxy=dict(mrt=5)), "proxy mrt requires general_queries: true"),
            (dict(proxy=dict(general_queries=True, mrt=5)), "is the default and removes the proxy"),
            (
                dict(
                    report_policy=[dict(policy_type="route_map", name="RM", interface="Po20")],
                    access_group=[
                        dict(policy_type="prefix_list", name="PL", interface="port-channel20")
                    ],
                ),
                "only one entry per interface",
            ),
            (dict(proxy=dict(general_queries=False, mrt=5)), "cannot be combined"),
            (
                dict(report_policy=[dict(policy_type="route_map", name="RM")]),
                "",
            ),
            (
                dict(access_group=[dict(policy_type="prefix_list", name="PL")]),
                "access_group prefix_list requires an interface",
            ),
        ]
        for extra, message in cases:
            vlan = dict(vlan_id=100)
            vlan.update(extra)
            set_module_args(dict(config=dict(vlans=[vlan]), state="rendered"), ignore_provider_arg)
            result = self.execute_module(failed=True)
            self.assertIn(message, result["msg"])

    def test_global_validation(self):
        for key, value in [("max_gq_miss", 2), ("syslog_threshold", 101), ("holddown_timer", 301)]:
            result = self._fail(config={key: value}, state="rendered")
            self.assertIn("must be in the range", result["msg"])

    def test_rendered_everything(self):
        result = self._run(
            False,
            config=dict(
                max_gq_miss=4,
                proxy=dict(general_queries=True),
                vlans=[dict(vlan_id=100, version=3, mrouter_interfaces=["Po20"], fast_leave=True)],
            ),
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            [
                "ip igmp snooping max-gq-miss 4",
                "ip igmp snooping proxy general-queries",
                VLAN_100,
                "ip igmp snooping mrouter interface port-channel20",
                "ip igmp snooping fast-leave",
                "ip igmp snooping version 3",
            ],
        )


class TestNxosIgmpSnoopingFacts(TestCase):
    """The two show commands and their combination, without the module mocks."""

    def test_nxos_igmp_snooping_get_config_commands(self):
        connection = MagicMock()
        connection.get.side_effect = [SECTION_OUTPUT, INCLUDE_OUTPUT]
        facts = Igmp_snoopingFacts(MagicMock())
        text = facts.get_config(connection)
        self.assertEqual(
            [call.args[0] for call in connection.get.call_args_list],
            [
                'show running-config | section "^vlan configuration"',
                'show running-config | include "^ip igmp snooping|^no ip igmp snooping"',
            ],
        )
        parsed = facts.populate_facts(connection, {"ansible_network_resources": {}}, data=text)
        self.assertEqual(
            parsed["ansible_network_resources"]["igmp_snooping"],
            dict(DEFAULTS, vxlan=True, vlans=[_vlan(100, "233.252.0.10", ["Ethernet1/10"])]),
        )

    def test_nxos_igmp_snooping_get_config_empty_output(self):
        connection = MagicMock()
        connection.get.return_value = None
        self.assertEqual(Igmp_snoopingFacts(MagicMock()).get_config(connection), "\n")
