# (c) 2023 Red Hat Inc.
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


# remove purge
# add non fc interfaces to the sh run
# check else statements in config file


from __future__ import absolute_import, division, print_function


__metaclass__ = type

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.fc_interfaces import (
    allowed_port_modes,
    allowed_speed_values,
)
from ansible_collections.cisco.nxos.plugins.modules import nxos_fc_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

sh_run = """
interface mgmt0
  ip address 10.126.94.175 255.255.255.0
  no switchport description
  switchport speed auto
  switchport duplex auto
  snmp trap link-status
  no shutdown
  lldp transmit
  lldp receive
  cdp enable
  spanning-tree port-priority 128
  spanning-tree cost auto
  spanning-tree link-type auto
  no spanning-tree bpduguard
  no spanning-tree bpdufilter

interface vsan1
  no shutdown
  ip address 111.111.111.175 255.255.255.0
  spanning-tree port-priority 128
  spanning-tree cost auto
  spanning-tree link-type auto
  no spanning-tree bpduguard
  no spanning-tree bpdufilter


interface fc1/1
    no out-of-service force
    switchport speed auto
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description This is a sample line
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc1/2
    no out-of-service force
    switchport speed 1000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode E
    no switchport description
    switchport vl-credit default
    switchport trunk mode off
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no errdisable detect cause link-down
    no errdisable detect cause trustsec-violation
    no errdisable detect cause bit-errors
    no errdisable detect cause signal-loss
    no errdisable detect cause sync-loss
    no errdisable detect cause link-reset
    no errdisable detect cause credit-loss
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc1/3
    no out-of-service force
    switchport speed 2000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode F
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/1
    no out-of-service force
    switchport speed 4000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode Fx
    no switchport description
    switchport vl-credit default
    switchport trunk mode auto
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/2
    no out-of-service force
    switchport speed 8000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode NP
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown
interface fc18/3
    no out-of-service force
    switchport speed 10000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode SD
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/4
    no out-of-service force
    switchport speed 16000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown
interface fc18/5
    no out-of-service force
    switchport speed 32000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/6
    no out-of-service force
    switchport speed 64000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown
interface fc18/7
    no out-of-service force
    switchport speed auto max 2000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/8
    no out-of-service force
    switchport speed auto max 4000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    no switchport description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown
interface fc18/9
    no out-of-service force
    switchport speed auto max 8000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description sample description
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/10
    no out-of-service force
    analytics type fc-nvme
    switchport speed auto max 16000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description $
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    shutdown

interface fc18/11
    no out-of-service force
    analytics type fc-scsi
    switchport speed auto max 32000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description a
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    shutdown

interface fc18/12
    no out-of-service force
    analytics type fc-scsi
    analytics type fc-nvme
    switchport speed auto max 64000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description 1
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown

interface fc18/13
    no out-of-service force
    analytics type fc-scsi
    analytics type fc-nvme
    switchport speed auto max 64000
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description 1
    switchport vl-credit default
    switchport trunk mode on
    no switchport beacon
    switchport fcbbscn
    link-state-trap
    switchport fcrxbufsize 2112
    no port-license
    no switchport owner
    switchport encap default
    switchport fcrxbbcredit performance-buffers default
    no switchport ignore bit-errors
    no switchport ignore interrupt-thresholds
    switchport fill-pattern ARBFF speed 8000
    switchport logical-type auto
    switchport max-npiv-limit 0
    switchport trunk-max-npiv-limit 0
    no switchport link-diag
    no shutdown
    """

gath_val = [
    {
        "name": "fc1/1",
        "speed": "auto",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
        "description": "This is a sample line",
    },
    {
        "name": "fc1/2",
        "speed": "1000",
        "mode": "E",
        "trunk_mode": "off",
        "enabled": True,
    },
    {
        "name": "fc1/3",
        "speed": "2000",
        "mode": "F",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/1",
        "speed": "4000",
        "mode": "Fx",
        "trunk_mode": "auto",
        "enabled": True,
    },
    {
        "name": "fc18/2",
        "speed": "8000",
        "mode": "NP",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/3",
        "speed": "10000",
        "mode": "SD",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/4",
        "speed": "16000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/5",
        "speed": "32000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/6",
        "speed": "64000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/7",
        "speed": "auto max 2000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/8",
        "speed": "auto max 4000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
    },
    {
        "name": "fc18/9",
        "speed": "auto max 8000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
        "description": "sample description",
    },
    {
        "name": "fc18/10",
        "speed": "auto max 16000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": False,
        "description": "$",
        "analytics": "fc-nvme",
    },
    {
        "name": "fc18/11",
        "speed": "auto max 32000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": False,
        "description": "a",
        "analytics": "fc-scsi",
    },
    {
        "name": "fc18/12",
        "speed": "auto max 64000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
        "description": "1",
        "analytics": "fc-all",
    },
    {
        "name": "fc18/13",
        "speed": "auto max 64000",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
        "description": "1",
        "analytics": "fc-all",
    },
]


class TestNxosFcInterfacesModule(TestNxosModule):
    module = nxos_fc_interfaces

    def setUp(self):
        super(TestNxosFcInterfacesModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.fc_interfaces.fc_interfaces.Fc_interfacesFacts.get_interfaces_data",
        )
        self.get_config = self.mock_get_config.start()
        self.get_config.return_value = dedent(sh_run)

        self.maxDiff = None

    def tearDown(self):
        super(TestNxosFcInterfacesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_analytics_no_to_all_3_types(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-scsi",
                    "mode": "E",
                },
                {
                    "name": "fc1/2",
                    "analytics": "fc-nvme",
                },
                {
                    "name": "fc1/3",
                    "analytics": "fc-all",
                },
                {
                    "name": "fc18/12",
                    "analytics": "fc-scsi",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/1",
                "switchport mode E",
                "analytics type fc-scsi",
                "interface fc1/2",
                "analytics type fc-nvme",
                "interface fc1/3",
                "analytics type fc-all",
            ],
        )

    def test_gathered(self):
        # test gathered for config
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gath_val)

    def test_parsed(self):
        # test parsed for config
        set_module_args(dict(state="parsed", running_config=sh_run), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], gath_val)

    def test_idempotency(self):
        args = dict(
            config=gath_val,
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_analytics_all_to_scsi(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-scsi",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["commands"],
            [],
        )

    def test_analytics_all_to_scsi_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-scsi",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/12", "no analytics type fc-all", "analytics type fc-scsi"],
        )

    def test_analytics_all_to_nvme(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-nvme",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["commands"],
            [],
        )

    def test_analytics_all_to_nvme_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-nvme",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/12", "no analytics type fc-all", "analytics type fc-nvme"],
        )

    def test_analytics_all_to_none_checkthis(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_analytics_all_to_none_desc_change(self):
        args = dict(
            config=[
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "2",
                    "analytics": "fc-all",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc18/12", "switchport description 2"])

    def test_analytics_scsi_to_nvme(self):
        args = dict(
            config=[
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                    "analytics": "fc-nvme",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/11", "analytics type fc-nvme"],
        )

    def test_analytics_scsi_to_nvme_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                    "analytics": "fc-nvme",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/11", "no analytics type fc-all", "analytics type fc-nvme"],
        )

    def test_analytics_scsi_to_all(self):
        args = dict(
            config=[
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                    "analytics": "fc-all",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc18/11", "analytics type fc-all"])

    def test_analytics_scsi_to_all_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                    "analytics": "fc-all",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/11", "analytics type fc-all"],
        )

    def test_analytics_scsi_to_none_checkthis(self):
        args = dict(
            config=[
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_analytics_nvme_to_scsi(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                    "analytics": "fc-scsi",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/10", "analytics type fc-scsi"],
        )

    def test_analytics_nvme_to_scsi_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                    "analytics": "fc-scsi",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "no analytics type fc-all",
                "analytics type fc-scsi",
            ],
        )

    def test_analytics_nvme_to_all(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                    "analytics": "fc-all",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/10", "analytics type fc-all"],
        )

    def test_analytics_nvme_to_all_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                    "analytics": "fc-all",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "analytics type fc-all",
            ],
        )

    def test_analytics_none_to_scsi(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-scsi",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc1/1", "analytics type fc-scsi"])

    def test_analytics_none_to_scsi_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-scsi",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/1",
                "no switchport description",
                "no switchport speed auto",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "analytics type fc-scsi",
            ],
        )

    def test_analytics_none_to_nvme(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-nvme",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc1/1", "analytics type fc-nvme"])

    def test_analytics_none_to_nvme_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-nvme",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/1",
                "no switchport description",
                "no switchport speed auto",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "analytics type fc-nvme",
            ],
        )

    def test_analytics_none_to_nvme_overridden(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-nvme",
                },
            ],
            state="overridden",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/2",
                "no switchport speed 1000",
                "no switchport mode E",
                "switchport trunk mode on",
                "shutdown",
                "interface fc1/3",
                "no switchport speed 2000",
                "no switchport mode F",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/1",
                "no switchport speed 4000",
                "no switchport mode Fx",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/2",
                "no switchport speed 8000",
                "no switchport mode NP",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/3",
                "no switchport speed 10000",
                "no switchport mode SD",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/4",
                "no switchport speed 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/5",
                "no switchport speed 32000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/6",
                "no switchport speed 64000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/7",
                "no switchport speed auto max 2000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/8",
                "no switchport speed auto max 4000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/9",
                "no switchport description",
                "no switchport speed auto max 8000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "no analytics type fc-all",
                "interface fc18/11",
                "no switchport description",
                "no switchport speed auto max 32000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "no analytics type fc-all",
                "interface fc18/12",
                "no switchport description",
                "no switchport speed auto max 64000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "no analytics type fc-all",
                "interface fc18/13",
                "no switchport description",
                "no switchport speed auto max 64000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "no analytics type fc-all",
                "interface fc1/1",
                "no switchport description",
                "no switchport speed auto",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "analytics type fc-nvme",
            ],
        )

    def test_analytics_none_to_all(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-all",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc1/1", "analytics type fc-all"])

    def test_analytics_none_to_all_replaced(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "analytics": "fc-all",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/1",
                "no switchport description",
                "no switchport speed auto",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "analytics type fc-all",
            ],
        )

    def test_analytics_nvme_to_none_checkthis(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_description_change_from_one_to_another(self):
        args = dict(
            config=[
                {
                    "name": "fc18/9",
                    "description": "changed from sample description to new description",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/9",
                "switchport description changed from sample description to new description",
            ],
        )

    def test_description_change_from_none_to_new(self):
        args = dict(
            config=[
                {
                    "name": "fc18/8",
                    "description": "new sample description",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/8",
                "switchport description new sample description",
            ],
        )

    def test_shut_to_noshut(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                    "enabled": True,
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/10",
                "no shutdown",
            ],
        )

    def test_noshut_to_shut(self):
        args = dict(
            config=[
                {
                    "name": "fc18/6",
                    "enabled": False,
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/6", "shutdown"],
        )

    def test_trunkmode_auto_to_off(self):
        args = dict(
            config=[
                {
                    "name": "fc18/1",
                    "trunk_mode": "off",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/1", "switchport trunk mode off"],
        )

    def test_trunkmode_auto_to_on(self):
        args = dict(
            config=[
                {
                    "name": "fc18/1",
                    "trunk_mode": "on",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc18/1", "switchport trunk mode on"],
        )

    def test_trunkmode_on_to_off(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "trunk_mode": "off",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc1/1", "switchport trunk mode off"],
        )

    def test_trunkmode_on_to_auto(self):
        args = dict(
            config=[
                {
                    "name": "fc1/1",
                    "trunk_mode": "auto",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc1/1", "switchport trunk mode auto"],
        )

    def test_trunkmode_off_to_on(self):
        args = dict(
            config=[
                {
                    "name": "fc1/2",
                    "trunk_mode": "on",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc1/2", "switchport trunk mode on"],
        )

    def test_trunkmode_off_to_auto(self):
        args = dict(
            config=[
                {
                    "name": "fc1/2",
                    "trunk_mode": "auto",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["interface fc1/2", "switchport trunk mode auto"],
        )

    def test_speed_combinations(self):
        port_speed = "auto"
        port_name = "fc1/1"
        for each_speed in allowed_speed_values:
            args = dict(
                config=[
                    {
                        "name": port_name,
                        "speed": each_speed,
                    },
                ],
                state="merged",
            )
            if each_speed == port_speed:
                changed = False
                cmds = []
            else:
                changed = True
                cmds = [f"interface {port_name}", f"switchport speed {each_speed}"]

            set_module_args(args, ignore_provider_arg)
            result = self.execute_module(changed=changed)
            self.assertEqual(
                result["commands"],
                cmds,
            )

    def test_port_mode_combinations(self):
        port_mode = "auto"
        port_name = "fc1/1"
        for each_mode in allowed_port_modes:
            args = dict(
                config=[
                    {
                        "name": port_name,
                        "mode": each_mode,
                    },
                ],
                state="merged",
            )
            if each_mode == port_mode:
                changed = False
                cmds = []
            else:
                changed = True
                cmds = [f"interface {port_name}", f"switchport mode {each_mode}"]

            set_module_args(args, ignore_provider_arg)
            result = self.execute_module(changed=changed)
            self.assertEqual(
                result["commands"],
                cmds,
            )

    def test_deleted_1(self):
        # before- trunk mode on
        args = dict(
            config=[
                {
                    "name": "fc1/2",
                },
            ],
            state="deleted",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/2",
                "no switchport speed 1000",
                "no switchport mode E",
                "switchport trunk mode on",
                "shutdown",
            ],
        )

    def test_deleted_2(self):
        # before- trunk mode off
        args = dict(
            config=[
                {
                    "name": "fc1/3",
                },
            ],
            state="deleted",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/3",
                "no switchport speed 2000",
                "no switchport mode F",
                "switchport trunk mode on",
                "shutdown",
            ],
        )

    def test_deleted_3(self):
        # before- port shut and with description and analytics config
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                },
            ],
            state="deleted",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "no analytics type fc-all",
            ],
        )

    def test_replaced_move_to_def(self):
        args = dict(
            config=[
                {
                    "name": "fc18/10",
                },
            ],
            state="replaced",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "shutdown",
                "no analytics type fc-all",
            ],
        )

    def test_deleted_combined(self):
        args = dict(
            config=[
                {
                    "name": "fc1/2",
                },
                {
                    "name": "fc1/3",
                },
                {
                    "name": "fc18/10",
                },
            ],
            state="deleted",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/2",
                "no switchport speed 1000",
                "no switchport mode E",
                "switchport trunk mode on",
                "shutdown",
                "interface fc1/3",
                "no switchport speed 2000",
                "no switchport mode F",
                "switchport trunk mode on",
                "shutdown",
                "interface fc18/10",
                "no switchport description",
                "no switchport speed auto max 16000",
                "no switchport mode auto",
                "switchport trunk mode on",
                "no analytics type fc-all",
            ],
        )

    def test_most_of_them_combined(self):
        args = dict(
            config=[
                {
                    "name": "fc18/13",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-all",
                },
                {
                    "name": "fc18/12",
                    "speed": "auto max 64000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": True,
                    "description": "1",
                    "analytics": "fc-scsi",
                },
                {
                    "name": "fc18/11",
                    "speed": "auto max 32000",
                    "mode": "auto",
                    "trunk_mode": "on",
                    "enabled": False,
                    "description": "a",
                    "analytics": "fc-all",
                },
                {
                    "name": "fc18/10",
                    "analytics": "fc-scsi",
                    "enabled": True,
                },
                {
                    "name": "fc18/9",
                    "description": "changed from sample description to new description",
                },
                {
                    "name": "fc18/8",
                    "description": "new sample description",
                },
                {
                    "name": "fc18/6",
                    "enabled": False,
                },
                {
                    "name": "fc18/1",
                    "trunk_mode": "off",
                },
                {
                    "name": "fc1/1",
                    "trunk_mode": "auto",
                    "analytics": "fc-all",
                },
                {
                    "name": "fc1/2",
                    "trunk_mode": "on",
                },
            ],
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "interface fc1/1",
                "switchport trunk mode auto",
                "analytics type fc-all",
            ]
            + [
                "interface fc1/2",
                "switchport trunk mode on",
            ]
            + [
                "interface fc18/1",
                "switchport trunk mode off",
            ]
            + [
                "interface fc18/6",
                "shutdown",
            ]
            + [
                "interface fc18/8",
                "switchport description new sample description",
            ]
            + [
                "interface fc18/9",
                "switchport description changed from sample description to new description",
            ]
            + [
                "interface fc18/10",
                "no shutdown",
                # "no analytics type fc-all",
                "analytics type fc-scsi",
            ]
            + [
                "interface fc18/11",
                "analytics type fc-all",
            ],
            # + [
            #     "interface fc18/12",
            #     # "no analytics type fc-all",
            #     "analytics type fc-scsi",
            # ],
        )
