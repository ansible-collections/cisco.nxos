# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Snmp_server parser templates file. This contains
a list of parser definitions and associated functions that
facilitates both facts gathering and native command generation for
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)


class Snmp_serverTemplate(NetworkTemplate):
    def __init__(self, lines=None, module=None):
        super(Snmp_serverTemplate, self).__init__(
            lines=lines, tmplt=self, module=module
        )

    # fmt: off
    PARSERS = [
        {
            "name": "aaa_user",
            "getval": re.compile(
                r"""
                ^snmp-server\saaa-user
                \scache-timeout\s(?P<cache_timeout>\d+)
                $""", re.VERBOSE),
            "setval": "snmp-server aaa-user cache-timeout {{ aaa_user.cache_timeout }}",
            "result": {
                "aaa_user": {
                    "cache_timeout": "{{ cache_timeout }}",
                }
            },
        },
        {
            "name": "communities.group",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scommunity\s(?P<community>\S+)
                \sgroup\s(?P<group>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server community {{ community }} group {{ group }}",
            "result": {
                "communities": {
                    "{{ community }}": {
                        "community": "{{ community }}",
                        "group": "{{ group }}",
                    }
                }
            },
        },
        {
            "name": "communities.use_ipv4acl",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scommunity\s(?P<community>\S+)
                \suse-ipv4acl\s(?P<use_ipv4acl>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server community {{ community }} use-ipv4acl {{ use_ipv4acl }}",
            "result": {
                "communities": {
                    "{{ community }}": {
                        "community": "{{ community }}",
                        "use_ipv4acl": "{{ use_ipv4acl }}",
                    }
                }
            },
        },
        {
            "name": "contact",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scontact\s(?P<contact>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server contact {{ contact }}",
            "result": {
                "contact": "{{ contact }}",
            },
        },
        {
            "name": "context",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scontext\s(?P<name>\S+)
                (\sinstance\s(?P<instance>\S+))?
                (\svrf\s(?P<vrf>\S+))?
                (\stopology\s(?P<topology>\S+))?
                $""", re.VERBOSE),
            "setval": "snmp-server context {{ context.name }}"
                      "{{ ' instance ' + context.instance if context.instance is defined else '' }}"
                      "{{ ' topology ' + context.topology if context.topology is defined else '' }}"
                      "{{ ' instance ' + context.instance if context.instance is defined else '' }}"
                      "{{ ' vrf ' + context.vrf if context.vrf is defined else '' }}",
            "result": {
                "context": {
                    "name": "{{ name }}",
                    "instance": "{{ instance }}",
                    "vrf": "{{ vrf }}",
                    "topology": "{{ topology }}",
                }

            },
        },
        {
            "name": "counter.enable",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scounter
                \scache\s(?P<enable>enable)
                $""", re.VERBOSE),
            "setval": "snmp-server counter cache enable",
            "result": {
                "counter": {
                    "cache": {
                        "enable": "{{ True if enable is defined else None }}",
                    }
                }
            },
        },
        {
            "name": "counter.timeout",
            "getval": re.compile(
                r"""
                ^snmp-server
                \scounter
                \scache\stimeout\s(?P<timeout>\d+)
                $""", re.VERBOSE),
            "setval": "snmp-server counter cache timeout {{ counter.timeout }}",
            "result": {
                "counter": {
                    "cache": {
                        "timeout": "{{ timeout }}",
                    }
                }
            },
        },
        {
            "name": "drop.unknown_engine_id",
            "getval": re.compile(
                r"""
                ^snmp-server\sdrop
                \s(?P<unknown_engine_id>unknown-engine-id)
                $""", re.VERBOSE),
            "setval": "snmp-server drop unknown-engine-id",
            "result": {
                "drop": {
                    "unknown_engine_id": "{{ not not unknown_engine_id }}",
                }
            },
        },
        {
            "name": "drop.unknown_user",
            "getval": re.compile(
                r"""
                ^snmp-server\sdrop
                \s(?P<unknown_user>unknown-user)
                $""", re.VERBOSE),
            "setval": "snmp-server drop unknown-user",
            "result": {
                "drop": {
                    "unknown_user": "{{ not not unknown_user }}",
                }
            },
        },
        {
            "name": "traps.aaa",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps\saaa\s(?P<server_state_change>server-state-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps aaa"
                      "{{ ' server-state-change' if traps.aaa.server_state_change|d(False) else ''}}",
            "result": {
                "traps": {
                    "aaa": {
                        "server_state_change": "{{ not not server_state_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.bridge.newroot",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sbridge\s(?P<newroot>newroot)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps bridge newroot",
            "result": {
                "traps": {
                    "bridge": {
                        "newroot": "{{ not not newroot }}",
                    }
                }
            },
        },
        {
            "name": "traps.bridge.topologychange",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sbridge\s(?P<topologychange>topologychange)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps bridge topologychange",
            "result": {
                "traps": {
                    "bridge": {
                        "topologychange": "{{ not not topologychange }}",
                    }
                }
            },
        },
        {
            "name": "traps.callhome.event_notify",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \scallhome\s(?P<event_notify>event-notify)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps callhome event-notify",
            "result": {
                "traps": {
                    "callhome": {
                        "event_notify": "{{ not not event_notify }}",
                    }
                }
            },
        },
        {
            "name": "traps.callhome.smtp_send_fail",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \scallhome\s(?P<smtp_send_fail>smtp-send-fail)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps callhome smtp-send-fail",
            "result": {
                "traps": {
                    "callhome": {
                        "smtp_send_fail": "{{ not not smtp_send_fail }}",
                    }
                }
            },
        },
        {
            "name": "traps.cfs.merge_failure",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \scfs\s(?P<merge_failure>merge-failure)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps cfs merge-failure",
            "result": {
                "traps": {
                    "cfs": {
                        "merge_failure": "{{ not not merge_failure }}",
                    }
                }
            },
        },
        {
            "name": "traps.cfs.state_change_notif",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \scfs\s(?P<state_change_notif>state-change-notif)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps cfs state-change-notif",
            "result": {
                "traps": {
                    "cfs": {
                        "state_change_notif": "{{ not not state_change_notif }}",
                    }
                }
            },
        },
        {
            "name": "traps.config.ccmCLIRunningConfigChanged",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sconfig\s(?P<ccmCLIRunningConfigChanged>ccmCLIRunningConfigChanged)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps config ccmCLIRunningConfigChanged",
            "result": {
                "traps": {
                    "config": {
                        "ccmCLIRunningConfigChanged": "{{ not not ccmCLIRunningConfigChanged }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.cefcMIBEnableStatusNotification",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<cefcMIBEnableStatusNotification>cefcMIBEnableStatusNotification)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity cefcMIBEnableStatusNotification",
            "result": {
                "traps": {
                    "entity": {
                        "cefcMIBEnableStatusNotification": "{{ not not cefcMIBEnableStatusNotification }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_fan_status_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_fan_status_change>entity-fan-status-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-fan-status-change",
            "result": {
                "traps": {
                    "entity": {
                        "entity_fan_status_change": "{{ not not entity_fan_status_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_mib_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_mib_change>entity-mib-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-mib-change",
            "result": {
                "traps": {
                    "entity": {
                        "entity_mib_change": "{{ not not entity_mib_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_module_inserted",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_module_inserted>entity-module-inserted)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-module-inserted",
            "result": {
                "traps": {
                    "entity": {
                        "entity_module_inserted": "{{ not not entity_module_inserted }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_module_status_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_module_status_change>entity-module-status-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-module-status-change",
            "result": {
                "traps": {
                    "entity": {
                        "entity_module_status_change": "{{ not not entity_module_status_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_power_out_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_power_out_change>entity-power-out-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-power-out-change",
            "result": {
                "traps": {
                    "entity": {
                        "entity_power_out_change": "{{ not not entity_power_out_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_power_status_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_power_status_change>entity_power_status_change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-power-status-change",
            "result": {
                "traps": {
                    "entity": {
                        "entity_power_status_change": "{{ not not entity_power_status_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_sensor",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_sensor>entity-sensor)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-sensor",
            "result": {
                "traps": {
                    "entity": {
                        "entity_sensor": "{{ not not entity_sensor }}",
                    }
                }
            },
        },
        {
            "name": "traps.entity.entity_unrecognised_module",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sentity\s(?P<entity_unrecognised_module>entity-unrecognised-module)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps entity entity-unrecognised-module",
            "result": {
                "traps": {
                    "entity": {
                        "entity_unrecognised_module": "{{ not not entity_unrecognised_module }}",
                    }
                }
            },
        },
        {
            "name": "traps.feature_control.featureOpStatusChange",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sfeature-control\s(?P<featureOpStatusChange>featureOpStatusChange)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps feature-control featureOpStatusChange",
            "result": {
                "traps": {
                    "feature_control": {
                        "featureOpStatusChange": "{{ not not featureOpStatusChange }}",
                    }
                }
            },
        },
        {
            "name": "traps.feature_control.ciscoFeatOpStatusChange",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sfeature-control\s(?P<ciscoFeatOpStatusChange>ciscoFeatOpStatusChange)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps feature-control ciscoFeatOpStatusChange",
            "result": {
                "traps": {
                    "feature_control": {
                        "ciscoFeatOpStatusChange": "{{ not not ciscoFeatOpStatusChange }}",
                    }
                }
            },
        },
        {
            "name": "traps.generic.coldStart",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sgeneric\s(?P<coldStart>coldStart)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps generic coldStart",
            "result": {
                "traps": {
                    "generic": {
                        "coldStart": "{{ not not coldStart }}",
                    }
                }
            },
        },
        {
            "name": "traps.generic.warmStart",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sgeneric\s(?P<warmStart>warmStart)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps generic warmStart",
            "result": {
                "traps": {
                    "generic": {
                        "warmStart": "{{ not not warmStart }}",
                    }
                }
            },
        },
        {
            "name": "traps.license.notify_license_expiry",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slicense\s(?P<notify_license_expiry>notify_license_expiry)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps license notify-license-expiry",
            "result": {
                "traps": {
                    "license": {
                        "notify_license_expiry": "{{ not not notify_license_expiry }}",
                    }
                }
            },
        },
        {
            "name": "traps.license.notify_license_expiry_warning",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slicense\s(?P<notify_license_expiry_warning>notify-license-expiry-warning)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps license notify-license-expiry-warning",
            "result": {
                "traps": {
                    "license": {
                        "notify_license_expiry_warning": "{{ not not notify_license_expiry_warning }}",
                    }
                }
            },
        },
        {
            "name": "traps.license.notify_licensefile_missing",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slicense\s(?P<notify_licensefile_missing>notify-licensefile-missing)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps license notify-licensefile-missing",
            "result": {
                "traps": {
                    "license": {
                        "notify_licensefile_missing": "{{ not not notify_licensefile_missing }}",
                    }
                }
            },
        },
        {
            "name": "traps.license.notify_no_license_for_feature",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slicense\s(?P<notify_no_license_for_feature>notify-no-license-for-feature)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps license notify-no-license-for-feature",
            "result": {
                "traps": {
                    "license": {
                        "notify_no_license_for_feature": "{{ not not notify_no_license_for_feature }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.cErrDisableInterfaceEventRev1",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<cErrDisableInterfaceEventRev1>cErrDisableInterfaceEventRev1)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link cErrDisableInterfaceEventRev1",
            "result": {
                "traps": {
                    "link": {
                        "cErrDisableInterfaceEventRev1": "{{ not not cErrDisableInterfaceEventRev1 }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.cieLinkDown",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<cieLinkDown>cieLinkDown)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link cieLinkDown",
            "result": {
                "traps": {
                    "link": {
                        "cieLinkDown": "{{ not not cieLinkDown }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.cieLinkUp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<cieLinkUp>cieLinkUp)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link cieLinkUp",
            "result": {
                "traps": {
                    "link": {
                        "cieLinkUp": "{{ not not cieLinkUp }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.cisco_xcvr_mon_status_chg",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<cisco_xcvr_mon_status_chg>cisco-xcvr-mon-status-chg)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link cisco_xcvr_mon_status_chg",
            "result": {
                "traps": {
                    "link": {
                        "cisco_xcvr_mon_status_chg": "{{ not not cisco_xcvr_mon_status_chg }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.cmn_mac_move_notification",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<cmn_mac_move_notification>cmn-mac-move-notification)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link cmn-mac-move-notification",
            "result": {
                "traps": {
                    "link": {
                        "cmn_mac_move_notification": "{{ not not cmn_mac_move_notification }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.delayed_link_state_change",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<delayed_link_state_change>delayed-link-state-change)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link delayed-link-state-change",
            "result": {
                "traps": {
                    "link": {
                        "delayed_link_state_change": "{{ not not delayed_link_state_change }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.extended_linkDown",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<extended_linkDown>extended-linkDown)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link extended-linkDown",
            "result": {
                "traps": {
                    "link": {
                        "extended_linkDown": "{{ not not extended_linkDown }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.extended_linkUp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<extended_linkUp>extended-linkUp)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link extended-linkUp",
            "result": {
                "traps": {
                    "link": {
                        "extended_linkUp": "{{ not not extended_linkUp }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.linkDown",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<linkDown>linkDown)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link linkDown",
            "result": {
                "traps": {
                    "link": {
                        "linkDown": "{{ not not linkDown }}",
                    }
                }
            },
        },
        {
            "name": "traps.link.linkUp",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \slink\s(?P<linkUp>linkUp)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps link linkUp",
            "result": {
                "traps": {
                    "link": {
                        "linkUp": "{{ not not linkUp }}",
                    }
                }
            },
        },
        {
            "name": "traps.mmode.cseMaintModeChangeNotify",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \smmode\s(?P<cseMaintModeChangeNotify>cseMaintModeChangeNotify)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps mmode cseMaintModeChangeNotify",
            "result": {
                "traps": {
                    "mmode": {
                        "cseMaintModeChangeNotify": "{{ not not cseMaintModeChangeNotify }}",
                    }
                }
            },
        },
        {
            "name": "traps.mmode.cseNormalModeChangeNotify",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \smmode\s(?P<cseNormalModeChangeNotify>cseNormalModeChangeNotify)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps mmode cseNormalModeChangeNotify",
            "result": {
                "traps": {
                    "mmode": {
                        "cseNormalModeChangeNotify": "{{ not not cseNormalModeChangeNotify }}",
                    }
                }
            },
        },
        {
            "name": "traps.rf.redundancy_framework",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \srf\s(?P<redundancy_framework>redundancy-framework)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps rf redundancy-framework",
            "result": {
                "traps": {
                    "rf": {
                        "redundancy_framework": "{{ not not redundancy_framework }}",
                    }
                }
            },
        },
        {
            "name": "traps.rmon.fallingAlarm",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \srmon\s(?P<fallingAlarm>fallingAlarm)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps rmon fallingAlarm",
            "result": {
                "traps": {
                    "rmon": {
                        "fallingAlarm": "{{ not not fallingAlarm }}",
                    }
                }
            },
        },
        {
            "name": "traps.rmon.hcFallingAlarm",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \srmon\s(?P<hcFallingAlarm>hcFallingAlarm)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps rmon hcFallingAlarm",
            "result": {
                "traps": {
                    "rmon": {
                        "hcFallingAlarm": "{{ not not hcFallingAlarm }}",
                    }
                }
            },
        },
        {
            "name": "traps.rmon.hcRisingAlarm",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \srmon\s(?P<hcRisingAlarm>hcRisingAlarm)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps rmon hcRisingAlarm",
            "result": {
                "traps": {
                    "rmon": {
                        "hcRisingAlarm": "{{ not not hcRisingAlarm }}",
                    }
                }
            },
        },
        {
            "name": "traps.rmon.risingAlarm",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \srmon\s(?P<risingAlarm>risingAlarm)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps rmon risingAlarm",
            "result": {
                "traps": {
                    "rmon": {
                        "risingAlarm": "{{ not not risingAlarm }}",
                    }
                }
            },
        },
        {
            "name": "traps.snmp.authentication",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \ssnmp\s(?P<authentication>authentication)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps snmp authentication",
            "result": {
                "traps": {
                    "snmp": {
                        "authentication": "{{ not not authentication }}",
                    }
                }
            },
        },
        {
            "name": "traps.storm_control.cpscEventRev1",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sstorm-control\s(?P<cpscEventRev1>cpscEventRev1)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps storm-control cpscEventRev1",
            "result": {
                "traps": {
                    "storm_control": {
                        "cpscEventRev1n": "{{ not not cpscEventRev1 }}",
                    }
                }
            },
        },
        {
            "name": "traps.storm_control.trap_rate",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \straps
                \sstorm-control\s(?P<trap_rate>trap-rate)
                $""", re.VERBOSE),
            "setval": "snmp-server enable traps storm-control trap-rate",
            "result": {
                "traps": {
                    "storm_control": {
                        "trap_rate": "{{ not not trap_rate }}",
                    }
                }
            },
        },
        {
            "name": "engine_id.local",
            "getval": re.compile(
                r"""
                ^snmp-server\senable
                \sengine-id
                \slocal\s(?P<local>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server engine-id local {{ engine_id.local }}",
            "result": {
                "engine_id": {
                    "local": "{{ local }}",
                }
            },
        },
        {
            "name": "global_enforce_priv",
            "getval": re.compile(
                r"""
                ^snmp-server
                \s(?P<global_enforce_priv>globalEnforcePriv)
                $""", re.VERBOSE),
            "setval": "snmp-server globalEnforcePriv",
            "result": {
                "global_enforce_priv": "{{ not not global_enforce_priv }}",
            },
        },
        {
            "name": "hosts",
            "getval": re.compile(
                r"""
                ^snmp-server
                \shost\s(?P<host>\S+)
                (\s((?P<traps>traps)|(?P<informs>informs)|(use-vrf\s(?P<use_vrf>\S+)|(filter-vrf\s(?P<filter_vrf>\S+))|(source-interface\s(?P<source_interface>\S+)))))
                (\sversion\s(?P<version>\S+))?
                (\s((auth\s(?P<auth>\S+))|(priv\s(?P<priv>\S+))|((?P<community>\S+))))?
                (\sudp-port\s(?P<udp_port>\S+))?
                $""", re.VERBOSE),
            "setval": "snmp-server host {{ host }}",
            "result": {
                "hosts": [
                    {
                        "host": "{{ host }}",
                        "community": "{{ community }}",
                        "filter_vrf": "{{ filter_vrf }}",
                        "informs": "{{ not not informs }}",
                        "source_interface": "{{ source_interface }}",
                        "traps": "{{ not not traps }}",
                        "use_vrf": "{{ use_vrf }}",
                        "version": "{{ version }}",
                        "udp_port": "{{ udp_port }}",
                        "auth": "{{ auth }}",
                        "priv": "{{ priv }}",
                    }
                ]
            },
        },
        {
            "name": "location",
            "getval": re.compile(
                r"""
                ^snmp-server
                \slocation\s(?P<location>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server location {{ location }}",
            "result": {
                "location": "{{ location }}",
            }
        },
        {
            "name": "mib",
            "getval": re.compile(
                r"""
                ^snmp-server
                \smib
                \scommunity-map\s(?P<community>\S+)
                \scontext\s(?P<context>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server mib community-map {{ community_map.community }} context {{ community_map.context }}",
            "result": {
                "mib": {
                    "community_map": {
                        "community": "{{ community }}",
                        "context": "{{ context }}",

                    }
                }
            }
        },
        {
            "name": "packetsize",
            "getval": re.compile(
                r"""
                ^snmp-server
                \spacket-size\s(?P<packet_size>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server packetsize {{ packetsize }}",
            "result": {
                "mib": {
                    "community_map": {
                        "community": "{{ community }}",
                        "context": "{{ context }}",

                    }
                }
            }
        },
        {
            "name": "protocol.enable",
            "getval": re.compile(
                r"""
                ^snmp-server
                \sprotocol\s(?P<enable>enable)
                $""", re.VERBOSE),
            "setval": "snmp-server protocol enable",
            "result": {
                "protocol": {
                    "enable": "{{ enable }}",
                }
            }
        },
        {
            "name": "source_interface.informs",
            "getval": re.compile(
                r"""
                ^snmp-server
                \ssource-interface\sinforms\s(?P<informs>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server source-interface informs {{ source_interface.informs }}",
            "result": {
                "source_interface": {
                    "informs": "{{ informs }}",
                }
            }
        },
        {
            "name": "source_interface.traps",
            "getval": re.compile(
                r"""
                ^snmp-server
                \ssource-interface\straps\s(?P<traps>\S+)
                $""", re.VERBOSE),
            "setval": "snmp-server source-interface traps {{ source_interface.traps }}",
            "result": {
                "source_interface": {
                    "traps": "{{ traps }}",
                }
            }
        },
        {
            "name": "system_shutdown",
            "getval": re.compile(
                r"""
                ^snmp-server
                \s(?P<system_shutdown>system-shutdown)
                $""", re.VERBOSE),
            "setval": "snmp-server system-shutdown",
            "result": {
                "system_shutdown": "{{ not not system_shutdown }}",
            }
        },
        {
            "name": "tcp_session",
            "getval": re.compile(
                r"""
                ^snmp-server
                \s(?P<tcp_session>tcp-session)
                (\sauth(?P<auth>auth))?
                $""", re.VERBOSE),
            "setval": "snmp-server tcp-session"
                      "{{ ' auth' if tcp_session.auth|d(False) else '' }}",
            "result": {
                "tcp_session": {
                    "enable": "{{ True if tcp_session is defined and auth is not defined else None }}",
                    "auth": "{{ not not auth }}",
                }
            }
        },
        {
            "name": "users",
            "getval": re.compile(
                r"""
                ^snmp-server
                \suser\s(?P<user>\S+)
                \s(?P<group>\S+)
                (\sauth\s(?P<algorithm>md5|sha)\s(?P<password>\S+))?
                (\spriv(\s(?P<aes_128>aes-128))?\s(?P<privacy_password>\S+))?
                (\s(?P<localized_key>localizedkey))?
                (\sengineID(?P<engine_id>\S+))?
                $""", re.VERBOSE),
            "setval": "",
            "result": {
                "users": [
                    {
                        "user": "{{ user }}",
                        "group": "{{ group }}",
                        "auth": {
                            "algorithm": "{{ algorithm }}",
                            "password": "'{{ password }}'",
                            "engine_id": "{{ engine_id }}",
                            "localized_key": "{{ not not localized_key }}",
                            "priv": {
                                "privacy_password": "'{{ privacy_password }}'",
                                "aes_128": "{{ not not aes_128 }}",
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "users.use_acl",
            "getval": re.compile(
                r"""
                ^snmp-server
                \suser\s(?P<user>\S+)
                (\suse-ipv4acl\s(?P<ipv4>\S+))?
                (\suse-ipv6acl\s(?P<ipv6>\S+))?
                $""", re.VERBOSE),
            "setval": "snmp-server user {{ user }}"
                      "{{ (' use-ipv4acl ' + ipv4) if ipv4 is defined else '' }}"
                      "{{ (' use-ipv6acl ' + ipv6) if ipv6 is defined else '' }}",
            "result": {
                "users": [
                    {
                        "user": "{{ user }}",
                        "use_acl": {
                            "ipv4": "{{ ipv4 }}",
                            "ipv6": "{{ ipv6 }}",
                        }
                    }
                ]
            }
        },
    ]
    # fmt: on
