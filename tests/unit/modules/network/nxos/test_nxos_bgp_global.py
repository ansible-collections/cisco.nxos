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
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_bgp_global

from .nxos_module import TestNxosModule, load_fixture, set_module_args

ignore_provider_arg = True


class TestNxosBgpGlobalModule(TestNxosModule):

    module = nxos_bgp_global

    def setUp(self):
        super(TestNxosBgpGlobalModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.bgp_global.bgp_global.Bgp_globalFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

        self.mock_cfg_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.bgp_global.bgp_global.Bgp_global._get_config"
        )
        self.cfg_get_config = self.mock_cfg_get_config.start()

    def tearDown(self):
        super(TestNxosBgpGlobalModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()
        self.cfg_get_config.stop()

    def test_nxos_bgp_global_merged(self):
        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.2",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=160),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        ),
                        dict(
                            neighbor_address="198.51.100.21",
                            remote_as="65537",
                            password=dict(
                                encryption=7, key="12090404011C03162E"
                            ),
                        ),
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                            neighbors=[
                                dict(
                                    neighbor_address="192.0.2.10",
                                    neighbor_affinity_group=dict(group_id=161),
                                    remote_as="65538",
                                    description="site-1-nbr-1",
                                    password=dict(
                                        encryption=3,
                                        key="13D4D3549493D2877B1DC116EE27A6BE",
                                    ),
                                )
                            ],
                        ),
                        dict(
                            vrf="site-2",
                            local_as="300",
                            log_neighbor_changes=True,
                            neighbor_down=dict(fib_accelerate=True),
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "log-neighbor-changes",
            "maxas-limit 20",
            "router-id 198.51.100.2",
            "neighbor 198.51.100.20",
            "remote-as 65537",
            "affinity-group 160",
            "description NBR-1",
            "low-memory exempt",
            "neighbor 198.51.100.21",
            "remote-as 65537",
            "password 7 12090404011C03162E",
            "vrf site-1",
            "local-as 200",
            "log-neighbor-changes",
            "neighbor 192.0.2.10",
            "affinity-group 161",
            "remote-as 65538",
            "description site-1-nbr-1",
            "password 3 13D4D3549493D2877B1DC116EE27A6BE",
            "vrf site-2",
            "local-as 300",
            "log-neighbor-changes",
            "neighbor-down fib-accelerate",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_global_merged_idempotent(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 160
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 161
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.2",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=160),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        ),
                        dict(
                            neighbor_address="198.51.100.21",
                            remote_as="65537",
                            password=dict(
                                encryption=7, key="12090404011C03162E"
                            ),
                        ),
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                            neighbors=[
                                dict(
                                    neighbor_address="192.0.2.10",
                                    neighbor_affinity_group=dict(group_id=161),
                                    remote_as="65538",
                                    description="site-1-nbr-1",
                                    password=dict(
                                        encryption=3,
                                        key="13D4D3549493D2877B1DC116EE27A6BE",
                                    ),
                                )
                            ],
                        ),
                        dict(
                            vrf="site-2",
                            local_as="300",
                            log_neighbor_changes=True,
                            neighbor_down=dict(fib_accelerate=True),
                        ),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_global_replaced(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.212",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=161),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                            neighbors=[
                                dict(
                                    neighbor_address="192.0.2.10",
                                    neighbor_affinity_group=dict(group_id=190),
                                    remote_as="65538",
                                    description="site-1-nbr-1",
                                    password=dict(
                                        encryption=3,
                                        key="13D4D3549493D2877B1DC116EE27A6BE",
                                    ),
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "router bgp 65536",
            "router-id 198.51.100.212",
            "no neighbor 198.51.100.21",
            "vrf site-1",
            "neighbor 192.0.2.10",
            "affinity-group 190",
            "no vrf site-2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_global_replaced_idempotent(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.212
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 190
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.212",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=161),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                            neighbors=[
                                dict(
                                    neighbor_address="192.0.2.10",
                                    neighbor_affinity_group=dict(group_id=190),
                                    remote_as="65538",
                                    description="site-1-nbr-1",
                                    password=dict(
                                        encryption=3,
                                        key="13D4D3549493D2877B1DC116EE27A6BE",
                                    ),
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_global_replaced_failed_1(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                address-family ipv4 unicast
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.212",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=161),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        )
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                            neighbors=[
                                dict(
                                    neighbor_address="192.0.2.10",
                                    neighbor_affinity_group=dict(group_id=190),
                                    remote_as="65538",
                                    description="site-1-nbr-1",
                                    password=dict(
                                        encryption=3,
                                        key="13D4D3549493D2877B1DC116EE27A6BE",
                                    ),
                                )
                            ],
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(failed=True)

    def test_nxos_bgp_global_replaced_failed_2(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                address-family ipv4 unicast
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.2",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=160),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        ),
                        dict(
                            neighbor_address="198.51.100.21",
                            remote_as="65537",
                            password=dict(
                                encryption=7, key="12090404011C03162E"
                            ),
                        ),
                    ],
                    vrfs=[
                        dict(
                            vrf="site-2",
                            local_as="300",
                            log_neighbor_changes=True,
                            neighbor_down=dict(fib_accelerate=True),
                        )
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(failed=True)

    def test_nxos_bgp_global_replaced_failed_3(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  address-family ipv4 unicast
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(
                config=dict(
                    as_number="65536",
                    router_id="198.51.100.2",
                    log_neighbor_changes=True,
                    maxas_limit=20,
                    neighbors=[
                        dict(
                            neighbor_address="198.51.100.20",
                            neighbor_affinity_group=dict(group_id=160),
                            remote_as="65537",
                            description="NBR-1",
                            low_memory=dict(exempt=True),
                        ),
                        dict(
                            neighbor_address="198.51.100.21",
                            remote_as="65537",
                            password=dict(
                                encryption=7, key="12090404011C03162E"
                            ),
                        ),
                    ],
                    vrfs=[
                        dict(
                            vrf="site-1",
                            local_as="200",
                            log_neighbor_changes=True,
                        ),
                        dict(
                            vrf="site-2",
                            local_as="300",
                            log_neighbor_changes=True,
                            neighbor_down=dict(fib_accelerate=True),
                        ),
                    ],
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(failed=True)

    def test_nxos_bgp_global_deleted(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "router bgp 65536",
            "no log-neighbor-changes",
            "no maxas-limit 20",
            "no router-id 198.51.100.2",
            "no neighbor 198.51.100.20",
            "no neighbor 198.51.100.21",
            "no vrf site-1",
            "no vrf site-2",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_global_deleted_idempotent_1(self):
        run_cfg = dedent(
            """\
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(dict(state="deleted"), ignore_provider_arg)

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_global_deleted_idempotent_2(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(
            dict(config=dict(as_number="65539"), state="deleted"),
            ignore_provider_arg,
        )

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_bgp_global_deleted_failed(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                address-family ipv4 unicast
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(dict(state="deleted"), ignore_provider_arg)
        result = self.execute_module(failed=True)

    def test_nxos_bgp_global_purged(self):
        run_cfg = dedent(
            """\
            router bgp 65536
              log-neighbor-changes
              maxas-limit 20
              router-id 198.51.100.2
              neighbor 198.51.100.20
                remote-as 65537
                affinity-group 161
                description NBR-1
                low-memory exempt
              neighbor 198.51.100.21
                remote-as 65537
                password 7 12090404011C03162E
              vrf site-1
                local-as 200
                log-neighbor-changes
                neighbor 192.0.2.10
                  affinity-group 170
                  remote-as 65538
                  description site-1-nbr-1
                  password 3 13D4D3549493D2877B1DC116EE27A6BE
              vrf site-2
                local-as 300
                log-neighbor-changes
                neighbor-down fib-accelerate
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(dict(state="purged"), ignore_provider_arg)
        commands = ["no router bgp 65536"]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_bgp_global_purged_idempotent(self):
        run_cfg = dedent(
            """\
            """
        )
        self.get_config.return_value = run_cfg
        self.cfg_get_config.return_value = run_cfg

        set_module_args(dict(state="purged"), ignore_provider_arg)

        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
