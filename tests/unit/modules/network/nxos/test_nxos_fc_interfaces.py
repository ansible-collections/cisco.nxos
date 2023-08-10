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


__metaclass__ = type

from textwrap import dedent

from ansible_collections.cisco.nxos.plugins.modules import nxos_fc_interfaces
from ansible_collections.cisco.nxos.tests.unit.compat.mock import patch

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


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

    def tearDown(self):
        super(TestNxosFcInterfacesModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    def test_nxos_1(self):
        # test gathered for empty config
        self.get_config.return_value = dedent(
            """\
            """,
        )
        a = {
            "state": "replaced",
            "config": [
                {
                    "analytics": "fc-scsi",
                    "name": "fc18/43",
                    "trunk_mode": False,
                    "speed": 8000,
                    "description": "configured by ansible script",
                    "enabled": True,
                    "mode": "auto",
                },
                {
                    "analytics": "fc-nvme",
                    "enabled": True,
                    "name": "fc18/45",
                    "description": "configured by ansible script to test second one",
                },
            ],
        }
        set_module_args(a, ignore_provider_arg)

        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], [])

    # def test_nxos_fc_interfaces_one(self):
    #     # test merged for linear attributes
    #     self.get_config.return_value = """
    #         interface fcip8


# 		use-profile 8
# 		peer-info ipaddr 1.1.1.32
#         tcp-connections 5
#         switchport mode E
#         spanning-tree port-priority 128
#         spanning-tree cost auto
#         spanning-tree link-type auto
#         no spanning-tree bpduguard
#         no spanning-tree bpdufilter
#         no switchport description
#         switchport vl-credit default
#         switchport trunk mode on
#         link-state-trap
#         switchport fec
#         switchport fec tts
#         no shutdown

#         interface fc1/1
#         no out-of-service force
#         switchport speed auto max 64000
#         no transceiver-frequency ethernet
#         switchport rate-mode default
#         switchport fcrxbbcredit default
#         switchport mode auto
#         no switchport description
#         switchport vl-credit default
#         switchport trunk mode on
#         no switchport beacon
#         switchport fcbbscn
#         link-state-trap
#         switchport fcrxbufsize 2112
#         no port-license
#         no errdisable detect cause link-down
#         no errdisable detect cause trustsec-violation
#         no errdisable detect cause bit-errors
#         no errdisable detect cause signal-loss
#         no errdisable detect cause sync-loss
#         no errdisable detect cause link-reset
#         no errdisable detect cause credit-loss
#         no switchport owner
#         switchport encap default
#         switchport fcrxbbcredit performance-buffers default
#         no switchport ignore bit-errors
#         no switchport ignore interrupt-thresholds
#         switchport fill-pattern ARBFF speed 8000
#         switchport logical-type auto
#         switchport max-npiv-limit 0
#         switchport trunk-max-npiv-limit 0
#         no switchport link-diag
#         no shutdown

#         interface fc1/2
#         no out-of-service force
#         switchport speed auto max 64000
#         no transceiver-frequency ethernet
#         switchport rate-mode default
#         switchport fcrxbbcredit default
#         switchport mode auto
#         no switchport description
#         switchport vl-credit default
#         switchport trunk mode on
#         no switchport beacon
#         switchport fcbbscn
#         link-state-trap
#         switchport fcrxbufsize 2112
#         no port-license
#         no errdisable detect cause link-down
#         no errdisable detect cause trustsec-violation
#         no errdisable detect cause bit-errors
#         no errdisable detect cause signal-loss
#         no errdisable detect cause sync-loss
#         no errdisable detect cause link-reset
#         no errdisable detect cause credit-loss
#         no switchport owner
#         switchport encap default
#         switchport fcrxbbcredit performance-buffers default
#         no switchport ignore bit-errors
#         no switchport ignore interrupt-thresholds
#         switchport fill-pattern ARBFF speed 8000
#         switchport logical-type auto
#         switchport max-npiv-limit 0
#         switchport trunk-max-npiv-limit 0
#         no switchport link-diag
#         no shutdown
#     """
#     set_module_args(
#         dict(
#             config=[
#                 {
#                     "name": "fc1/1",
#                     "description": "configured by ansible script",
#                 },
#             ],
#             state="merged",
#         ),
#         ignore_provider_arg,
#     )
#     commands = [
#         "route-map rmap1 permit 10",
#         "description rmap1-permit-10",
#         "continue 30",
#         "route-map rmap1 deny 40",
#         "description rmap1-deny-40",
#         "set as-path prepend last-as 10",
#         "set as-path tag",
#         "set comm-list comm1 delete",
#         "set dampening 10 20 30 80",
#         "set extcomm-list extcomm1 delete",
#         "set forwarding-address",
#         "route-map rmap2 permit 10",
#         "set interface null0",
#         "set tag 10",
#         "set weight 40",
#     ]
#     result = self.execute_module(changed=True)
#     self.assertEqual(set(result["commands"]), set(commands))
