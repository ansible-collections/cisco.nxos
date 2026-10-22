# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The module file for nxos_nve_interface"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_nve_interface
short_description: NVE interface resource module.
description:
  - This module provides declarative management of Network Virtualization Endpoint (NVE)
    overlay interface that terminates VXLAN tunnels.
version_added: 13.1.0
author:
  - Jørn Ivar Holland (@jiholland)
notes:
  - Tested against NXOS 10.3(7)
  - Unsupported for Cisco MDS
  - Only the C(interface nve1) interface is managed.
  - Within a VNI, C(suppress-arp) and C(suppress-arp disable) are alternatives, as are
    C(mcast-group) and C(ingress-replication protocol bgp). The module fails if both
    options of such a pair are true (or, for I(mcast_group), set) in the task.
  - M(cisco.nxos.nxos_vxlan_vtep) and M(cisco.nxos.nxos_vxlan_vtep_vni) manage an overlapping
    part of the same C(interface nve1) configuration. Prefer this module for whole-interface,
    declarative management (including C(replaced), C(overridden) and C(gathered)). Do not
    manage the same NVE settings with both this module and the older modules in one play.
options:
  config:
    description: A List of NVE interface options.
    type: dict
    suboptions:
      enabled:
        description:
          - Administrative state of the interface. Set the value to C(true) to
            administratively enable the interface or C(false) to disable it.
        type: bool
      description:
        description:
          - Interface description
        type: str
      host_reachability_bgp:
        description:
          - Enable/disable host reachability with bgp
        type: bool
      advertise_virtual_rmac:
        description:
          - Enable/disable virtual RMAC advertisement
        type: bool
      source_interface_name:
        description:
          - Source loopback interface name
        type: str
      source_interface_hold_time:
        description:
          - Source loopback interface hold-down-time in seconds
        type: int
      global_suppress_arp:
        description:
          - Enable/disable global ARP suppression
        type: bool
      global_ingress_replication_bgp:
        description:
          - Enable/disable global bgp ingress replication
        type: bool
      global_multicast_group:
        description:
          - Global multicast group.
          - On NX-OS 10.6(4) a group with mode C(L3) is accepted but never shown in the running-config,
            so it cannot be gathered and is configured again on every run. The C(L2) mode is not affected.
        type: dict
        suboptions:
          address:
            description:
              - Multicast address
            type: str
          mode:
            description:
              - VNI type.
            type: str
            required: true
            choices:
              - L2
              - L3
      multisite_interface:
        description:
          - Multisite border gateway source interface
        type: str
      vnis:
        description:
          - Configure Virtual Network Identifier membership
        type: list
        elements: dict
        suboptions:
          vni_id:
            description:
              - Virtual Network Identifier ID
              - Valid range is 1-16777214.
            type: int
            required: true
          associate_vrf:
            description:
              - Associate L3VNI with VRF
            type: bool
          suppress_arp:
            description:
              - Enable/disable ARP suppression for L2VNI
              - Mutually exclusive with I(suppress_arp_disable) when both are true.
            type: bool
          suppress_arp_disable:
            description:
              - Disable/enable the global setting for ARP suppression for L2VNI
              - Mutually exclusive with I(suppress_arp) when both are true.
            type: bool
          multisite_ingress_replication:
            description:
              - Enable/disable multisite ingress replication for L2VNI
            type: bool
          ingress_replication_bgp:
            description:
              - Enable/disable bgp ingress replication for L2VNI
              - Mutually exclusive with I(mcast_group).
            type: bool
          mcast_group:
            description:
              - Multicast group used for BUM traffic of this VNI (C(mcast-group)).
              - Mutually exclusive with I(ingress_replication_bgp).
              - With state C(merged), setting this option removes a configured
                I(ingress_replication_bgp) from the VNI (and vice versa).
            type: dict
            suboptions:
              address:
                description:
                  - Multicast group address.
                type: str
                required: true
              secondary_address:
                description:
                  - Optional second multicast group address accepted by C(mcast-group).
                  - Accepted by the CLI of NX-OS 10.6(4) on N9Kv without an error but not applied there, so it is not
                    covered by the integration tests.
                type: str
  state:
    description:
      - The state of the configuration after module completion.
      - States C(replaced) and C(overridden) have the same behaviour for this module.
      - With state C(deleted) and no I(config), the whole C(interface nve1) is removed.
      - With state C(deleted) and an I(config), only the listed I(vnis) and the listed
        top-level attributes that are configured on the device are removed. Other VNIs
        and attributes, and the interface itself, are left in place.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - parsed
      - gathered
      - rendered
    default: merged
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section "^interface nve1").
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
"""
EXAMPLES = """
# Using merged

# Before state:
# -------------
# switch# show running-config | section "^interface nve1"
# switch#

- name: Merge the provided NVE configuration with the existing running configuration.
  cisco.nxos.nxos_nve_interface:
    config:
      enabled: true
      description: vxlan vtep
      advertise_virtual_rmac: true
      host_reachability_bgp: true
      source_interface_name: loopback1
      source_interface_hold_time: 60
      global_multicast_group:
        address: 233.252.0.20
        mode: L2
      vnis:
        - associate_vrf: true
          vni_id: 11111
        - associate_vrf: false
          vni_id: 22222
        - suppress_arp: true
          vni_id: 33333
        - vni_id: 44444
          mcast_group:
            address: 233.252.0.10
    state: merged

# Task output:
# ------------
# before: {}
#
# commands:
#   - interface nve1
#   - description vxlan vtep
#   - host-reachability protocol bgp
#   - advertise virtual-rmac
#   - source-interface loopback1
#   - source-interface hold-down-time 60
#   - member vni 11111 associate-vrf
#   - member vni 22222
#   - member vni 33333
#   - suppress-arp
#   - member vni 44444
#   - mcast-group 233.252.0.10
#   - no shutdown
#   - global mcast-group 233.252.0.20 L2
#
# after:
#   enabled: true
#   description: vxlan vtep
#   advertise_virtual_rmac: true
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#   source_interface_hold_time: 60
#   global_multicast_group:
#     address: 233.252.0.20
#     mode: L2
#   vnis:
#     - associate_vrf: true
#       vni_id: 11111
#     - vni_id: 22222
#     - suppress_arp: true
#       vni_id: 33333
#     - vni_id: 44444
#       mcast_group:
#         address: 233.252.0.10
#
# After state:
# ------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   advertise virtual-rmac
#   source-interface loopback1
#   source-interface hold-down-time 60
#   global mcast-group 233.252.0.20 L2
#   member vni 11111 associate-vrf
#   member vni 22222
#   member vni 33333
#     suppress-arp
#   member vni 44444
#     mcast-group 233.252.0.10


# Using gathered

# Existing config:
# ---------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   advertise virtual-rmac
#   source-interface loopback1
#   source-interface hold-down-time 60
#   global mcast-group 233.252.0.20 L2
#   member vni 11111 associate-vrf
#   member vni 22222
#   member vni 33333
#     suppress-arp

- name: Gather NVE interface facts using gathered
  cisco.nxos.nxos_nve_interface:
    state: gathered

# Task output:
# ------------
# gathered:
#   enabled: true
#   description: vxlan vtep
#   advertise_virtual_rmac: true
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#   source_interface_hold_time: 60
#   global_multicast_group:
#     address: 233.252.0.20
#     mode: L2
#   vnis:
#     - associate_vrf: true
#       vni_id: 11111
#     - vni_id: 22222
#     - suppress_arp: true
#       vni_id: 33333


# Using overridden

# Before state:
# -------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   advertise virtual-rmac
#   source-interface loopback1
#   source-interface hold-down-time 60
#   global mcast-group 233.252.0.20 L2
#   member vni 11111 associate-vrf
#   member vni 22222
#   member vni 33333
#     suppress-arp

- name: Override NVE interface configuration with provided configuration.
  cisco.nxos.nxos_nve_interface:
    config:
      enabled: true
      advertise_virtual_rmac: true
      host_reachability_bgp: true
      source_interface_name: loopback1
      global_multicast_group:
        address: 233.252.0.30
        mode: L2
      vnis:
        - associate_vrf: false
          ingress_replication_bgp: true
          suppress_arp: true
          vni_id: 11111
        - associate_vrf: true
          vni_id: 22222
        - associate_vrf: true
          vni_id: 33333
    state: overridden

# Task output:
# ------------
# before:
#   enabled: true
#   description: vxlan vtep
#   advertise_virtual_rmac: true
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#   source_interface_hold_time: 60
#   global_multicast_group:
#     address: 233.252.0.20
#     mode: L2
#   vnis:
#     - associate_vrf: true
#       vni_id: 11111
#     - vni_id: 22222
#     - suppress_arp: true
#       vni_id: 33333
#
# commands:
#   - interface nve1
#   - no description vxlan vtep
#   - no source-interface hold-down-time 60
#   - no member vni 11111 associate-vrf
#   - member vni 11111
#   - suppress-arp
#   - ingress-replication protocol bgp
#   - no member vni 22222
#   - member vni 22222 associate-vrf
#   - no member vni 33333
#   - member vni 33333 associate-vrf
#   - global mcast-group 233.252.0.30 L2
#
# after:
#   enabled: true
#   advertise_virtual_rmac: true
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#   global_multicast_group:
#     address: 233.252.0.30
#     mode: L2
#   vnis:
#     - ingress_replication_bgp: true
#       suppress_arp: true
#       vni_id: 11111
#     - associate_vrf: true
#       vni_id: 22222
#     - associate_vrf: true
#       vni_id: 33333
#
# After state:
# ------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   host-reachability protocol bgp
#   advertise virtual-rmac
#   source-interface loopback1
#   global mcast-group 233.252.0.40 L2
#   member vni 11111
#     suppress-arp
#     ingress-replication protocol bgp
#   member vni 22222 associate-vrf
#   member vni 33333 associate-vrf


# Using replaced

# Before state:
# -------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   host-reachability protocol bgp
#   advertise virtual-rmac
#   source-interface loopback1
#   global mcast-group 233.252.0.40 L2
#   member vni 11111
#     suppress-arp
#     ingress-replication protocol bgp
#   member vni 22222 associate-vrf
#   member vni 33333 associate-vrf

- name: Replace NVE interface configuration with provided configuration.
  cisco.nxos.nxos_nve_interface:
    config:
      description: vxlan vtep
      host_reachability_bgp: true
      source_interface_name: loopback1
    state: replaced

# Task output:
# ------------
# before:
#   enabled: true
#   advertise_virtual_rmac: true
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#   global_multicast_group:
#     address: 233.252.0.40
#     mode: L2
#   vnis:
#     - ingress_replication_bgp: true
#       suppress_arp: true
#       vni_id: 11111
#     - associate_vrf: true
#       vni_id: 22222
#     - associate_vrf: true
#       vni_id: 33333
#
# commands:
#   - interface nve1
#   - description vxlan vtep
#   - no advertise virtual-rmac
#   - no member vni 11111
#   - no member vni 22222 associate-vrf
#   - no member vni 33333 associate-vrf
#   - shutdown
#   - no global mcast-group L2
#
# after:
#   enabled: false
#   description: vxlan vtep
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#
# After state:
# ------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   source-interface loopback1


# Using deleted

# Before state:
# -------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   source-interface loopback1

- name: Delete the whole NVE interface.
  cisco.nxos.nxos_nve_interface:
    state: deleted

# Task output:
# ------------

# before:
#   description: vxlan vtep
#   host_reachability_bgp: true
#   source_interface_name: loopback1
#
# commands:
#   - no interface nve1
#
# after: {}
#
# After state:
# ------------
# switch# show running-config | section "^interface nve1"
# switch#


# Using deleted with a config to remove only the listed VNIs

# Before state:
# -------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   host-reachability protocol bgp
#   source-interface loopback1
#   member vni 11111
#   member vni 22222 associate-vrf
#   member vni 33333

- name: Delete only the listed VNIs.
  cisco.nxos.nxos_nve_interface:
    config:
      vnis:
        - vni_id: 11111
        - vni_id: 22222
    state: deleted

# Task output:
# ------------

# commands:
#   - interface nve1
#   - no member vni 11111
#   - no member vni 22222 associate-vrf
#
# After state:
# ------------
# switch# show running-config | section "^interface nve1"
# interface nve1
#   no shutdown
#   host-reachability protocol bgp
#   source-interface loopback1
#   member vni 33333


# Using rendered

- name: Render platform specific configuration lines (without connecting to the device)
  cisco.nxos.nxos_nve_interface:
    config:
      enabled: true
      description: vxlan vtep
      advertise_virtual_rmac: true
      host_reachability_bgp: true
      source_interface_name: loopback1
      global_multicast_group:
        address: 233.252.0.20
        mode: L2
      vnis:
        - suppress_arp: true
          vni_id: 11111
        - suppress_arp_disable: true
          vni_id: 22222
    state: rendered

# Task output:
# ------------
# rendered:
#   - interface nve1
#   - description vxlan vtep
#   - host-reachability protocol bgp
#   - advertise virtual-rmac
#   - source-interface loopback1
#   - member vni 11111
#   - suppress-arp
#   - member vni 22222
#   - suppress-arp disable
#   - no shutdown
#   - global mcast-group 233.252.0.20 L2


# Using parsed

# parsed.cfg
# ----------
# interface nve1
#   no shutdown
#   description vxlan vtep
#   host-reachability protocol bgp
#   source-interface loopback1
#   global mcast-group 233.252.0.20 L2
#   member vni 22222
#   member vni 33333

- name: Parse externally provided NVE interface config
  cisco.nxos.nxos_nve_interface:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   description: vxlan vtep
#   enabled: true
#   global_multicast_group:
#     address: 233.252.0.20
#     mode: L2
#  host_reachability_bgp: true
#  source_interface_name: loopback1
#  vnis:
#    - vni_id: 22222
#    - vni_id: 33333
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
    - interface nve1
    - no shutdown
    - description vxlan vtep
    - host-reachability protocol bgp
    - advertise virtual-rmac
    - source-interface loopback1
    - global mcast-group 233.252.0.20 L2
    - member vni 11111 associate-vrf
    - member vni 22222
    - suppress-arp
"""

from ansible.module_utils.basic import (
    AnsibleModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.nve_interface.nve_interface import (
    Nve_interfaceArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.nve_interface.nve_interface import (
    Nve_interface,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Nve_interfaceArgs.argument_spec,
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

    result = Nve_interface(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
