# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Logging_global parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Logging_globalTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Logging_globalTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "console",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\sconsole
                (\s(?P<level>\d))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "console": {
                    "state": "{{ 'disabled' if negated is defined else None }}",
                    "level": "{{ level }}",
                },
            },
        },
        {
            "name": "event.link_status.enable",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\sevent\slink-status\senable
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "event": {
                    "link_status": {
                        "enable": "{{ False if negated is defined else True }}",
                    }
                }
            },
        },
        {
            "name": "event.link_status.default",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\sevent\slink-status\sdefault
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "event": {
                    "link_status": {
                        "default": "{{ False if negated is defined else True }}",
                    }
                }
            },
        },
        {
            "name": "event.trunk_status.enable",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\sevent\strunk-status\senable
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "event": {
                    "trunk_status": {
                        "enable": "{{ False if negated is defined else True }}",
                    }
                }
            },
        },
        {
            "name": "event.trunk_status.default",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\sevent\strunk-status\sdefault
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "event": {
                    "trunk_status": {
                        "default": "{{ False if negated is defined else True }}",
                    }
                }
            },
        },
        {
            "name": "history.level",
            "getval": re.compile(
                r"""
                ^logging\shistory
                \s(?P<level>\d)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "history": {
                    "level": "{{ level }}",
                },
            },
        },
        {
            "name": "history.size",
            "getval": re.compile(
                r"""
                ^logging\shistory\ssize
                \s(?P<size>\d+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "history": {
                    "size": "{{ size }}",
                },
            },
        },
        {
            "name": "ip.access_list.cache.entries",
            "getval": re.compile(
                r"""
                ^logging\sip\saccess-list\scache
                \sentries\s(?P<entries>\d+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "access_list": {
                        "cache": {
                            "entries": "{{ entries }}",
                        },
                    }
                },
            },
        },
        {
            "name": "ip.access_list.cache.interval",
            "getval": re.compile(
                r"""
                ^logging\sip\saccess-list\scache
                \sinterval\s(?P<interval>\d+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "access_list": {
                        "cache": {
                            "interval": "{{ interval }}",
                        },
                    }
                },
            },
        },
        {
            "name": "ip.access_list.cache.threshold",
            "getval": re.compile(
                r"""
                ^logging\sip\saccess-list\scache
                \sthreshold\s(?P<threshold>\d+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "access_list": {
                        "cache": {
                            "threshold": "{{ threshold }}",
                        },
                    }
                },
            },
        },
        {
            "name": "ip.access_list.detailed",
            "getval": re.compile(
                r"""
                ^logging\sip\saccess-list
                \s(?P<detailed>detailed)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "access_list": {
                        "detailed": "{{ not not detailed }}",
                    }
                },
            },
        },
        {
            "name": "ip.access_list.include.sgt",
            "getval": re.compile(
                r"""
                ^logging\sip\saccess-list\sinclude
                \s(?P<sgt>sgt)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "ip": {
                    "access_list": {
                        "include": {
                            "sgt": "{{ not not sgt }}",
                        }
                    }
                },
            },
        },
        {
            "name": "facilities",
            "getval": re.compile(
                r"""
                ^logging\slevel
                \s(?P<facility>\S+)
                \s(?P<level>\d+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "facilities": [
                    {
                        "facility": "{{ facility }}",
                        "level": "{{ level }}",
                    },
                ]
            },
        },
        {
            "name": "logfile",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\slogfile
                (\s(?P<name>\S+))?
                (\s(?P<level>\d+))?
                (\ssize\s(?P<size>\d+))?
                (\spersistent\sthreshold\s(?P<persistent_threshold>\d+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "logfile": {
                    "state": "{{ 'disabled' if negated is defined else None }}",
                    "name": "{{ name }}",
                    "level": "{{ level }}",
                    "persistent_threshold": "{{ persistent_threshold }}",
                    "size": "{{ size }}",
                },
            },
        },
        {
            "name": "module",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\smodule
                (\s(?P<level>\d))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "module": {
                    "state": "{{ 'disabled' if negated is defined else None }}",
                    "level": "{{ level }}",
                },
            },
        },
        {
            "name": "monitor",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging\smonitor
                (\s(?P<level>\d))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "monitor": {
                    "state": "{{ 'disabled' if negated is defined else None }}",
                    "level": "{{ level }}",
                },
            },
        },
        {
            "name": "origin_id",
            "getval": re.compile(
                r"""
                ^logging\sorigin-id
                (\s(?P<hostname>hostname))?
                (\sip\s(?P<ip>\S+))?
                (\sstring\s(?P<string>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "origin_id": {
                    "hostname": "{{ not not hostname }}",
                    "ip": "{{ ip }}",
                    "string": "{{ string }}",
                }
            },
        },
        {
            "name": "rate_limit",
            "getval": re.compile(
                r"""
                ^(?P<negated>no\s)?
                logging
                \s(?P<rate_limit>rate-limit)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "rate_limit": "{{ 'disabled' if negated is defined else None }}",
            },
        },
        {
            "name": "rfc_strict",
            "getval": re.compile(
                r"""
                logging\srfc-strict
                \s(?P<rfc_strict>5424)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "rfc_strict": "{{ not not rfc_strict }}",
            },
        },
        {
            "name": "servers",
            "getval": re.compile(
                r"""
                ^logging\sserver
                \s(?P<server>\S+)
                (\s(?P<level>\d))?
                (\sport\s(?P<port>\d+))?
                (\ssecure\strustpoint\sclient-identity\s(?P<client_identity>\S+))?
                (\suse-vrf\s(?P<use_vrf>\S+))?
                (\sfacility\s(?P<facility>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "servers": [
                    {
                        "server": "{{ server }}",
                        "level": "{{ level }}",
                        "secure": {
                            "trustpoint": {
                                "client_identity": "{{ client_identity }}",
                            }
                        },
                        "port": "{{ port }}",
                        "facility": "{{ facility }}",
                        "use_vrf": "{{ use_vrf }}",
                    }
                ]
            },
        },
        {
            "name": "source_interface",
            "getval": re.compile(
                r"""
                ^logging\ssource-interface
                \s(?P<source_interface>\S+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "source_interface": "{{ source_interface }}",
            },
        },
        {
            "name": "timestamp",
            "getval": re.compile(
                r"""
                ^logging\stimestamp
                \s(?P<timestamp>\S+)
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "timestamp": "{{ timestamp }}",
            },
        },
    ]
    # fmt: on
