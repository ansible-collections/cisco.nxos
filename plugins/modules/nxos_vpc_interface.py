#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_vpc_interface
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_vpc_interface
version_added: 1.0.0
short_description: VPC interface resource module
description:
  - This module manages VPC (Virtual Port Channel) configuration on port-channel
    interfaces of Cisco NX-OS devices.
notes:
  - Tested against NX-OS 9.3.6.
  - Unsupported for Cisco MDS.
  - C(vpc) and C(peer_link) are mutually exclusive for a given port-channel.
  - C(orphan_port_suspend) applies to any interface type, including Ethernet interfaces.
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does
    not connect to the device.
author: Ansible Network Eng Team
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section ^interface).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description:
      - A list of VPC interface configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface (e.g. C(port-channel10) or C(Ethernet1/3)).
        type: str
        required: true
      vpc:
        description:
          - VPC ID to assign to this port-channel.
          - Mutually exclusive with I(peer_link).
        type: str
      peer_link:
        description:
          - When C(true), configure this port-channel as the VPC peer-link.
          - Mutually exclusive with I(vpc).
        type: bool
      orphan_port_suspend:
        description:
          - When C(true), configure the interface as a VPC orphan-port that
            suspends when the VPC secondary peer-link goes down.
          - Supported on any interface type.
        type: bool
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
      - rendered
      - parsed
    default: merged
extends_documentation_fragment:
  - cisco.nxos.nxos
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
# nxos# show running-config | section ^interface port-channel
# interface port-channel10
#   switchport
# interface port-channel20
#   switchport

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_vpc_interface:
    config:
      - name: port-channel10
        vpc: 100
      - name: port-channel20
        peer_link: true
      - name: Ethernet1/3
        orphan_port_suspend: true
    state: merged

# Task output:
# ------------
# before: []
#
# commands:
#   - interface port-channel10
#   - vpc 100
#   - interface port-channel20
#   - vpc peer-link
#   - interface Ethernet1/3
#   - vpc orphan-port suspend
#
# after:
#   - name: Ethernet1/3
#     orphan_port_suspend: true
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true

# After state:
# ------------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link


# Using replaced

# Before state:
# -------------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link

- name: Replace the VPC configuration of listed port-channels
  cisco.nxos.nxos_vpc_interface:
    config:
      - name: port-channel10
        vpc: 200
    state: replaced

# Task output:
# ------------
# before:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true
#
# commands:
#   - interface port-channel10
#   - no vpc
#   - vpc 200
#
# after:
#   - name: port-channel10
#     vpc: "200"
#   - name: port-channel20
#     peer_link: true

# Note: port-channel20 is unchanged because it is not in the config list.


# Using overridden

# Before state:
# -------------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link
# interface port-channel30
#   vpc 300

- name: Override all VPC interface configuration with provided configuration
  cisco.nxos.nxos_vpc_interface:
    config:
      - name: port-channel10
        vpc: 100
      - name: port-channel20
        peer_link: true
    state: overridden

# Task output:
# ------------
# before:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true
#   - name: port-channel30
#     vpc: "300"
#
# commands:
#   - interface port-channel30
#   - no vpc
#
# after:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true

# Note: port-channel30 is removed because it is not in the want list.


# Using deleted

# Before state:
# -------------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link

- name: Delete the VPC configuration of listed port-channels
  cisco.nxos.nxos_vpc_interface:
    config:
      - name: port-channel10
    state: deleted

# Task output:
# ------------
# before:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true
#
# commands:
#   - interface port-channel10
#   - no vpc
#
# after:
#   - name: port-channel20
#     peer_link: true

# Using deleted (no config — removes all VPC interface configuration)

- name: Delete the VPC configuration of all port-channels
  cisco.nxos.nxos_vpc_interface:
    state: deleted

# Task output:
# ------------
# commands:
#   - interface port-channel10
#   - no vpc
#   - interface port-channel20
#   - no vpc peer-link


# Using gathered

# Existing device config:
# -----------------------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link

- name: Gather VPC interface facts from the device
  cisco.nxos.nxos_vpc_interface:
    state: gathered

# Task output:
# ------------
# gathered:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true


# Using rendered

- name: Render platform specific configuration lines
  cisco.nxos.nxos_vpc_interface:
    config:
      - name: port-channel10
        vpc: 100
      - name: port-channel20
        peer_link: true
    state: rendered

# Task output:
# ------------
# rendered:
#   - interface port-channel10
#   - vpc 100
#   - interface port-channel20
#   - vpc peer-link


# Using parsed

# parsed.cfg
# ----------
# interface port-channel10
#   vpc 100
# interface port-channel20
#   vpc peer-link

- name: Parse externally supplied configuration into structured data
  cisco.nxos.nxos_vpc_interface:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   - name: port-channel10
#     vpc: "100"
#   - name: port-channel20
#     peer_link: true
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
    - interface port-channel10
    - vpc 100
    - interface port-channel20
    - vpc peer-link
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface port-channel10
    - vpc 100
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.vpc_interfaces.vpc_interfaces import (
    Vpc_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vpc_interfaces.vpc_interfaces import (
    Vpc_interfaces,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Vpc_interfacesArgs.argument_spec,
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

    result = Vpc_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
