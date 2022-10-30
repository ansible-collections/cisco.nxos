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

from ansible_collections.cisco.nxos.plugins.modules import nxos_ping
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import AnsibleFailJson

from .nxos_module import TestNxosModule, load_fixture, set_module_args


ignore_provider_arg = True


class TestNxosPingModule(TestNxosModule):
    """Class used for Unit Tests agains ios_ping module"""

    module = nxos_ping

    def setUp(self):
        super(TestNxosPingModule, self).setUp()
        self.mock_run_commands = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_ping.run_commands",
        )
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestNxosPingModule, self).tearDown()
        self.mock_run_commands.stop()

    def test_nxos_ping_expected_success(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", vrf="management"))
        result = self.execute_module()
        self.assertEqual(result["commands"], ["ping 172.28.128.7 count 5 vrf management"])
        self.assertEqual(result["packet_loss"], "0.00%")
        self.assertEqual(result["packets_rx"], 5)
        self.assertEqual(result["packets_tx"], 5)
        self.assertEqual(result["rtt"]["min"], 1.597)
        self.assertEqual(result["rtt"]["avg"], 2.32)
        self.assertEqual(result["rtt"]["max"], 4.197)

    def test_nxos_ping_expected_failure(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.8 (172.28.128.8): 56 data bytes
            Request 0 timed out
            Request 1 timed out
            Request 2 timed out
            Request 3 timed out
            Request 4 timed out

            --- 172.28.128.8 ping statistics ---
            5 packets transmitted, 0 packets received, 100.00% packet loss
        """,
        ]
        set_module_args(dict(dest="172.28.128.8", vrf="management", state="absent"))
        self.execute_module(failed=False)

    def test_nxos_ping_expected_success_but_failed(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.8 (172.28.128.8): 56 data bytes
            Request 0 timed out
            Request 1 timed out
            Request 2 timed out
            Request 3 timed out
            Request 4 timed out

            --- 172.28.128.8 ping statistics ---
            5 packets transmitted, 0 packets received, 100.00% packet loss
        """,
        ]
        set_module_args(dict(dest="172.28.128.8", vrf="management"))
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "Ping failed unexpectedly")

    def test_nxos_ping_expected_failure_but_succeeded(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", vrf="management", state="absent"))
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "Ping succeeded unexpectedly")

    def test_nxos_ping_expected_success_source(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", source="192.168.1.10"))
        result = self.execute_module()
        self.assertEqual(
            result["commands"],
            ["ping 172.28.128.7 count 5 source 192.168.1.10"],
        )
        self.assertEqual(result["packet_loss"], "0.00%")
        self.assertEqual(result["packets_rx"], 5)
        self.assertEqual(result["packets_tx"], 5)
        self.assertEqual(result["rtt"]["min"], 1.597)
        self.assertEqual(result["rtt"]["avg"], 2.32)
        self.assertEqual(result["rtt"]["max"], 4.197)

    def test_nxos_ping_expected_success_df_bit(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", df_bit=True))
        result = self.execute_module()
        self.assertEqual(result["commands"], ["ping 172.28.128.7 count 5 df-bit"])

    def test_nxos_ping_expected_success_size(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", size=65468))
        result = self.execute_module()
        self.assertEqual(result["commands"], ["ping 172.28.128.7 count 5 packet-size 65468"])

    def test_nxos_ping_expected_success_all(self):
        self.run_commands.return_value = [
            """
            PING 172.28.128.7 (172.28.128.7): 56 data bytes
            64 bytes from 172.28.128.7: icmp_seq=0 ttl=253 time=2.564 ms
            64 bytes from 172.28.128.7: icmp_seq=1 ttl=253 time=4.197 ms
            64 bytes from 172.28.128.7: icmp_seq=2 ttl=253 time=1.597 ms
            64 bytes from 172.28.128.7: icmp_seq=3 ttl=253 time=1.622 ms
            64 bytes from 172.28.128.7: icmp_seq=4 ttl=253 time=1.621 ms

            --- 172.28.128.7 ping statistics ---
            5 packets transmitted, 5 packets received, 0.00% packet loss
            round-trip min/avg/max = 1.597/2.32/4.197 ms
        """,
        ]
        set_module_args(
            dict(
                dest="172.28.128.7",
                count=10,
                size=65468,
                df_bit=True,
                source="192.168.1.1",
                vrf="management",
            ),
        )
        result = self.execute_module()
        self.assertEqual(
            result["commands"],
            [
                "ping 172.28.128.7 count 10 source 192.168.1.1 vrf management packet-size 65468 df-bit",
            ],
        )

    def test_nxos_ping_failed_cant_bind(self):
        self.run_commands.return_value = [
            """
            ping: can't bind to address 192.168.1.10
        """,
        ]
        set_module_args(
            dict(
                dest="172.28.128.7",
                count=10,
                size=65468,
                df_bit=True,
                source="192.168.1.1",
                vrf="management",
            ),
        )
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "Can't bind to source address.")

    def test_nxos_ping_failed_bad_context(self):
        self.run_commands.return_value = [
            """
            ping: bad context site-1
        """,
        ]
        set_module_args(dict(dest="172.28.128.7", count=10, vrf="site-1"))
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "Wrong VRF name inserted.")

    def test_nxos_ping_failed_error(self):
        """Test for successful pings when destination should be reachable"""
        self.run_commands.return_value = [""""""]
        set_module_args(dict(dest="172.28.128.7", count=10, vrf="site-1"))
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "An unexpected error occurred. Check all params.")
