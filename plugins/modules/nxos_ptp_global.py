#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_ptp_global
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_ptp_global
version_added: 14.0.0
short_description: PTP global resource module.
description:
  - This module manages the global Precision Time Protocol (PTP) configuration of Cisco NX-OS devices.
  - The PTP settings of the interfaces are managed by M(cisco.nxos.nxos_ptp_interfaces).
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - The PTP commands only exist when C(feature ptp) is enabled, use M(cisco.nxos.nxos_feature) for it.
    PTP on an interface needs I(source) to be configured first.
  - NX-OS does not display a setting that has its default value in the running configuration.
    The default values are I(domain) C(0), I(priority1) and I(priority2) C(255),
    I(mean_path_delay) C(1000000000), I(correction_range.value) C(100000) and I(management) C(true).
    A setting that is given with its default value is removed from the device, and the facts only
    return the settings that the device displays, so I(management) is only returned as C(false).
  - A setting that is given as C(false) (for the flags) is removed from the device.
  - NX-OS only removes a setting with a value when the C(no) command carries a value, the module
    sends the value that is configured on the device.
  - I(delay_tolerance) values are displayed with two decimals, C(10) and C(10.5) are compared as C(10.00) and C(10.50).
  - The periodic update interval of I(clock_periodic_update) has the default C(60), which NX-OS does not display.
  - The I(ipv6_multicast_scope) defaults are C(0x1-0xE) for I(rx) and C(0x1) for I(tx).
  - The C(offload), C(device-type), C(pdelay-req-interval), C(enhanced-client-scale) and
    C(forward-version1) commands are not managed by this module. N9K-C93180YC-FX with NX-OS 10.6(4)
    rejects C(offload), C(device-type generalized-ptp), C(enhanced-client-scale), C(forward-version1) and C(pdelay-req-interval).
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does not connect to the device.
author:
  - Jørgen Spange (@jorgenspange)
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | include "^ptp|^no ptp").
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: PTP global configuration.
    type: dict
    suboptions:
      source:
        description:
          - The source address of the PTP packets (C(ptp source)). One IPv4 and one IPv6 address can be configured.
        type: dict
        suboptions:
          ipv4:
            description: The IPv4 source address.
            type: dict
            suboptions:
              address:
                description: The IPv4 address.
                type: str
              vrf:
                description: The VRF of the address, C(management) or the name of a VRF.
                type: str
          ipv6:
            description: The IPv6 source address.
            type: dict
            suboptions:
              address:
                description: The IPv6 address.
                type: str
              vrf:
                description: The VRF of the address, C(management) or the name of a VRF.
                type: str
      domain:
        description: The PTP domain (C(ptp domain)), in the range 0-127. Defaults to C(0).
        type: int
      priority1:
        description: The clock priority1 (C(ptp priority1)), in the range 0-255. Defaults to C(255).
        type: int
      priority2:
        description: The clock priority2 (C(ptp priority2)), in the range 0-255. Defaults to C(255).
        type: int
      management:
        description: Enables the PTP management messages (C(ptp management)). Defaults to C(true).
        type: bool
      unicast_negotiation:
        description: Enables the PTP unicast negotiation (C(ptp unicast-negotiation)).
        type: bool
      ipv6_multicast_scope:
        description: The scopes of the IPv6 multicast addresses of the PTP messages (C(ptp ipv6 multicast scope)).
        type: dict
        suboptions:
          rx:
            description:
              - The scopes that are received, a list of values from C(0x1) to C(0xe) such as C(0x2-0x4,0x6).
                Defaults to C(0x1-0xE). NX-OS displays the digits in upper case, the module compares them that way.
            type: str
          tx:
            description: The scope that is sent, one value from C(0x1) to C(0xe). Defaults to C(0x1).
            type: str
      mean_path_delay:
        description: The mean path delay limit in nanoseconds (C(ptp mean-path-delay)), in the range 10-1000000000. Defaults to C(1000000000).
        type: int
      correction_range:
        description: The PTP correction range (C(ptp correction-range)).
        type: dict
        suboptions:
          value:
            description: The correction range in nanoseconds, in the range 10-1000000000. Defaults to C(100000).
            type: int
          logging:
            description: Logs the packets that are outside of the correction range (C(ptp correction-range logging)).
            type: bool
      delay_tolerance:
        description: The tolerance of the delay (C(ptp delay tolerance)).
        type: dict
        suboptions:
          mean_path:
            description: The mean path tolerance, from 1.0 to 100.0. NX-OS displays it with two decimals.
            type: str
          reverse_path:
            description: The reverse path tolerance, from 1.0 to 100.0. NX-OS displays it with two decimals.
            type: str
      notification:
        description: The PTP notifications (C(ptp notification type)).
        type: dict
        suboptions:
          gm_change:
            description: Notify about a grandmaster change.
            type: bool
          parent_change:
            description: Notify about a parent change.
            type: bool
          port_state_change:
            description: Notify about a port state change.
            type: bool
          high_correction:
            description: Notify about a high correction.
            type: dict
            suboptions:
              enabled:
                description: Enables the notification. It is enabled when I(interval) is given.
                type: bool
              interval:
                description: The interval in seconds, 1-300, or C(immediate).
                type: str
      clock_periodic_update:
        description: Periodic update of the clock (C(ptp clock periodic-update)).
        type: dict
        suboptions:
          enabled:
            description: Enables the periodic update. It is enabled when I(interval) is given.
            type: bool
          interval:
            description: The interval in seconds, 0-3600.
            type: int
      time_distribution_hold:
        description: Holds the time distribution when a threshold is exceeded (C(ptp time distribution-hold)).
        type: dict
        suboptions:
          enabled:
            description: Enables the hold. It is enabled when a threshold is given.
            type: bool
          correction_threshold:
            description: The correction threshold in nanoseconds, 1-100000.
            type: int
          delay_threshold:
            description: The delay threshold in nanoseconds, 1-5000.
            type: int
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) what is given is added to the device and nothing is removed, except the settings
        that are given with their default value or as C(false), which are removed.
      - With I(replaced) and I(overridden) the settings that are not given are removed from the device.
        The two states are the same for this module, the configuration is a single set of settings.
      - With I(deleted) all the PTP global settings are removed. C(feature ptp) is not touched.
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
# nxos# show running-config | include "^ptp|^no ptp"
# (nothing is shown)

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_ptp_global:
    config:
      source:
        ipv4:
          address: 192.0.2.1
      domain: 5
      priority1: 100
      priority2: 120
      correction_range:
        value: 5000
        logging: true
      management: false
    state: merged

# Task output:
# ------------
# before: {}
# commands:
#   - ptp source 192.0.2.1
#   - ptp domain 5
#   - ptp priority1 100
#   - ptp priority2 120
#   - ptp correction-range 5000
#   - ptp correction-range logging
#   - no ptp management
# after:
#   source:
#     ipv4:
#       address: 192.0.2.1
#   domain: 5
#   priority1: 100
#   priority2: 120
#   correction_range:
#     value: 5000
#     logging: true
#   management: false

# After state:
# ------------
# nxos# show running-config | include "^ptp|^no ptp"
# ptp source 192.0.2.1
# ptp priority1 100
# ptp priority2 120
# ptp correction-range 5000
# ptp correction-range logging
# ptp domain 5
# no ptp management

# Using replaced

# Before state:
# -------------
# nxos# show running-config | include "^ptp|^no ptp"
# ptp source 192.0.2.1
# ptp priority1 100
# ptp priority2 120
# ptp correction-range 5000
# ptp correction-range logging
# ptp domain 5
# no ptp management

- name: Replace the PTP global configuration with the provided one
  cisco.nxos.nxos_ptp_global:
    config:
      source:
        ipv4:
          address: 192.0.2.1
      priority1: 90
    state: replaced

# Task output:
# ------------
# commands:
#   - ptp priority1 90
#   - no ptp priority2 120
#   - no ptp correction-range 5000
#   - no ptp correction-range logging
#   - no ptp domain 5
#   - ptp management

# After state:
# ------------
# nxos# show running-config | include "^ptp|^no ptp"
# ptp source 192.0.2.1
# ptp priority1 90

# Using deleted

# Before state:
# -------------
# nxos# show running-config | include "^ptp|^no ptp"
# ptp source 192.0.2.1
# ptp priority1 90

- name: Remove the PTP global configuration
  cisco.nxos.nxos_ptp_global:
    state: deleted

# Task output:
# ------------
# commands:
#   - no ptp source 192.0.2.1
#   - no ptp priority1 90

# After state:
# ------------
# nxos# show running-config | include "^ptp|^no ptp"
# (nothing is shown)

# Using gathered

# Before state:
# -------------
# nxos# show running-config | include "^ptp|^no ptp"
# ptp source 192.0.2.1
# ptp priority1 90
# ptp notification type high-correction interval 60

- name: Gather the PTP global configuration from the device
  cisco.nxos.nxos_ptp_global:
    state: gathered

# Task output:
# ------------
# gathered:
#   source:
#     ipv4:
#       address: 192.0.2.1
#   priority1: 90
#   notification:
#     high_correction:
#       enabled: true
#       interval: "60"

# Using rendered

- name: Render the commands for the provided configuration
  cisco.nxos.nxos_ptp_global:
    config:
      source:
        ipv4:
          address: 192.0.2.1
          vrf: management
      delay_tolerance:
        mean_path: "10.5"
      time_distribution_hold:
        correction_threshold: 500
        delay_threshold: 100
    state: rendered

# Task output:
# ------------
# rendered:
#   - ptp source 192.0.2.1 vrf management
#   - ptp delay tolerance mean-path 10.50
#   - ptp time distribution-hold correction-threshold 500 delay-threshold 100

# Using parsed

# parsed.cfg
# ----------
# ptp source 192.0.2.1
# ptp domain 5
# no ptp management

- name: Parse the provided configuration
  cisco.nxos.nxos_ptp_global:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output:
# ------------
# parsed:
#   source:
#     ipv4:
#       address: 192.0.2.1
#   domain: 5
#   management: false
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
    - ptp source 192.0.2.1
    - ptp domain 5
    - no ptp management
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - ptp source 192.0.2.1
    - ptp domain 5
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.ptp_global.ptp_global import (
    Ptp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.ptp_global.ptp_global import (
    Ptp_global,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Ptp_globalArgs.argument_spec,
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

    result = Ptp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
