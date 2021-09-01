#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_ntp_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_ntp_global
short_description: NTP Global resource module.
description:
- This module manages ntp configuration on devices running Cisco NX-OS.
version_added: 2.6.0
notes:
- Tested against NX-OS 9.3.6.
- This module works with connection C(network_cli) and C(httpapi).
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config ntp).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A dict of ntp configuration.
    type: dict
    suboptions:
      access_group:
        description: NTP access-group.
        type: dict
        suboptions:
          match_all:
            description: Scan ACLs present in all ntp access groups.
            type: bool
          peer:
            description: Access-group peer.
            type: list
            elements: str
          query_only:
            description: Access-group query-only.
            type: list
            elements: str
          serve:
            description: Access-group serve.
            type: list
            elements: str
          serve_only:
            description: Access-group serve-only.
            type: list
            elements: str
      allow:
        description: Enable/Disable the packets.
        type: dict
        suboptions:
          control:
            description: Control mode packets.
            type: dict
            suboptions:
              rate_limit:
                description: Rate-limit delay.
                type: int
          private:
            description: Enable/Disable Private mode packets.
            type: bool
      authenticate:
        description: Enable/Disable authentication.
        type: bool
      authentication_keys:
        description: NTP authentication key.
        type: list
        elements: dict
        suboptions:
          id:
            description: Authentication key number (range 1-65535).
            type: int
          key:
            description: Authentication key.
            type: str
          encryption:
            description:
              - 0 for Clear text
              - 7 for Encrypted
            type: int
      logging:
        description: Enable/Disable logging of NTPD Events.
        type: bool
      master:
        description:
          - Act as NTP master clock.
          - Stratum number.
        type: int
      passive:
        description: NTP passive command.
        type: bool
      peers:
        description: NTP Peers.
        type: list
        elements: dict
        suboptions:
          peer:
            description: Hostname/IP address of the NTP Peer.
            type: str
          key:
            description: Keyid to be used while communicating to this server.
            type: int
          maxpoll:
            description:
              - Maximum interval to poll a peer.
              - Poll interval in secs to a power of 2.
            type: int
          minpoll:
            description:
              - Minimum interval to poll a peer.
              - Poll interval in secs to a power of 2.
            type: int
          prefer:
            description:
              - Preferred Server.
            type: bool
          use_vrf:
            description: Display per-VRF information.
            type: str
      servers:
        description: NTP servers.
        type: list
        elements: dict
        suboptions:
          server:
            description: Hostname/IP address of the NTP Peer.
            type: str
          key:
            description: Keyid to be used while communicating to this server.
            type: int
          maxpoll:
            description:
              - Maximum interval to poll a peer.
              - Poll interval in secs to a power of 2.
            type: int
          minpoll:
            description:
              - Minimum interval to poll a peer.
              - Poll interval in secs to a power of 2.
            type: int
          prefer:
            description:
              - Preferred Server.
            type: bool
          use_vrf:
            description: Display per-VRF information.
            type: str
      source:
        description: Source of NTP packets.
        type: str
      source_interface:
        description: Source interface sending NTP packets.
        type: str
      trusted_keys:
        description: NTP trusted-key number.
        type: list
        elements: int
  state:
    description:
    - The state the configuration should be left in.
    - Refer to examples for more details.
    - With state I(replaced), for the listed route-maps,
      sequences that are in running-config but not in the task are negated.
    - With state I(overridden), all route-maps that are in running-config but
      not in the task are negated.
    - Please refer to examples for more details.
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

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - sample command 1
    - sample command 2
    - sample command 3
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ntp_global.ntp_global import (
    Ntp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.ntp_global.ntp_global import (
    Ntp_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ntp_globalArgs.argument_spec,
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

    result = Ntp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
