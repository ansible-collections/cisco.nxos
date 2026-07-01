from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_lacp

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True


class TestNxosLacpModule(TestNxosModule):
    module = nxos_lacp

    def setUp(self):
        super(TestNxosLacpModule, self).setUp()

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
        super(TestNxosLacpModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()

    def test_nxos_lacp_rendered(self):
        playbook = dict(
            config=dict(
                system=dict(
                    priority=10,
                    mac=dict(address="00c1.4c00.bd15"),
                ),
            ),
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("lacp system-priority 10", result["rendered"])
        self.assertIn("lacp system-mac 00c1.4c00.bd15", result["rendered"])

    def test_nxos_lacp_parsed(self):
        running_config = "lacp system-priority 10\nlacp system-mac 00c1.4c00.bd15 role secondary\n"
        playbook = dict(
            running_config=running_config,
            state="parsed",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        parsed = result["parsed"]
        self.assertEqual(parsed["system"]["priority"], 10)
        self.assertEqual(parsed["system"]["mac"]["address"], "00c1.4c00.bd15")
        self.assertEqual(parsed["system"]["mac"]["role"], "secondary")

    def test_nxos_lacp_rendered_with_role(self):
        playbook = dict(
            config=dict(
                system=dict(
                    priority=15,
                    mac=dict(address="00c1.4c00.bd15", role="primary"),
                ),
            ),
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertIn("lacp system-priority 15", result["rendered"])
