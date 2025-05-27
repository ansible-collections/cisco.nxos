#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_interfaces
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_interfaces
short_description: Interfaces resource module
description: This module manages the interface attributes of NX-OS interfaces.
version_added: 1.0.0
author:
  - Trishna Guha (@trishnaguha)
  - Vinay Mulugund (@roverflow)
notes:
  - Tested against NXOS 10.4(2) on CML
  - Unsupported for Cisco MDS
options:
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - 'Full name of interface, e.g. Ethernet1/1, port-channel10.'
        type: str
        required: true
      description:
        description:
          - Interface description.
        type: str
      enabled:
        description:
          - Administrative state of the interface. Set the value to C(true) to
            administratively enable the interface or C(false) to disable it
        type: bool
      speed:
        description:
          - Interface link speed. Applicable for Ethernet interfaces only.
        type: str
      mode:
        description:
          - Manage Layer2 or Layer3 state of the interface. Applicable for
            Ethernet and port channel interfaces only.
        choices:
          - layer2
          - layer3
        type: str
      mtu:
        description:
          - MTU for a specific interface. Must be an even number between 576 and
            9216. Applicable for Ethernet interfaces only.
        type: str
      duplex:
        description:
          - Interface link status. Applicable for Ethernet interfaces only.
        type: str
        choices:
          - full
          - half
          - auto
      ip_forward:
        description:
          - Enable or disable IP forward feature on SVIs. Set the value to
            C(true) to enable  or C(false) to disable.
        type: bool
      fabric_forwarding_anycast_gateway:
        description:
          - Associate SVI with anycast gateway under VLAN configuration mode.
            Applicable for SVI interfaces only.
        type: bool
      mac_address:
        description: E.E.E  MAC address.
        type: str
      logging:
        description: "Logging interface events"
        type: "dict"
        suboptions:
          link_status:
            description: "UPDOWN and CHANGE messages"
            type: bool
          trunk_status:
            description: "TRUNK status messages"
            type: bool
      snmp:
        description: "Modify SNMP interface parameters"
        type: dict
        suboptions:
          trap:
            description: Allow a specific SNMP trap
            type: dict
            suboptions:
              link_status:
                description: Allow SNMP LINKUP and LINKDOWN traps (snmp trap link-status permit duplicates)
                type: bool
      service_policy:
        description: Service policy configuration
        type: dict
        suboptions:
          input:
            description: Assign policy-map to the input of an interface
            type: str
          output:
            description: Assign policy-map to the output of an interface
            type: str
          type_options:
            description: Specify the type of this policy
            type: dict
            suboptions:
              qos:
                description: Configure qos Service Policy
                type: dict
                suboptions:
                  input:
                    description: Assign policy-map to the input of an interface
                    type: str
                  output:
                    description: Assign policy-map to the output of an interface
                    type: str
              queuing:
                description: Configure queuing Service Policy
                type: dict
                suboptions:
                  input:
                    description: Assign policy-map to the input of an interface
                    type: str
                  output:
                    description: Assign policy-map to the output of an interface
                    type: str
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS
        device by executing the command B(show running-config | section
        ^interface)
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  state:
    description:
      - The state of the configuration after module completion
      - The state I(rendered) considers the system default mode for interfaces
        to be "Layer 3" and the system default state for interfaces to be
        shutdown.
      - The state I(purged) negates virtual interfaces that are specified in
        task from running-config.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
      - rendered
      - parsed
      - purged
    default: merged
"""

EXAMPLES = """

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
  sample: ['interface Ethernet1/1', 'mtu 1800']
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.interfaces.interfaces import (
    InterfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.interfaces.interfaces import (
    Interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=InterfacesArgs.argument_spec,
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

    result = Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
