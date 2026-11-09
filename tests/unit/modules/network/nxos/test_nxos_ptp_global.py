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
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_ptp_global

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

# `show running-config | include "^ptp|^no ptp"` of a switch with many settings, the order
# is the one of the device
BASE = dedent(
    """\
    ptp source 192.0.2.1
    ptp priority1 100
    ptp priority2 120
    ptp notification type gm-change
    ptp notification type high-correction interval 60
    ptp correction-range 5000
    ptp correction-range logging
    ptp clock periodic-update interval 60
    ptp mean-path-delay 5000
    ptp domain 5
    ptp time distribution-hold correction-threshold 500 delay-threshold 100
    ptp delay tolerance mean-path 10.50
    no ptp management
    """,
)

BASE_FACTS = dict(
    source=dict(ipv4=dict(address="192.0.2.1")),
    priority1=100,
    priority2=120,
    notification=dict(
        gm_change=True,
        high_correction=dict(enabled=True, interval="60"),
    ),
    correction_range=dict(value=5000, logging=True),
    clock_periodic_update=dict(enabled=True, interval=60),
    mean_path_delay=5000,
    domain=5,
    time_distribution_hold=dict(enabled=True, correction_threshold=500, delay_threshold=100),
    delay_tolerance=dict(mean_path="10.50"),
    management=False,
)

SMALL = dedent(
    """\
    ptp source 192.0.2.1
    ptp priority1 90
    """,
)


class TestNxosPtpGlobalModule(TestNxosModule):
    module = nxos_ptp_global

    def setUp(self):
        super(TestNxosPtpGlobalModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ptp_global.ptp_global.Ptp_globalFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosPtpGlobalModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    def _fail(self, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(failed=True)

    # facts

    def test_nxos_ptp_global_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_ptp_global_gathered(self):
        self.get_config.return_value = BASE
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)

    def test_nxos_ptp_global_gathered_nothing(self):
        self.get_config.return_value = ""
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], {})

    def test_nxos_ptp_global_parsed_source_forms(self):
        cfg = dedent(
            """\
            ptp source 192.0.2.1 vrf management
            ptp source 2001:db8::1
            ptp notification type high-correction
            ptp notification type parent-change
            ptp notification type port-state-change
            ptp clock periodic-update
            ptp time distribution-hold
            ptp time distribution-hold correction-threshold 500
            ptp delay tolerance reverse-path 100.00
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                source=dict(
                    ipv4=dict(address="192.0.2.1", vrf="management"),
                    ipv6=dict(address="2001:db8::1"),
                ),
                notification=dict(
                    high_correction=dict(enabled=True),
                    parent_change=True,
                    port_state_change=True,
                ),
                clock_periodic_update=dict(enabled=True),
                time_distribution_hold=dict(enabled=True, correction_threshold=500),
                delay_tolerance=dict(reverse_path="100.00"),
            ),
        )

    def test_nxos_ptp_global_parsed_lines_with_trailing_spaces(self):
        # the device displays some lines with trailing spaces
        cfg = (
            "ptp notification type high-correction interval 60  \n"
            "ptp notification type parent-change \n"
            "ptp clock periodic-update \n"
            "ptp unicast-negotiation\n"
            "ptp ipv6 multicast scope rx 0x2-0xE\n"
            "ptp ipv6 multicast scope tx 0xE\n"
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                notification=dict(
                    parent_change=True,
                    high_correction=dict(enabled=True, interval="60"),
                ),
                clock_periodic_update=dict(enabled=True),
                unicast_negotiation=True,
                ipv6_multicast_scope=dict(rx="0x2-0xE", tx="0xE"),
            ),
        )

    def test_nxos_ptp_global_the_default_periodic_update_interval_is_not_displayed(self):
        # `ptp clock periodic-update interval 60` is stored as `ptp clock periodic-update`
        self.get_config.return_value = "ptp clock periodic-update \n"
        for state in ["merged", "replaced"]:
            self._run(False, config=dict(clock_periodic_update=dict(interval=60)), state=state)
        self.get_config.return_value = "ptp clock periodic-update interval 100\n"
        result = self._run(
            True,
            config=dict(clock_periodic_update=dict(interval=60)),
            state="merged",
        )
        self.assertEqual(result["commands"], ["ptp clock periodic-update"])

    def test_nxos_ptp_global_high_correction_with_trailing_spaces_is_idempotent(self):
        self.get_config.return_value = "ptp notification type high-correction interval 60  \n"
        for state in ["merged", "replaced"]:
            self._run(
                False,
                config=dict(notification=dict(high_correction=dict(interval="60"))),
                state=state,
            )

    def test_nxos_ptp_global_unicast_negotiation_and_ipv6_scope(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                unicast_negotiation=True,
                ipv6_multicast_scope=dict(rx="0x2-0xe", tx="0xe"),
            ),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "ptp unicast-negotiation",
                    "ptp ipv6 multicast scope rx 0x2-0xE",
                    "ptp ipv6 multicast scope tx 0xE",
                ],
            ),
        )
        # the same as the device displays it is idempotent, whatever the case
        self.get_config.return_value = "ptp unicast-negotiation\nptp ipv6 multicast scope rx 0x2,0x5\nptp ipv6 multicast scope tx 0x2\n"
        self._run(
            False,
            config=dict(
                unicast_negotiation=True,
                ipv6_multicast_scope=dict(rx="0x2, 0x5", tx="0x2"),
            ),
            state="merged",
        )

    def test_nxos_ptp_global_ipv6_scope_default_values_are_removed(self):
        self.get_config.return_value = (
            "ptp ipv6 multicast scope rx 0x2-0x4\nptp ipv6 multicast scope tx 0x2\n"
        )
        result = self._run(
            True,
            config=dict(ipv6_multicast_scope=dict(rx="0x1-0xe", tx="0x1")),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                ["no ptp ipv6 multicast scope rx 0x2-0x4", "no ptp ipv6 multicast scope tx 0x2"],
            ),
        )
        self.get_config.return_value = ""
        self._run(
            False,
            config=dict(ipv6_multicast_scope=dict(rx="0x1-0xE", tx="0x1")),
            state="merged",
        )

    def test_nxos_ptp_global_ipv6_scope_validation(self):
        for config in (
            dict(rx="0x0"),
            dict(rx="0xf"),
            dict(rx="2-4"),
            dict(tx="0x2-0x3"),
            dict(tx="0xf"),
        ):
            result = self._fail(config=dict(ipv6_multicast_scope=config), state="rendered")
            self.assertIn("ipv6_multicast_scope", result["msg"])

    # rendered

    def test_nxos_ptp_global_rendered(self):
        result = self._run(
            False,
            config=dict(
                source=dict(ipv4=dict(address="192.0.2.1", vrf="management")),
                domain=5,
                priority1=100,
                management=False,
                correction_range=dict(value=5000, logging=True),
                delay_tolerance=dict(mean_path="10.5"),
                notification=dict(high_correction=dict(interval="immediate")),
                clock_periodic_update=dict(interval=30),
                time_distribution_hold=dict(correction_threshold=500, delay_threshold=100),
            ),
            state="rendered",
        )
        self.assertEqual(
            sorted(result["rendered"]),
            sorted(
                [
                    "ptp source 192.0.2.1 vrf management",
                    "ptp domain 5",
                    "ptp priority1 100",
                    "no ptp management",
                    "ptp correction-range 5000",
                    "ptp correction-range logging",
                    "ptp delay tolerance mean-path 10.50",
                    "ptp notification type high-correction interval immediate",
                    "ptp clock periodic-update interval 30",
                    "ptp time distribution-hold correction-threshold 500 delay-threshold 100",
                ],
            ),
        )

    def test_nxos_ptp_global_rendered_defaults_send_nothing(self):
        result = self._run(
            False,
            config=dict(domain=0, priority1=255, priority2=255, management=True),
            state="rendered",
        )
        self.assertEqual(result["rendered"], [])

    # merged

    def test_nxos_ptp_global_merged_from_empty(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                source=dict(ipv4=dict(address="192.0.2.1")),
                domain=5,
                priority1=100,
                notification=dict(gm_change=True),
            ),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "ptp source 192.0.2.1",
                    "ptp domain 5",
                    "ptp priority1 100",
                    "ptp notification type gm-change",
                ],
            ),
        )

    def test_nxos_ptp_global_merged_idempotent_with_the_gathered_data(self):
        self.get_config.return_value = BASE
        for state in ["merged", "replaced", "overridden"]:
            self._run(False, config=BASE_FACTS, state=state)

    def test_nxos_ptp_global_merged_changes_a_value_without_removing_the_old_one(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=dict(priority1=50), state="merged")
        self.assertEqual(result["commands"], ["ptp priority1 50"])

    def test_nxos_ptp_global_merged_default_value_and_false_remove_the_setting(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                domain=0,
                management=True,
                correction_range=dict(logging=False),
                notification=dict(gm_change=False),
                clock_periodic_update=dict(enabled=False),
            ),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "no ptp domain 5",
                    "ptp management",
                    "no ptp correction-range logging",
                    "no ptp notification type gm-change",
                    "no ptp clock periodic-update",
                ],
            ),
        )

    def test_nxos_ptp_global_merged_default_and_false_on_a_clean_switch_send_nothing(self):
        self.get_config.return_value = ""
        self._run(
            False,
            config=dict(domain=0, priority2=255, management=True),
            state="merged",
        )

    def test_nxos_ptp_global_merged_management_off_is_idempotent(self):
        self.get_config.return_value = "no ptp management\n"
        self._run(False, config=dict(management=False), state="merged")

    def test_nxos_ptp_global_merged_source_with_vrf_and_ipv6(self):
        self.get_config.return_value = "ptp source 192.0.2.1\n"
        result = self._run(
            True,
            config=dict(
                source=dict(
                    ipv4=dict(address="192.0.2.1", vrf="management"),
                    ipv6=dict(address="2001:db8::1"),
                ),
            ),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(["ptp source 192.0.2.1 vrf management", "ptp source 2001:db8::1"]),
        )

    def test_nxos_ptp_global_merged_groups(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=dict(
                notification=dict(high_correction=dict(interval="immediate")),
                clock_periodic_update=dict(interval=120),
                time_distribution_hold=dict(correction_threshold=800, delay_threshold=100),
            ),
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"]),
            sorted(
                [
                    "ptp notification type high-correction interval immediate",
                    "ptp clock periodic-update interval 120",
                    "ptp time distribution-hold correction-threshold 800 delay-threshold 100",
                ],
            ),
        )

    # replaced / overridden

    def test_nxos_ptp_global_replaced_removes_what_is_not_given(self):
        self.get_config.return_value = BASE
        for state in ["replaced", "overridden"]:
            result = self._run(
                True,
                config=dict(source=dict(ipv4=dict(address="192.0.2.1")), priority1=90),
                state=state,
            )
            self.assertEqual(
                sorted(result["commands"]),
                sorted(
                    [
                        "ptp priority1 90",
                        "no ptp priority2 120",
                        "no ptp notification type gm-change",
                        "no ptp notification type high-correction",
                        "no ptp correction-range 5000",
                        "no ptp correction-range logging",
                        "no ptp clock periodic-update",
                        "no ptp mean-path-delay 5000",
                        "no ptp domain 5",
                        "no ptp time distribution-hold",
                        "no ptp delay tolerance mean-path 10.50",
                        "ptp management",
                    ],
                ),
            )

    def test_nxos_ptp_global_replaced_default_have_is_idempotent(self):
        self.get_config.return_value = ""
        self._run(False, config=dict(domain=0), state="replaced")

    # deleted

    def test_nxos_ptp_global_deleted(self):
        self.get_config.return_value = SMALL + "no ptp management\n"
        result = self._run(True, state="deleted")
        self.assertEqual(
            sorted(result["commands"]),
            sorted(["no ptp source 192.0.2.1", "no ptp priority1 90", "ptp management"]),
        )

    def test_nxos_ptp_global_deleted_nothing_to_delete(self):
        self.get_config.return_value = ""
        self._run(False, state="deleted")

    # validation

    def test_nxos_ptp_global_validation(self):
        cases = [
            (dict(domain=128), "domain must be in the range 0-127"),
            (dict(domain=-1), "domain must be in the range 0-127"),
            (dict(priority1=256), "priority1 must be in the range 0-255"),
            (dict(mean_path_delay=9), "mean_path_delay must be in the range 10-1000000000"),
            (
                dict(correction_range=dict(value=1000000001)),
                "correction_range.value must be in the range",
            ),
            (
                dict(clock_periodic_update=dict(interval=3601)),
                "clock_periodic_update.interval must be in the range 0-3600",
            ),
            (
                dict(time_distribution_hold=dict(correction_threshold=0)),
                "correction_threshold must be in the range 1-100000",
            ),
            (
                dict(time_distribution_hold=dict(delay_threshold=5001)),
                "delay_threshold must be in the range 1-5000",
            ),
            (
                dict(delay_tolerance=dict(mean_path="0.9")),
                "delay_tolerance mean_path must be between 1.0 and 100.0",
            ),
            (
                dict(delay_tolerance=dict(reverse_path="100.1")),
                "delay_tolerance reverse_path must be between",
            ),
            (
                dict(delay_tolerance=dict(mean_path="abc")),
                "delay_tolerance mean_path must be between",
            ),
            (
                dict(notification=dict(high_correction=dict(interval="0"))),
                "high_correction interval must be",
            ),
            (
                dict(notification=dict(high_correction=dict(interval="301"))),
                "high_correction interval must be",
            ),
            (dict(source=dict(ipv4=dict(address="999.1.1.1"))), "must be an IP address"),
            (dict(source=dict(ipv4=dict(address="2001:db8::1"))), "must be an IPv4 address"),
            (dict(source=dict(ipv6=dict(address="192.0.2.1"))), "must be an IPv6 address"),
            (dict(source=dict(ipv4=dict(vrf="management"))), "needs an address"),
        ]
        for config, message in cases:
            result = self._fail(config=config, state="rendered")
            self.assertIn(message, result["msg"])

    def test_nxos_ptp_global_values_of_the_device_are_not_validated(self):
        # a value the device has is only compared, it does not fail the module
        self.get_config.return_value = "ptp domain 200\nptp delay tolerance mean-path 0.50\n"
        result = self._run(True, config=dict(domain=5), state="merged")
        self.assertEqual(result["commands"], ["ptp domain 5"])

    def test_nxos_ptp_global_empty_config(self):
        set_module_args(dict(config={}, state="merged"), ignore_provider_arg)
        result = self.execute_module(failed=True)
        self.assertIn("must not be empty", result["msg"])

    def test_nxos_ptp_global_check_mode_sends_nothing(self):
        self.get_config.return_value = ""
        set_module_args(
            dict(config=dict(domain=5), state="merged", _ansible_check_mode=True),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["ptp domain 5"])
        self.get_resource_connection.return_value.edit_config.assert_not_called()
