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
    """
    Unit tests for the nxos_nve_interface.
    """

    module = nxos_nve_interface

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
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
        """
        Clean up after each test method.
        """
        super().tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_get_config.stop()

    def test_nxos_nve_interface_merged(self):
        """
        Test state merged.
        """
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
                        "address": "239.239.239.239",
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
            "global mcast-group 239.239.239.239 L2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_nve_interface_merged_idempotent(self):
        """
        Test idempotency for state merged.
        """
        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             description vxlan vtep
             advertise virtual-rmac
             host-reachability protocol bgp
             source-interface loopback1
             source-interface hold-down-time 60
             global mcast-group 239.239.239.239 L2
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
                        "address": "239.239.239.239",
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
        """
        Test state replaced.
        """
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
                        "address": "230.230.230.230",
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
            "global mcast-group 230.230.230.230 L2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_nve_interface_replaced_idempotent(self):
        """
        Test idempotency for state replaced.
        """
        self.get_config.return_value = dedent(
            """\
            interface nve1
             no shutdown
             advertise virtual-rmac
             host-reachability protocol bgp
             source-interface loopback1
             global mcast-group 230.230.230.230 L2
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
                        "address": "230.230.230.230",
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
        """
        Test state overridden.
        """
        self.get_config.return_value = dedent(
            """\
            interface nve1
             global mcast-group 230.230.230.230 L2
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
        """
        Test idempotency for state overridden.
        """
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
        """
        Test state deleted.
        """
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
