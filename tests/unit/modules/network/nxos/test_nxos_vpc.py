# (c) 2024 Red Hat Inc.
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
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vpc

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosVpcModule(TestNxosModule):
    module = nxos_vpc

    def setUp(self):
        super(TestNxosVpcModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vpc.vpc.VpcFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosVpcModule, self).tearDown()
        self.get_resource_connection.stop()
        self.get_config.stop()

    # -- merged ------------------------------------------------------------

    def test_nxos_vpc_merged_empty_have(self):
        # a device with feature vpc enabled but no domain configured must not
        # trip the `domain` required-suboption check while gathering facts
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    domain="10",
                    role_priority="150",
                    system_priority="2000",
                    pkl_dest="192.168.2.2",
                    pkl_src="192.168.2.1",
                    pkl_vrf="management",
                    peer_gw=True,
                    auto_recovery=True,
                    delay_restore="150",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "vpc domain 10",
            "role priority 150",
            "system-priority 2000",
            "delay restore 150",
            "auto-recovery",
            "peer-gateway",
            "peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)
        self.assertEqual(result["before"], {})

    def test_nxos_vpc_merged_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              system-priority 2000
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
              delay restore 150
              peer-gateway
              auto-recovery
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    domain="10",
                    role_priority="150",
                    system_priority="2000",
                    pkl_dest="192.168.2.2",
                    pkl_src="192.168.2.1",
                    peer_gw=True,
                    auto_recovery=True,
                    delay_restore="150",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_merged_default_pkl_vrf_idempotent(self):
        # NX-OS does not write `vrf management` to running-config, so asking
        # for the default VRF must not re-push the keepalive line every run
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    domain="10",
                    pkl_dest="192.168.2.2",
                    pkl_src="192.168.2.1",
                    pkl_vrf="management",
                ),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_merged_pkl_retains_existing_keys(self):
        # merged layers want on top of have, so an omitted optional key is
        # carried over instead of being dropped from the rebuilt command
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf orange
            """,
        )
        set_module_args(
            dict(
                config=dict(domain="10", pkl_vrf="blue", pkl_dest="192.168.2.2"),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "vpc domain 10",
            "peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf blue",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_merged_bool_false_absent_from_have(self):
        # an absent line means the feature is already off, so asking for
        # false is a no-op rather than a spurious `no` form every run
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
            """,
        )
        set_module_args(
            dict(
                config=dict(domain="10", peer_gw=False, peer_sw=False, auto_recovery=False),
                state="merged",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_merged_bool_false_present_in_have(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              peer-switch
              peer-gateway
              auto-recovery
            """,
        )
        set_module_args(
            dict(
                config=dict(domain="10", peer_gw=False, peer_sw=False, auto_recovery=False),
                state="merged",
            ),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "vpc domain 10",
            "no auto-recovery",
            "no peer-gateway",
            "no peer-switch",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_merged_negated_auto_recovery_in_have(self):
        # platforms that default auto-recovery on write the negated form
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              no auto-recovery
            """,
        )
        set_module_args(
            dict(config=dict(domain="10", auto_recovery=True), state="merged"),
            ignore_provider_arg,
        )
        commands = ["vpc domain 10", "auto-recovery"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    # -- replaced ----------------------------------------------------------

    def test_nxos_vpc_replaced(self):
        # numeric sub-commands are reset with the platform default because
        # NX-OS rejects the bare no-form of some of them
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              system-priority 2000
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
              delay restore 150
              peer-gateway
              auto-recovery
            """,
        )
        set_module_args(
            dict(
                config=dict(domain="10", pkl_dest="192.168.2.2", pkl_src="192.168.2.1"),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "vpc domain 10",
            "role priority 32667",
            "system-priority 32667",
            "delay restore 60",
            "no auto-recovery",
            "no peer-gateway",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_replaced_pkl_is_want_only(self):
        # unlike merged, replaced drops the optional keepalive keys that
        # were not supplied
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf orange
            """,
        )
        set_module_args(
            dict(
                config=dict(domain="10", pkl_dest="192.168.2.2"),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        commands = [
            "vpc domain 10",
            "peer-keepalive destination 192.168.2.2 vrf management",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_replaced_removes_peer_keepalive(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf orange
              peer-switch
            """,
        )
        set_module_args(
            dict(config=dict(domain="10", role_priority="150"), state="replaced"),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "vpc domain 10",
            "role priority 150",
            "no peer-switch",
            "no peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf orange",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_replaced_idempotent(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
            """,
        )
        set_module_args(
            dict(
                config=dict(
                    domain="10",
                    role_priority="150",
                    pkl_dest="192.168.2.2",
                    pkl_src="192.168.2.1",
                ),
                state="replaced",
            ),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nxos_vpc_replaced_new_domain(self):
        # only one VPC domain can exist, so switching IDs tears down the old
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              peer-switch
            """,
        )
        set_module_args(
            dict(config=dict(domain="20", role_priority="150"), state="replaced"),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "no vpc domain 10",
            "vpc domain 20",
            "role priority 150",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    # -- overridden --------------------------------------------------------

    def test_nxos_vpc_overridden(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              system-priority 2000
              delay restore interface-vlan 20
              delay restore orphan-port 30
              auto-recovery reload-delay 300
              peer-keepalive destination 192.168.2.2
            """,
        )
        set_module_args(
            dict(config=dict(domain="10", role_priority="150"), state="overridden"),
            ignore_provider_arg,
        )
        commands = [
            "vpc domain 10",
            "role priority 150",
            "system-priority 32667",
            "delay restore interface-vlan 10",
            "delay restore orphan-port 0",
            "auto-recovery reload-delay 240",
            "no peer-keepalive destination 192.168.2.2 vrf management",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    # -- deleted -----------------------------------------------------------

    def test_nxos_vpc_deleted(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        commands = ["terminal dont-ask", "no vpc domain 10"]
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], commands)

    def test_nxos_vpc_deleted_empty_have(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(state="deleted"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    # -- rendered ----------------------------------------------------------

    def test_nxos_vpc_rendered(self):
        set_module_args(
            dict(
                config=dict(
                    domain="10",
                    role_priority="150",
                    peer_gw=True,
                    pkl_dest="192.168.2.2",
                    pkl_src="192.168.2.1",
                    pkl_vrf="management",
                ),
                state="rendered",
            ),
            ignore_provider_arg,
        )
        commands = [
            "terminal dont-ask",
            "vpc domain 10",
            "role priority 150",
            "peer-gateway",
            "peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management",
        ]
        result = self.execute_module(changed=False)
        self.assertEqual(result["rendered"], commands)

    # -- parsed ------------------------------------------------------------

    def test_nxos_vpc_parsed(self):
        cfg = dedent(
            """\
            vpc domain 10
              role priority 150
              system-priority 2000
              peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf orange
              delay restore 150
              delay restore interface-vlan 20
              delay restore orphan-port 30
              peer-switch
              peer-gateway
              auto-recovery
            """,
        )
        set_module_args(dict(running_config=cfg, state="parsed"), ignore_provider_arg)
        parsed = {
            "domain": "10",
            "role_priority": "150",
            "system_priority": "2000",
            "pkl_dest": "192.168.2.2",
            "pkl_src": "192.168.2.1",
            "pkl_vrf": "orange",
            "delay_restore": "150",
            "delay_restore_interface_vlan": "20",
            "delay_restore_orphan_port": "30",
            "peer_sw": True,
            "peer_gw": True,
            "auto_recovery": True,
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], parsed)

    def test_nxos_vpc_parsed_no_domain(self):
        # running-config section with no vpc domain must not trip the
        # `domain` required-suboption check
        set_module_args(dict(running_config="!\n", state="parsed"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["parsed"], {})

    # -- gathered ----------------------------------------------------------

    def test_nxos_vpc_gathered(self):
        self.get_config.return_value = dedent(
            """\
            vpc domain 10
              role priority 150
              peer-keepalive destination 192.168.2.2 source 192.168.2.1
              auto-recovery reload-delay 300
              no auto-recovery
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        gathered = {
            "domain": "10",
            "role_priority": "150",
            "pkl_dest": "192.168.2.2",
            "pkl_src": "192.168.2.1",
            "auto_recovery_reload_delay": "300",
            "auto_recovery": False,
        }
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], gathered)

    def test_nxos_vpc_gathered_empty(self):
        self.get_config.return_value = dedent(
            """\
            """,
        )
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["gathered"], {})
