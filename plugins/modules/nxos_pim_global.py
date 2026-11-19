# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The module file for nxos_pim_global"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_pim_global
short_description: PIM global resource module.
description:
  - This module manages the global Protocol Independent Multicast (PIM) configuration
    of a device running Cisco NX-OS, the C(ip pim) commands of the global configuration.
  - It covers the SSM range, the static RP addresses and the anycast RP sets, together with a few
    simple global options.
version_added: 14.1.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - The feature C(pim) must be enabled, for example with M(cisco.nxos.nxos_feature).
  - The configuration of the PIM interfaces (C(ip pim sparse-mode)) and of the VRFs is not managed.
  - NX-OS replaces the default SSM range C(232.0.0.0/8) when another range is configured. Add
    C(232.0.0.0/8) to I(ssm_range) to keep it. The default is not displayed in the running configuration
    and is not returned by the module.
  - A static RP without I(group_list), I(prefix_list) and I(route_map) is stored by NX-OS with the
    group list C(224.0.0.0/4), which the module returns and expects in I(replaced) and I(overridden).
  - A static RP line with a keyword other than C(group-list), C(prefix-list), C(route-map) and C(bidir)
    is not recognised. I(gathered) and I(parsed) do not return it, and I(replaced), I(overridden) and
    I(deleted) do not remove it.
  - M(cisco.nxos.nxos_pim) and M(cisco.nxos.nxos_pim_rp_address) manage a part of the same
    configuration. Prefer this module for declarative management, including I(replaced),
    I(overridden) and I(gathered). Do not manage the same settings with both in one play.
options:
  config:
    description: The global PIM configuration.
    type: dict
    suboptions:
      bfd:
        description:
          - Enable BFD on all PIM interfaces (C(ip pim bfd)).
          - Needs C(feature bfd), the device rejects the command without it.
        type: bool
      log_neighbor_changes:
        description: Log the PIM neighbor state changes (C(ip pim log-neighbor-changes)).
        type: bool
      flush_routes:
        description: Remove the routes when PIM is restarted (C(ip pim flush-routes)).
        type: bool
      register_rate_limit:
        description:
          - Rate limit of the PIM data registers in packets per second (C(ip pim register-rate-limit)).
        type: int
      ssm_range:
        description:
          - The group ranges for Source Specific Multicast (C(ip pim ssm range)).
          - NX-OS keeps these in one line, so the list is configured as a whole. The keyword C(none)
            removes all SSM ranges and must be the only item.
          - With I(state) C(merged) the ranges are added to the configured ranges.
          - A list that is only C(232.0.0.0/8) resets the line to the default.
        type: list
        elements: str
      rp_addresses:
        description:
          - The static RP addresses (C(ip pim rp-address)), one entry for each line.
          - An RP can have several entries with different group lists.
        type: list
        elements: dict
        suboptions:
          rp_address:
            description: The IPv4 address of the RP.
            type: str
            required: true
          group_list:
            description:
              - The multicast group range of the RP (C(group-list)).
              - When none of I(group_list), I(prefix_list) and I(route_map) is given the RP is
                configured for all groups, which NX-OS displays as C(group-list 224.0.0.0/4).
            type: str
          prefix_list:
            description: The prefix list that defines the groups of the RP (C(prefix-list)).
            type: str
          route_map:
            description: The route map that defines the groups of the RP (C(route-map)).
            type: str
          bidir:
            description: The groups are handled in PIM bidirectional mode (C(bidir)).
            type: bool
      anycast_rps:
        description:
          - The anycast RP sets (C(ip pim anycast-rp)).
        type: list
        elements: dict
        suboptions:
          anycast_rp:
            description: The IPv4 address of the anycast RP.
            type: str
            required: true
          members:
            description:
              - The IPv4 addresses of the set members, one C(ip pim anycast-rp) line for each member.
              - The own address of the device is also a member of the set.
            type: list
            elements: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | include "^ip pim ").
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) what is given is added to the device, nothing is removed. The static
        RP lines and anycast RP members are added, the SSM range list is extended.
      - With I(replaced) and I(overridden) the global PIM configuration of the device is made identical
        to I(config). The module manages a single global configuration, so both states behave the same.
        Everything that is not given is removed, also the static RPs and the anycast RP members.
      - With I(deleted) the settings listed in I(config) are removed. Without I(config) all global
        PIM configuration that the module manages is removed.
      - With I(rendered) the commands for I(config) are returned and nothing is sent to the device.
      - With I(gathered) the configuration is read from the device and returned in I(gathered).
      - With I(parsed) the text of I(running_config) is converted to structured data.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - parsed
    default: merged
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
# switch# show running-config | include "^ip pim "
# switch#

- name: Merge the provided PIM configuration with the existing running configuration.
  cisco.nxos.nxos_pim_global:
    config:
      log_neighbor_changes: true
      register_rate_limit: 100
      ssm_range:
        - 232.0.0.0/8
        - 239.255.250.0/24
      rp_addresses:
        - rp_address: 192.0.2.1
          group_list: 239.255.0.0/16
        - rp_address: 192.0.2.2
          group_list: 239.254.0.0/16
          bidir: true
        - rp_address: 192.0.2.3
          prefix_list: PL_RP3
        - rp_address: 192.0.2.4
          route_map: RM_RP4
      anycast_rps:
        - anycast_rp: 192.0.2.10
          members:
            - 192.0.2.11
            - 192.0.2.12
    state: merged

# Task output:
# ------------
# before: {}
#
# commands:
#   - ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
#   - ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
#   - ip pim rp-address 192.0.2.3 prefix-list PL_RP3
#   - ip pim rp-address 192.0.2.4 route-map RM_RP4
#   - ip pim anycast-rp 192.0.2.10 192.0.2.11
#   - ip pim anycast-rp 192.0.2.10 192.0.2.12
#   - ip pim log-neighbor-changes
#   - ip pim register-rate-limit 100
#   - ip pim ssm range 232.0.0.0/8 239.255.250.0/24
#
# after:
#   log_neighbor_changes: true
#   register_rate_limit: 100
#   ssm_range:
#     - 232.0.0.0/8
#     - 239.255.250.0/24
#   rp_addresses:
#     - rp_address: 192.0.2.1
#       group_list: 239.255.0.0/16
#     - rp_address: 192.0.2.2
#       group_list: 239.254.0.0/16
#       bidir: true
#     - rp_address: 192.0.2.3
#       prefix_list: PL_RP3
#     - rp_address: 192.0.2.4
#       route_map: RM_RP4
#   anycast_rps:
#     - anycast_rp: 192.0.2.10
#       members:
#         - 192.0.2.11
#         - 192.0.2.12

# After state:
# ------------
# switch# show running-config | include "^ip pim "
# ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
# ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
# ip pim rp-address 192.0.2.3 prefix-list PL_RP3
# ip pim rp-address 192.0.2.4 route-map RM_RP4
# ip pim ssm range 232.0.0.0/8 239.255.250.0/24
# ip pim log-neighbor-changes
# ip pim register-rate-limit 100
# ip pim anycast-rp 192.0.2.10 192.0.2.11
# ip pim anycast-rp 192.0.2.10 192.0.2.12

# Using replaced

# Before state:
# -------------
# switch# show running-config | include "^ip pim "
# ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
# ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
# ip pim log-neighbor-changes
# ip pim anycast-rp 192.0.2.10 192.0.2.11

- name: Replace the global PIM configuration.
  cisco.nxos.nxos_pim_global:
    config:
      rp_addresses:
        - rp_address: 192.0.2.1
          group_list: 239.255.0.0/16
        - rp_address: 192.0.2.5
          group_list: 239.253.0.0/16
    state: replaced

# Task output:
# ------------
# commands:
#   - no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
#   - no ip pim anycast-rp 192.0.2.10 192.0.2.11
#   - no ip pim log-neighbor-changes
#   - ip pim rp-address 192.0.2.5 group-list 239.253.0.0/16

# Using overridden

# The global PIM configuration is a single resource, so overridden removes what is not
# given in the same way as replaced.

# Before state:
# -------------
# switch# show running-config | include "^ip pim "
# ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
# ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
# ip pim ssm range 232.0.0.0/8 239.255.250.0/24
# ip pim log-neighbor-changes
# ip pim anycast-rp 192.0.2.10 192.0.2.11

- name: Override the global PIM configuration.
  cisco.nxos.nxos_pim_global:
    config:
      ssm_range:
        - 232.0.0.0/8
        - 239.255.250.0/24
      rp_addresses:
        - rp_address: 192.0.2.1
          group_list: 239.255.0.0/16
        - rp_address: 192.0.2.5
          group_list: 239.253.0.0/16
    state: overridden

# Task output:
# ------------
# commands:
#   - no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
#   - no ip pim anycast-rp 192.0.2.10 192.0.2.11
#   - no ip pim log-neighbor-changes
#   - ip pim rp-address 192.0.2.5 group-list 239.253.0.0/16

# Using deleted

# Before state:
# -------------
# switch# show running-config | include "^ip pim "
# ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
# ip pim ssm range 232.0.0.0/8 239.255.250.0/24
# ip pim anycast-rp 192.0.2.10 192.0.2.11

- name: Remove the SSM range and the anycast RP set.
  cisco.nxos.nxos_pim_global:
    config:
      ssm_range:
        - 232.0.0.0/8
      anycast_rps:
        - anycast_rp: 192.0.2.10
          members:
            - 192.0.2.11
    state: deleted

# Task output:
# ------------
# commands:
#   - no ip pim anycast-rp 192.0.2.10 192.0.2.11
#   - no ip pim ssm range 232.0.0.0/8

# Using rendered

- name: Render the commands without a device connection.
  cisco.nxos.nxos_pim_global:
    config:
      bfd: true
      rp_addresses:
        - rp_address: 192.0.2.1
    state: rendered

# Task output:
# ------------
# rendered:
#   - ip pim rp-address 192.0.2.1 group-list 224.0.0.0/4
#   - ip pim bfd

# Using gathered

- name: Gather the global PIM configuration.
  cisco.nxos.nxos_pim_global:
    state: gathered

# Task output:
# ------------
# gathered:
#   log_neighbor_changes: true
#   ssm_range:
#     - 232.0.0.0/8
#     - 239.255.250.0/24
#   rp_addresses:
#     - rp_address: 192.0.2.1
#       group_list: 239.255.0.0/16

# Using parsed

# parsed.cfg
# ----------
# ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
# ip pim anycast-rp 192.0.2.10 192.0.2.11

- name: Parse the text of the running configuration.
  cisco.nxos.nxos_pim_global:
    running_config: "{{ lookup('ansible.builtin.file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   rp_addresses:
#     - rp_address: 192.0.2.1
#       group_list: 239.255.0.0/16
#   anycast_rps:
#     - anycast_rp: 192.0.2.10
#       members:
#         - 192.0.2.11
"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: dict
  sample: >
    The configuration returned will always be in the same format
    of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: dict
  sample: >
    The configuration returned will always be in the same format
    of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    - ip pim anycast-rp 192.0.2.10 192.0.2.11
    - ip pim ssm range 232.0.0.0/8 239.255.250.0/24
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
"""

from ansible.module_utils.basic import (
    AnsibleModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.pim_global.pim_global import (
    Pim_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.pim_global.pim_global import (
    Pim_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Pim_globalArgs.argument_spec,
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

    result = Pim_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
