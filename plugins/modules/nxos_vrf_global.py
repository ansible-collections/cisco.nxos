#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_vrf_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_vrf_global
short_description: Resource module to configure VRF definitions.
description: This module provides declarative management of VRF definitions on Cisco NXOS.
version_added: 8.1.0
author: Vinay Mulugund (@roverflow)
notes:
  - Tested against NX-OS 9.3.6.
  - This module works with connection C(network_cli) and C(httpapi).
    See U(https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html)
options:
  config:
    description: A list containing device configurations for VRF.
    type: dict
    suboptions:
      vrfs:
        description: List of VRF definitions.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the VRF..
            required: true
            type: str
          description:
            description: Description of the VRF.
            type: str
          ip:
            description: Configure IP features for the specified vrf.
            type: dict
            suboptions:
              auto_discard:
                description: Auto 0.0.0.0/0 discard route.
                type: bool
              domain_list:
                description: Add list domain names.
                type: list
                elements: str
              domain_name:
                description: Specify default domain name.
                type: str
              icmp_err:
                description: Enable ICMP error message.
                type: dict
                suboptions:
                  source_interace:
                    description: Configure source-address for applications.
                    type: dict
                    suboptions:
                      interface:
                        description: Source interface for ICMP error messages.
                        type: str
                        choices:
                          - loopback
                          - ethernet
                          - port-channel
                      interface_value:
                        description: Source interface value for ICMP error messages.
                        type: str
              igmp:
                description: IGMP global configuration commands
                type: dict
                suboptions:
                  ssm_translate:
                    description: Translate IGMPv1/v2 reports to (S,G) route entries.
                    type: list
                    elements: dict
                    suboptions:
                      group:
                        description: Source address.
                        type: str
                      source:
                        description: Group address.
                        type: str
              mroutes:
                description: Configure multicast routes.
                type: list
                elements: dict
                suboptions:
                  group:
                    description: Multicast group address.
                    type: str
                  source:
                    description: Source address.
                    type: str
                  preference:
                    description: Preference value.
                    type: int
                  vrf:
                    description: VRF name.
                    type: str
              multicast:
                description: Configure IP multicast global parameters.
                type: dict
                suboptions:
                  group_range_prefix_list:
                    description: Group range prefix-list policy for multicast boundary.
                    type: str
                  multipath:
                    description: Configure ECMP multicast load splitting.
                    type: dict
                    suboptions:
                      resilient:
                        description: Configure resilient RPF interface.
                        type: bool
                      splitting_type:
                        description: Configure multicast load splitting type.
                        type: dict
                        mutually_exclusive:
                          [
                            [
                              "legacy",
                              "nbm",
                              "none",
                              "sg_hash",
                              "sg_hash_next_hop",
                            ],
                          ]
                        suboptions:
                          none:
                            description: Disable multicast load splitting.
                            type: bool
                          sg_hash:
                            description: Configure hash based on source and group address.
                            type: bool
                          sg_hash_next_hop:
                            description: Configure hash based on source and group address and next-hop.
                            type: bool
                  rpf:
                    description: Configure RPF check.
                    type: list
                    elements: dict
                    suboptions:
                      vrf_name:
                        description: VRF for RPF lookup.
                        type: str
                      group_list_range:
                        description: Group range for RPF select.
                        type: str
              name_server:
                description: Specify nameserver address.
                type: dict
                suboptions:
                  address_list:
                    description: Configure multicast name server address.
                    type: list
                    elements: str
                  use_vrf:
                    description: Display per-VRF information.
                    type: dict
                    suboptions:
                      vrf:
                        description: VRF name.
                        type: str
                      source_address:
                        description: source address for configuring name server.
                        type: str
              route:
                description: Configure static routes.
                type: list
                elements: dict
                mutually_exclusive: [["tags", "vrf", "track"]]
                suboptions:
                  source:
                    description: Destination prefix.
                    type: str
                  destination:
                    description: Next-hop address.
                    type: str
                  tags:
                    description: Route tag.
                    type: dict
                    suboptions:
                      tag_value:
                        description: Route tag value.
                        type: int
                      route_pref:
                        description: Route preference.
                        type: int
                  vrf:
                    description: add vrf to the route.
                    type: str
                  track:
                    description: Configure track object.
                    type: str
          vni:
            description: Virtual Network Identifier.
            type: dict
            suboptions:
              vni_number:
                description: VNI number.
                type: int
              layer_3:
                description: Configure Layer 3 VNI.
                type: bool
          multicast:
            description: Configure IP multicast options.
            type: dict
            suboptions:
              service_reflect:
                description: Configure service reflect option.
                type: list
                elements: dict
                suboptions:
                  service_interface:
                    description: configure service interface.
                    type: dict
                    suboptions:
                      interface:
                        description: Interface name.
                        type: str
                      interface_value:
                        description: Interface value / Regex.
                        type: str
                  map_to:
                    description: Map to interface.
                    type: dict
                    suboptions:
                      interface:
                        description: Interface name.
                        type: str
                      interface_value:
                        description: Interface value / Regex.
                        type: str
          ipv6:
            description: Configure IPv6 features for the specified vrf.
            type: dict
            suboptions:
              mld_ssm_translate:
                description: Translate MLDv1/v2 reports to (S,G) route entries.
                type: list
                elements: dict
                suboptions:
                  icmp:
                    description: Configure ICMP parameters with mld.
                    type: bool
                  group:
                    description: Source address.
                    type: str
                  source:
                    description: Group address.
                    type: str
              multicast:
                description: Configure IP multicast global parameters for ipv6.
                type: dict
                suboptions:
                  group_range_prefix_list:
                    description: Group range prefix-list policy for multicast boundary.
                    type: str
                  multipath:
                    description: Configure ECMP multicast load splitting.
                    type: dict
                    suboptions:
                      resilient:
                        description: Configure resilient RPF interface.
                        type: bool
                      splitting_type:
                        description: Configure multicast load splitting type.
                        type: dict
                        mutually_exclusive:
                          [["none", "sg_hash", "sg_hash_next_hop"]]
                        suboptions:
                          none:
                            description: Disable multicast load splitting.
                            type: bool
                          sg_hash:
                            description: Configure hash based on source and group address.
                            type: bool
                          sg_hash_next_hop:
                            description: Configure hash based on source and group address and next-hop.
                            type: bool
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section ^vrf).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
      [
        parsed,
        gathered,
        deleted,
        merged,
        replaced,
        rendered,
        overridden,
        purged,
      ]
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
from ansible_collections.cisco.nxos.nxos.plugins.module_utils.network.nxos.argspec.vrf_global.vrf_global import (
    Vrf_globalArgs,
)
from ansible_collections.cisco.nxos.nxos.plugins.module_utils.network.nxos.config.vrf_global.vrf_global import (
    Vrf_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Vrf_globalArgs.argument_spec,
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

    result = Vrf_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
