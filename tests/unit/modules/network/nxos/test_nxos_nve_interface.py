# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for the nxos_nve_interface Ansible module.

This module tests the behavior of nxos_nve_interface including:
- Merged state
- Overridden state
- Replaced state
- Deleted state
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_nve_interface

from .nxos_module import TestNxosModule, set_module_args


class TestNxosNveInterfaceModule(TestNxosModule):
    """Unit tests for the nxos_nve_interface."""

    module = nxos_nve_interface

    def setUp(self):
        """Set up test fixtures before each test method."""

        super().setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base."
            "resource_module_base.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.nve_interface."
            "nve_interface.Nve_interfaceFacts.get_nve_interface_data",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        """Clean up after each test method."""

        super().tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()

    def test_nxos_nve_interface_merged(self):
        """Test state merged."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             host-reachability protocol bgp
             source-interface loopback1
             member vni 11111
             member vni 22222 associate-vrf
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "description": "vxlan vtep",
                    "enabled": True,
                    "global_multicast_group": {
                        "address": "233.252.0.20",
                        "mode": "L2",
                    },
                    "source_interface_hold_time": 60,
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "suppress_arp": True,
                        },
                        {
                            "vni_id": 33333,
                            "suppress_arp": True,
                        },
                    ],
                },
                "state": "merged",
            },
        )
        commands = [
            "interface nve1",
            "description vxlan vtep",
            "advertise virtual-rmac",
            "source-interface hold-down-time 60",
            "member vni 11111",
            "suppress-arp",
            "member vni 33333",
            "suppress-arp",
            "global mcast-group 233.252.0.20 L2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_nve_interface_merged_idempotent(self):
        """Test idempotency for state merged."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             description vxlan vtep
             advertise virtual-rmac
             host-reachability protocol bgp
             source-interface loopback1
             source-interface hold-down-time 60
             global mcast-group 233.252.0.20 L2
             member vni 11111
              suppress-arp
             member vni 22222 associate-vrf
             member vni 33333
              suppress-arp
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "description": "vxlan vtep",
                    "enabled": True,
                    "global_multicast_group": {
                        "address": "233.252.0.20",
                        "mode": "L2",
                    },
                    "source_interface_hold_time": 60,
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "suppress_arp": True,
                        },
                        {
                            "vni_id": 33333,
                            "suppress_arp": True,
                        },
                    ],
                },
                "state": "merged",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_nve_interface_replaced(self):
        """Test state replaced."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             host-reachability protocol bgp
             source-interface loopback1
             member vni 11111
             member vni 22222
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "enabled": True,
                    "global_multicast_group": {
                        "address": "233.252.0.30",
                        "mode": "L2",
                    },
                    "host_reachability_bgp": True,
                    "source_interface_name": "loopback1",
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "ingress_replication_bgp": True,
                            "suppress_arp": True,
                        },
                        {
                            "vni_id": 22222,
                            "associate_vrf": True,
                        },
                        {
                            "vni_id": 33333,
                            "suppress_arp": True,
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        commands = [
            "interface nve1",
            "advertise virtual-rmac",
            "member vni 11111",
            "suppress-arp",
            "ingress-replication protocol bgp",
            "no member vni 22222",
            "member vni 22222 associate-vrf",
            "member vni 33333",
            "suppress-arp",
            "global mcast-group 233.252.0.30 L2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_nve_interface_replaced_idempotent(self):
        """Test idempotency for state replaced."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             advertise virtual-rmac
             host-reachability protocol bgp
             source-interface loopback1
             global mcast-group 233.252.0.30 L2
             member vni 11111
              ingress-replication protocol bgp
              suppress-arp
             member vni 22222 associate-vrf
             member vni 33333
              suppress-arp
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "enabled": True,
                    "global_multicast_group": {
                        "address": "233.252.0.30",
                        "mode": "L2",
                    },
                    "host_reachability_bgp": True,
                    "source_interface_name": "loopback1",
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "ingress_replication_bgp": True,
                            "suppress_arp": True,
                        },
                        {
                            "vni_id": 22222,
                            "associate_vrf": True,
                        },
                        {
                            "vni_id": 33333,
                            "suppress_arp": True,
                        },
                    ],
                },
                "state": "replaced",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_nve_interface_overridden(self):
        """Test state overridden."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             global mcast-group 233.252.0.30 L2
             host-reachability protocol bgp
             source-interface loopback2
             member vni 11111 associate-vrf
             member vni 22222
              suppress-arp
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "enabled": True,
                    "host_reachability_bgp": True,
                    "source_interface_name": "loopback1",
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "suppress_arp": True,
                            "ingress_replication_bgp": True,
                        },
                        {
                            "vni_id": 22222,
                            "associate_vrf": True,
                        },
                        {
                            "vni_id": 33333,
                        },
                    ],
                },
                "state": "overridden",
            },
        )
        commands = [
            "interface nve1",
            "advertise virtual-rmac",
            "source-interface loopback1",
            "no member vni 11111",
            "member vni 11111",
            "suppress-arp",
            "ingress-replication protocol bgp",
            "no member vni 22222",
            "member vni 22222 associate-vrf",
            "member vni 33333",
            "no shutdown",
            "no global mcast-group L2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_nve_interface_overridden_idempotent(self):
        """Test idempotency for state overridden."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             advertise virtual-rmac
             host-reachability protocol bgp
             source-interface loopback1
             member vni 11111
              suppress-arp
              ingress-replication protocol bgp
             member vni 22222 associate-vrf
             member vni 33333
            """,
        )
        set_module_args(
            {
                "config": {
                    "advertise_virtual_rmac": True,
                    "enabled": True,
                    "host_reachability_bgp": True,
                    "source_interface_name": "loopback1",
                    "vnis": [
                        {
                            "vni_id": 11111,
                            "suppress_arp": True,
                            "ingress_replication_bgp": True,
                        },
                        {
                            "vni_id": 22222,
                            "associate_vrf": True,
                        },
                        {
                            "vni_id": 33333,
                        },
                    ],
                },
                "state": "overridden",
            },
        )
        self.execute_module(changed=False, commands=[])

    def test_nxos_nve_interface_deleted(self):
        """Test state deleted."""

        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             source-interface loopback1
             host-reachability protocol bgp
             member vni 11111
             member vni 22222
            """,
        )
        set_module_args(
            {
                "config": {},
                "state": "deleted",
            },
        )
        commands = [
            "no interface nve1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def _run(self, running, config, state, changed=True, failed=False):
        """Run the module against a running-config and return the result."""

        self.get_config.return_value = dedent(running)
        set_module_args({"config": config, "state": state})
        return self.execute_module(changed=changed, failed=failed)

    def test_nxos_nve_interface_mcast_group_merged(self):
        """Test per-VNI mcast-group, including the optional second address."""

        running = """\
            interface nve1
              no shutdown
              source-interface loopback1
              member vni 10100
                suppress-arp
            """
        config = {
            "vnis": [
                {"vni_id": 10100, "mcast_group": {"address": "233.252.0.1"}},
                {
                    "vni_id": 10200,
                    "mcast_group": {"address": "233.252.0.2", "secondary_address": "233.252.0.3"},
                },
            ],
        }
        result = self._run(running, config, "merged")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "mcast-group 233.252.0.1",
                "member vni 10200",
                "mcast-group 233.252.0.2 233.252.0.3",
            ],
        )

    def test_nxos_nve_interface_mcast_group_idempotent(self):
        """Test mcast-group is parsed and compared without changes."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                mcast-group 233.252.0.1
              member vni 10200
                mcast-group 233.252.0.2 233.252.0.3
            """
        config = {
            "vnis": [
                {"vni_id": 10100, "mcast_group": {"address": "233.252.0.1"}},
                {
                    "vni_id": 10200,
                    "mcast_group": {"address": "233.252.0.2", "secondary_address": "233.252.0.3"},
                },
            ],
        }
        for state in ("merged", "replaced", "overridden"):
            self._run(running, dict(config, enabled=True), state, changed=False)

    def test_nxos_nve_interface_mcast_group_change_and_remove(self):
        """Test changing a group and removing it with replaced."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                mcast-group 233.252.0.1
              member vni 10200
                mcast-group 233.252.0.2 233.252.0.3
            """
        config = {
            "enabled": True,
            "vnis": [
                {"vni_id": 10100, "mcast_group": {"address": "233.252.0.9"}},
                {"vni_id": 10200},
            ],
        }
        result = self._run(running, config, "replaced")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "mcast-group 233.252.0.9",
                "member vni 10200",
                "no mcast-group 233.252.0.2 233.252.0.3",
            ],
        )

    def test_nxos_nve_interface_merged_mcast_group_replaces_ingress_replication(self):
        """Test merged mcast-group removes the alternative ingress-replication."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                ingress-replication protocol bgp
            """
        config = {"vnis": [{"vni_id": 10100, "mcast_group": {"address": "233.252.0.1"}}]}
        result = self._run(running, config, "merged")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "no ingress-replication protocol bgp",
                "mcast-group 233.252.0.1",
            ],
        )

    def test_nxos_nve_interface_merged_ingress_replication_replaces_mcast_group(self):
        """Test merged ingress-replication removes the alternative mcast-group."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                mcast-group 233.252.0.1
            """
        config = {"vnis": [{"vni_id": 10100, "ingress_replication_bgp": True}]}
        result = self._run(running, config, "merged")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "no mcast-group 233.252.0.1",
                "ingress-replication protocol bgp",
            ],
        )

    def test_nxos_nve_interface_merged_suppress_arp_swap(self):
        """Test suppress-arp and suppress-arp disable replace each other."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                suppress-arp
              member vni 10200
                suppress-arp disable
            """
        config = {
            "vnis": [
                {"vni_id": 10100, "suppress_arp_disable": True},
                {"vni_id": 10200, "suppress_arp": True},
            ],
        }
        result = self._run(running, config, "merged")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "no suppress-arp",
                "suppress-arp disable",
                "member vni 10200",
                "no suppress-arp disable",
                "suppress-arp",
            ],
        )

    def test_nxos_nve_interface_replaced_ingress_replication_to_mcast_group(self):
        """Test removal is ordered before the alternative option."""

        running = """\
            interface nve1
              no shutdown
              member vni 10100
                multisite ingress-replication
                ingress-replication protocol bgp
            """
        config = {
            "enabled": True,
            "vnis": [
                {
                    "vni_id": 10100,
                    "multisite_ingress_replication": True,
                    "mcast_group": {"address": "233.252.0.1"},
                },
            ],
        }
        result = self._run(running, config, "replaced")
        self.assertEqual(
            result["commands"],
            [
                "interface nve1",
                "member vni 10100",
                "no ingress-replication protocol bgp",
                "mcast-group 233.252.0.1",
            ],
        )

    def test_nxos_nve_interface_mutually_exclusive_vni_options(self):
        """Test alternatives cannot both be requested."""

        running = "interface nve1\n  no shutdown\n"
        for vni in (
            {"suppress_arp": True, "suppress_arp_disable": True},
            {"mcast_group": {"address": "233.252.0.1"}, "ingress_replication_bgp": True},
        ):
            config = {"vnis": [dict(vni, vni_id=10100)]}
            result = self._run(running, config, "merged", failed=True)
            self.assertIn("mutually exclusive", result["msg"])

    def test_nxos_nve_interface_parsed_mcast_group(self):
        """Test parsing of every per-VNI option."""

        set_module_args(
            {
                "running_config": dedent(
                    """\
                    interface nve1
                      no shutdown
                      member vni 10100
                        suppress-arp
                        mcast-group 233.252.0.1 233.252.0.2
                      member vni 10200
                        suppress-arp disable
                        multisite ingress-replication
                        ingress-replication protocol bgp
                      member vni 50001 associate-vrf
                    """,
                ),
                "state": "parsed",
            },
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "enabled": True,
                "vnis": [
                    {
                        "vni_id": 10100,
                        "suppress_arp": True,
                        "mcast_group": {
                            "address": "233.252.0.1",
                            "secondary_address": "233.252.0.2",
                        },
                    },
                    {
                        "vni_id": 10200,
                        "suppress_arp_disable": True,
                        "multisite_ingress_replication": True,
                        "ingress_replication_bgp": True,
                    },
                    {"vni_id": 50001, "associate_vrf": True},
                ],
            },
        )

    def test_nxos_nve_interface_parsed_multisite_and_trailing_whitespace(self):
        """Test multisite interface parsing and tolerance of trailing whitespace."""

        running = (
            "interface nve1  \n"
            "  no shutdown \n"
            "  host-reachability protocol bgp   \n"
            "  multisite border-gateway interface loopback100\n"
            "  member vni 10100 \n"
            "    multisite ingress-replication  \n"
            "    ingress-replication protocol bgp\n"
            "  member vni 10200\n"
            "    suppress-arp\n"
        )
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"],
            {
                "enabled": True,
                "host_reachability_bgp": True,
                "multisite_interface": "loopback100",
                "vnis": [
                    {
                        "vni_id": 10100,
                        "multisite_ingress_replication": True,
                        "ingress_replication_bgp": True,
                    },
                    {"vni_id": 10200, "suppress_arp": True},
                ],
            },
        )

    def test_nxos_nve_interface_parsed_pathological_whitespace(self):
        """Test very long whitespace runs are parsed without stalling."""

        running = (
            "interface nve1\n  description"
            + " " * 100000
            + "x\n  member vni 1"
            + " " * 100000
            + "x\n"
        )
        set_module_args({"running_config": running, "state": "parsed"})
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], {"description": "x"})

    def test_nxos_nve_interface_multisite_interface_idempotent(self):
        """Test multisite border-gateway interface compares without changes."""

        running = """\
            interface nve1
              no shutdown
              multisite border-gateway interface loopback100
            """
        config = {"enabled": True, "multisite_interface": "loopback100"}
        for state in ("merged", "replaced", "overridden"):
            self._run(running, config, state, changed=False)
        result = self._run(running, {"multisite_interface": "loopback101"}, "merged")
        self.assertEqual(
            result["commands"],
            ["interface nve1", "multisite border-gateway interface loopback101"],
        )
