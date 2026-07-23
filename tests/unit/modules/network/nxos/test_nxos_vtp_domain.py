#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vtp_domain

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVtpDomainModule(TestNxosModule):
    module = nxos_vtp_domain

    def setUp(self):
        super(TestNxosVtpDomainModule, self).setUp()
        self.mock_get_vtp_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_domain.get_vtp_config",
        )
        self.get_vtp_config = self.mock_get_vtp_config.start()

        self.mock_load_config = patch(
            "ansible_collections.cisco.nxos.plugins.modules.nxos_vtp_domain.load_config",
        )
        self.load_config = self.mock_load_config.start()

    def tearDown(self):
        super(TestNxosVtpDomainModule, self).tearDown()
        self.mock_get_vtp_config.stop()
        self.mock_load_config.stop()

    def load_fixtures(self, commands=None, device=""):
        self.load_config.return_value = None

    def test_nxos_vtp_domain_no_change(self):
        self.get_vtp_config.return_value = {
            "domain": "test-domain",
            "version": "2",
            "vtp_password": "",
        }
        set_module_args(
            dict(
                domain="test-domain",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertFalse(result["changed"])
