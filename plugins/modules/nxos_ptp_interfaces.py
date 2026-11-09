#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_ptp_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_ptp_interfaces
version_added: 14.0.0
short_description: PTP interfaces resource module.
description:
  - This module manages the Precision Time Protocol (PTP) configuration of the interfaces of Cisco NX-OS devices.
  - The global PTP settings are managed by M(cisco.nxos.nxos_ptp_global).
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - The PTP commands only exist when C(feature ptp) is enabled, use M(cisco.nxos.nxos_feature) for it.
  - PTP can only be enabled on an interface when a PTP source address is configured, see M(cisco.nxos.nxos_ptp_global).
    Every other PTP setting of an interface needs PTP to be enabled on the interface first, so I(enabled) must be C(true)
    for an interface with other settings, unless I(state) is C(merged) and the interface already has PTP.
  - C(no ptp) removes all the PTP settings of an interface, I(enabled=false) and the states I(deleted), I(replaced)
    and I(overridden) use it for an interface that is not configured with I(enabled=true).
  - NX-OS does not display a setting that has its default value in the running configuration. The default values are
    I(role) C(dynamic), I(transport) C(ipv4), I(transmission) C(multicast), I(announce_interval) C(1),
    I(announce_timeout) C(3), I(sync_interval) C(-2) and I(delay_request_interval) C(0), without a profile.
    The values with a profile are always displayed, also when they are equal to the default of the plain form.
    A setting that is given with its default value is removed from the device, and the facts only return
    the settings that the device displays.
  - NX-OS only removes a setting with a value when the C(no) command carries a value, the module sends the
    value that is configured on the device.
  - The values with the C(aes67) and C(smpte_2059_2) profiles of the interval settings cannot be mixed on one
    interface. When another profile is configured, the module removes the old line before it sets the new one.
  - The C(ptp cost) command, the C(ptp ipv6 multicast scope) command and the C(negotiation-schema) of the C(ptp transmission),
    C(ptp master) and C(ptp slave) commands of an interface are not managed by this module. N9K-C93180YC-FX with NX-OS 10.6(4)
    does not support C(ptp cost), and a negotiation schema cannot be created with the CLI there.
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does not connect to the device.
author:
  - Jorgen Spange (@jorgenspange)
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | include "^interface|^  ptp").
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of PTP interface configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description: The name of the interface, for example C(Ethernet1/1). Interface names are normalised.
        type: str
        required: true
      enabled:
        description: Enables PTP on the interface (C(ptp)). C(false) removes all PTP settings of the interface (C(no ptp)).
        type: bool
      role:
        description: The PTP role of the port (C(ptp role)). Defaults to C(dynamic). C(slave) needs the unicast transmission.
        type: str
        choices:
          - dynamic
          - master
          - slave
      transmission:
        description: The transmission mode of the port (C(ptp transmission)). Defaults to C(multicast).
        type: str
        choices:
          - unicast
          - multicast
      transport:
        description: The transport of the PTP messages (C(ptp transport)). Defaults to C(ipv4). C(ipv6) needs a global IPv6 PTP source.
        type: str
        choices:
          - ipv4
          - ipv6
      vlan:
        description: The VLAN of the PTP messages (C(ptp vlan)), in the range 1-4094. The reserved VLANs are rejected by the device.
        type: int
      announce_interval:
        description: The announce interval, the logarithm of the number of seconds (C(ptp announce interval)).
        type: dict
        suboptions:
          value:
            description:
              - The value. The range is 0-4 without a profile, 0-4 with C(aes67) and -3 to 1 with C(smpte_2059_2). Defaults to C(1) without a profile.
            type: int
            required: true
          profile:
            description: The profile of the value.
            type: str
            choices:
              - aes67
              - smpte_2059_2
      announce_timeout:
        description: The number of announce intervals before a timeout (C(ptp announce timeout)).
        type: dict
        suboptions:
          value:
            description:
              - The value. The range is 2-4 without a profile and 2-10 with the profiles. Defaults to C(3) without a profile.
            type: int
            required: true
          profile:
            description: The profile of the value.
            type: str
            choices:
              - aes67
              - smpte_2059_2
      sync_interval:
        description: The sync interval, the logarithm of the number of seconds (C(ptp sync interval)).
        type: dict
        suboptions:
          value:
            description:
              - The value. The range is -3 to 1 without a profile, -4 to 1 with C(aes67) and -7 to 0 with C(smpte_2059_2).
                Defaults to C(-2) without a profile.
            type: int
            required: true
          profile:
            description: The profile of the value.
            type: str
            choices:
              - aes67
              - smpte_2059_2
      delay_request_interval:
        description: The minimum delay request interval, the logarithm of the number of seconds (C(ptp delay-request minimum interval)).
        type: dict
        suboptions:
          value:
            description:
              - The value. The range is -1 to 6 without a profile and -4 to 5 with the profiles. Defaults to C(0) without a profile.
            type: int
            required: true
          profile:
            description: The profile of the value.
            type: str
            choices:
              - aes67
              - smpte_2059_2
      asymmetric_delay:
        description:
          - The asymmetric delay of the path in nanoseconds (C(ptp asymmetric-delay)).
          - The device keeps one value, the direction and the value, the last one that is configured wins.
            Only one of I(forward_path) and I(reverse_path) can be given.
        type: dict
        suboptions:
          forward_path:
            description: The delay of the forward path, in the range 1-512000000.
            type: int
          reverse_path:
            description: The delay of the reverse path, in the range 1-512000000.
            type: int
      master:
        description: The unicast master addresses (C(ptp master)), IPv4 or IPv6. Several can be configured on an interface.
        type: list
        elements: str
      slave:
        description: The unicast slave addresses (C(ptp slave)), IPv4 or IPv6. Several can be configured on an interface.
        type: list
        elements: str
      peer:
        description: The unicast peer address (C(ptp peer)), IPv4 or IPv6. The device accepts one peer on an interface.
        type: str
      ucast_source:
        description: The unicast source addresses (C(ptp ucast-source)). The device accepts one for each address family.
        type: dict
        suboptions:
          ipv4:
            description: The IPv4 address.
            type: str
          ipv6:
            description: The IPv6 address.
            type: str
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) what is given is added to the interfaces and nothing is removed, except the settings that are
        given with their default value, which are removed.
      - With I(replaced) the PTP settings of the listed interfaces are made identical to the given ones, the other
        interfaces are not touched.
      - With I(overridden) the same applies and the PTP settings of the interfaces that are not listed are removed.
      - With I(deleted) the PTP settings of the listed interfaces are removed (C(no ptp)), without I(config) those of all the
        interfaces. C(feature ptp) is not touched.
      - With I(gathered) the configuration is read from the device.
      - With I(rendered) the commands for I(config) are returned without connecting to the device.
      - With I(parsed) I(running_config) is returned as structured data.
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
# nxos# show running-config | include "^interface|^  ptp"
# interface Ethernet1/1
# interface Ethernet1/2

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_ptp_interfaces:
    config:
      - name: Ethernet1/1
        enabled: true
        vlan: 100
        announce_interval:
          value: 3
          profile: aes67
        sync_interval:
          value: -2
          profile: aes67
        delay_request_interval:
          value: -2
          profile: aes67
      - name: Ethernet1/2
        enabled: true
        role: master
        transmission: unicast
    state: merged

# Task output:
# ------------
# before: []
# commands:
#   - interface Ethernet1/1
#   - ptp
#   - ptp vlan 100
#   - ptp delay-request minimum interval aes67 -2
#   - ptp announce interval aes67 3
#   - ptp sync interval aes67 -2
#   - interface Ethernet1/2
#   - ptp
#   - ptp role master
#   - ptp transmission unicast
# after:
#   - name: Ethernet1/1
#     enabled: true
#     vlan: 100
#     announce_interval:
#       value: 3
#       profile: aes67
#     sync_interval:
#       value: -2
#       profile: aes67
#     delay_request_interval:
#       value: -2
#       profile: aes67
#   - name: Ethernet1/2
#     enabled: true
#     role: master
#     transmission: unicast

# After state:
# ------------
# nxos# show running-config | include "^interface|^  ptp"
# interface Ethernet1/1
#   ptp
#   ptp delay-request minimum interval aes67 -2
#   ptp announce interval aes67 3
#   ptp vlan 100
#   ptp sync interval aes67 -2
# interface Ethernet1/2
#   ptp
#   ptp role master
#   ptp transmission unicast

# Using replaced

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  ptp"
# interface Ethernet1/1
#   ptp
#   ptp vlan 100
#   ptp sync interval aes67 -2
# interface Ethernet1/2
#   ptp
#   ptp role master

- name: Replace the PTP configuration of Ethernet1/1
  cisco.nxos.nxos_ptp_interfaces:
    config:
      - name: Ethernet1/1
        enabled: true
        vlan: 200
    state: replaced

# Task output:
# ------------
# commands:
#   - interface Ethernet1/1
#   - ptp vlan 200
#   - no ptp sync interval aes67 -2

# Using overridden

- name: Override the PTP configuration of all the interfaces
  cisco.nxos.nxos_ptp_interfaces:
    config:
      - name: Ethernet1/1
        enabled: true
        vlan: 200
    state: overridden

# Task output:
# ------------
# commands:
#   - interface Ethernet1/2
#   - no ptp

# Using deleted

- name: Remove the PTP configuration of Ethernet1/1
  cisco.nxos.nxos_ptp_interfaces:
    config:
      - name: Ethernet1/1
    state: deleted

# Task output:
# ------------
# commands:
#   - interface Ethernet1/1
#   - no ptp

# Using gathered

# Before state:
# -------------
# nxos# show running-config | include "^interface|^  ptp"
# interface Ethernet1/1
#   ptp
#   ptp vlan 200
# interface Ethernet1/2

- name: Gather the PTP configuration of the interfaces
  cisco.nxos.nxos_ptp_interfaces:
    state: gathered

# Task output:
# ------------
# gathered:
#   - name: Ethernet1/1
#     enabled: true
#     vlan: 200

# Using rendered

- name: Render the commands for the provided configuration
  cisco.nxos.nxos_ptp_interfaces:
    config:
      - name: Eth1/3
        enabled: true
        master:
          - 192.0.2.10
        asymmetric_delay:
          forward_path: 100
    state: rendered

# Task output:
# ------------
# rendered:
#   - interface Ethernet1/3
#   - ptp
#   - ptp asymmetric-delay forward-path 100
#   - ptp master 192.0.2.10

# Using parsed

# parsed.cfg
# ----------
# interface Ethernet1/1
#   ptp
#   ptp vlan 200
# interface Ethernet1/2

- name: Parse the provided configuration
  cisco.nxos.nxos_ptp_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   - name: Ethernet1/1
#     enabled: true
#     vlan: 200
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
    - ptp
    - ptp vlan 100
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface Ethernet1/1
    - ptp
    - ptp vlan 100
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ptp_interfaces.ptp_interfaces import (
    Ptp_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.ptp_interfaces.ptp_interfaces import (
    Ptp_interfaces,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Ptp_interfacesArgs.argument_spec,
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

    result = Ptp_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
