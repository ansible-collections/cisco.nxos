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
from typing import Sequence

__metaclass__ = type

from textwrap import dedent
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleFailJson,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_logging_global

from .nxos_module import TestNxosModule, set_module_args

ignore_provider_arg = True


class TestNxosLoggingGlobalModule(TestNxosModule):

    module = nxos_logging_global

    def setUp(self):
        super(TestNxosLoggingGlobalModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection"
        )
        self.get_resource_connection = (
            self.mock_get_resource_connection.start()
        )

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.logging_global.logging_global.Logging_globalFacts.get_config"
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosLoggingGlobalModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_logging_global_linear_merged(self):
        # test merged for linear attributes
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(severity="alert"),
                    module=dict(severity="notification"),
                    monitor=dict(severity="critical"),
                    history=dict(severity="informational", size=4096),
                    rate_limit="disabled",
                    rfc_strict=True,
                    origin_id=dict(string="nodeA"),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging console 1",
            "logging module 5",
            "logging monitor 2",
            "logging history 6",
            "logging history size 4096",
            "no logging rate-limit",
            "logging rfc-strict 5424",
            "logging origin-id string nodeA",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_merged_idempotent(self):
        # test merged for linear attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            logging origin-id string nodeA
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(severity="alert"),
                    module=dict(severity="notification"),
                    monitor=dict(severity="critical"),
                    history=dict(severity="informational", size=4096),
                    rate_limit="disabled",
                    rfc_strict=True,
                    origin_id=dict(string="nodeA"),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_logging_global_linear_merged_2(self):
        # test merged for linear attributes - 2
        self.get_config.return_value = dedent(
            """\
            logging console 1
            no logging module
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(state="disabled"),
                    module=dict(state="enabled"),
                    monitor=dict(state="disabled"),
                    history=dict(severity="informational", size=4096),
                    rate_limit="enabled",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no logging console 1",
            "logging module",
            "no logging monitor 2",
            "logging rate-limit",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_replaced(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            logging origin-id string nodeA
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(severity="notification"),
                    monitor=dict(severity="critical"),
                    history=dict(size=4096),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging console 5",
            "logging module",
            "no logging history 6",
            "logging rate-limit",
            "no logging rfc-strict 5424",
            "no logging origin-id string nodeA",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_replaced(self):
        # test replaced for linear attributes
        self.get_config.return_value = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(severity="notification"),
                    monitor=dict(severity="critical"),
                    history=dict(size=4096),
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging console 5",
            "logging module",
            "no logging history 6",
            "logging rate-limit",
            "no logging rfc-strict 5424",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_merged_3(self):
        # test merged for linear attributes - 3
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    origin_id=dict(hostname=True),
                    ip=dict(
                        access_list=dict(
                            cache=dict(
                                entries=16384, interval=200, threshold=80
                            ),
                            detailed=True,
                            include=dict(sgt=True),
                        )
                    ),
                    source_interface="Ethernet1/100",
                    timestamp="milliseconds",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging origin-id hostname",
            "logging ip access-list cache entries 16384",
            "logging ip access-list cache interval 200",
            "logging ip access-list cache threshold 80",
            "logging ip access-list detailed",
            "logging ip access-list include sgt",
            "logging source-interface Ethernet1/100",
            "logging timestamp milliseconds",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_merged_3_idempotent(self):
        # test merged for linear attributes - 3 (idempotent)
        self.get_config.return_value = dedent(
            """\
            logging origin-id hostname
            logging ip access-list cache entries 16384
            logging ip access-list cache interval 200
            logging ip access-list cache threshold 80
            logging ip access-list detailed
            logging ip access-list include sgt
            logging source-interface Ethernet1/100
            logging timestamp milliseconds
            """
        )
        set_module_args(
            dict(
                config=dict(
                    origin_id=dict(hostname=True),
                    ip=dict(
                        access_list=dict(
                            cache=dict(
                                entries=16384, interval=200, threshold=80
                            ),
                            detailed=True,
                            include=dict(sgt=True),
                        )
                    ),
                    source_interface="Ethernet1/100",
                    timestamp="milliseconds",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_logging_global_linear_replaced_3(self):
        # test replaced for linear attributes - 3
        self.get_config.return_value = dedent(
            """\
            logging origin-id hostname
            logging ip access-list cache entries 16384
            logging ip access-list cache interval 200
            logging ip access-list cache threshold 80
            logging ip access-list detailed
            logging ip access-list include sgt
            logging source-interface Ethernet1/100
            logging timestamp milliseconds
            """
        )
        set_module_args(
            dict(
                config=dict(
                    origin_id=dict(ip="192.168.1.1"),
                    ip=dict(
                        access_list=dict(
                            cache=dict(entries=16384, interval=210)
                        )
                    ),
                    source_interface="Ethernet1/120",
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no logging origin-id hostname",
            "logging origin-id ip 192.168.1.1",
            "logging ip access-list cache interval 210",
            "no logging ip access-list cache threshold 80",
            "no logging ip access-list detailed",
            "no logging ip access-list include sgt",
            "logging source-interface Ethernet1/120",
            "no logging timestamp milliseconds",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_complex_merged(self):
        # test merged for complex attributes
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    logfile=dict(
                        name="nodeA_log",
                        size=4096,
                        severity="critical",
                        persistent_threshold=80,
                    ),
                    facilities=[
                        dict(facility="auth", severity="alert"),
                        dict(facility="ospfv3", severity="critical"),
                        dict(facility="cron", severity="notification"),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging logfile nodeA_log 2 size 4096 persistent threshold 80",
            "logging level cron 5",
            "logging level ospfv3 2",
            "logging level auth 1",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_complex_merged_idempotent(self):
        # test merged for complex attributes (idempotent)
        self.get_config.return_value = dedent(
            """\
            logging logfile nodeA_log 2 size 4096 persistent threshold 80
            logging level cron 5
            logging level ospfv3 2
            logging level auth 1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    logfile=dict(
                        name="nodeA_log",
                        size=4096,
                        severity="critical",
                        persistent_threshold=80,
                    ),
                    facilities=[
                        dict(facility="auth", severity="alert"),
                        dict(facility="ospfv3", severity="critical"),
                        dict(facility="cron", severity="notification"),
                    ],
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_logging_global_complex_replaced(self):
        # test replaced for complex attributes
        self.get_config.return_value = dedent(
            """\
            logging logfile nodeA_log 2 size 4096 persistent threshold 80
            logging level cron 5
            logging level ospfv3 2
            logging level auth 1
            """
        )
        set_module_args(
            dict(
                config=dict(
                    facilities=[
                        dict(facility="auth", severity="alert"),
                        dict(facility="ospfv3", severity="critical"),
                        dict(facility="ospf", severity="notification"),
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )

        commands = [
            "logging logfile messages 5",
            "no logging level cron 5",
            "logging level ospf 5",
        ]

        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_event_merged(self):
        # test merged for `event`
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    event=dict(
                        link_status=dict(enable=False, default=False),
                        trunk_status=dict(enable=False, default=True),
                    )
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "no logging event link-status enable",
            "no logging event link-status default",
            "no logging event trunk-status enable",
            "logging event trunk-status default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_event_merged(self):
        # test merged for `event`
        self.get_config.return_value = dedent(
            """\
            no logging event link-status enable
            no logging event link-status default
            no logging event trunk-status enable
            logging event trunk-status default
            """
        )
        set_module_args(
            dict(
                config=dict(
                    event=dict(
                        link_status=dict(enable=False, default=False),
                        trunk_status=dict(enable=False, default=True),
                    )
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_logging_global_event_replaced(self):
        # test replaced for `event`
        self.get_config.return_value = dedent(
            """\
            no logging event link-status enable
            no logging event link-status default
            no logging event trunk-status enable
            logging event trunk-status default
            """
        )
        set_module_args(
            dict(
                config=dict(
                    event=dict(
                        link_status=dict(default=False),
                        trunk_status=dict(enable=False),
                    )
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )

        commands = [
            "logging event link-status enable",
            "no logging event trunk-status default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_gathered_empty(self):
        set_module_args(
            dict(running_config="", state="gathered"), ignore_provider_arg
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})

    def test_nxos_logging_global_gathered(self):
        # test gathered
        self.get_config.return_value = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            logging origin-id string nodeA
            """
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = {
            "console": {"severity": "alert"},
            "module": {"severity": "notification"},
            "monitor": {"severity": "critical"},
            "history": {"severity": "informational", "size": 4096},
            "rate_limit": "disabled",
            "rfc_strict": True,
            "origin_id": {"string": "nodeA"},
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_logging_global_parsed(self):
        # test parsed
        cfg = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            logging origin-id string nodeA
            """
        )
        set_module_args(
            dict(running_config=cfg, state="parsed"), ignore_provider_arg
        )
        parsed = {
            "console": {"severity": "alert"},
            "module": {"severity": "notification"},
            "monitor": {"severity": "critical"},
            "history": {"severity": "informational", "size": 4096},
            "rate_limit": "disabled",
            "rfc_strict": True,
            "origin_id": {"string": "nodeA"},
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_logging_global_hosts_merged(self):
        # test merged for `hosts`
        self.get_config.return_value = dedent(
            """\
            """
        )
        set_module_args(
            dict(
                config=dict(
                    hosts=[
                        dict(
                            host="192.168.1.1",
                            severity="alert",
                            facility="auth",
                            port=5891,
                            use_vrf="default",
                            secure=dict(
                                trustpoint=dict(client_identity="test")
                            ),
                        ),
                        dict(host="192.168.1.2"),
                        dict(host="192.168.1.3", severity="critical"),
                    ]
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging server 192.168.1.1 1 port 5891 secure trustpoint client-identity test facility auth use-vrf default",
            "logging server 192.168.1.2",
            "logging server 192.168.1.3 2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_hosts_replaced(self):
        # test replaced for `hosts`
        self.get_config.return_value = dedent(
            """\
            logging server 192.168.1.1 1 port 5891 secure trustpoint client-identity test facility auth use-vrf default
            logging server 192.168.1.2
            logging server 192.168.1.3 2
            """
        )
        set_module_args(
            dict(
                config=dict(
                    hosts=[
                        dict(
                            host="192.168.1.1",
                            severity="alert",
                            facility="auth",
                            port=5891,
                            use_vrf="default",
                            secure=dict(
                                trustpoint=dict(client_identity="test")
                            ),
                        ),
                        dict(
                            host="192.168.1.3",
                            severity="debugging",
                            use_vrf="management",
                        ),
                    ]
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging server 192.168.1.1 1 port 5891 secure trustpoint client-identity test facility auth use-vrf default",
            "no logging server 192.168.1.2",
            "no logging server 192.168.1.3 2",
            "logging server 192.168.1.3 7 use-vrf management",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_linear_negated_merged(self):
        # test merged for negated linear attributes
        self.get_config.return_value = dedent(
            """\
            no logging console
            no logging module
            no logging monitor
            """
        )
        set_module_args(
            dict(
                config=dict(
                    console=dict(severity="notification"),
                    module=dict(state="enabled"),
                    monitor=dict(severity="critical"),
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = ["logging console 5", "logging module", "logging monitor 2"]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_deleted(self):
        # test deleted
        self.get_config.return_value = dedent(
            """\
            logging console 1
            logging module 5
            logging monitor 2
            logging history 6
            logging history size 4096
            no logging rate-limit
            logging rfc-strict 5424
            logging origin-id string nodeA
            """
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = [
            "logging console",
            "logging module",
            "logging monitor",
            "no logging history 6",
            "no logging history size 4096",
            "logging rate-limit",
            "no logging rfc-strict 5424",
            "no logging origin-id string nodeA",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_event_replaced_2(self):
        # test replaced for `event` - 2
        self.get_config.return_value = dedent(
            """\
            no logging event link-status enable
            no logging event link-status default
            no logging event trunk-status enable
            logging event trunk-status default
            """
        )
        set_module_args(
            dict(
                config=dict(
                    event=dict(trunk_status=dict(enable=False, default=True))
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging event link-status enable",
            "logging event link-status default",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_logging_global_event_replaced_2(self):
        # test replaced for `event` - 2
        self.get_config.return_value = dedent(
            """\
            no logging event link-status enable
            no logging event link-status default
            no logging event trunk-status enable
            logging event trunk-status default
            """
        )
        set_module_args(
            dict(
                config=dict(console=dict(severity="critical")),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "logging event link-status enable",
            "logging event link-status default",
            "logging event trunk-status enable",
            "no logging event trunk-status default",
            "logging console 2",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))
