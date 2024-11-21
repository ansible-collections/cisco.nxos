#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_vrf_address_family
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_vrf_address_family
short_description: Resource module to configure VRF definitions.
description: This module provides declarative management of VRF definitions on Cisco NXOS.
version_added: 9.2.1
author: Vinay Mulugund (@roverflow)
notes:
  - Tested against NX-OS 9.3.6.
  - This module works with connection C(network_cli) and C(httpapi).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html)
options:
  config:
    description: A list of device configurations for VRF.
    type: list
    elements: dict
    suboptions:
      name:
        description: Name of the VRF.
        type: str
        required: true
      address_families:
        description: Enable address family and enter its config mode - AFI/SAFI configuration
        type: list
        elements: dict
        suboptions:
          afi:
            description: Address Family Identifier (AFI)
            type: str
            choices: ["ipv4", "ipv6"]
          safi:
            description: Address Family modifier
            type: str
            choices: ["multicast", "unicast"]
          maximum:
            description: Set a limit of routes
            type: dict
            suboptions:
              max_routes:
                description: Maximum number of routes allowed
                type: int
              max_route_options:
                description: Configure the options for maximum routes
                type: dict
                mutually_exclusive: [["warning_only", "threshold"]]
                suboptions:
                  warning_only:
                    description: Configure only give a warning message if limit is exceeded
                    type: bool
                  threshold:
                    description: Configure threshold & its options
                    type: dict
                    suboptions:
                      threshold_value:
                        description: Threshold value (%) at which to generate a warning msg
                        type: int
                      reinstall_threshold:
                        description: Threshold value (%) at which to reinstall routes back to VRF
                        type: int
          route_target:
            description: Specify Target VPN Extended Communities
            type: list
            elements: dict
            mutually_exclusive: [["import", "export"]]
            suboptions:
              import:
                description: Import Target-VPN community
                type: str
              export:
                description: Export Target-VPN community
                type: str
          export:
            description: VRF export
            type: list
            elements: dict
            mutually_exclusive: [["map", "vrf"]]
            suboptions:
              map:
                description: Route-map based VRF export
                type: str
              vrf:
                description: Virtual Router Context
                type: dict
                suboptions:
                  max_prefix:
                    description: Maximum prefix limit
                    type: int
                  map_import:
                    description: Route-map based VRF import
                    type: str
                  allow_vpn:
                    description: Allow re-importation of VPN imported routes
                    type: bool
          import:
            description: VRF import
            type: list
            elements: dict
            mutually_exclusive: [["map", "vrf"]]
            suboptions:
              map:
                description: Route-map based VRF export
                type: str
              vrf:
                description: Virtual Router Context
                type: dict
                suboptions:
                  max_prefix:
                    description: Maximum prefix limit
                    type: int
                  map_import:
                    description: Route-map based VRF import
                    type: str
                  advertise_vpn:
                    description: Allow leaked routes to be advertised to VPN
                    type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device by
        executing the command B(show running-config | section ^vrf).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices: [parsed, gathered, deleted, merged, replaced, rendered, overridden]
    default: merged
    description:
      - The state the configuration should be left in
      - The states I(rendered), I(gathered) and I(parsed) does not perform any change
        on the device.
      - The state I(rendered) will transform the configuration in C(config) option to
        platform specific CLI commands which will be returned in the I(rendered) key
        within the result. For state I(rendered) active connection to remote host is
        not required.
      - The state I(gathered) will fetch the running configuration from device and transform
        it into structured data in the format as per the resource module argspec and
        the value is returned in the I(gathered) key within the result.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into JSON format as per the resource module parameters and the
        value is returned in the I(parsed) key within the result. The value of C(running_config)
        option should be the same format as the output of command I(show running-config | section ^vrf).
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden), C(deleted) or C(purged)
  type: list
  sample:
    - vrf context management
    - address-family ipv4 unicast
    - maximum routes 500 60 reinstall 80
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - vrf context test1
    - address-family ipv6 unicast
    - route-target export 65512:200
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.vrf_address_family.vrf_address_family import (
    Vrf_address_familyArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vrf_address_family.vrf_address_family import (
    Vrf_address_family,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vrf_address_familyArgs.argument_spec,
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

    result = Vrf_address_family(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
