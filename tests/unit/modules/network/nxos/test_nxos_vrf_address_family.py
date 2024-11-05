# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_address_family

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfAddressFamilyModule(TestNxosModule):
    """Test the nxos_vrf_address_family module."""

    module = nxos_vrf_address_family

    def setUp(self):
        """Set up for nxos_vrf_address_family module tests."""
        super(TestNxosVrfAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vrf_address_family.vrf_address_family."
            "Vrf_address_familyFacts.get_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosVrfAddressFamilyModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_vrf_address_fam_gathered(self):
        """Test the get_config method."""
        self.execute_show_command.return_value = dedent(
            """
            vrf context VRF1
              address-family ipv4 unicast
            vrf context VRF2
              address-family ipv6 unicast
            """,
        )

        set_module_args({})
        self.module.get_config(self.mock_connection)

        self.execute_show_command.assert_called_once_with(self.mock_connection)
