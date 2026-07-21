#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase


class TestHttpapiNxosImport(TestCase):
    def test_httpapi_imports_to_text_from_common_converters(self):
        from ansible_collections.cisco.nxos.plugins.httpapi.nxos import to_text

        self.assertTrue(callable(to_text))
