#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_netflow_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_netflow_interfaces
version_added: 14.1.0
short_description: NetFlow interfaces resource module.
description:
  - This module manages the assignment of flow monitors to the interfaces of Cisco NX-OS devices.
  - It manages the C(ip flow monitor), C(ipv6 flow monitor) and C(layer2-switched flow monitor) commands of an interface.
  - The flow monitors themselves must already exist on the device, they are managed by C(cisco.nxos.nxos_netflow_global).
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - The flow monitor commands need C(feature netflow), and the flow monitors must already exist with an exporter.
  - The C(layer2_switched) protocol is only accepted on a switchport.
  - The direction C(output) needs the C(egr-netflow) TCAM region to be carved, C(ipv6) only accepts C(input) on the tested platform.
  - The C(sampler) option of the flow monitor commands is not available on the tested platform.
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does not connect to the device.
author:
  - Jørgen Spange (@jorgenspange)
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor").
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of the flow monitor assignments of interfaces.
    type: list
    elements: dict
    suboptions:
      name:
        description: The name of the interface, for example C(Ethernet1/1), C(port-channel10) or C(Vlan100). Interface names are normalised.
        type: str
        required: true
      flow_monitors:
        description: The flow monitors that are applied on the interface.
        type: list
        elements: dict
        suboptions:
          monitor:
            description: The name of the flow monitor.
            type: str
            required: true
          direction:
            description: The direction of the traffic that the flow monitor is applied on.
            type: str
            required: true
            choices:
              - input
              - output
          protocol:
            description: The protocol, C(ipv4) is C(ip flow monitor), C(ipv6) is C(ipv6 flow monitor) and C(layer2_switched) is C(layer2-switched flow monitor).
            type: str
            default: ipv4
            choices:
              - ipv4
              - ipv6
              - layer2_switched
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) the flow monitors are added, a flow monitor with another name for the same protocol and direction is replaced.
      - With I(replaced) the flow monitors of the interfaces in I(config) are replaced by the given ones.
      - With I(overridden) the flow monitors of all the interfaces are replaced, the interfaces not in I(config) lose theirs.
      - With I(deleted) the flow monitors of the interfaces in I(config) are removed, without I(config) those of all the interfaces.
      - With I(gathered), I(rendered) and I(parsed) nothing is changed on the device.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
# interface Ethernet1/1
# interface Ethernet1/2

- name: Apply flow monitors on the interfaces
  cisco.nxos.nxos_netflow_interfaces:
    config:
      - name: Ethernet1/1
        flow_monitors:
          - monitor: MON_V4
            direction: input
          - monitor: MON_V6
            protocol: ipv6
            direction: input
      - name: Ethernet1/2
        flow_monitors:
          - monitor: MON_L2
            protocol: layer2_switched
            direction: input
    state: merged

# Task output:
# ------------
# before: []
# commands:
#   - interface Ethernet1/1
#   - ip flow monitor MON_V4 input
#   - ipv6 flow monitor MON_V6 input
#   - interface Ethernet1/2
#   - layer2-switched flow monitor MON_L2 input
# after:
#   - name: Ethernet1/1
#     flow_monitors:
#       - monitor: MON_V4
#         direction: input
#         protocol: ipv4
#       - monitor: MON_V6
#         direction: input
#         protocol: ipv6
#   - name: Ethernet1/2
#     flow_monitors:
#       - monitor: MON_L2
#         direction: input
#         protocol: layer2_switched

# Using replaced

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
# interface Ethernet1/1
#   ip flow monitor MON_V4 input
#   ipv6 flow monitor MON_V6 input

- name: Replace the flow monitors of Ethernet1/1
  cisco.nxos.nxos_netflow_interfaces:
    config:
      - name: Ethernet1/1
        flow_monitors:
          - monitor: MON_V4_NEW
            direction: input
    state: replaced

# Task output:
# ------------
# commands:
#   - interface Ethernet1/1
#   - no ip flow monitor MON_V4 input
#   - ip flow monitor MON_V4_NEW input
#   - no ipv6 flow monitor MON_V6 input

# Using overridden

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
# interface Ethernet1/1
#   ip flow monitor MON_V4 input
# interface Ethernet1/2
#   layer2-switched flow monitor MON_L2 input

- name: Override the flow monitors of all the interfaces
  cisco.nxos.nxos_netflow_interfaces:
    config:
      - name: Ethernet1/1
        flow_monitors:
          - monitor: MON_V4
            direction: input
    state: overridden

# Task output:
# ------------
# commands:
#   - interface Ethernet1/2
#   - no layer2-switched flow monitor MON_L2 input

# Using deleted

- name: Remove the flow monitors of Ethernet1/1
  cisco.nxos.nxos_netflow_interfaces:
    config:
      - name: Ethernet1/1
    state: deleted

# Task output:
# ------------
# commands:
#   - interface Ethernet1/1
#   - no ip flow monitor MON_V4 input

- name: Remove the flow monitors of all the interfaces
  cisco.nxos.nxos_netflow_interfaces:
    state: deleted

# Using gathered

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
# interface Ethernet1/1
#   ip flow monitor MON_V4 input
# interface Ethernet1/2

- name: Gather the flow monitors of the interfaces
  cisco.nxos.nxos_netflow_interfaces:
    state: gathered

# Task output:
# ------------
# gathered:
#   - name: Ethernet1/1
#     flow_monitors:
#       - monitor: MON_V4
#         direction: input
#         protocol: ipv4

# Using rendered

- name: Render the commands for the provided configuration
  cisco.nxos.nxos_netflow_interfaces:
    config:
      - name: Eth1/3
        flow_monitors:
          - monitor: MON_V4
            direction: input
          - monitor: MON_V6
            protocol: ipv6
            direction: input
    state: rendered

# Task output:
# ------------
# rendered:
#   - interface Ethernet1/3
#   - ip flow monitor MON_V4 input
#   - ipv6 flow monitor MON_V6 input

# Using parsed

# parsed.cfg
# ----------
# interface Ethernet1/1
#   ip flow monitor MON_V4 input
# interface Ethernet1/2

- name: Parse the provided configuration
  cisco.nxos.nxos_netflow_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   - name: Ethernet1/1
#     flow_monitors:
#       - monitor: MON_V4
#         direction: input
#         protocol: ipv4
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - interface Ethernet1/1
    - ip flow monitor MON_V4 input
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface Ethernet1/1
    - ip flow monitor MON_V4 input
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option, parsed into structured data.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.netflow_interfaces.netflow_interfaces import (
    Netflow_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.netflow_interfaces.netflow_interfaces import (
    Netflow_interfaces,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Netflow_interfacesArgs.argument_spec,
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

    result = Netflow_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
