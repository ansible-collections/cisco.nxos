from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_lag_interfaces

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosLagInterfacesModule(TestNxosModule):
    module = nxos_lag_interfaces

    def setUp(self):
        super(TestNxosLagInterfacesModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS",
        )
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

    def tearDown(self):
        super(TestNxosLagInterfacesModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()

    def test_nxos_lag_interfaces_rendered(self):
        playbook = dict(
            config=[
                dict(
                    name="port-channel10",
                    members=[
                        dict(member="Ethernet1/800", mode="active"),
                    ],
                ),
            ],
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("interface Ethernet1/800", result["rendered"])
        self.assertIn("channel-group 10 mode active", result["rendered"])

    def test_nxos_lag_interfaces_parsed(self):
        running_config = (
            "interface port-channel10\n"
            "interface Ethernet1/800\n"
            "  channel-group 10 mode active\n"
            "interface Ethernet1/801\n"
            "  channel-group 10 mode active\n"
        )
        playbook = dict(
            running_config=running_config,
            state="parsed",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertTrue(len(result["parsed"]) > 0)

    def test_nxos_lag_interfaces_rendered_multiple(self):
        playbook = dict(
            config=[
                dict(
                    name="port-channel10",
                    members=[dict(member="Ethernet1/1", mode="active")],
                ),
                dict(
                    name="port-channel11",
                    members=[dict(member="Ethernet1/2", mode="passive")],
                ),
            ],
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("channel-group 10 mode active", result["rendered"])
        self.assertIn("channel-group 11 mode passive", result["rendered"])
