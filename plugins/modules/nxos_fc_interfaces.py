#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_fc_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: nxos_fc_interfaces
short_description: Fc Interfaces resource module
description: This module manages the interface attributes of NX-OS fc interfaces.
version_added: 1.0.0
author: Suhas Bharadwaj (@srbharadwaj)
notes:
  - Tested against NXOS 9.3(2) on Cisco MDS Switches
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS
        device by executing the command B(show running-config interface)
      - The state I(parsed) reads the configuration from C(running_config)
        option and transforms it into Ansible structured data as per the
        resource module's argspec and the value is then returned in the
        I(parsed) key within the result.
    type: str
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of interface, e.g. fc1/1, fc18/48
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
          - Interface link speed.
        choices:
          - auto
          - 1000
          - 2000
          - 4000
          - 8000
          - 16000
          - 32000
          - 64000
          - auto max 2000
          - auto max 4000
          - auto max 8000
          - auto max 16000
          - auto max 32000
          - auto max 64000
        type: str
      mode:
        description:
          - Port mode of the fc interface
        choices:
          - auto
          - E
          - F
          - Fx
          - NP
          - SD
        type: str
      trunk_mode:
        description:
          - Trunk mode of the fc interface
        choices:
          - auto
          - on
          - off
        type: str
      analytics:
        description:
          - Analytics type on the fc interface
        choices:
          - fc-scsi
          - fc-nvme
          - fc-all
        type: str
  state:
    description:
      - The state of the configuration after module completion
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
    - interface fc1/1
    - description sample description
    - shutdown
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - interface fc1/1
    - description sample description
    - shutdown
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.fc_interfaces.fc_interfaces import (
    Fc_interfacesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.fc_interfaces.fc_interfaces import (
    Fc_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Fc_interfacesArgs.argument_spec,
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

    result = Fc_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
