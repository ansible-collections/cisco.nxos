#!/usr/bin/env python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase


class TestTerminalNxosImport(TestCase):
    def test_terminal_imports_converters_from_common(self):
        from ansible_collections.cisco.nxos.plugins.terminal.nxos import to_bytes, to_text

        self.assertTrue(callable(to_bytes))
        self.assertTrue(callable(to_text))
