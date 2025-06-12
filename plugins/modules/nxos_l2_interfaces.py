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
            type: str
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
      cdp_enable:
        type: bool
        description: Enable/disable CDP on the interface
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
