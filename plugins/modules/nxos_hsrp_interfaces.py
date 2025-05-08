#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_hsrp_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_hsrp_interfaces
short_description: HSRP interfaces resource module
description: Resource module to configure HSRP on interfaces.
version_added: 1.0.0
author:
  - Chris Van Heuveln (@chrisvanheuveln)
  - Sagar Paul (@KB-perByte)
notes:
  - Tested against NX-OS 10.4(2) Nexus 9000v.
  - Feature bfd and hsrp, should be enabled for this module.
  - Unsupported for Cisco MDS
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section '^interface').
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A dictionary of HSRP configuration options to add to interface
    type: list
    elements: dict
    suboptions:
      name:
        type: str
        description: The name of the interface.
      bfd:
        type: str
        description:
          - Enable/Disable HSRP Bidirectional Forwarding Detection (BFD) on the interface.
        choices:
          - enable
          - disable
      standby_options:
        description: Group number and group options for standby (HSRP)
        type: list
        elements: dict
        suboptions:
          group_no:
            description: Group number
            type: int
          authentication:
            description: Authentication configuration
            type: dict
            suboptions:
              key_chain:
                description: Set key chain
                type: str
              key_string:
                description: Set key string
                type: str
              password_text:
                description: Password text valid for plain text and and key-string
                type: str
          follow:
            description: Groups to be followed
            type: str
          mac_address:
            description: Virtual MAC address
            type: str
          ip:
            description: Enable HSRP IPv4 and set the virtual IP address
            type: list
            elements: dict
            suboptions:
              virtual_ip:
                description: Virtual IP address
                type: str
              secondary:
                description: Make this IP address a secondary virtual IP address
                type: bool
          group_name:
            description: Redundancy name string
            type: str
          preempt:
            description: Overthrow lower priority Active routers
            type: dict
            suboptions:
              minimum:
                description: Delay at least this long
                type: int
              reload:
                description: Delay after reload
                type: int
              sync:
                description: Wait for IP redundancy clients
                type: int
          priority:
            description: Priority level
            type: dict
            suboptions:
              level:
                description: Priority level value
                type: int
              upper:
                description: Set upper threshold value (forwarding-threshold)
                type: int
              lower:
                description: Set lower threshold value (forwarding-threshold)
                type: int
          timer:
            description: Overthrow lower priority Active routers
            type: dict
            suboptions:
              hello_interval:
                description: Hello interval in seconds
                type: int
              hold_time:
                description: Hold time in seconds
                type: int
              msec:
                description: Specify hello interval in milliseconds
                type: bool
          track:
            description: Priority tracking
            type: list
            elements: dict
            suboptions:
              object_no:
                description: Track object number
                type: int
              decrement:
                description: Priority decrement
                type: int
      standby:
        description:
          - Standby options generic, not idempotent when version 1 (HSRP)
        type: dict
        suboptions:
          bfd:
            description: Enable HSRP BFD
            type: bool
          delay:
            description: HSRP initialization delay
            type: dict
            suboptions:
              minimum:
                description: Delay at least this long
                type: int
              reload:
                description: Delay after reload
                type: int
          mac_refresh:
            description: Refresh MAC cache on switch by periodically sending packet from virtual mac address
            type: int
          use_bia:
            description: HSRP uses interface's burned in address (does not work with mac address)
            type: dict
            suboptions:
              set:
                description: Set use-bia only
                type: bool
              scope:
                description: Scope interface option (hsrp use-bia scope interface)
                type: bool
          version:
            description: HSRP version
            type: int
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - parsed
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
        option should be the same format as the output of command
        I(show running-config | section ^interface) executed on device. For state I(parsed) active
        connection to remote host is not required.
    type: str
"""

EXAMPLES = """
#test# sh run | section interface
#feature interface-vlan
#interface Vlan1
#interface Vlan14
#  bandwidth 99999
#  hsrp bfd
#  hsrp version 2
#  hsrp delay minimum 22 reload 123
#  hsrp mac-refresh 222
#  hsrp 14
#    follow testfolow
#    ip 10.0.1.1 secondary
#    ip 10.1.1.3
#  hsrp 15
#    authentication md5 key-string testmesecurte
#    mac-address 0423.4567.89AB
#    preempt delay minimum 33 reload 23 sync 22
#    priority 22 forwarding-threshold lower 12 upper 22
#    timers msec 456  33
#interface Vlan1000
#  hsrp 10
#    authentication md5 key-string testmesecurte
#    name testhsr
#    mac-address 0423.4567.89AB
#    preempt delay minimum 33 reload 23 sync 22
#    priority 22 forwarding-threshold lower 12 upper 22
#    timers msec 456  33
#    ip 10.15.8.1 secondary



# Using deleted

- name: Configure hsrp attributes on interfaces
  cisco.nxos.nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
      - name: Ethernet1/2
    operation: deleted


# Using merged

- name: Configure hsrp attributes on interfaces
  cisco.nxos.nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: merged


# Using overridden

- name: Configure hsrp attributes on interfaces
  cisco.nxos.nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: overridden


# Using replaced

- name: Configure hsrp attributes on interfaces
  cisco.nxos.nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/1
        bfd: enable
      - name: Ethernet1/2
        bfd: disable
    operation: replaced

# Using rendered

- name: Use rendered state to convert task input to device specific commands
  cisco.nxos.nxos_hsrp_interfaces:
    config:
      - name: Ethernet1/800
        bfd: enable
      - name: Ethernet1/801
        bfd: enable
    state: rendered

# Task Output (redacted)
# -----------------------

# rendered:
#   - "interface Ethernet1/800"
#   - "hsrp bfd"
#   - "interface Ethernet1/801"
#   - "hsrp bfd"

# Using parsed

# parsed.cfg
# ------------
# interface Ethernet1/800
#   no switchport
#   hsrp bfd
# interface Ethernet1/801
#   no switchport
#   hsrp bfd

- name: Use parsed state to convert externally supplied config to structured format
  cisco.nxos.nxos_hsrp_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output (redacted)
# -----------------------

# parsed:
#   - name: Ethernet1/800
#     bfd: enable
#   - name: Ethernet1/801
#     bfd: enable

# Using gathered

# Existing device config state
# -------------------------------

# interface Ethernet1/1
#   no switchport
#   hsrp bfd
# interface Ethernet1/2
#   no switchport
#   hsrp bfd
# interface Ethernet1/3
#   no switchport

- name: Gather hsrp_interfaces facts from the device using nxos_hsrp_interfaces
  cisco.nxos.nxos_hsrp_interfaces:
    state: gathered

# Task output (redacted)
# -----------------------

# gathered:
#   - name: Ethernet1/1
#     bfd: enable
#   - name: Ethernet1/2
#     bfd: enable
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.hsrp_interfaces.hsrp_interfaces import (
    Hsrp_interfaces,
)


# import debugpy

# debugpy.listen(5003)
# debugpy.wait_for_client()


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Hsrp_interfacesArgs.argument_spec,
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

    result = Hsrp_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
