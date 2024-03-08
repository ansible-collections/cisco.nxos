#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_spanning_tree_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_spanning_tree_global
extends_documentation_fragment:
- cisco.nxos.nxos
short_description: Resource module to configure spanning tree.
description: This module configures and manages the attributes of Spanning-tree on Cisco NXOS.
version_added: 6.0.3
author: Vinay Mulugund (@roverflow)
notes:
- Tested against NX-OS 9.3.6 on Cisco Nexus Switches.
- This module works with connection C(network_cli) and C(httpapi).
- Tested against Cisco MDS NX-OS 9.2(2) with connection C(network_cli).
options:
  config:
    description: A dict of Spanning-tree options.
    type: dict
    suboptions:
      bridge:
        description: Bridge options in spanning-tree.
        type: dict
        suboptions:
          bridge_assurance:
            description: Enable bridge assurance.
            type: bool
          bridge_domain:
            decsription: Bridge-Domain Spanning Trees range.
            type: dict
            suboptions:
              bd_list_range:
                description: Bridge-Domain Spanning Trees range.
                type: str
              forward_time:
                description: Forward time for bridge domain.
                type: int
              hello_time:
                description: Hello time for bridge domain.
                type: int
              max_age:
                description: Max age for bridge domain.
                type: int
              priority:
                description: Priority for bridge domain.
                type: int
              root:
                description: Configure switch as root.
                type: dict
                mutually_exclusive: [["primary", "secondary"]]
                suboptions:
                  primary:
                    description: Configure primary root.
                    type: dict
                    suboptions:
                      enable:
                        description: Enable primary root.
                        type: bool
                      diameter:
                        description: Priority for primary root.
                        type: int
                      hello_time:
                        description: Configure secondary root.
                        type: int
                  secondary:
                    description: Configure secondary root.
                    type: dict
                    suboptions:
                      enable:
                        description: Enable primary root.
                        type: bool
                      diameter:
                        description: Priority for primary root.
                        type: int
                      hello_time:
                        description: Configure secondary root.
                        type: int
      domain:
        description: Spanning tree domain options.
        type: dict
        mutually_exclusive: [["identifier", "disable", "enable"]]
        suboptions:
          identifier:
            description: Spanning tree domain identifier.
            type: int
          disable:
            description: Disable spanning tree domain.
            type: bool
          enable:
            description: Enable spanning tree domain.
            type: bool
          clear_stats:
            description: Clear spanning tree domain statistics.
            type: bool
      fcoe:
        description: Enable STP for FCoE VLANs.
        type: bool
      lc_issu:
        description: Configure Linecard ISSU type.
        type: str
        choices:
          - auto
          - disruptive
          - non-disruptive
      loopguard_default:
        description: Spanning tree loopguard .
        type: bool
      mode:
        description: Spanning tree mode.
        type: str
        choices:
          - mst
          - rapid-pvst
      mst:
        description: Multiple spanning tree configuration.
        type: dict
        suboptions:
          forward-time:
            description: Forward time for MST.
            type: int
          hello-time:
            description: Hello time for MST.
            type: int
          max_age:
            description: Max age for MST.
            type: int
          max_hops:
            description: Max hops for MST.
            type: int
          simulate_pvst_global:
            description: Enable Simulate PVST global.
            type: bool
          configure_mst:
            description: MST configuration submode options.
            type: list
            elements: dict
            suboptions:
              name:
                description: MST configuration submode instance name.
                type: str
              revision:
                description: MST configuration submode instance revision.
                type: int
              private_vlan_sync:
                description: MST configuration submode private vlan sync.
                type: bool
              instance_vlan:
                description: MST configuration submode instance.
                type: dict
                suboptions:
                  instance_id:
                    description: MST configuration submode instance id.
                    type: int
                  vlan_range:
                    description: MST configuration submode instance vlan range.
                    type: str
      pathcost_method:
        description: Spanning tree pathcost options.
        type: str
        choices:
          - long
          - short
      port_type:
        description: Spanning tree port type.
        type: dict
        mutually_exclusive: [["edge", "network", "default"]]
        suboptions:
          edge:
            description: Enable edge port type.
            type: str
            choices:
              - bpdufilter
              - bpduguard
              - default
          network:
            description: Enable network port type.
            type: bool
          default:
            description: Enable default port type.
            type: bool
      pseudo_info:
        description: Configure spanning tree pseudo information
        type: dict
        suboptions:
          bridge_domain_info:
            description: Pseudo information bridge domain.
            type: dict
            mutually_exclusive: [["designated", "root"]]
            suboptions:
              range:
                description: Pseudo information bridge domain range.
                type: str
              designated_priority:
                description: Pseudo information bridge domain designated priority.
                type: int
              root_priority:
                description: Pseudo information bridge domain root priority.
                type: int
          mst_info:
            description: Pseudo information MST.
            type: dict
            mutually_exclusive: [["designated", "root"]]
            suboptions:
              range:
                description: Pseudo information MST range.
                type: str
              designated_priority:
                description: Pseudo information MST designated priority.
                type: int
              root_priority:
                description: Pseudo information MST root priority.
                type: int
          vlan_info:
            description: Pseudo information MST.
            type: dict
            mutually_exclusive: [["designated", "root"]]
            suboptions:
              range:
                description: Pseudo information MST range.
                type: str
              designated_priority:
                description: Pseudo information MST designated priority.
                type: int
              root_priority:
                description: Pseudo information MST root priority.
                type: int
      vlan:
        description: VLAN Switch Spanning Trees.
        type: dict
        suboptions:
          vlan_range:
            description: VLAN range for spanning tree.
            type: str
          forward_time:
            description: Forward time for VLAN.
            type: int
          hello_time:
            description: Hello time for VLAN.
            type: int
          max_age:
            description: Max age for VLAN.
            type: int
          priority:
            description: Priority for VLAN.
            type: int
          root:
            description: Configure switch as root.
            type: dict
            mutually_exclusive: [["primary", "secondary"]]
            suboptions:
              primary:
                description: Configure primary root.
                type: dict
                suboptions:
                  enable:
                    description: Enable primary root.
                    type: bool
                  diameter:
                    description: Priority for primary root.
                    type: int
                  hello_time:
                    description: Configure secondary root.
                    type: int
              secondary:
                description: Configure secondary root.
                type: dict
                suboptions:
                  enable:
                    description: Enable primary root.
                    type: bool
                  diameter:
                    description: Priority for primary root.
                    type: int
                  hello_time:
                    description: Configure secondary root.
                    type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NXOS device by
        executing the command B(show running-config | section ^spanning-tree).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - rendered
      - gathered
      - purged
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
        option should be the same format as the output of command I(show running-config
        | include ip route|ipv6 route) executed on device. For state I(parsed) active
        connection to remote host is not required.
      - The state I(purged) negates virtual/logical interfaces that are specified in task
        from running-config.
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.spanning_tree_global.spanning_tree_global import (
    Spanning_tree_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.spanning_tree_global.spanning_tree_global import (
    Spanning_tree_global,
)

import debugpy
debugpy.listen(3000)
debugpy.wait_for_client()
def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Spanning_tree_globalArgs.argument_spec,
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

    result = Spanning_tree_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
