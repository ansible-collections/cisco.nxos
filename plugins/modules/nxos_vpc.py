#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_vpc
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_vpc
version_added: 1.0.0
short_description: VPC global domain resource module.
description:
- This module manages global VPC domain configuration on devices running Cisco NX-OS.
notes:
- Unsupported for Cisco MDS
- Tested against NXOSv 7.3.(0)D1(1)
- The feature vpc must be enabled before this module can be used.
- If not using management vrf, the vrf must be globally configured on the device
  before using it in the peer-keepalive configuration.
- Both pkl_src and pkl_dest are needed when changing peer-keepalive VRF.
author: Ansible Network Eng Team
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section '^vpc domain').
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: Global VPC domain configuration.
    type: dict
    suboptions:
      domain:
        description:
        - VPC domain ID.
        type: str
        required: true
      role_priority:
        description:
        - Role priority for device. Lower values are preferred.
        type: str
      system_priority:
        description:
        - System priority. Must match between VPC peers.
        type: str
      pkl_src:
        description:
        - Source IP address used for peer keepalive link.
        type: str
      pkl_dest:
        description:
        - Destination (remote) IP address used for peer keepalive link.
        - Required whenever any peer keepalive options are used.
        type: str
      pkl_vrf:
        description:
        - VRF used for peer keepalive link. Defaults to management.
        type: str
      peer_gw:
        description:
        - Enable or disable peer gateway.
        type: bool
      peer_sw:
        description:
        - Enable or disable peer-switch.
        type: bool
      auto_recovery:
        description:
        - Enable or disable auto-recovery.
        type: bool
      auto_recovery_reload_delay:
        description:
        - Delay in seconds before auto-recovery after reload.
        type: str
      delay_restore:
        description:
        - Delay in seconds before VPC comes back up after reload.
        type: str
      delay_restore_interface_vlan:
        description:
        - Delay in seconds before interface-vlan comes back up after reload.
        type: str
      delay_restore_orphan_port:
        description:
        - Delay in seconds for orphan port delay restore.
        type: str
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
"""

EXAMPLES = """
# Using merged

# Before state:
# -------------
# (no vpc domain configured)

- name: Merge VPC global domain configuration
  cisco.nxos.nxos_vpc:
    config:
      domain: "10"
      role_priority: "150"
      system_priority: "2000"
      pkl_dest: 192.168.2.2
      pkl_src: 192.168.2.1
      pkl_vrf: management
      peer_gw: true
      auto_recovery: true
      delay_restore: "150"
    state: merged

# Task output:
# ------------
# commands:
#   - terminal dont-ask
#   - vpc domain 10
#   - role priority 150
#   - system-priority 2000
#   - auto-recovery
#   - peer-gateway
#   - delay restore 150
#   - peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management

# After state:
# ------------
# vpc domain 10
#   role priority 150
#   system-priority 2000
#   peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management
#   peer-gateway
#   auto-recovery
#   delay restore 150

# Using replaced

# Before state:
# -------------
# vpc domain 10
#   role priority 150
#   system-priority 2000
#   peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management
#   peer-gateway
#   auto-recovery
#   delay restore 150

- name: Replace VPC global domain configuration
  cisco.nxos.nxos_vpc:
    config:
      domain: "10"
      pkl_dest: 192.168.2.2
      pkl_src: 192.168.2.1
    state: replaced

# Task output:
# ------------
# commands:
#   - vpc domain 10
#   - no role priority
#   - no system-priority
#   - no delay restore
#   - no auto-recovery
#   - no peer-gateway
#   - peer-keepalive destination 192.168.2.2 source 192.168.2.1

# After state:
# ------------
# vpc domain 10
#   peer-keepalive destination 192.168.2.2 source 192.168.2.1

# Using deleted

# Before state:
# -------------
# vpc domain 10
#   peer-keepalive destination 192.168.2.2 source 192.168.2.1

- name: Delete VPC global domain configuration
  cisco.nxos.nxos_vpc:
    state: deleted

# Task output:
# ------------
# commands:
#   - terminal dont-ask
#   - no vpc domain 10

# After state:
# ------------
# (no vpc domain configured)

# Using gathered

- name: Gather VPC global domain facts from the device
  cisco.nxos.nxos_vpc:
    state: gathered

# Task output:
# ------------
# gathered:
#   domain: "10"
#   role_priority: "150"
#   system_priority: "2000"
#   pkl_dest: 192.168.2.2
#   pkl_src: 192.168.2.1
#   pkl_vrf: management
#   peer_gw: true
#   auto_recovery: true
#   delay_restore: "150"

# Using rendered

- name: Render VPC configuration (offline, no device connection)
  cisco.nxos.nxos_vpc:
    config:
      domain: "10"
      role_priority: "150"
      peer_gw: true
      pkl_dest: 192.168.2.2
      pkl_src: 192.168.2.1
      pkl_vrf: management
    state: rendered

# Task output:
# ------------
# rendered:
#   - terminal dont-ask
#   - vpc domain 10
#   - role priority 150
#   - peer-gateway
#   - peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management

# Using parsed

- name: Parse VPC configuration from provided running-config
  cisco.nxos.nxos_vpc:
    running_config: |
      vpc domain 10
        role priority 150
        peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management
        peer-gateway
        auto-recovery
    state: parsed

# Task output:
# ------------
# parsed:
#   domain: "10"
#   role_priority: "150"
#   pkl_dest: 192.168.2.2
#   pkl_src: 192.168.2.1
#   pkl_vrf: management
#   peer_gw: true
#   auto_recovery: true
"""

RETURN = """
before:
  description: The configuration prior to the module invocation.
  returned: always
  type: dict
  sample: >
    The configuration returned will always be in the same format
    of the parameters above.
after:
  description: The resulting configuration after module invocation.
  returned: when changed
  type: dict
  sample: >
    The configuration returned will always be in the same format
    of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample:
    - terminal dont-ask
    - vpc domain 10
    - role priority 150
    - peer-gateway
    - peer-keepalive destination 192.168.2.2 source 192.168.2.1 vrf management
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - terminal dont-ask
    - vpc domain 10
    - role priority 150
    - peer-gateway
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option parsed into structured data as per module argspec.
  returned: when I(state) is C(parsed)
  type: dict
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.vpc.vpc import (
    VpcArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vpc.vpc import (
    Vpc,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=VpcArgs.argument_spec,
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

    result = Vpc(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
