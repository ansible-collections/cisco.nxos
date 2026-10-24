#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_igmp_snooping
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_igmp_snooping
version_added: 1.0.0
short_description: IGMP snooping resource module.
description:
- This module manages the global IGMP snooping configuration and the IGMP snooping settings
  of the per-VLAN context (C(vlan configuration <id>)), including static groups, multicast
  router ports, the querier and report policies, on devices running Cisco NX-OS.
notes:
- Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
- Unsupported for Cisco MDS.
- This module was rewritten as a resource module. The former flat parameters
  and the C(present) and C(default) states are gone, use I(config) with the
  I(state) C(merged) or C(deleted) instead.
- The IGMP snooping configuration must be identical on both vPC peers.
- IGMP snooping over VXLAN is supported with BGP EVPN only, not with flood-and-learn,
  and not on VLANs with FEX member ports. The global I(vxlan) setting
  (C(ip igmp snooping vxlan)) must be enabled for snooping to be active on VXLAN VLANs.
- A VLAN without PIM needs an IGMP querier, configure it with I(querier) of the VLAN.
- The settings of a VLAN do not apply until the VLAN exists. NX-OS keeps a
  C(vlan configuration) block when the VLAN itself is removed, use I(state) C(deleted),
  C(replaced) or C(overridden) to remove such blocks.
- NX-OS does not show a setting that has its default value in the running configuration.
  The facts therefore report the global settings with their effective value, which means
  that C(gathered) and C(parsed) return C(snooping), C(link_local_groups_suppression),
  C(report_suppression), C(v3_report_suppression), C(vxlan), C(disable_nve_static_router_port),
  C(max_gq_miss), C(syslog_threshold) and C(holddown_timer) even when they are not configured.
  The group timeout and the proxy are only returned when they are configured. The settings of a
  C(vlan configuration) block are only returned when the block shows them; a value equal to the
  default is not shown by the device and counts as not set.
- The global defaults are C(snooping=true), C(link_local_groups_suppression=true),
  C(report_suppression=true), C(v3_report_suppression=false), C(vxlan=false),
  C(disable_nve_static_router_port=false), C(max_gq_miss=3), C(syslog_threshold=90),
  C(holddown_timer=210) and no group timeout and no proxy. The defaults of a VLAN are
  C(snooping=true), C(explicit_tracking=true), C(link_local_groups_suppression=true),
  C(report_suppression=true), C(v3_report_suppression=false), C(fast_leave=false),
  C(querier_timeout=255), C(query_interval=125), C(query_max_response_time=10),
  C(robustness_variable=2), C(last_member_query_interval=1) and C(version=3). Setting an option to
  its default value removes its line from the configuration, and is a no-op when the device already has it.
- C(startup_query_count) and C(startup_query_interval) have no default, the device shows them as soon as they are configured.
- Tested against NX-OS 10.6(4) on N9K-C93180YC-FX, global and per VLAN, that every option is accepted, stored as
  written by the module, and removed again. The group timeout is accepted while snooping is disabled.
  The route-maps and prefix-lists of I(report_policy) and I(access_group) do not have to exist,
  and the interfaces of I(mrouter_interfaces), I(report_flood), I(report_policy), I(access_group) and
  I(static_groups) do not have to be members of the VLAN.
- The group timeout is sent after the other global settings, except when snooping ends up disabled.
- C(event-history) (debug buffer sizes) and C(optimise-multicast-flood) (not available on the tested platform)
  are not managed by this module.
- A C(vlan configuration) block is managed completely. Under I(state) C(replaced) and C(overridden) a listed
  VLAN gets exactly the given settings, the others return to the default, and a VLAN without any setting has
  no block. C(deleted) and C(overridden) remove the blocks, together with all content, of the VLANs they remove.
- A static group is accepted and stored for any interface, but C(show ip igmp snooping groups vlan <id>)
  only lists it (type S) when the interface is a member port of that VLAN.
- C(state=deleted) without I(config) and C(state=overridden) remove every C(vlan configuration) block on the
  switch that is not listed, including blocks created by other tools or roles. Run the task in check mode first.
- A C(vlan configuration) block that is not for a single VLAN (for example a range) is ignored.
- A VLAN that is listed without any setting is not created by C(merged),
  because an empty C(vlan configuration) block has no effect. It is reported
  by C(gathered) when the device has one.
- Interface names are normalised before they are compared, so C(Eth1/10),
  C(ethernet1/10) and C(Ethernet1/10) are the same, as are C(Po20) and C(port-channel20).
- This module works with connection C(network_cli) and C(httpapi).
- The I(parsed) state reads configuration from I(running_config) and does
  not connect to the device.
author:
- Jason Edelman (@jedelman8)
- Gabriele Gerbino (@GGabriele)
- Jorgen Spange (@jorgenspange)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the commands B(show running-config | section "^vlan configuration")
      and B(show running-config | include "ip igmp snooping"), or the full running configuration.
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
    version_added: 13.1.0
  config:
    description: IGMP snooping configuration.
    type: dict
    version_added: 13.1.0
    suboptions:
      snooping:
        description:
        - Enables or disables IGMP snooping on the switch (C(ip igmp snooping)).
        - Defaults to C(true).
        type: bool
      group_timeout:
        description:
        - Group membership timeout for all VLANs on the device (C(ip igmp snooping group-timeout)).
        - Accepted values are an integer in the range 1-10080 (minutes) and C(never).
        - It is removed by I(state) C(deleted), and by I(state) C(replaced) and C(overridden)
          when it is not given.
        type: str
      link_local_groups_suppression:
        description:
        - Global link-local groups suppression (C(ip igmp snooping link-local-groups-suppression)).
        - Defaults to C(true).
        type: bool
      report_suppression:
        description:
        - Global IGMPv1/IGMPv2 report suppression (C(ip igmp snooping report-suppression)).
        - Defaults to C(true).
        type: bool
      v3_report_suppression:
        description:
        - Global IGMPv3 report suppression and proxy reporting (C(ip igmp snooping v3-report-suppression)).
        - Defaults to C(false).
        type: bool
      vxlan:
        description:
        - Enables IGMP snooping for VXLAN VLANs (C(ip igmp snooping vxlan)).
        - Defaults to C(false).
        type: bool
      disable_nve_static_router_port:
        description:
        - Do not include the NVE interface as a static router port in the VXLAN VLANs
          (C(ip igmp snooping disable-nve-static-router-port)).
        - Defaults to C(false).
        type: bool
      max_gq_miss:
        description:
        - Number of general queries without an answer after which the mrouter port is removed
          (C(ip igmp snooping max-gq-miss)), in the range 3-5.
        - Defaults to C(3).
        type: int
      syslog_threshold:
        description:
        - Percentage of the multicast table size at which a syslog message is raised
          (C(ip igmp snooping syslog-threshold)), in the range 1-100.
        - Defaults to C(90).
        type: int
      holddown_timer:
        description:
        - Hold-down timer in seconds (C(ip igmp snooping holddown-timer)), in the range 1-300.
        - Defaults to C(210).
        type: int
      proxy:
        description:
        - IGMP snooping proxy for general queries (C(ip igmp snooping proxy general-queries)).
        - Removed by I(state) C(replaced) and C(overridden) when it is not given.
        type: dict
        suboptions:
          general_queries:
            description:
            - Enables (C(true)) or removes (C(false)) the proxy.
            - Required when I(mrt) is given.
            type: bool
          mrt:
            description:
            - Maximum response time in seconds (C(mrt)), in the range 1-25.
            type: int
      vlans:
        description:
        - The VLANs with a C(vlan configuration) block.
        - With I(state) C(replaced) the settings of a listed VLAN are made identical to the
          ones given, VLANs that are not listed are left alone.
        - With I(state) C(overridden) the VLANs that are not listed are removed.
        type: list
        elements: dict
        suboptions:
          vlan_id:
            description:
            - The VLAN ID, in the range 1-4094.
            type: int
            required: true
          snooping:
            description:
            - Enables or disables IGMP snooping for the VLAN (C(ip igmp snooping)). Defaults to C(true).
            type: bool
          group_timeout:
            description:
            - Group membership timeout of the VLAN (C(ip igmp snooping group-timeout)),
              1-10080 minutes or C(never).
            type: str
          link_local_groups_suppression:
            description:
            - Link-local groups suppression of the VLAN. Defaults to C(true).
            type: bool
          report_suppression:
            description:
            - IGMPv1/IGMPv2 report suppression of the VLAN. Defaults to C(true).
            type: bool
          v3_report_suppression:
            description:
            - IGMPv3 report suppression of the VLAN. Defaults to C(false).
            type: bool
          explicit_tracking:
            description:
            - Explicit host tracking for IGMPv3 (C(ip igmp snooping explicit-tracking)). Defaults to C(true).
            type: bool
          fast_leave:
            description:
            - Fast leave (C(ip igmp snooping fast-leave)). Defaults to C(false).
            type: bool
          proxy:
            description:
            - IGMP snooping proxy for general queries of the VLAN (C(ip igmp snooping proxy general-queries)).
            type: dict
            suboptions:
              general_queries:
                description:
                - Enables (C(true)) or removes (C(false)) the proxy. Required when I(mrt) is given.
                type: bool
              mrt:
                description:
                - Maximum response time in seconds, in the range 1-25.
                type: int
          proxy_leave_use_group_address:
            description:
            - Use the group address in proxy leaves (C(ip igmp snooping proxy-leave use-group-address)).
              Defaults to C(false).
            type: bool
          querier:
            description:
            - The IPv4 source address of the IGMP snooping querier (C(ip igmp snooping querier)).
            - The querier with the lowest address wins the election.
            type: str
          querier_timeout:
            description:
            - Querier timeout in seconds (C(ip igmp snooping querier-timeout)), in the range 1-65535. Defaults to C(255).
            type: int
          query_interval:
            description:
            - Query interval in seconds (C(ip igmp snooping query-interval)), in the range 1-18000. Defaults to C(125).
            type: int
          query_max_response_time:
            description:
            - Maximum query response time in seconds (C(ip igmp snooping query-max-response-time)),
              in the range 1-25. Defaults to C(10).
            type: int
          startup_query_count:
            description:
            - Number of queries sent at startup (C(ip igmp snooping startup-query-count)), in the range 1-10.
            type: int
          startup_query_interval:
            description:
            - Interval of the startup queries in seconds (C(ip igmp snooping startup-query-interval)),
              in the range 1-18000.
            type: int
          robustness_variable:
            description:
            - Robustness variable (C(ip igmp snooping robustness-variable)), in the range 1-7. Defaults to C(2).
            type: int
          last_member_query_interval:
            description:
            - Last member query interval in seconds (C(ip igmp snooping last-member-query-interval)),
              in the range 1-25. Defaults to C(1).
            type: int
          version:
            description:
            - IGMP version used by the snooping process (C(ip igmp snooping version)), 2 or 3. Defaults to C(3).
            type: int
          mrouter_interfaces:
            description:
            - Static multicast router ports (C(ip igmp snooping mrouter interface)).
            type: list
            elements: str
          report_flood:
            description:
            - Floods the reports (C(ip igmp snooping report-flood)) to all ports or to selected interfaces.
            type: dict
            suboptions:
              all:
                description:
                - Flood the reports to all ports (C(report-flood all)).
                type: bool
              interfaces:
                description:
                - Flood the reports to these interfaces (C(report-flood interface)).
                type: list
                elements: str
          report_policy:
            description:
            - Report filters (C(ip igmp snooping report-policy)) per interface.
            type: list
            elements: dict
            suboptions:
              policy_type:
                description: The kind of policy.
                type: str
                required: true
                choices:
                - route_map
                - prefix_list
              name:
                description: The name of the route-map or prefix-list. It does not have to exist.
                type: str
                required: true
              interface:
                description: The interface the policy applies to.
                type: str
                required: true
          access_group:
            description:
            - Group access filters (C(ip igmp snooping access-group)).
            - Without I(interface) the line is C(ip igmp snooping access-group <route-map>), which is
              only possible for a C(route_map).
            type: list
            elements: dict
            suboptions:
              policy_type:
                description: The kind of policy.
                type: str
                required: true
                choices:
                - route_map
                - prefix_list
              name:
                description: The name of the route-map or prefix-list. It does not have to exist.
                type: str
                required: true
              interface:
                description: The interface the policy applies to. Required for a C(prefix_list).
                type: str
          static_groups:
            description:
            - Static multicast groups of the VLAN (C(ip igmp snooping static-group)).
            type: list
            elements: dict
            suboptions:
              group:
                description:
                - The IPv4 multicast group address.
                type: str
                required: true
              source:
                description:
                - The IPv4 source address of the group, for IGMPv3.
                type: str
              interfaces:
                description:
                - The interfaces on which the group is statically joined.
                - One C(ip igmp snooping static-group) line is configured for each interface.
                type: list
                elements: str
                required: true
  state:
    description:
    - The state the configuration should be left in.
    - The states and the call shape changed in 13.1.0. Only the resource module states exist, the former
      C(present) and C(default) states are replaced by C(merged) and C(deleted).
    - With I(merged) what is given is added to the device, nothing is removed. A setting that
      is not given is not touched.
    - With I(replaced) the global settings that are not given are reset to their default, the
      listed VLANs are made identical to the given ones and the other VLANs are not touched.
    - With I(overridden) the same applies and the VLANs that are not listed are removed.
    - With I(deleted) and without I(config) all global settings are reset to their default and
      all C(vlan configuration) blocks are removed. With I(config) the listed global settings
      are reset, a listed VLAN without any setting is removed, and for a listed VLAN
      with settings only these are removed.
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
extends_documentation_fragment:
- cisco.nxos.nxos
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# (nothing is shown, the device has the default configuration)

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_igmp_snooping:
    config:
      vxlan: true
      v3_report_suppression: true
      group_timeout: "300"
      vlans:
        - vlan_id: 100
          static_groups:
            - group: 233.252.0.10
              interfaces:
                - Eth1/10
                - Po20
            - group: 233.252.0.11
              source: 192.0.2.10
              interfaces:
                - Ethernet1/10
    state: merged

# Task output:
# ------------
# before:
#   snooping: true
#   link_local_groups_suppression: true
#   report_suppression: true
#   v3_report_suppression: false
#   vxlan: false
#   disable_nve_static_router_port: false
#   max_gq_miss: 3
#   syslog_threshold: 90
#   holddown_timer: 210
# commands:
#   - ip igmp snooping v3-report-suppression
#   - ip igmp snooping vxlan
#   - ip igmp snooping group-timeout 300
#   - vlan configuration 100
#   - ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
#   - ip igmp snooping static-group 233.252.0.10 interface port-channel20
#   - ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10
# after:
#   snooping: true
#   link_local_groups_suppression: true
#   report_suppression: true
#   v3_report_suppression: true
#   vxlan: true
#   disable_nve_static_router_port: false
#   max_gq_miss: 3
#   syslog_threshold: 90
#   holddown_timer: 210
#   group_timeout: "300"
#   vlans:
#     - vlan_id: 100
#       static_groups:
#         - group: 233.252.0.10
#           interfaces:
#             - Ethernet1/10
#             - port-channel20
#         - group: 233.252.0.11
#           source: 192.0.2.10
#           interfaces:
#             - Ethernet1/10

# After state:
# ------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# ip igmp snooping v3-report-suppression
# ip igmp snooping group-timeout 300
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
#   ip igmp snooping static-group 233.252.0.10 interface port-channel20
#   ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10

# Using merged with the per-VLAN settings

- name: Configure the querier, the router ports and the filters of a VLAN
  cisco.nxos.nxos_igmp_snooping:
    config:
      max_gq_miss: 4
      proxy:
        general_queries: true
        mrt: 8
      vlans:
        - vlan_id: 100
          querier: 192.0.2.1
          query_interval: 200
          version: 2
          fast_leave: true
          mrouter_interfaces:
            - Po20
          report_flood:
            interfaces:
              - Po20
          report_policy:
            - policy_type: route_map
              name: RM_REPORTS
              interface: Po20
          access_group:
            - policy_type: route_map
              name: RM_GROUPS
    state: merged

# Task output:
# ------------
# commands:
#   - ip igmp snooping max-gq-miss 4
#   - ip igmp snooping proxy general-queries mrt 8
#   - vlan configuration 100
#   - ip igmp snooping mrouter interface port-channel20
#   - ip igmp snooping report-flood interface port-channel20
#   - ip igmp snooping report-policy route-map RM_REPORTS interface port-channel20
#   - ip igmp snooping access-group RM_GROUPS
#   - ip igmp snooping fast-leave
#   - ip igmp snooping query-interval 200
#   - ip igmp snooping version 2
#   - ip igmp snooping querier 192.0.2.1

# Using replaced

# Before state:
# -------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# ip igmp snooping v3-report-suppression
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
#   ip igmp snooping static-group 233.252.0.10 interface port-channel20
# vlan configuration 200
#   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

- name: Replace the global settings and the listed VLANs
  cisco.nxos.nxos_igmp_snooping:
    config:
      vxlan: true
      vlans:
        - vlan_id: 100
          static_groups:
            - group: 233.252.0.10
              interfaces:
                - Ethernet1/10
    state: replaced

# Task output:
# ------------
# commands:
#   - no ip igmp snooping v3-report-suppression
#   - vlan configuration 100
#   - no ip igmp snooping static-group 233.252.0.10 interface port-channel20

# After state:
# ------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
# vlan configuration 200
#   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

# Using overridden

# Before state:
# -------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
# vlan configuration 200
#   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

# WARNING: every vlan configuration block that is not listed is removed, also the ones
# created by other tools or roles. Run it with check_mode first.
- name: Override the IGMP snooping configuration
  cisco.nxos.nxos_igmp_snooping:
    config:
      vxlan: true
      vlans:
        - vlan_id: 100
          static_groups:
            - group: 233.252.0.10
              interfaces:
                - Ethernet1/10
    state: overridden

# Task output:
# ------------
# commands:
#   - no vlan configuration 200

# After state:
# ------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10

# Using deleted

# Before state:
# -------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# ip igmp snooping group-timeout 300
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
# vlan configuration 200
#   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

- name: Delete the VLAN 200 configuration only
  cisco.nxos.nxos_igmp_snooping:
    config:
      vlans:
        - vlan_id: 200
    state: deleted

# Task output:
# ------------
# commands:
#   - no vlan configuration 200

# Using deleted without config

# Before state:
# -------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# ip igmp snooping vxlan
# ip igmp snooping group-timeout 300
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10

# WARNING: this removes EVERY vlan configuration block on the switch, also the ones
# created by other tools or roles. Run it with check_mode first.
- name: Reset all global settings and remove all vlan configuration blocks
  cisco.nxos.nxos_igmp_snooping:
    state: deleted

# Task output:
# ------------
# commands:
#   - no ip igmp snooping vxlan
#   - no ip igmp snooping group-timeout 300
#   - no vlan configuration 100

# After state:
# ------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# (nothing is shown, the device has the default configuration)

# Using rendered

- name: Render platform specific configuration lines (without connecting to the device)
  cisco.nxos.nxos_igmp_snooping:
    config:
      snooping: true
      report_suppression: false
      vlans:
        - vlan_id: 100
          static_groups:
            - group: 233.252.0.10
              source: 192.0.2.10
              interfaces:
                - Po20
    state: rendered

# Task Output:
# ------------
# rendered:
#   - ip igmp snooping
#   - no ip igmp snooping report-suppression
#   - vlan configuration 100
#   - ip igmp snooping static-group 233.252.0.10 source 192.0.2.10 interface port-channel20

# Using parsed

# parsed.cfg
# ----------
# ip igmp snooping vxlan
# ip igmp snooping group-timeout 300
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
#   ip igmp snooping static-group 233.252.0.10 interface port-channel20

- name: Parse the provided configuration
  cisco.nxos.nxos_igmp_snooping:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   snooping: true
#   link_local_groups_suppression: true
#   report_suppression: true
#   v3_report_suppression: false
#   vxlan: true
#   disable_nve_static_router_port: false
#   max_gq_miss: 3
#   syslog_threshold: 90
#   holddown_timer: 210
#   group_timeout: "300"
#   vlans:
#     - vlan_id: 100
#       static_groups:
#         - group: 233.252.0.10
#           interfaces:
#             - Ethernet1/10
#             - port-channel20

# Using gathered

# Existing device config:
# -----------------------
# nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
# no ip igmp snooping link-local-groups-suppression
# vlan configuration 100
#   ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10

- name: Gather the IGMP snooping configuration from the device
  cisco.nxos.nxos_igmp_snooping:
    state: gathered

# Task output:
# ------------
# gathered:
#   snooping: true
#   link_local_groups_suppression: false
#   report_suppression: true
#   v3_report_suppression: false
#   vxlan: false
#   disable_nve_static_router_port: false
#   max_gq_miss: 3
#   syslog_threshold: 90
#   holddown_timer: 210
#   vlans:
#     - vlan_id: 100
#       static_groups:
#         - group: 233.252.0.11
#           source: 192.0.2.10
#           interfaces:
#             - Ethernet1/10
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - ip igmp snooping vxlan
    - vlan configuration 100
    - ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
rendered:
  description: The provided configuration in the device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - ip igmp snooping vxlan
    - vlan configuration 100
    - ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option, parsed into structured data.
  returned: when I(state) is C(parsed)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.igmp_snooping.igmp_snooping import (
    Igmp_snoopingArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.igmp_snooping.igmp_snooping import (
    Igmp_snooping,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Igmp_snoopingArgs.argument_spec,
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

    result = Igmp_snooping(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
