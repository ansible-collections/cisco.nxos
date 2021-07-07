#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_logging_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_logging_global
short_description: Logging resource module.
description:
- This module manages logging configuration on devices running Cisco NX-OS.
version_added: 2.5.0
notes:
- Tested against NX-OS 9.3.6.
- This module works with connection C(network_cli) and C(httpapi).
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | include logging).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A dictionary of logging configuration.
    type: dict
    suboptions:
      console:
        description: Set console logging parameters.
        type: dict
        suboptions:
          state:
            description: Enable or disable monitor logging.
            type: str
            choices: ["enabled", "disabled"]
          level:
            description:  Set severity level for console (0-7).
            type: int
      event:
        description: Interface events.
        type: dict
        suboptions:
          link_status:
            description: UPDOWN and CHANGE messages.
            type: dict
            suboptions: &event
              enable:
                description: To enable logging overriding port level configuration.
                type: bool
              default:
                description: Default logging configuration used by interfaces not explicitly configured.
                type: bool
          trunk_status:
            description: TRUNK status messages.
            type: dict
            suboptions: *event
      history:
        description: Modifies severity level or size for history table.
        type: dict
        suboptions:
          level:
            description: Set severity level for history.
            type: int
          size:
            description: Set history table size.
            type: int
      ip:
        description: IP configuration.
        type: dict
        suboptions:
          access_list:
            description: Access-List.
            type: dict
            suboptions:
              cache:
                description: Set caching settings.
                type: dict
                suboptions:
                  entries:
                    description: Maximum number of log entries cached in software.
                    type: int
                  interval:
                    description: Log-update interval (in sec).
                    type: int
                  threshold:
                    description: Log-update threshold (number of hits)
                    type: int
              detailed:
                description: Detailed ACL information.
                type: bool
              include:
                description: Include additional fields in syslogs.
                type: dict
                suboptions:
                  sgt:
                    description: Include source group tag info in syslogs.
                    type: bool
      facilities:
        description: Facility parameter for syslog messages.
        type: list
        elements: dict
        suboptions:
          facility:
            description: Facility name.
            type: str
          level:
            description: Set severity level for the facility (0-7).
            type: int
      logfile:
        description: Set file logging.
        type: dict
        suboptions:
          state:
            description: Enable or disable logfile.
            type: str
            choices: ["enabled", "disabled"]
          name:
            description: Logfile name.
            type: str
          level:
            description: Set severity level for logfile.
            type: int
          persistent_threshold:
            description: Set persistent logging utilization alert threshold in percentage.
            type: int
          size:
            description: Enter the logfile size in bytes.
            type: int
      module:
        description: Set module(linecard) logging.
        type: dict
        suboptions:
          state:
            description: Enable or disable module logging.
            type: str
            choices: ["enabled", "disabled"]
          level:
            description: Set severity level for module logging.
            type: int
      monitor:
        description: Set terminal line(monitor) logging level.
        type: dict
        suboptions:
          state:
            description: Enable or disable monitor logging.
            type: str
            choices: ["enabled", "disabled"]
          level:
            description: Set severity level for monitor logging.
            type: int
      origin_id:
        description: Enable origin information for Remote Syslog Server.
        type: dict
        suboptions:
          hostname:
            description: Use hostname as origin-id of logging messages.
            type: bool
          ip:
            description: Use ip address as origin-id of logging messages.
            type: str
          string:
            description: Use text string as origin-id of logging messages.
            type: str
      rate_limit:
        description: Enable or disable rate limit for log messages.
        type: str
        choices: ["enabled", "disabled"]
      rfc_strict:
        description:
          - Set RFC to which messages should compliant.
          - Syslogs will be compliant to RFC 5424.
        type: bool
      servers:
        description: Enable forwarding to Remote Syslog Servers.
        type: list
        elements: dict
        suboptions:
          server:
            description: Hostname/IPv4/IPv6 address of the Remote Syslog Server.
            type: str
          level:
            description: Set severity level for host.
            type: int
          facility:
            description: Facility to use when forwarding to server.
            type: str
          port:
            description: Destination Port when forwarding to remote server.
            type: str
          secure:
            description: Enable secure connection to remote server.
            type: dict
            suboptions:
              trustpoint:
                description: Trustpoint configuration.
                type: dict
                suboptions:
                  client_identity:
                    description:
                      - Client Identity certificate for mutual authentication.
                      - Trustpoint to use for client certificate authentication.
                    type: str
          use_vrf:
            description: Display per-VRF information.
            type: str
      source_interface:
        description: Enable Source-Interface for Remote Syslog Server.
        type: str
      timestamp:
        description: Set logging timestamp granularity.
        type: str
        choices: ["microseconds", "milliseconds", "seconds"]
  state:
    description:
    - The state the configuration should be left in.
    - Refer to examples for more details.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - parsed
    - gathered
    - rendered
    default: merged
"""
EXAMPLES = """

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.logging_global.logging_global import (
    Logging_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.logging_global.logging_global import (
    Logging_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Logging_globalArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Logging_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
