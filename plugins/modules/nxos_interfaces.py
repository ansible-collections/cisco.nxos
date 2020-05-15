#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for nxos_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "network",
}

DOCUMENTATION = """module: nxos_interfaces
short_description: Interfaces Resource Module
description: This module manages the interface attributes of NX-OS interfaces.
author: Trishna Guha (@trishnaguha)
notes:
- Tested against NXOS 7.3.(0)D1(1) on VIRL
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device by executing
        the command B(show running-config | section ^interface)
      - The state I(parsed) reads the configuration from C(running_config) option and transforms
        it into Ansible structured data as per the resource module's argspec and the value is then
        returned in the I(parsed) key within the result.
    type: str
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, e.g. Ethernet1/1, port-channel10.
        type: str
        required: true
      description:
        description:
        - Interface description.
        type: str
      enabled:
        description:
        - Administrative state of the interface. Set the value to C(true) to administratively
          enable the interface or C(false) to disable it
        type: bool
      speed:
        description:
        - Interface link speed. Applicable for Ethernet interfaces only.
        type: str
      mode:
        description:
        - Manage Layer2 or Layer3 state of the interface. Applicable for Ethernet
          and port channel interfaces only.
        choices:
        - layer2
        - layer3
        type: str
      mtu:
        description:
        - MTU for a specific interface. Must be an even number between 576 and 9216.
          Applicable for Ethernet interfaces only.
        type: str
      duplex:
        description:
        - Interface link status. Applicable for Ethernet interfaces only.
        type: str
        choices:
        - full
        - half
        - auto
      ip_forward:
        description:
        - Enable or disable IP forward feature on SVIs. Set the value to C(true) to
          enable  or C(false) to disable.
        type: bool
      fabric_forwarding_anycast_gateway:
        description:
        - Associate SVI with anycast gateway under VLAN configuration mode. Applicable
          for SVI interfaces only.
        type: bool
  state:
    description:
    - The state of the configuration after module completion
    - The state I(rendered) considers the system default mode for interfaces to be "Layer 3"
      and the system default state for interfaces to be shutdown.
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
#
# interface Ethernet1/1
#   description testing
#   mtu 1800

- name: Merge provided configuration with device configuration
  nxos_interfaces:
    config:
      - name: Ethernet1/1
        description: 'Configured by Ansible'
        enabled: True
      - name: Ethernet1/2
        description: 'Configured by Ansible Network'
        enabled: False
    state: merged

# After state:
# ------------
#
# interface Ethernet1/1
#    description Configured by Ansible
#    no shutdown
#    mtu 1800
# interface Ethernet2
#    description Configured by Ansible Network
#    shutdown


# Using replaced

# Before state:
# -------------
#
# interface Ethernet1/1
#    description Interface 1/1
# interface Ethernet1/2

- name: Replaces device configuration of listed interfaces with provided configuration
  nxos_interfaces:
    config:
      - name: Ethernet1/1
        description: 'Configured by Ansible'
        enabled: True
        mtu: 2000
      - name: Ethernet1/2
        description: 'Configured by Ansible Network'
        enabled: False
        mode: layer2
    state: replaced

# After state:
# ------------
#
# interface Ethernet1/1
#   description Configured by Ansible
#   no shutdown
#   mtu 1500
# interface Ethernet2/2
#    description Configured by Ansible Network
#    shutdown
#    switchport


# Using overridden

# Before state:
# -------------
#
# interface Ethernet1/1
#    description Interface Ethernet1/1
# interface Ethernet1/2
# interface mgmt0
#    description Management interface
#    ip address dhcp

- name: Override device configuration of all interfaces with provided configuration
  nxos_interfaces:
    config:
      - name: Ethernet1/1
        enabled: True
      - name: Ethernet1/2
        description: 'Configured by Ansible Network'
        enabled: False
    state: overridden

# After state:
# ------------
#
# interface Ethernet1/1
# interface Ethernet1/2
#    description Configured by Ansible Network
#    shutdown
# interface mgmt0
#    ip address dhcp


# Using deleted

# Before state:
# -------------
#
# interface Ethernet1/1
#    description Interface Ethernet1/1
# interface Ethernet1/2
# interface mgmt0
#    description Management interface
#    ip address dhcp

- name: Delete or return interface parameters to default settings
  nxos_interfaces:
    config:
      - name: Ethernet1/1
    state: deleted

# After state:
# ------------
#
# interface Ethernet1/1
# interface Ethernet1/2
# interface mgmt0
#    description Management interface
#    ip address dhcp

# Using rendered

- name: Use rendered state to convert task input to device specific commands
  cisco.nxos.nxos_interfaces:
    config:
      - name: Ethernet1/1
        description: outbound-intf
        mode: layer3
        speed: 100
      - name: Ethernet1/2
        mode: layer2
        enabled: True
        duplex: full
    state: rendered

# Task Output (redacted)
# -----------------------

# rendered:
#   - "interface Ethernet1/1"
#   - "description outbound-intf"
#   - "speed 100"
#   - "interface Ethernet1/2"
#   - "switchport"
#   - "duplex full"
#   - "no shutdown"

# Using parsed

# parsed.cfg
# ------------
# interface Ethernet1/800
#   description test-1
#   speed 1000
#   shutdown
#   no switchport
#   duplex half
# interface Ethernet1/801
#   description test-2
#   switchport
#   no shutdown
#   mtu 1800

- name: Use parsed state to convert externally supplied config to structured format
  cisco.nxos.nxos_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output (redacted)
# -----------------------
#  parsed:
#    - description: "test-1"
#      duplex: "half"
#      enabled: false
#      mode: "layer3"
#      name: "Ethernet1/800"
#      speed: "1000"
#
#    - description: "test-2"
#      enabled: true
#      mode: "layer2"
#      mtu: "1800"
#      name: "Ethernet1/801"

# Using gathered

# Existing device config state
# -----------------------------
# interface Ethernet1/1
#   description outbound-intf
#   switchport
#   no shutdown
# interface Ethernet1/2
#   description intf-l3
#   speed 1000
# interface Ethernet1/3
# interface Ethernet1/4
# interface Ethernet1/5

- name: Gather interfaces facts from the device using nxos_interfaces
  cisco.nxos.nxos_interfaces:
    state: gathered

# Task output (redacted)
# -----------------------
# - name: Ethernet1/1
#   description: outbound-intf
#   mode: layer2
#   enabled: True
# - name: Ethernet1/2
#   description: intf-l3
#   speed: "1000"
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['interface Ethernet1/1', 'mtu 1800']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces import (
    Interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
