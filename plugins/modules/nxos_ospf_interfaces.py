#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_ospf_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_ospf_interfaces
version_added: 1.3.0
short_description: OSPF Interfaces Resource Module.
description:
- This module manages OSPF(v2/v3) configuration of interfaces on devices running Cisco NX-OS.
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section "^interface").
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of OSPF configuration for interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name/Identifier of the interface.
        type: str
        required: True
      address_family:
        description:
        - OSPF settings on the interfaces in address-family context.
        type: list
        elements: dict
        suboptions:
          afi:
            description:
            - Address Family Identifier (AFI) for OSPF settings on the interfaces.
            type: str
            choices: ['ipv4', 'ipv6']
            required: True
          processes:
            description:
            - Interfaces configuration for an OSPF process.
            type: list
            elements: dict
            suboptions:
              process_id:
                description:
                - OSPF process tag.
                type: str
                required: True
              area:
                description:
                - Area associated with interface.
                type: dict
                suboptions:
                  area_id:
                    description:
                    - Area ID as a decimal or IP address format.
                    type: str
                    required: True
                  secondaries:
                    description:
                    - Do not include secondary IPv4/IPv6 addresses.
                    type: bool
              multi_areas:
                description:
                - Multi-Areas associated with interface.
                - Valid values are Area Ids as an integer or IP address.
                type: list
                elements: str
          multi_areas:
            description:
            - Multi-Areas associated with interface (not tied to OSPF process).
            - Valid values are Area Ids as an integer or IP address.
            type: list
            elements: str
          authentication:
            description:
            - Authentication settings on the interface.
            type: dict
            suboptions:
              key_chain:
                description:
                - Authentication password key-chain.
                type: str
              message_digest:
                description:
                - Use message-digest authentication.
                type: bool
              enable:
                description:
                - Enable/disable authentication on the interface.
                type: bool
              null_auth:
                description:
                - Use null(disable) authentication.
                type: bool
          authentication_key:
            description:
            - Configure the authentication key for the interface.
            type: dict
            suboptions:
              encryption:
                description:
                - 0 Specifies an UNENCRYPTED authentication key will follow.
                - 3 Specifies an 3DES ENCRYPTED authentication key will follow.
                - 7 Specifies a Cisco type 7  ENCRYPTED authentication key will follow.
                type: int
              key:
                description:
                - Authentication key.
                - Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password
                  and UNENCRYPTED (cleartext) password based on the value of encryption key.
                type: str
                required: True
          message_digest_key:
            description:
            - Message digest authentication password (key) settings.
            type: dict
            suboptions:
              key_id:
                description:
                - Key ID.
                type: int
                required: True
              encryption:
                description:
                - 0 Specifies an UNENCRYPTED ospf password (key) will follow.
                - 3 Specifies an 3DES ENCRYPTED ospf password (key) will follow.
                - 7 Specifies a Cisco type 7 ENCRYPTED the ospf password (key) will follow.
                type: int
              key:
                description:
                - Authentication key.
                - Valid values are Cisco type 7 ENCRYPTED password, 3DES ENCRYPTED password
                  and UNENCRYPTED (cleartext) password based on the value of encryption key.
                type: str
                required: True
          cost:
            description:
            - Cost associated with interface.
            type: int
          dead_interval:
            description:
            - Dead interval value (in seconds).
            type: int
          hello_interval:
            description:
            - Hello interval value (in seconds).
            type: int
          instance:
            description:
            - Instance identifier.
            type: int
          mtu_ignore:
            description:
            - Enable/disable OSPF MTU mismatch detection.
            type: bool
          network:
            description:
            - Network type.
            type: str
            choices: ["broadcast", "point-to-point"]
          passive_interface:
            description:
            - Suppress routing updates on the interface.
            type: bool
          priority:
            description:
            - Router priority.
            type: int
          retransmit_interval:
            description:
            - Packet retransmission interval.
            type: int
          shutdown:
            description:
            - Shutdown OSPF on this interface.
            type: bool
          transmit_delay:
            description:
            - Packet transmission delay.
            type: int
  state:
    description:
      - The state the configuration should be left in.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - parsed
    - rendered
    default: merged
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ospf_interfaces.ospf_interfaces import (
    Ospf_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.ospf_interfaces.ospf_interfaces import (
    Ospf_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Ospf_interfacesArgs.argument_spec,
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

    result = Ospf_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
