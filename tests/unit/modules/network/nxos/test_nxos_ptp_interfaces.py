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

from copy import deepcopy
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_ptp_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

# `show running-config | include "^interface|^  ptp"`: the interfaces without ptp are only a header
BASE = dedent(
    """\
    interface Ethernet1/1
      ptp
      ptp delay-request minimum interval aes67 -2
      ptp announce interval aes67 3
      ptp vlan 100
      ptp sync interval aes67 -2
    interface Ethernet1/2
      ptp
      ptp role master
      ptp transmission unicast
      ptp master 192.0.2.10
      ptp master 192.0.2.11
      ptp peer 192.0.2.20
      ptp ucast-source 192.0.2.30
      ptp asymmetric-delay forward-path 100
    interface Ethernet1/3
    interface Ethernet1/4
      ptp
      ptp announce interval 0
      ptp announce timeout 4
      ptp sync interval 1
      ptp delay-request minimum interval 3
      ptp transport ipv6
    interface port-channel20
    """,
)

BASE_FACTS = [
    dict(
        name="Ethernet1/1",
        enabled=True,
        vlan=100,
        announce_interval=dict(value=3, profile="aes67"),
        sync_interval=dict(value=-2, profile="aes67"),
        delay_request_interval=dict(value=-2, profile="aes67"),
    ),
    dict(
        name="Ethernet1/2",
        enabled=True,
        role="master",
        transmission="unicast",
        master=["192.0.2.10", "192.0.2.11"],
        peer="192.0.2.20",
        ucast_source=dict(ipv4="192.0.2.30"),
        asymmetric_delay=dict(forward_path=100),
    ),
    dict(
        name="Ethernet1/4",
        enabled=True,
        transport="ipv6",
        announce_interval=dict(value=0),
        announce_timeout=dict(value=4),
        sync_interval=dict(value=1),
        delay_request_interval=dict(value=3),
    ),
]


class TestNxosPtpInterfacesModule(TestNxosModule):
    module = nxos_ptp_interfaces

    def setUp(self):
        super(TestNxosPtpInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.ptp_interfaces.ptp_interfaces.Ptp_interfacesFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosPtpInterfacesModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    def _fail(self, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(failed=True)

    # facts

    def test_nxos_ptp_interfaces_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_ptp_interfaces_gathered(self):
        self.get_config.return_value = BASE
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)

    def test_nxos_ptp_interfaces_gathered_nothing(self):
        self.get_config.return_value = "interface Ethernet1/1\ninterface Ethernet1/2\n"
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], [])

    def test_nxos_ptp_interfaces_parsed_smpte_and_ipv6(self):
        cfg = dedent(
            """\
            interface Ethernet1/9
              ptp
              ptp sync interval smpte-2059-2 -5
              ptp slave 2001:db8::1 negotiation-schema S2
              ptp transmission multicast
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            [
                dict(
                    name="Ethernet1/9",
                    enabled=True,
                    sync_interval=dict(value=-5, profile="smpte_2059_2"),
                    slave=["2001:db8::1"],
                    transmission="multicast",
                ),
            ],
        )

    def test_nxos_ptp_interfaces_parsed_lines_with_trailing_spaces(self):
        # the device displays some lines with trailing spaces
        cfg = "interface Ethernet1/9\n  ptp \n  ptp vlan 100  \n  ptp role master \n"
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            [dict(name="Ethernet1/9", enabled=True, vlan=100, role="master")],
        )

    # rendered

    def test_nxos_ptp_interfaces_rendered(self):
        result = self._run(
            False,
            config=[
                dict(
                    name="Eth1/3",
                    enabled=True,
                    vlan=100,
                    role="master",
                    transmission="unicast",
                    master=["192.0.2.10"],
                    asymmetric_delay=dict(reverse_path=200),
                    sync_interval=dict(value=-2, profile="aes67"),
                    announce_interval=dict(value=3),
                ),
            ],
            state="rendered",
        )
        rendered = result["rendered"]
        self.assertEqual(rendered[:2], ["interface Ethernet1/3", "ptp"])
        self.assertEqual(
            sorted(rendered[2:]),
            sorted(
                [
                    "ptp vlan 100",
                    "ptp role master",
                    "ptp transmission unicast",
                    "ptp master 192.0.2.10",
                    "ptp asymmetric-delay reverse-path 200",
                    "ptp sync interval aes67 -2",
                    "ptp announce interval 3",
                ],
            ),
        )

    def test_nxos_ptp_interfaces_rendered_defaults_send_nothing(self):
        result = self._run(
            False,
            config=[
                dict(
                    name="Ethernet1/3",
                    enabled=True,
                    role="dynamic",
                    transport="ipv4",
                    transmission="multicast",
                    announce_interval=dict(value=1),
                    announce_timeout=dict(value=3),
                    sync_interval=dict(value=-2),
                    delay_request_interval=dict(value=0),
                ),
            ],
            state="rendered",
        )
        self.assertEqual(result["rendered"], ["interface Ethernet1/3", "ptp"])

    # merged

    def test_nxos_ptp_interfaces_merged_idempotent_with_the_gathered_data(self):
        self.get_config.return_value = BASE
        for state in ["merged", "replaced", "overridden"]:
            self._run(False, config=deepcopy(BASE_FACTS), state=state)

    def test_nxos_ptp_interfaces_merged_enables_and_sets(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/3", enabled=True, vlan=10, sync_interval=dict(value=0))],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/3", "ptp", "ptp vlan 10", "ptp sync interval 0"],
        )

    def test_nxos_ptp_interfaces_merged_on_an_interface_that_has_ptp_does_not_need_enabled(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(name="Ethernet1/1", vlan=200)], state="merged")
        self.assertEqual(result["commands"], ["interface Ethernet1/1", "ptp vlan 200"])

    def test_nxos_ptp_interfaces_merged_keeps_what_is_not_given(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/2", master=["192.0.2.12"])],
            state="merged",
        )
        self.assertEqual(result["commands"], ["interface Ethernet1/2", "ptp master 192.0.2.12"])

    def test_nxos_ptp_interfaces_merged_default_value_removes_the_line(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/4",
                    transport="ipv4",
                    announce_timeout=dict(value=3),
                    sync_interval=dict(value=-2),
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            sorted(result["commands"][1:]),
            sorted(
                ["no ptp transport ipv6", "no ptp announce timeout 4", "no ptp sync interval 1"],
            ),
        )

    def test_nxos_ptp_interfaces_merged_defaults_on_a_clean_interface_send_nothing(self):
        self.get_config.return_value = BASE
        self._run(
            False,
            config=[dict(name="Ethernet1/3", role="dynamic", sync_interval=dict(value=-2))],
            state="merged",
        )

    def test_nxos_ptp_interfaces_merged_enabled_false_removes_ptp(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(name="Ethernet1/1", enabled=False)], state="merged")
        self.assertEqual(result["commands"], ["interface Ethernet1/1", "no ptp"])

    def test_nxos_ptp_interfaces_merged_enabled_false_on_a_clean_interface_is_idempotent(self):
        self.get_config.return_value = BASE
        self._run(False, config=[dict(name="Ethernet1/3", enabled=False)], state="merged")

    def test_nxos_ptp_interfaces_profile_switch_removes_the_old_line_first(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/1",
                    enabled=True,
                    vlan=100,
                    announce_interval=dict(value=0, profile="smpte_2059_2"),
                    sync_interval=dict(value=-5, profile="smpte_2059_2"),
                    delay_request_interval=dict(value=-2, profile="smpte_2059_2"),
                ),
            ],
            state="replaced",
        )
        commands = result["commands"]
        self.assertEqual(commands[0], "interface Ethernet1/1")
        removals = commands[1:4]
        self.assertEqual(
            sorted(removals),
            sorted(
                [
                    "no ptp announce interval aes67 3",
                    "no ptp sync interval aes67 -2",
                    "no ptp delay-request minimum interval aes67 -2",
                ],
            ),
        )
        self.assertEqual(
            sorted(commands[4:]),
            sorted(
                [
                    "ptp announce interval smpte-2059-2 0",
                    "ptp sync interval smpte-2059-2 -5",
                    "ptp delay-request minimum interval smpte-2059-2 -2",
                ],
            ),
        )

    # replaced / overridden

    def test_nxos_ptp_interfaces_replaced_removes_what_is_not_given(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/2", enabled=True, role="master", master=["192.0.2.11"])],
            state="replaced",
        )
        self.assertEqual(result["commands"][0], "interface Ethernet1/2")
        self.assertEqual(
            sorted(result["commands"][1:]),
            sorted(
                [
                    "no ptp transmission unicast",
                    "no ptp master 192.0.2.10",
                    "no ptp peer 192.0.2.20",
                    "no ptp ucast-source 192.0.2.30",
                    "no ptp asymmetric-delay forward-path 100",
                ],
            ),
        )

    def test_nxos_ptp_interfaces_replaced_without_enabled_removes_ptp(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(name="Ethernet1/1")], state="replaced")
        self.assertEqual(result["commands"], ["interface Ethernet1/1", "no ptp"])

    def test_nxos_ptp_interfaces_replaced_a_changed_peer_is_replaced_one_after_the_other(self):
        # the device accepts one peer: the old one goes first
        self.get_config.return_value = BASE
        config = dict(
            name="Ethernet1/2",
            enabled=True,
            role="master",
            transmission="unicast",
            master=["192.0.2.10", "192.0.2.11"],
            peer="192.0.2.21",
            ucast_source=dict(ipv4="192.0.2.31"),
            asymmetric_delay=dict(reverse_path=300),
        )
        result = self._run(True, config=[config], state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/2",
                "ptp asymmetric-delay reverse-path 300",
                "no ptp peer 192.0.2.20",
                "ptp peer 192.0.2.21",
                "ptp ucast-source 192.0.2.31",
            ],
        )

    def test_nxos_ptp_interfaces_ucast_source_one_for_each_address_family(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/2", ucast_source=dict(ipv6="2001:db8::30"))],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/2", "ptp ucast-source 2001:db8::30"],
        )
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/2",
                    enabled=True,
                    ucast_source=dict(ipv4="192.0.2.30", ipv6="2001:db8::30"),
                ),
            ],
            state="replaced",
        )
        self.assertIn("ptp ucast-source 2001:db8::30", result["commands"])
        self.assertIn("no ptp transmission unicast", result["commands"])

    def test_nxos_ptp_interfaces_asymmetric_delay_direction_change_replaces_the_value(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/2", asymmetric_delay=dict(reverse_path=200))],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/2", "ptp asymmetric-delay reverse-path 200"],
        )

    def test_nxos_ptp_interfaces_overridden_removes_the_other_interfaces(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    name="Ethernet1/1",
                    enabled=True,
                    vlan=100,
                    announce_interval=dict(value=3, profile="aes67"),
                    sync_interval=dict(value=-2, profile="aes67"),
                    delay_request_interval=dict(value=-2, profile="aes67"),
                ),
            ],
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            ["interface Ethernet1/2", "no ptp", "interface Ethernet1/4", "no ptp"],
        )

    # deleted

    def test_nxos_ptp_interfaces_deleted_listed(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(name="Ethernet1/2"), dict(name="Ethernet1/3")],
            state="deleted",
        )
        self.assertEqual(result["commands"], ["interface Ethernet1/2", "no ptp"])

    def test_nxos_ptp_interfaces_deleted_everything(self):
        self.get_config.return_value = BASE
        result = self._run(True, state="deleted")
        self.assertEqual(
            result["commands"],
            [
                "interface Ethernet1/1",
                "no ptp",
                "interface Ethernet1/2",
                "no ptp",
                "interface Ethernet1/4",
                "no ptp",
            ],
        )

    def test_nxos_ptp_interfaces_deleted_nothing_to_delete(self):
        self.get_config.return_value = "interface Ethernet1/1\n"
        self._run(False, state="deleted")

    # validation

    def test_nxos_ptp_interfaces_validation(self):
        base = dict(name="Ethernet1/3", enabled=True)
        cases = [
            (dict(vlan=0), "vlan must be in the range 1-4094"),
            (dict(vlan=4095), "vlan must be in the range 1-4094"),
            (dict(announce_interval=dict(value=5)), "announce_interval must be in the range 0-4"),
            (
                dict(announce_interval=dict(value=5, profile="aes67")),
                "announce_interval with the profile aes67 must be in the range 0-4",
            ),
            (
                dict(announce_interval=dict(value=2, profile="smpte_2059_2")),
                "with the profile smpte_2059_2 must be in the range -3-1",
            ),
            (dict(announce_timeout=dict(value=1)), "announce_timeout must be in the range 2-4"),
            (dict(announce_timeout=dict(value=11, profile="aes67")), "must be in the range 2-10"),
            (dict(sync_interval=dict(value=-4)), "sync_interval must be in the range -3-1"),
            (
                dict(sync_interval=dict(value=1, profile="smpte_2059_2")),
                "must be in the range -7-0",
            ),
            (
                dict(delay_request_interval=dict(value=7)),
                "delay_request_interval must be in the range -1-6",
            ),
            (
                dict(asymmetric_delay=dict(forward_path=0)),
                "asymmetric_delay forward_path must be in the range 1-512000000",
            ),
            (
                dict(asymmetric_delay=dict(reverse_path=512000001)),
                "asymmetric_delay reverse_path must be in the range",
            ),
            (
                dict(asymmetric_delay=dict(forward_path=1, reverse_path=2)),
                "only have one of forward_path and reverse_path",
            ),
            (dict(master=["not-an-address"]), "master must be an IP address"),
            (dict(slave=["192.0.2.1", "999.1.1.1"]), "slave must be an IP address"),
            (dict(peer="999.1.1.1"), "peer must be an IP address"),
            (dict(ucast_source=dict(ipv4="2001:db8::1")), "must be an IPv4 address"),
            (dict(ucast_source=dict(ipv6="192.0.2.1")), "must be an IPv6 address"),
            (
                dict(
                    announce_interval=dict(value=1, profile="aes67"),
                    sync_interval=dict(value=-2, profile="smpte_2059_2"),
                ),
                "cannot be mixed",
            ),
            (dict(role="slave"), "the role slave needs the transmission mode unicast"),
            (
                dict(role="slave", transmission="multicast"),
                "the role slave needs the transmission mode unicast",
            ),
        ]
        for extra, message in cases:
            entry = dict(base)
            entry.update(extra)
            result = self._fail(config=[entry], state="rendered")
            self.assertIn(message, result["msg"])

    def test_nxos_ptp_interfaces_other_settings_need_ptp_on_the_interface(self):
        self.get_config.return_value = BASE
        for state in ["replaced", "overridden", "rendered"]:
            result = self._fail(config=[dict(name="Ethernet1/3", vlan=100)], state=state)
            self.assertIn("set enabled to true", result["msg"])
        result = self._fail(config=[dict(name="Ethernet1/3", vlan=100)], state="merged")
        self.assertIn("set enabled to true", result["msg"])
        result = self._fail(
            config=[dict(name="Ethernet1/3", enabled=False, vlan=100)],
            state="merged",
        )
        self.assertIn("set enabled to true", result["msg"])

    def test_nxos_ptp_interfaces_values_of_the_device_are_not_validated(self):
        self.get_config.return_value = (
            "interface Ethernet1/3\n  ptp\n  ptp vlan 4094\n  ptp master not-an-address\n"
        )
        result = self._run(True, config=[dict(name="Ethernet1/3", vlan=100)], state="merged")
        self.assertEqual(result["commands"], ["interface Ethernet1/3", "ptp vlan 100"])

    def test_nxos_ptp_interfaces_empty_config(self):
        set_module_args(dict(config=[], state="merged"), ignore_provider_arg)
        result = self.execute_module(failed=True)
        self.assertIn("must not be empty", result["msg"])

    def test_nxos_ptp_interfaces_check_mode_sends_nothing(self):
        self.get_config.return_value = BASE
        set_module_args(
            dict(
                config=[dict(name="Ethernet1/1", vlan=200)],
                state="merged",
                _ansible_check_mode=True,
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface Ethernet1/1", "ptp vlan 200"])
        self.get_resource_connection.return_value.edit_config.assert_not_called()
