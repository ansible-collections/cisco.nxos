from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_lldp_global

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosLldpGlobalModule(TestNxosModule):
    module = nxos_lldp_global

    def setUp(self):
        super(TestNxosLldpGlobalModule, self).setUp()

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
        super(TestNxosLldpGlobalModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()

    def test_nxos_lldp_global_rendered(self):
        playbook = dict(
            config=dict(holdtime=130, reinit=5),
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("lldp holdtime 130", result["rendered"])
        self.assertIn("lldp reinit 5", result["rendered"])

    def test_nxos_lldp_global_parsed(self):
        running_config = (
            "lldp holdtime 131\n"
            "lldp reinit 7\n"
            "no lldp tlv-select system-name\n"
            "no lldp tlv-select system-description\n"
        )
        playbook = dict(
            running_config=running_config,
            state="parsed",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        self.assertEqual(parsed["holdtime"], 131)
        self.assertEqual(parsed["reinit"], 7)

    def test_nxos_lldp_global_rendered_with_timer(self):
        playbook = dict(
            config=dict(timer=35, holdtime=100),
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("lldp timer 35", result["rendered"])
        self.assertIn("lldp holdtime 100", result["rendered"])
