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

from __future__ import absolute_import, division, print_function
import re

__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.nxos.plugins.modules import nxos_fc_interfaces
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

sh_run = """
interface fc1/1
    no out-of-service force
    switchport speed auto
    no transceiver-frequency ethernet
    switchport rate-mode default
    switchport fcrxbbcredit default
    switchport mode auto
    switchport description This is a long line of description for port fc18/1 which is of 254 characters to test with ansible This is a long line of description for port fc18/1 which is of 254 characters to test with ansible A B C D E F G H I J K L M N O P Q R S T U V W X Y Z BYE
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
    """

gath_val = [
    {
        "name": "fc1/1",
        "speed": "auto",
        "mode": "auto",
        "trunk_mode": "on",
        "enabled": True,
        "description": "This is a long line of description for port fc18/1 which is of 254 characters to test with ansible This is a long line of description for port fc18/1 which is of 254 characters to test with ansible A B C D E F G H I J K L M N O P Q R S T U V W X Y Z BYE",
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
]


class TestNxosFcInterfacesModule(TestNxosModule):
    # Testing strategy
    # ------------------
    # (a) The unit tests cover `merged` and `replaced` for every attribute.
    #     Since `overridden` is essentially `replaced` but at a larger
    #     scale, these indirectly cover `overridden` as well.

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

    def test_fc_interfaces_gathered(self):
        # test gathered for config
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gath_val)

    def test_fc_interfaces_idempotency(self):
        args = dict(
            config=gath_val,
            state="merged",
        )
        set_module_args(args, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_fc_interfaces_analytics_all_to_scsi(self):
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
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc18/12", "no analytics type fc-nvme"])

    def test_fc_interfaces_analytics_all_to_nvme(self):
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
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["interface fc18/12", "no analytics type fc-scsi"])

    def test_fc_interfaces_analytics_all_to_none_checkthis(self):
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

    def test_fc_interfaces_analytics_scsi_to_nvme(self):
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
            ["interface fc18/11", "no analytics type fc-scsi", "analytics type fc-nvme"],
        )

    # def test_fc_interfaces_analytics_scsi_to_all(self):
    #     args = dict(
    #         config=[
    #             {
    #                 "name": "fc18/11",
    #                 "speed": "auto max 32000",
    #                 "mode": "auto",
    #                 "trunk_mode": "on",
    #                 "enabled": False,
    #                 "description": "a",
    #                 "analytics": "fc-all",
    #             },
    #         ],
    #         state="merged",
    #     )
    #     set_module_args(args, ignore_provider_arg)
    #     result = self.execute_module(changed=True)
    #     self.assertEqual(result["commands"], ["interface fc18/11", "analytics type fc-nvme"])

    # def test_fc_interfaces_analytics_scsi_to_none_checkthis(self):
    #     args = dict(
    #         config=[
    #             {
    #                 "name": "fc18/11",
    #                 "speed": "auto max 32000",
    #                 "mode": "auto",
    #                 "trunk_mode": "on",
    #                 "enabled": False,
    #                 "description": "a",
    #             },
    #         ],
    #         state="merged",
    #     )
    #     set_module_args(args, ignore_provider_arg)
    #     result = self.execute_module(changed=False)
    #     self.assertEqual(result["commands"], [])
