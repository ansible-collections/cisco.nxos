# (c) 2025 Red Hat Inc.
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


from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_hsrp_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosHsrpInterfacesModule(TestNxosModule):
    module = nxos_hsrp_interfaces

    def setUp(self):
        super(TestNxosHsrpInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.hsrp_interfaces.hsrp_interfaces.Hsrp_interfacesFacts.get_hsrp_data",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosHsrpInterfacesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_hsrp_interfaces_merged(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan1",
                        "standby": {"version": 2},
                        "standby_options": [
                            {
                                "authentication": {"key_chain": "KEYCHAIN1"},
                                "group_no": 10,
                                "timer": {"hello_interval": 200, "hold_time": 700, "msec": True},
                            },
                        ],
                    },
                    {
                        "name": "Vlan14",
                        "standby": {
                            "bfd": True,
                            "delay": {"minimum": 30, "reload": 300},
                            "mac_refresh": 300,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "follow": "VLAN14-GROUP",
                                "group_no": 14,
                                "ip": [
                                    {"secondary": True, "virtual_ip": "192.168.14.2"},
                                    {"virtual_ip": "192.168.14.1"},
                                ],
                                "mac_address": "00AA.14BB.14CC",
                                "track": [
                                    {"decrement": 20, "object_no": 101},
                                    {"decrement": 30, "object_no": 102},
                                ],
                            },
                            {
                                "authentication": {"key_string": "SECUREKEY14"},
                                "group_no": 15,
                                "mac_address": "00BB.14CC.15DD",
                                "preempt": {"minimum": 10, "reload": 100, "sync": 5},
                                "priority": {"level": 110, "lower": 90, "upper": 130},
                                "timer": {"hello_interval": 300, "hold_time": 900, "msec": True},
                            },
                        ],
                    },
                    {"name": "Vlan2"},
                    {
                        "name": "Vlan10",
                        "standby": {
                            "bfd": True,
                            "delay": {"minimum": 40, "reload": 200},
                            "mac_refresh": 400,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "authentication": {"key_string": "SECUREKEY10"},
                                "group_name": "VLAN10-GROUP",
                                "group_no": 10,
                                "ip": [{"secondary": True, "virtual_ip": "10.10.10.2"}],
                                "mac_address": "00CC.10DD.10EE",
                                "preempt": {"minimum": 15, "reload": 120, "sync": 10},
                                "priority": {"level": 100, "lower": 80, "upper": 120},
                                "timer": {"hello_interval": 250, "hold_time": 750, "msec": True},
                                "track": [
                                    {"decrement": 25, "object_no": 201},
                                    {"decrement": 35, "object_no": 202},
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Vlan1",
            "hsrp version 2",
            "hsrp 10",
            "timers msec 200 700",
            "authentication md5 key-chain KEYCHAIN1",
            "interface Vlan14",
            "hsrp version 2",
            "hsrp bfd",
            "hsrp delay 30 300",
            "hsrp mac-refresh 300",
            "hsrp 14",
            "follow VLAN14-GROUP",
            "mac-address 00AA.14BB.14CC",
            "ip 192.168.14.2 secondary",
            "ip 192.168.14.1",
            "track 101 decrement 20",
            "track 102 decrement 30",
            "hsrp 15",
            "mac-address 00BB.14CC.15DD",
            "preempt delay minimum 10 reload 100 sync 5",
            "priority 110 forwarding-threshold lower 90 upper 130",
            "timers msec 300 900",
            "authentication md5 key-string SECUREKEY14",
            "interface Vlan10",
            "hsrp version 2",
            "hsrp bfd",
            "hsrp delay 40 200",
            "hsrp mac-refresh 400",
            "hsrp 10",
            "mac-address 00CC.10DD.10EE",
            "name VLAN10-GROUP",
            "preempt delay minimum 15 reload 120 sync 10",
            "priority 100 forwarding-threshold lower 80 upper 120",
            "timers msec 250 750",
            "authentication md5 key-string SECUREKEY10",
            "ip 10.10.10.2 secondary",
            "track 201 decrement 25",
            "track 202 decrement 35",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_hsrp_interfaces_merged_idempotent(self):
        self.get_config.return_value = dedent(
            """\
                interface Vlan1
                  hsrp version 2
                  hsrp 10
                    authentication md5 key-chain KEYCHAIN1
                    timers msec 250  255
                interface Vlan10
                  hsrp bfd
                  hsrp version 2
                  hsrp mac-refresh 400
                  hsrp 10
                    authentication md5 key-string SECUREKEY10
                    name VLAN10-GROUP
                    mac-address 00CC.10DD.10EE
                    preempt delay minimum 15 reload 120 sync 10
                    ip 10.10.10.2 secondary
                interface Vlan14
                  bandwidth 99999
                  hsrp bfd
                  hsrp version 2
                  hsrp delay minimum 22 reload 123
                  hsrp mac-refresh 300
                  hsrp 14
                    follow VLAN14-GROUP
                    mac-address 00AA.14BB.14CC
                    ip 192.168.14.1 secondary
                    ip 192.168.14.2 secondary
                  hsrp 15
                    authentication md5 key-string SECUREKEY14
                    mac-address 00BB.14CC.15DD
                    preempt delay minimum 10 reload 100 sync 5
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                interface Vlan1000
                  hsrp 10
                    authentication md5 key-string SECUREKEY100
                    name VLAN100-GROUP
                    mac-address 00AA.14BB.14KC
                    preempt delay minimum 33 reload 23 sync 22
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                    ip 192.168.14.2 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan1",
                        "standby": {"version": 2},
                        "standby_options": [
                            {
                                "authentication": {"key_chain": "KEYCHAIN1"},
                                "group_no": 10,
                                "timer": {"hello_interval": 250, "hold_time": 255, "msec": True},
                            },
                        ],
                    },
                    {
                        "name": "Vlan14",
                        "standby": {
                            "bfd": True,
                            "delay": {"minimum": 22, "reload": 123},
                            "mac_refresh": 300,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "follow": "VLAN14-GROUP",
                                "group_no": 14,
                                "ip": [
                                    {"secondary": True, "virtual_ip": "192.168.14.2"},
                                    {"virtual_ip": "192.168.14.1"},
                                ],
                                "mac_address": "00AA.14BB.14CC",
                            },
                            {
                                "authentication": {"key_string": "SECUREKEY14"},
                                "group_no": 15,
                                "mac_address": "00BB.14CC.15DD",
                                "preempt": {"minimum": 10, "reload": 100, "sync": 5},
                                "priority": {"level": 22, "lower": 12, "upper": 22},
                                "timer": {"hello_interval": 456, "hold_time": 33, "msec": True},
                            },
                        ],
                    },
                    {"name": "Vlan2"},
                    {
                        "name": "Vlan10",
                        "standby": {
                            "bfd": True,
                            "mac_refresh": 400,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "authentication": {"key_string": "SECUREKEY10"},
                                "group_name": "VLAN10-GROUP",
                                "group_no": 10,
                                "ip": [{"secondary": True, "virtual_ip": "10.10.10.2"}],
                                "mac_address": "00CC.10DD.10EE",
                                "preempt": {"minimum": 15, "reload": 120, "sync": 10},
                            },
                        ],
                    },
                ],
                state="merged",
            ),
            ignore_provider_arg,
        )
        self.execute_module(changed=False)

    def test_nxos_hsrp_interfaces_overridden(self):
        self.get_config.return_value = dedent(
            """\
                interface Vlan1
                  hsrp version 2
                  hsrp 10
                    authentication md5 key-chain KEYCHAIN1
                    timers msec 250  255
                interface Vlan10
                  hsrp bfd
                  hsrp version 2
                  hsrp mac-refresh 400
                  hsrp 10
                    authentication md5 key-string SECUREKEY10
                    name VLAN10-GROUP
                    mac-address 00CC.10DD.10EE
                    preempt delay minimum 15 reload 120 sync 10
                    ip 10.10.10.2 secondary
                interface Vlan14
                  bandwidth 99999
                  hsrp bfd
                  hsrp version 2
                  hsrp delay minimum 22 reload 123
                  hsrp mac-refresh 300
                  hsrp 14
                    follow VLAN14-GROUP
                    mac-address 00AA.14BB.14CC
                    ip 192.168.14.1 secondary
                    ip 192.168.14.2 secondary
                  hsrp 15
                    authentication md5 key-string SECUREKEY14
                    mac-address 00BB.14CC.15DD
                    preempt delay minimum 10 reload 100 sync 5
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                interface Vlan1000
                  hsrp 10
                    authentication md5 key-string SECUREKEY100
                    name VLAN100-GROUP
                    mac-address 00AA.14BB.14KC
                    preempt delay minimum 33 reload 23 sync 22
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                    ip 192.168.14.2 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan1",
                        "standby": {"version": 2},
                        "standby_options": [
                            {
                                "authentication": {"key_chain": "KEYCHAIN1"},
                                "group_no": 10,
                                "timer": {"hello_interval": 250, "hold_time": 255, "msec": True},
                            },
                        ],
                    },
                    {
                        "name": "Vlan14",
                        "standby": {
                            "bfd": True,
                            "delay": {"minimum": 22, "reload": 123},
                            "mac_refresh": 300,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "follow": "VLAN14-GROUP",
                                "group_no": 12,
                                "ip": [
                                    {"secondary": True, "virtual_ip": "192.168.14.2"},
                                    {"virtual_ip": "192.168.14.1"},
                                ],
                                "mac_address": "00AA.14BB.14CC",
                            },
                            {
                                "authentication": {"key_string": "SECUREKEY14"},
                                "group_no": 15,
                                "mac_address": "00BB.14CC.15DD",
                                "preempt": {"minimum": 10, "reload": 100, "sync": 5},
                                "priority": {"level": 22, "lower": 12, "upper": 22},
                                "timer": {"hello_interval": 456, "hold_time": 33, "msec": True},
                            },
                        ],
                    },
                    {"name": "Vlan2"},
                    {
                        "name": "Vlan10",
                        "standby": {
                            "bfd": True,
                            "mac_refresh": 400,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "authentication": {"key_string": "SECUREKEY10"},
                                "group_name": "VLAN10-GROUP",
                                "group_no": 11,
                                "ip": [{"secondary": True, "virtual_ip": "10.10.10.2"}],
                                "mac_address": "00CC.10DD.10EE",
                                "preempt": {"minimum": 15, "reload": 120, "sync": 10},
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Vlan1000",
            "no hsrp 10",
            "interface Vlan14",
            "hsrp 12",
            "follow VLAN14-GROUP",
            "mac-address 00AA.14BB.14CC",
            "ip 192.168.14.2 secondary",
            "ip 192.168.14.1",
            "no hsrp 14",
            "interface Vlan10",
            "hsrp 11",
            "mac-address 00CC.10DD.10EE",
            "name VLAN10-GROUP",
            "preempt delay minimum 15 reload 120 sync 10",
            "authentication md5 key-string SECUREKEY10",
            "ip 10.10.10.2 secondary",
            "no hsrp 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_hsrp_interfaces_replaced(self):
        self.get_config.return_value = dedent(
            """\
                interface Vlan1
                  hsrp version 2
                  hsrp 10
                    authentication md5 key-chain KEYCHAIN1
                    timers msec 250  255
                interface Vlan10
                  hsrp bfd
                  hsrp version 2
                  hsrp mac-refresh 400
                  hsrp 10
                    authentication md5 key-string SECUREKEY10
                    name VLAN10-GROUP
                    mac-address 00CC.10DD.10EE
                    preempt delay minimum 15 reload 120 sync 10
                    ip 10.10.10.2 secondary
                interface Vlan14
                  bandwidth 99999
                  hsrp bfd
                  hsrp version 2
                  hsrp delay minimum 22 reload 123
                  hsrp mac-refresh 300
                  hsrp 14
                    follow VLAN14-GROUP
                    mac-address 00AA.14BB.14CC
                    ip 192.168.14.1 secondary
                    ip 192.168.14.2 secondary
                  hsrp 15
                    authentication md5 key-string SECUREKEY14
                    mac-address 00BB.14CC.15DD
                    preempt delay minimum 10 reload 100 sync 5
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                interface Vlan1000
                  hsrp 10
                    authentication md5 key-string SECUREKEY100
                    name VLAN100-GROUP
                    mac-address 00AA.14BB.14KC
                    preempt delay minimum 33 reload 23 sync 22
                    priority 22 forwarding-threshold lower 12 upper 22
                    timers msec 456  33
                    ip 192.168.14.2 secondary
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan1",
                        "standby": {"version": 2},
                        "standby_options": [
                            {
                                "authentication": {"key_chain": "KEYCHAIN1"},
                                "group_no": 10,
                                "timer": {"hello_interval": 250, "hold_time": 255, "msec": True},
                            },
                        ],
                    },
                    {
                        "name": "Vlan14",
                        "standby": {
                            "bfd": True,
                            "delay": {"minimum": 22, "reload": 123},
                            "mac_refresh": 300,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "follow": "VLAN14-GROUP",
                                "group_no": 14,
                                "ip": [
                                    {"secondary": True, "virtual_ip": "192.168.14.2"},
                                ],
                                "mac_address": "00AA.14BB.14CC",
                            },
                            {
                                "authentication": {"key_string": "SECUREKEY14"},
                                "group_no": 15,
                                "mac_address": "00BB.14CC.15DD",
                                "preempt": {"minimum": 10, "reload": 100, "sync": 5},
                                "priority": {"level": 22, "lower": 12, "upper": 22},
                                "timer": {"hello_interval": 456, "hold_time": 33, "msec": True},
                            },
                        ],
                    },
                    {"name": "Vlan2"},
                    {
                        "name": "Vlan10",
                        "standby": {
                            "bfd": True,
                            "mac_refresh": 400,
                            "version": 2,
                        },
                        "standby_options": [
                            {
                                "authentication": {"key_string": "SECUREKEY10"},
                                "group_name": "VLAN10-GROUP",
                                "group_no": 11,
                                "ip": [{"secondary": True, "virtual_ip": "10.10.10.2"}],
                                "mac_address": "00CC.10DD.10EE",
                                "preempt": {"minimum": 15, "reload": 120, "sync": 10},
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "interface Vlan14",
            "hsrp 14",
            "no ip 192.168.14.1 secondary",
            "interface Vlan10",
            "hsrp 11",
            "mac-address 00CC.10DD.10EE",
            "name VLAN10-GROUP",
            "preempt delay minimum 15 reload 120 sync 10",
            "authentication md5 key-string SECUREKEY10",
            "ip 10.10.10.2 secondary",
            "no hsrp 10",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(set(result["commands"]), set(commands))

    def test_nxos_hsrp_interfaces_deprecated_bfd(self):
        self.get_config.return_value = dedent(
            """\
                interface Vlan1
                  hsrp version 2
                interface Vlan10
                  hsrp bfd
                interface Vlan14
                  bandwidth 99999
                  hsrp bfd
                interface Vlan1000
                  hsrp 10
                    authentication md5 key-string SECUREKEY100
            """,
        )
        set_module_args(
            dict(
                config=[
                    {
                        "name": "Vlan1",
                        "bfd": "enable",
                    },
                    {
                        "name": "Vlan14",
                        "bfd": "enable",
                    },
                    {"name": "Vlan2"},
                    {
                        "name": "Vlan10",
                        "bfd": "disable",
                    },
                ],
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        commands = [
            "interface Vlan1",
            "hsrp bfd",
            "interface Vlan10",
            "no hsrp bfd",
            "no hsrp version 2",
        ]
        self.assertEqual(set(result["commands"]), set(commands))
