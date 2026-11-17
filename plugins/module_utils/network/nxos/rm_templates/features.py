# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The Features parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class FeaturesTemplate(NetworkTemplate):
    """The parser templates class of nxos_features."""

    def __init__(self, lines=None, module=None):
        super(FeaturesTemplate, self).__init__(lines=lines, tmplt=self, module=module)

    # fmt: off
    PARSERS = [
        {
            "name": "feature",
            "getval": re.compile(
                r"""
                ^(?P<negate>no\s)?feature\s(?P<name>\S.*?)
                \s*$""", re.VERBOSE,
            ),
            "setval": "feature {{ name }}",
            "result": {
                "{{ name }}": {
                    "name": "{{ name }}",
                    "enabled": "{{ False if negate is defined else True }}",
                },
            },
        },
    ]
    # fmt: on
