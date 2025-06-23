#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_l3_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_l3_interfaces
short_description: L3 interfaces resource module
description: This module manages Layer-3 interfaces attributes of NX-OS Interfaces.
version_added: 1.0.0
author:
  - Trishna Guha (@trishnaguha)
  - Nikhil Bhasin (@nickbhasin)
notes:
- Tested against NXOS 7.3.(0)D1(1) on VIRL
- Unsupported for Cisco MDS
options:
  config:
    description: A dictionary of Layer-3 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of L3 interface, i.e. Ethernet1/1.
        type: str
        required: true
      mac_address:
        description: >-
          Manually set interface MAC address or extract the MAC address (3) from the
          IPv6 address configured on the interface.
        type: str
      bandwidth:
        description: Manually set the bandwidth
        type: dict
        suboptions:
          kilobits:
            description: Bandwidth in kilobits
            type: int
          inherit:
            description: Specify that bandwidth is inherited
            type: bool
      ipv4:
        description: IPv4 address and attributes of the L3 interface.
        type: dict
        suboptions:
          address:
            description: IPV4 address of the L3 interface.
            type: list
            elements: dict
            suboptions:
              dhcp:
                description: Configure IP address from a dhcp server
                type: bool
              ip_address:
                description: IP address in format i.i.i.i or IP prefix and network mask length in format x.x.x.x/m
                type: str
              ip_network_mask:
                description: IP network mask in format m.m.m.m
                type: str
              route_preference:
                description: URIB route preference for local/direct routes
                type: int
              tag:
                description: URIB route tag value for local/direct routes
                type: int
              secondary:
                description: Configure additional IP addresses on interface
                type: bool
          redirects:
            description: Send ICMP Redirect messages.
            type: bool
          unreachables:
            description: Enable sending ICMP unreachables (other than port-unreachable).
            type: bool
          proxy_arp:
            description: Configure proxy ARP.
            type: bool
          port_unreachable:
            description: Enable sending ICMP port-unreachable.
            type: bool
          verify:
            description: Configure Unicast Reverse Path Forwarding or IP Source Guard.
            type: dict
            suboptions:
              unicast:
                description: Unicast Reverse Path Forwarding.
                type: dict
                suboptions:
                  source:
                    description: Validation of source address.
                    type: dict
                    suboptions:
                      reachable_via:
                        description: Specify reachability check to apply to the source address.
                        type: dict
                        suboptions:
                          mode:
                            description: Source is reachable via any/rx interface.
                            type: str
                          allow_default:
                            description: Loose Default Route Unicast Reverse Path Forwarding.
                            type: bool
          dhcp:
            description: Configure DHCP snooping or relay
            type: dict
            suboptions:
              option82:
                description: DHCP option82.
                type: dict
                suboptions:
                  suboption:
                    description: DHCP option82.
                    type: dict
                    suboptions:
                      circuit_id:
                        description: DHCP option82 suboption circuit-id string configuration.
                        type: str
              smart_relay:
                description: Configure DHCP smart relay on interface.
                type: bool
              relay:
                description: Configure relay agent.
                type: dict
                suboptions:
                  information:
                    description: Relay agent information option.
                    type: dict
                    suboptions:
                      trusted:
                        description: Enable relay trust on this interface.
                        type: bool
                  subnet_selection:
                    description: Configure gateway address for DHCP relay
                    type: dict
                    suboptions:
                      subnet_ip:
                        description: IP address
                        type: str
                  source_interface:
                    description: Configure gateway address for DHCP relay
                    type: dict
                    suboptions:
                      interface_type:
                        description: Type of interface
                        type: str
                      interface_id:
                        description: Interface ID
                        type: str
                  address:
                    description: Configure DHCP server to refer to
                    type: list
                    elements: dict
                    suboptions:
                      relay_ip:
                        description: IP address
                        type: str
                      vrf_name:
                        description: Helper address VRF membership
                        type: str
      ipv6:
        description: IPv6 address and attributes of the L3 interface.
        type: dict
        suboptions:
          address:
            description: IPV6 address of the L3 interface.
            type: list
            elements: dict
            suboptions:
              dhcp:
                description: Configure IPv6 address from a dhcp server
                type: bool
              autoconfig:
                description: Configure IPv6 Stateless address autoconfig
                type: bool
              use_link_local_only:
                description: Enable IPv6 on interface using only a single link-local address
                type: bool
              ipv6_address:
                description: IPv6 prefix format - xxxx:xxxx/ml, xxxx:xxxx::/ml, xxxx::xx/128
                type: str
              default:
                description: For SLAAC, adds default route and the nh would be fetched from RA source address
                type: bool
              aggregate_prefix_length:
                description: Prefix-Length for AM Route Aggregation
                type: int
              anycast:
                description: Configure IPv6 anycast address on interface
                type: bool
              eui64:
                description: Configure Extended Unique Identifier for the low-order 64 bits
                type: bool
              route_preference:
                description: URIB route preference for local/direct routes
                type: int
              tag:
                description: URIB route tag value for local/direct routes
                type: int
              use_bia:
                description: Use BIA
                type: bool
          redirects:
            description: Send ICMP Redirect messages.
            type: bool
          unreachables:
            description: Enable sending ICMP unreachables (other than port-unreachable).
            type: bool
          verify:
            description: Unicast Reverse Path Forwarding.
            type: dict
            suboptions:
              unicast:
                description: Unicast Reverse Path Forwarding.
                type: dict
                suboptions:
                  source:
                    description: Validation of source address.
                    type: dict
                    suboptions:
                      reachable_via:
                        description: Specify reachability check to apply to the source address.
                        type: dict
                        suboptions:
                          mode:
                            description: Source is reachable via any/rx interface.
                            type: str
                          allow_default:
                            description: Loose Default Route Unicast Reverse Path Forwarding.
                            type: bool
          dhcp:
            description: Configure DHCP snooping or relay
            type: dict
            suboptions:
              smart_relay:
                description: Configure DHCP smart relay on interface.
                type: bool
              relay:
                description: Configure relay agent.
                type: dict
                suboptions:
                  source_interface:
                    description: Configure source interface for DHCPv6 relay.
                    type: dict
                    suboptions:
                      interface_type:
                        description: Type of interface
                        type: str
                      interface_id:
                        description: Interface ID
                        type: str
                  address:
                    description: Configure DHCPv6 server relay address
                    type: list
                    elements: dict
                    suboptions:
                      relay_ip:
                        description: IP address
                        type: str
                      vrf_name:
                        description: Helper address VRF membership
                        type: str
                      interface_type:
                        description: Type of interface
                        type: str
                      interface_id:
                        description: Interface ID
                        type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - >-
        The value of this option should be the output received from the IOS
        device by executing the command B(show running-config | section
        ^interface).
      - >-
        The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
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
      - >-
        The states I(rendered), I(gathered) and I(parsed) does not perform any
        change on the device.
      - >-
        The state I(rendered) will transform the configuration in C(config)
        option to platform specific CLI commands which will be returned in the
        I(rendered) key within the result. For state I(rendered) active
        connection to remote host is not required.
      - >-
        The state I(gathered) will fetch the running configuration from device
        and transform it into structured data in the format as per the resource
        module argspec and the value is returned in the I(gathered) key within
        the result.
      - >-
        The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into JSON format as per the resource module
        parameters and the value is returned in the I(parsed) key within the
        result. The value of C(running_config) option should be the same format
        as the output of command I(show running-config | section ^interface)
        executed on device. For state I(parsed) active connection to remote host
        is not required.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Merge provided configuration with device configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
      - name: Ethernet1/6
        ipv4:
          - address: 192.168.1.1/24
            tag: 5
          - address: 10.1.1.1/24
            secondary: true
            tag: 10
        ipv6:
          - address: fd5d:12c9:2201:2::1/64
            tag: 6
      - name: Ethernet1/7.42
        redirects: false
        unreachables: false
    state: merged

# Task Output
# -----------
#
# before:
# - name: Ethernet1/6
# - name: Ethernet1/7
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - ip address 192.168.1.1/24 tag 5
# - ip address 10.1.1.1/24 secondary tag 10
# - ipv6 address fd5d:12c9:2201:2::1/64 tag 6
# - interface Ethernet1/7
# - no ip redirects
# after:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management


# Using replaced

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Replace device configuration of specified L3 interfaces with provided configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
      - name: Ethernet1/6
        ipv4:
          - address: 192.168.22.3/24
    state: replaced

# Task Output
# -----------
#
# before:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - ip address 192.168.22.3/24
# - no ipv6 address fd5d:12c9:2201:2::1/64
# - ip redirects
# after:
# - ipv4:
#   - address: 192.168.22.3/24
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.22.3/24
#   ip address 10.1.1.1/24 secondary tag 10
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using overridden

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no ip redirects
#   ip address 192.168.1.1/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no ip redirects
#   no shutdown
# interface Ethernet1/7.42
#   no ip redirects
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Override device configuration with provided configuration.
  cisco.nxos.nxos_l3_interfaces:
    config:
      - ipv4:
          - address: dhcp
        name: mgmt0
      - name: Ethernet1/6
        ipv4:
          - address: 192.168.22.3/24
    state: overridden

# Task Output
# -----------
#
# before:
# - ipv4:
#   - address: 192.168.1.1/24
#     tag: 5
#   - address: 10.1.1.1/24
#     secondary: true
#     tag: 10
#   ipv6:
#   - address: fd5d:12c9:2201:2::1/64
#     tag: 6
#   name: Ethernet1/6
#   redirects: false
# - name: Ethernet1/7
#   redirects: false
# - name: Ethernet1/7.42
#   redirects: false
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - no ipv6 address fd5d:12c9:2201:2::1/64
# - no ip address 10.1.1.1/24 secondary
# - ip address 192.168.22.3/24
# - ip redirects
# - interface Ethernet1/7
# - ip redirects
# - interface Ethernet1/7.42
# - ip redirects
# after:
# - ipv4:
#   - address: 192.168.22.3/24
#   name: Ethernet1/6
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   ip address 192.168.22.3/24
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using deleted

# Before state:
# -------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   ip address 192.168.22.3/24
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

- name: Delete L3 attributes of given interfaces (This won't delete the interface
    itself).
  cisco.nxos.nxos_l3_interfaces:
    config:
      - name: Ethernet1/6
      - name: Ethernet1/2
    state: deleted

# Task Output
# -----------
#
# before:
# - name: Ethernet1/2
# - ipv4:
#   - address: 192.168.22.3/24
#   name: Ethernet1/6
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0
# commands:
# - interface Ethernet1/6
# - no ip address
# after:
# - name: Ethernet1/2
# - name: Ethernet1/7
# - name: Ethernet1/7.42
# - ipv4:
#   - address: dhcp
#   name: mgmt0

# After state:
# ------------
#
# router# show running-config | section interface
# interface Ethernet1/6
#   description Configured by Ansible Network
#   no switchport
#   no shutdown
# interface Ethernet1/7
#   description Configured by Ansible
#   no switchport
#   no shutdown
# interface Ethernet1/7.42
# interface mgmt0
#   description mgmt interface
#   ip address dhcp
#   vrf member management

# Using rendered

- name: Use rendered state to convert task input to device specific commands
  cisco.nxos.nxos_l3_interfaces:
    config:
      - name: Ethernet1/800
        ipv4:
          - address: 192.168.1.100/24
            tag: 5
          - address: 10.1.1.1/24
            secondary: true
            tag: 10
      - name: Ethernet1/800
        ipv6:
          - address: fd5d:12c9:2201:2::1/64
            tag: 6
    state: rendered

# Task Output
# -----------
#
# rendered:
#   - interface Ethernet1/800
#   - ip address 192.168.1.100/24 tag 5
#   - ip address 10.1.1.1/24 secondary tag 10
#   - interface Ethernet1/800
#   - ipv6 address fd5d:12c9:2201:2::1/64 tag 6

# Using parsed

# parsed.cfg
# ----------
#
# interface Ethernet1/800
#   ip address 192.168.1.100/24 tag 5
#   ip address 10.1.1.1/24 secondary tag 10
#   no ip redirects
# interface Ethernet1/801
#   ipv6 address fd5d:12c9:2201:2::1/64 tag 6
#   ip unreachables
# interface mgmt0
#   ip address dhcp
#   vrf member management

- name: Use parsed state to convert externally supplied config to structured format
  cisco.nxos.nxos_l3_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output
# -----------
#
# parsed:
#   - name: Ethernet1/800
#     ipv4:
#       - address: 192.168.1.100/24
#         tag: 5
#       - address: 10.1.1.1/24
#         secondary: True
#         tag: 10
#     redirects: False
#   - name: Ethernet1/801
#     ipv6:
#      - address: fd5d:12c9:2201:2::1/64
#        tag: 6
#     unreachables: True

# Using gathered

# Before state:
# -------------
#
# interface Ethernet1/1
#   ip address 192.0.2.100/24
# interface Ethernet1/2
#   no ip redirects
#   ip address 203.0.113.10/24
#   ip unreachables
#   ipv6 address 2001:db8::1/32

- name: Gather l3_interfaces facts from the device using nxos_l3_interfaces
  cisco.nxos.nxos_l3_interfaces:
    state: gathered

# Task output
# -----------
#
# gathered:
#   - name: Ethernet1/1
#     ipv4:
#       - address: 192.0.2.100/24
#   - name: Ethernet1/2
#     ipv4:
#       - address: 203.0.113.10/24
#     ipv6:
#       - address: 2001:db8::1/32
#     redirects: False
#     unreachables: True
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.l3_interfaces.l3_interfaces import (
    L3_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.l3_interfaces.l3_interfaces import (
    L3_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L3_interfacesArgs.argument_spec,
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

    result = L3_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
