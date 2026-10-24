#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_l2_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_l2_interfaces
short_description: L2 interfaces resource module
description: This module manages Layer-2 interfaces attributes of NX-OS Interfaces.
version_added: 1.0.0
author:
  - Trishna Guha (@trishnaguha)
  - Vinay Mulugund (@roverflow)
notes:
- Tested against NXOS 10.3(2) on CML
- Unsupported for Cisco MDS
- Tested against NX-OS 10.6(4) on N9K-C93180YC-FX for C(spanning_tree) C(port_type) (C(edge) and C(edge_trunk)),
  C(bpduguard) (C(true)), C(guard) (C(root)), C(cost), C(port_priority), C(link_type) (C(point_to_point))
  and C(storm_control) C(level) of C(broadcast), C(multicast) and C(unicast).
- The other C(spanning_tree) and C(storm_control) values are generated from the documented NX-OS
  command syntax but were not verified on a device.
- Only explicit interface lines are managed. Global settings such as C(spanning-tree port type edge default),
  C(spanning-tree bpduguard default) and C(spanning-tree loopguard default) change the effective behaviour
  of a port but are not interface configuration and are neither read nor changed by this module.
- Values that the device accepts but never displays (C(spanning-tree link-type auto), C(spanning-tree port-priority 128),
  C(storm-control <type> level 100.00)) are treated like unset values, listing them removes a different configured value.
  Values that are displayed (C(port_type) C(normal), C(bpduguard) C(false), C(bpdufilter) C(false), C(guard) C(none))
  are managed as explicit lines.
- C(spanning_tree) and C(storm_control) apply to switchports and port-channels. The interface commands do not exist
  on a routed port. When one of the options is used with I(state=merged), I(state=replaced) or I(state=overridden)
  the module fails before sending any command unless the interface is a confirmed switchport, that is it has a
  C(switchport) line or no C(no switchport) line while C(system default switchport) is configured. To know the default
  the module runs C(show running-config all | incl 'system default switchport') once. Routed ports are not reported
  in the facts.
- Interface level C(storm-control <type> level pps <n>) is not supported by this module because N9K-C93180YC-FX
  NX-OS 10.6(4) accepts it without storing it.
- I(state=overridden) removes the C(spanning_tree) and C(storm_control) settings of every interface that is not listed.
- I(state=replaced) and I(state=overridden) send C(no cdp enable) unless C(cdp_enable=true) is listed for the interface
  (existing behaviour).
- Configure C(spanning_tree) and C(storm_control) on the port-channel, not on its member ports.
- On a vPC port-channel the C(spanning_tree) settings must be identical on both vPC peers. A mismatch makes the vPC
  type-1 inconsistent until the settings are aligned.
- C(storm-control multi) commands are not supported.
options:
  config:
    description: A List of Layer-2 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, i.e. Ethernet1/1.
        type: str
        required: true
      access:
        description:
        - Switchport mode access command to configure the interface as a Layer-2 access.
        type: dict
        suboptions:
          vlan:
            description:
            - Configure given VLAN in access port. It's used as the access VLAN ID.
            type: int
      trunk:
        description:
        - Switchport mode trunk command to configure the interface as a Layer-2 trunk.
        type: dict
        suboptions:
          native_vlan:
            description:
            - Native VLAN to be configured in trunk port. It is used as the trunk
              native VLAN ID.
            type: int
          allowed_vlans:
            description:
            - List of allowed VLANs in a given trunk port. These are the only VLANs
              that will be configured on the trunk.
            - The module would consider 1-4093 as the default range enabled if switchport
              mode is trunk.
            type: str
          allowed_vlans_none:
            description:
            - This option governs the `switchport trunk allowed vlan none` configuration
            - negation of this command would consider 1-4093 as the default.
            - This attribute does not ensure idempotency.
            type: bool
          allowed_vlans_implicit:
            description:
            - Read-only flag set by the module in gathered/parsed facts when a trunk
              interface has no explicit C(switchport trunk allowed vlan) line and the
              module synthesizes the default C(1-4094) range.
            - When this flag is present in the current device state and C(state=merged)
              is used, the module generates a SET command instead of ADD, allowing users
              to restrict default trunks to specific VLANs without switching to
              C(state=replaced).
            - This option should not be set in playbook config; it is informational only.
            type: bool
      mode:
        description:
        - Mode in which interface needs to be configured.
        - Access mode is not shown in interface facts, so idempotency will not be
          maintained for switchport mode access and every time the output will come
          as changed=True.
        type: str
        choices:
        - dot1q-tunnel
        - access
        - trunk
        - fex-fabric
        - fabricpath
        aliases:
          - switchport_mode
      cdp_enable:
        type: bool
        description:
        - Enable/disable CDP on the interface.
        - For port-channel member interfaces, configure CDP on the
          port-channel interface as Ansible does not support configuring
          CDP directly on port-channel member interfaces.
      link_flap:
        type: dict
        description: Configure actions on link-flap
        suboptions:
          error_disable:
            type: dict
            description: Configure the port to error-disable on link-flap
            suboptions:
              count:
                type: int
                description: Configure the number of link-flaps to trigger the action
              interval:
                type: int
                description: Configure the interval to trigger the action
      beacon:
        type: bool
        description: Disable/enable the beacon for an interface
      spanning_tree:
        description:
        - Spanning-tree settings of the interface.
        - Only the explicit interface lines are managed, values left out are removed with
          I(state=replaced), I(state=overridden) and I(state=deleted).
        type: dict
        version_added: 13.1.0
        suboptions:
          port_type:
            description:
            - Spanning-tree port type, C(spanning-tree port type edge|edge trunk|network|normal).
            type: str
            choices:
            - edge
            - edge_trunk
            - network
            - normal
          bpduguard:
            description:
            - BPDU guard of the interface, C(spanning-tree bpduguard enable|disable).
            - C(true) configures C(enable), C(false) configures C(disable). When not set no line is configured
              and the global default applies.
            type: bool
          bpdufilter:
            description:
            - BPDU filter of the interface, C(spanning-tree bpdufilter enable|disable).
            - C(true) configures C(enable), C(false) configures C(disable). When not set no line is configured
              and the global default applies.
            type: bool
          guard:
            description:
            - Spanning-tree guard, C(spanning-tree guard loop|root|none).
            type: str
            choices:
            - loop
            - root
            - none
          cost:
            description:
            - Spanning-tree path cost, C(spanning-tree cost <n>).
            - The range is enforced by the device. C(spanning-tree cost auto) is the default and is not managed.
            type: int
          port_priority:
            description:
            - Spanning-tree port priority, C(spanning-tree port-priority <n>).
            - Must be a multiple of 32 from 0 to 224, other values are rejected before any command is sent.
            - C(128) is the default, the device does not display it. It is treated like an unset priority.
            type: int
          link_type:
            description:
            - Spanning-tree link type, C(spanning-tree link-type auto|point-to-point|shared).
            - C(auto) is the default, the device does not display it. It is treated like an unset link type.
            type: str
            choices:
            - auto
            - point_to_point
            - shared
          mst:
            description:
            - Per MST instance cost and port priority, C(spanning-tree mst <instances> cost|port-priority <n>).
            type: list
            elements: dict
            suboptions:
              instances:
                description:
                - MST instance or list of instances, for example C(0,2-4).
                type: str
                required: true
              cost:
                description: Path cost for the instances, at least 1 (the device rejects 0).
                type: int
              port_priority:
                description: Port priority for the instances, a multiple of 32 from 0 to 224.
                type: int
          vlans:
            description:
            - Per VLAN cost and port priority, C(spanning-tree vlan <vlans> cost|port-priority <n>).
            type: list
            elements: dict
            suboptions:
              vlans:
                description:
                - VLAN or list of VLANs, for example C(1,3-5).
                type: str
                required: true
              cost:
                description: Path cost for the VLANs.
                type: int
              port_priority:
                description: Port priority for the VLANs, a multiple of 32 from 0 to 224.
                type: int
      storm_control:
        description:
        - Storm-control settings of the interface.
        - Only the explicit interface lines are managed, values left out are removed with
          I(state=replaced), I(state=overridden) and I(state=deleted).
        type: dict
        version_added: 13.1.0
        suboptions:
          broadcast:
            description: Broadcast storm-control, C(storm-control broadcast level <level>).
            type: dict
            suboptions:
              level:
                description:
                - Suppression level in percent as a decimal string such as C(0.01) or C(1.00).
                - Compared as a number, C(1.0) and C(1.00) are the same level.
                - C(100.00) is the default, the device does not display it. It is treated like an unset level.
                type: str
          multicast:
            description: Multicast storm-control, C(storm-control multicast level <level>).
            type: dict
            suboptions:
              level:
                description:
                - Suppression level in percent as a decimal string such as C(0.01) or C(1.00).
                - Compared as a number, C(1.0) and C(1.00) are the same level.
                - C(100.00) is the default, the device does not display it. It is treated like an unset level.
                type: str
          unicast:
            description: Unicast storm-control, C(storm-control unicast level <level>).
            type: dict
            suboptions:
              level:
                description:
                - Suppression level in percent as a decimal string such as C(0.01) or C(1.00).
                - Compared as a number, C(1.0) and C(1.00) are the same level.
                - C(100.00) is the default, the device does not display it. It is treated like an unset level.
                type: str
          action:
            description: Action taken when a storm is detected, C(storm-control action shutdown|trap).
            type: str
            choices:
            - shutdown
            - trap
  state:
    description:
    - The state of the configuration after module completion.
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
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section ^interface).
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
# interface Ethernet1/2
#   switchport trunk native vlan 20
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

- name: Merge provided configuration with device configuration
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
        trunk:
          native_vlan: 10
          allowed_vlans: 2,4,15
      - name: Ethernet1/2
        access:
          vlan: 30
    state: merged

# Task Output
# -----------
#
# before:
# - name: Loopback999
# - name: Ethernet1/2
# - name: mgmt0
# - name: Ethernet1/1
# commands:
# - interface Ethernet1/1
# - switchport trunk allowed vlan 2,4,15
# - switchport trunk native vlan 10
# - interface Ethernet1/2
# - switchport access vlan 30
# after:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: 2,4,15
#     native_vlan: 10
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0
# - name: Loopback999

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport trunk native vlan 10
#   switchport trunk allowed vlans 2,4,15
# interface Ethernet1/2
#   switchport access vlan 30
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

# Using merged to restrict default trunk VLANs

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/4
#   switchport mode trunk
#   switchport trunk native vlan 99
#
# Note: No explicit "switchport trunk allowed vlan" line means the
# interface allows all VLANs (1-4094) by default. The module detects
# this as implicit and sets allowed_vlans_implicit: true in facts.

- name: Restrict default trunk to specific VLANs using merged state
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/4
        trunk:
          allowed_vlans: "100,200"
    state: merged

# Task Output
# -----------
#
# before:
# - name: Ethernet1/4
#   mode: trunk
#   trunk:
#     allowed_vlans: "1-4094"
#     allowed_vlans_implicit: true
#     native_vlan: 99
# commands:
# - interface Ethernet1/4
# - switchport trunk allowed vlan 100,200
# after:
# - name: Ethernet1/4
#   mode: trunk
#   trunk:
#     allowed_vlans: "100,200"
#     native_vlan: 99

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/4
#   switchport mode trunk
#   switchport trunk native vlan 99
#   switchport trunk allowed vlan 100,200
#
# Note: Because the have VLANs were implicit (default), merged used a
# SET command to restrict the trunk. If the trunk already had explicit
# VLANs, merged would use ADD to append only new VLANs.

# Using replaced

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport trunk native vlan 10
#   switchport trunk allowed vlans 2,4,15
# interface Ethernet1/2
#   switchport access vlan 30
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

- name: Replace device configuration of specified L2 interfaces with provided configuration.
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
        trunk:
          native_vlan: 20
          allowed_vlans: 5-10, 15
    state: replaced

# Task Output
# -----------
#
# before:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: 2,4,15
#     native_vlan: 10
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0
# commands:
# - interface Ethernet1/1
# - no switchport trunk native vlan
# - switchport trunk allowed vlan 5-10,15
# - switchport trunk native vlan 20
# after:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: 5-10,15
#     native_vlan: 20
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport trunk native vlan 20
#   switchport trunk allowed vlan 5-10,15
# interface Ethernet1/2
#   switchport trunk native vlan 20
#   switchport mode trunk
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

# Using overridden

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport trunk native vlan 20
#   switchport trunk allowed vlan 5-10,15
# interface Ethernet1/2
#   switchport trunk native vlan 20
#   switchport mode trunk
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

- name: Override device configuration with provided configuration.
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/2
        access:
          vlan: 30
    state: overridden

# Task Output
# -----------
#
# before:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: 5,6,7,8,9,10,15
#     native_vlan: 20
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0
# commands:
# - interface Ethernet1/1
# - no switchport trunk allowed vlan
# - no switchport trunk native vlan
# after:
# - name: Ethernet1/1
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
# interface Ethernet1/2
#   switchport access vlan 30
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config


# Using deleted

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport trunk native vlan 10
#   switchport trunk allowed vlan 2,4,15
# interface Ethernet1/2
#   switchport access vlan 30
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

- name: Delete L2 attributes of given interfaces (Note This won't delete the interface
    itself).
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
      - name: Ethernet1/2
    state: deleted

# Task Output
# -----------
#
# before:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: 2,4,15
#     native_vlan: 10
# - access:
#     vlan: 30
#   name: Ethernet1/2
# - name: mgmt0
# commands:
# - interface Ethernet1/1
# - no switchport trunk allowed vlan
# - no switchport trunk native vlan
# - interface Ethernet1/2
# - no switchport access vlan
# after:
# - name: Ethernet1/1
# - name: Ethernet1/2
# - name: mgmt0

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
# interface Ethernet1/2
# interface mgmt0
#   ip address dhcp
#   ipv6 address auto-config

# Using rendered

- name: Render platform specific configuration lines (without connecting to the device)
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
        trunk:
          native_vlan: 10
          allowed_vlans: 2,4,15
      - name: Ethernet1/2
        access:
          vlan: 30
      - name: Ethernet1/3
        trunk:
          native_vlan: 20
          allowed_vlans: 5-10, 15
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface Ethernet1/1
# - switchport trunk allowed vlan 2,4,15
# - switchport trunk native vlan 10
# - interface Ethernet1/2
# - switchport access vlan 30
# - interface Ethernet1/3
# - switchport trunk allowed vlan 5-10,15
# - switchport trunk native vlan 20

# Using parsed

# parsed.cfg
# ------------
#
# interface Ethernet1/800
#   switchport access vlan 18
#   switchport trunk allowed vlan 210
# interface Ethernet1/801
#   switchport trunk allowed vlan 2,4,15

- name: Use parsed state to convert externally supplied config to structured format
  cisco.nxos.nxos_l2_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output
# -----------
#
# parsed:
#  - name: Ethernet1/800
#    access:
#      vlan: 18
#    trunk:
#      allowed_vlans: "210"
#  - name: Ethernet1/801
#    trunk:
#      allowed_vlans: "2,4,15"

# Using gathered

# Before state:
# -------------
#
# switch# sh running-config | section ^interface
# interface Ethernet1/1
#   switchport access vlan 6
#   switchport trunk allowed vlan 200
# interface Ethernet1/2
#   switchport trunk native vlan 10

- name: Gather l2_interfaces facts from the device using nxos_l2_interfaces
  cisco.nxos.nxos_l2_interfaces:
    state: gathered

# Task output
# -----------
#
# gathered:
#  - name: "Ethernet1/1"
#    access:
#      vlan: 6
#    trunk:
#      allowed_vlans: "200"
#  - name: "Ethernet1/2"
#    trunk:
#      native_vlan: 10

# Using allowed_vlans_none

# Before state:
# -------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport mode trunk
#   switchport trunk allowed vlan 10-100
# interface Ethernet1/2
#   switchport mode trunk

- name: Configure trunk interface to allow no VLANs (block all traffic)
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
        trunk:
          allowed_vlans_none: true
    state: merged

# Task Output
# -----------
#
# before:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans: "10-100"
# - name: Ethernet1/2
#   trunk:
#     allowed_vlans: "1-4094"
# commands:
# - interface Ethernet1/1
# - switchport trunk allowed vlan none
# after:
# - name: Ethernet1/1
#   trunk:
#     allowed_vlans_none: true
# - name: Ethernet1/2
#   trunk:
#     allowed_vlans: "1-4094"

# After state:
# ------------
#
# switch# show running-config | section interface
# interface Ethernet1/1
#   switchport mode trunk
#   switchport trunk allowed vlan none
# interface Ethernet1/2
#   switchport mode trunk

# Note: When allowed_vlans_none is not configured on a trunk interface,
# the module assumes the default allowed VLANs range of 1-4094.
# This is consistent with NX-OS default behavior where all VLANs are
# allowed on trunk ports unless explicitly restricted.

- name: Configure specific VLANs after removing none restriction
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/1
        trunk:
          allowed_vlans: "10,20,30"
      - name: Ethernet1/2
        trunk:
          allowed_vlans_none: true
    state: replaced

# Task Output
# -----------
#
# commands:
# - interface Ethernet1/1
# - switchport trunk allowed vlan 10,20,30
# - interface Ethernet1/2
# - switchport trunk allowed vlan none

# Using merged with spanning_tree and storm_control

# Before state:
# -------------
#
# switch# show running-config | section ^interface
# interface Ethernet1/25
#   switchport
#   switchport mode trunk
#   spanning-tree guard root
# interface port-channel20
#   switchport

- name: Merge spanning-tree and storm-control settings
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/25
        spanning_tree:
          port_type: edge_trunk
          bpduguard: true
          cost: 100
        storm_control:
          broadcast:
            level: "0.01"
          multicast:
            level: "10.50"
          action: trap
      - name: port-channel20
        spanning_tree:
          port_type: network
          mst:
            - instances: "0,2-4"
              cost: 200
    state: merged

# Task Output
# -----------
#
# commands:
# - interface Ethernet1/25
# - spanning-tree port type edge trunk
# - spanning-tree bpduguard enable
# - spanning-tree cost 100
# - storm-control broadcast level 0.01
# - storm-control multicast level 10.50
# - storm-control action trap
# - interface port-channel20
# - spanning-tree port type network
# - spanning-tree mst 0,2-4 cost 200

# After state:
# ------------
#
# switch# show running-config | section ^interface
# interface Ethernet1/25
#   switchport
#   switchport mode trunk
#   spanning-tree cost 100
#   spanning-tree port type edge trunk
#   spanning-tree bpduguard enable
#   spanning-tree guard root
#   storm-control broadcast level 0.01
#   storm-control multicast level 10.50
#   storm-control action trap
# interface port-channel20
#   switchport
#   spanning-tree port type network
#   spanning-tree mst 0,2-4 cost 200

# Using replaced with spanning_tree and storm_control

# Before state:
# -------------
#
# interface Ethernet1/25
#   switchport
#   switchport mode trunk
#   spanning-tree cost 100
#   spanning-tree port type edge trunk
#   spanning-tree bpduguard enable
#   spanning-tree guard root
#   storm-control broadcast level 0.01

- name: Replace the settings of an interface, whatever is not listed is removed
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/25
        mode: trunk
        cdp_enable: true
        spanning_tree:
          port_type: edge_trunk
          bpduguard: false
        storm_control:
          broadcast:
            level: "1.0"
    state: replaced

# Task Output
# -----------
#
# commands:
# - interface Ethernet1/25
# - spanning-tree bpduguard disable
# - no spanning-tree guard
# - no spanning-tree cost
# - storm-control broadcast level 1.00

# After state:
# ------------
#
# interface Ethernet1/25
#   switchport
#   switchport mode trunk
#   spanning-tree port type edge trunk
#   spanning-tree bpduguard disable
#   storm-control broadcast level 1.00

# Using overridden with spanning_tree and storm_control

# Before state:
# -------------
#
# interface Ethernet1/25
#   switchport
#   spanning-tree port type edge
# interface Ethernet1/26
#   switchport
#   spanning-tree bpduguard enable
#   storm-control unicast level 5.00

- name: Override the layer-2 configuration of all interfaces
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/25
        cdp_enable: true
        spanning_tree:
          port_type: edge
    state: overridden

# Task Output
# -----------
#
# commands:
# - interface Ethernet1/26
# - no spanning-tree bpduguard
# - no storm-control unicast level 5.00

# After state:
# ------------
#
# interface Ethernet1/25
#   switchport
#   spanning-tree port type edge
# interface Ethernet1/26
#   switchport

# Using deleted with spanning_tree and storm_control

# Before state:
# -------------
#
# interface Ethernet1/25
#   switchport
#   spanning-tree port type edge trunk
#   spanning-tree vlan 1,3-5 cost 10
#   storm-control broadcast level 0.01
#   storm-control action shutdown

- name: Remove the layer-2 configuration of an interface
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/25
    state: deleted

# Task Output
# -----------
#
# commands:
# - interface Ethernet1/25
# - no spanning-tree port type edge trunk
# - no storm-control broadcast level 0.01
# - no storm-control action shutdown
# - no spanning-tree vlan 1,3-5 cost

# After state:
# ------------
#
# interface Ethernet1/25
#   switchport

# Using rendered with spanning_tree and storm_control

- name: Render the commands for spanning-tree and storm-control
  cisco.nxos.nxos_l2_interfaces:
    config:
      - name: Ethernet1/25
        spanning_tree:
          port_type: edge
          link_type: point_to_point
          vlans:
            - vlans: "1,3-5"
              port_priority: 64
        storm_control:
          unicast:
            level: "5"
    state: rendered

# Task Output
# -----------
#
# rendered:
# - interface Ethernet1/25
# - spanning-tree port type edge
# - spanning-tree link-type point-to-point
# - storm-control unicast level 5.00
# - spanning-tree vlan 1,3-5 port-priority 64

# Using gathered with spanning_tree and storm_control

# Before state:
# -------------
#
# interface Ethernet1/25
#   switchport
#   switchport mode trunk
#   spanning-tree port-priority 64
#   spanning-tree port type edge trunk
#   spanning-tree bpduguard enable
#   storm-control broadcast level 0.01
#   storm-control multicast level 1.00

- name: Gather spanning-tree and storm-control settings
  cisco.nxos.nxos_l2_interfaces:
    state: gathered

# Task Output
# -----------
#
# gathered:
# - name: Ethernet1/25
#   mode: trunk
#   spanning_tree:
#     bpduguard: true
#     port_priority: 64
#     port_type: edge_trunk
#   storm_control:
#     broadcast:
#       level: "0.01"
#     multicast:
#       level: "1.00"

# Using parsed with spanning_tree and storm_control

# File: parsed.cfg
# ----------------
#
# interface port-channel20
#   spanning-tree port type network
#   spanning-tree bpduguard disable
#   spanning-tree mst 0,2-4 cost 200
#   storm-control broadcast level 50.50

- name: Parse the provided configuration
  cisco.nxos.nxos_l2_interfaces:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task Output
# -----------
#
# parsed:
# - name: port-channel20
#   spanning_tree:
#     bpduguard: false
#     mst:
#       - cost: 200
#         instances: 0,2-4
#     port_type: network
#   storm_control:
#     broadcast:
#       level: "50.50"
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
  sample:
    - "interface Ethernet1/1"
    - "switchport trunk allowed vlan 2,4,15"
    - "switchport trunk native vlan 10"
    - "interface Ethernet1/2"
    - "switchport access vlan 30"
    - "interface Ethernet1/3"
    - "switchport trunk allowed vlan 5,6,7,8,9,10,15"
    - "switchport trunk native vlan 20"
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.l2_interfaces.l2_interfaces import (
    L2_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=L2_interfacesArgs.argument_spec,
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

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
