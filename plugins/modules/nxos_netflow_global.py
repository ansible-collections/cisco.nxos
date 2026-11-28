#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_netflow_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_netflow_global
version_added: 14.1.0
short_description: NetFlow global resource module.
description:
  - This module manages the global NetFlow configuration of Cisco NX-OS devices, the flow exporters,
    the flow records, the flow monitors and the flow timeout.
  - The assignment of the flow monitors to the interfaces is managed by M(cisco.nxos.nxos_netflow_interfaces).
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - The NetFlow commands only exist when C(feature netflow) is enabled, use M(cisco.nxos.nxos_feature) for it.
  - NX-OS 10.6(4) supports only C(version 9) exporters, no C(sampler) and no flow monitor cache settings.
  - A flow monitor has two exporters at most and its record can only be replaced, never removed.
  - Settings given with their default value, or a flag given as C(false), are removed from the device.
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does not connect to the device.
author:
  - Jørgen Spange (@jorgenspange)
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section ^flow).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: NetFlow global configuration.
    type: dict
    suboptions:
      timeout:
        description:
          - The flow timeout in seconds (C(flow timeout)), in the range 5-60. Defaults to C(10).
        type: int
      exporters:
        description: The flow exporters (C(flow exporter)).
        type: list
        elements: dict
        suboptions:
          name:
            description: The name of the flow exporter.
            type: str
            required: true
          description:
            description: The description of the flow exporter.
            type: str
          destination:
            description:
              - The collector the flow records are exported to (C(destination)).
            type: dict
            suboptions:
              address:
                description: The IPv4 or IPv6 address of the collector.
                type: str
                required: true
              vrf:
                description: The VRF used to reach the collector, C(management) or the name of a VRF. Defaults to C(default).
                type: str
          source:
            description:
              - The source interface of the exported packets (C(source)), such as C(Ethernet1/1),
                C(loopback0), C(mgmt0), C(port-channel10) or C(Vlan10).
              - The name is normalised, C(Eth1/1) is the same as C(Ethernet1/1).
            type: str
          transport_udp:
            description: The destination UDP port (C(transport udp)), in the range 1-65535. Defaults to C(9995).
            type: int
          dscp:
            description: The DSCP value of the exported packets (C(dscp)), in the range 0-63. Defaults to C(0).
            type: int
          template_data_timeout:
            description:
              - The refresh time of the version 9 data templates in seconds (C(template data timeout)),
                in the range 1-86400. Defaults to C(15).
            type: int
          option_exporter_stats_timeout:
            description:
              - The refresh time of the version 9 exporter statistics option in seconds (C(option exporter-stats timeout)),
                in the range 0-86400. Defaults to C(0).
            type: int
          option_interface_table_timeout:
            description:
              - The refresh time of the version 9 interface table option in seconds (C(option interface-table timeout)),
                in the range 0-86400. Defaults to C(0).
            type: int
      records:
        description: The flow records (C(flow record)).
        type: list
        elements: dict
        suboptions:
          name:
            description: The name of the flow record.
            type: str
            required: true
          description:
            description: The description of the flow record.
            type: str
          match:
            description:
              - The key fields of the record (C(match)). A field is added with C(true) and removed with C(false).
              - A record has C(datalink), C(ipv4) or C(ipv6) fields, not a mix of them.
            type: dict
            suboptions:
              datalink:
                description: The Layer 2 fields.
                type: dict
                suboptions:
                  mac_source_address:
                    description: Match the source MAC address (C(match datalink mac source-address)).
                    type: bool
                  mac_destination_address:
                    description: Match the destination MAC address (C(match datalink mac destination-address)).
                    type: bool
                  vlan:
                    description: Match the VLAN (C(match datalink vlan)).
                    type: bool
                  ethertype:
                    description: Match the ethertype (C(match datalink ethertype)).
                    type: bool
              ip:
                description: The IP fields.
                type: dict
                suboptions:
                  protocol:
                    description: Match the IP protocol (C(match ip protocol)).
                    type: bool
                  tos:
                    description: Match the IP type of service (C(match ip tos)).
                    type: bool
              ipv4:
                description: The IPv4 fields.
                type: dict
                suboptions:
                  source_address:
                    description: Match the IPv4 source address (C(match ipv4 source address)).
                    type: bool
                  destination_address:
                    description: Match the IPv4 destination address (C(match ipv4 destination address)).
                    type: bool
              ipv6:
                description: The IPv6 fields.
                type: dict
                suboptions:
                  source_address:
                    description: Match the IPv6 source address (C(match ipv6 source address)).
                    type: bool
                  destination_address:
                    description: Match the IPv6 destination address (C(match ipv6 destination address)).
                    type: bool
                  flow_label:
                    description: Match the IPv6 flow label (C(match ipv6 flow-label)).
                    type: bool
                  options:
                    description: Match the IPv6 options (C(match ipv6 options)).
                    type: bool
              transport:
                description: The transport layer fields.
                type: dict
                suboptions:
                  source_port:
                    description: Match the transport source port (C(match transport source-port)).
                    type: bool
                  destination_port:
                    description: Match the transport destination port (C(match transport destination-port)).
                    type: bool
          collect:
            description: The non-key fields of the record (C(collect)). A field is added with C(true) and removed with C(false).
            type: dict
            suboptions:
              counter:
                description: The counters.
                type: dict
                suboptions:
                  bytes:
                    description: Collect the number of bytes (C(collect counter bytes)).
                    type: bool
                  packets:
                    description: Collect the number of packets (C(collect counter packets)).
                    type: bool
              timestamp_sys_uptime:
                description: The timestamps.
                type: dict
                suboptions:
                  first:
                    description: Collect the system uptime of the first packet (C(collect timestamp sys-uptime first)).
                    type: bool
                  last:
                    description: Collect the system uptime of the last packet (C(collect timestamp sys-uptime last)).
                    type: bool
              transport_tcp_flags:
                description: Collect the TCP flags (C(collect transport tcp flags)).
                type: bool
              ip_version:
                description: Collect the IP version (C(collect ip version)).
                type: bool
      monitors:
        description: The flow monitors (C(flow monitor)).
        type: list
        elements: dict
        suboptions:
          name:
            description: The name of the flow monitor.
            type: str
            required: true
          description:
            description: The description of the flow monitor.
            type: str
          record:
            description:
              - The flow record of the monitor (C(record)), the name of a record or one of the predefined
                ones such as C(netflow-original), C(netflow ipv4 original-input), C(netflow ipv6 original-input),
                C(netflow layer2-switched input) and C(netflow protocol-port).
              - The device cannot remove the record of a monitor, it can only be replaced.
            type: str
          exporters:
            description:
              - The names of the flow exporters of the monitor (C(exporter)), two at most.
            type: list
            elements: str
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) what is given is added to the configuration and nothing is removed, except the settings that
        are given with their default value or with C(false), which are removed.
      - With I(replaced) the exporters, records and monitors that are listed are made identical to the given ones,
        the ones that are not listed are not touched. The I(timeout) is set to the default when it is not given.
      - With I(overridden) the same applies and what is not listed is removed, C(timeout) set to C(10) alone wipes everything.
      - With I(deleted) the listed exporters, records and monitors are removed, without I(config) all of them
        and the I(timeout).
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
# nxos# show running-config | section ^flow
# nxos#

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_netflow_global:
    config:
      timeout: 30
      exporters:
        - name: EXPORTER1
          description: Collector 1
          destination:
            address: 192.0.2.10
            vrf: management
          source: Ethernet1/1
          transport_udp: 9996
          dscp: 10
          template_data_timeout: 600
          option_exporter_stats_timeout: 300
      records:
        - name: RECORD1
          description: IPv4 flows
          match:
            ipv4:
              source_address: true
              destination_address: true
            ip:
              protocol: true
            transport:
              source_port: true
              destination_port: true
          collect:
            counter:
              bytes: true
              packets: true
      monitors:
        - name: MONITOR1
          record: RECORD1
          exporters:
            - EXPORTER1
    state: merged

# Task output:
# ------------
# before: {}
# commands:
#   - flow timeout 30
#   - flow exporter EXPORTER1
#   - description Collector 1
#   - destination 192.0.2.10 use-vrf management
#   - transport udp 9996
#   - source Ethernet1/1
#   - dscp 10
#   - version 9
#   - template data timeout 600
#   - option exporter-stats timeout 300
#   - flow record RECORD1
#   - description IPv4 flows
#   - match ip protocol
#   - match ipv4 source address
#   - match ipv4 destination address
#   - match transport source-port
#   - match transport destination-port
#   - collect counter bytes
#   - collect counter packets
#   - flow monitor MONITOR1
#   - record RECORD1
#   - exporter EXPORTER1

# Using replaced

# Before state:
# -------------
# nxos# show running-config | section ^flow
# flow exporter EXPORTER1
#   description Collector 1
#   destination 192.0.2.10 use-vrf management
#   transport udp 9996
#   source Ethernet1/1
#   dscp 10
#   version 9
#     template data timeout 600
# flow exporter EXPORTER2
#   destination 198.51.100.5
#   version 9

- name: Replace the configuration of the listed exporters
  cisco.nxos.nxos_netflow_global:
    config:
      exporters:
        - name: EXPORTER1
          destination:
            address: 192.0.2.20
    state: replaced

# Task output:
# ------------
# commands:
#   - flow exporter EXPORTER1
#   - no description
#   - no transport udp
#   - no source
#   - no dscp
#   - destination 192.0.2.20 use-vrf default
#   - version 9
#   - template data timeout 15

# After state:
# ------------
# nxos# show running-config | section ^flow
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9
# flow exporter EXPORTER2
#   destination 198.51.100.5
#   version 9

# Using overridden

# Before state:
# -------------
# nxos# show running-config | section ^flow
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9
# flow exporter EXPORTER2
#   destination 198.51.100.5
#   version 9

- name: Override the configuration, what is not listed is removed
  cisco.nxos.nxos_netflow_global:
    config:
      exporters:
        - name: EXPORTER1
          destination:
            address: 192.0.2.20
    state: overridden

# Task output:
# ------------
# commands:
#   - no flow exporter EXPORTER2

# After state:
# ------------
# nxos# show running-config | section ^flow
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9

# Using deleted

# Before state:
# -------------
# nxos# show running-config | section ^flow
# flow timeout 30
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9
# flow record RECORD1
#   match ipv4 source address
# flow monitor MONITOR1
#   record RECORD1
#   exporter EXPORTER1

- name: Remove all the NetFlow configuration
  cisco.nxos.nxos_netflow_global:
    state: deleted

# Task output:
# ------------
# commands:
#   - no flow monitor MONITOR1
#   - no flow record RECORD1
#   - no flow exporter EXPORTER1
#   - no flow timeout

# After state:
# ------------
# nxos# show running-config | section ^flow
# nxos#

# Using gathered

# Before state:
# -------------
# nxos# show running-config | section ^flow
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9
# flow monitor MONITOR1
#   record netflow-original
#   exporter EXPORTER1

- name: Gather the NetFlow configuration from the device
  cisco.nxos.nxos_netflow_global:
    state: gathered

# Task output:
# ------------
# gathered:
#   exporters:
#     - name: EXPORTER1
#       destination:
#         address: 192.0.2.20
#   monitors:
#     - name: MONITOR1
#       record: netflow-original
#       exporters:
#         - EXPORTER1

# Using rendered

- name: Render the commands of a configuration
  cisco.nxos.nxos_netflow_global:
    config:
      exporters:
        - name: EXPORTER1
          destination:
            address: 198.51.100.7
            vrf: management
          source: Eth1/1
      monitors:
        - name: MONITOR1
          record: netflow-original
          exporters:
            - EXPORTER1
    state: rendered

# Task output:
# ------------
# rendered:
#   - flow exporter EXPORTER1
#   - destination 198.51.100.7 use-vrf management
#   - source Ethernet1/1
#   - flow monitor MONITOR1
#   - record netflow-original
#   - exporter EXPORTER1

# Using parsed

# parsed.cfg
# ----------
# flow exporter EXPORTER1
#   destination 192.0.2.20
#   version 9
# flow monitor MONITOR1
#   record netflow-original
#   exporter EXPORTER1

- name: Parse the configuration
  cisco.nxos.nxos_netflow_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   exporters:
#     - name: EXPORTER1
#       destination:
#         address: 192.0.2.20
#   monitors:
#     - name: MONITOR1
#       record: netflow-original
#       exporters:
#         - EXPORTER1
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
    - flow exporter EXPORTER1
    - destination 192.0.2.10 use-vrf management
    - flow monitor MONITOR1
    - record netflow-original
    - exporter EXPORTER1
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - flow exporter EXPORTER1
    - destination 192.0.2.10 use-vrf management
    - flow monitor MONITOR1
    - record netflow-original
    - exporter EXPORTER1
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.netflow_global.netflow_global import (
    Netflow_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.netflow_global.netflow_global import (
    Netflow_global,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Netflow_globalArgs.argument_spec,
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

    result = Netflow_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
