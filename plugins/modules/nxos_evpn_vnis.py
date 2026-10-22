#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_evpn_vnis
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_evpn_vnis
version_added: 13.1.0
short_description: EVPN VNIs resource module
description:
  - This module manages the Layer 2 VNIs configured under the C(evpn) section
    (C(vni <id> l2)) on Cisco NX-OS devices, with their route distinguisher
    and route targets.
  - It is the resource module counterpart of M(cisco.nxos.nxos_evpn_vni), which
    manages a single VNI per task.
notes:
  - The display format of the C(evpn) section has not been verified on hardware.
  - Unsupported for Cisco MDS.
  - C(nv overlay evpn) must be enabled for the C(evpn) section to be available.
  - C(route_target_both) is an input convenience. It is expanded into
    I(route_target_import) and I(route_target_export) before comparing with the
    device and is never returned by C(gathered) or C(parsed). If the device
    displays C(route-target both), it is parsed as an import and an export.
  - Under I(merged), route targets are only added and the route distinguisher
    is only replaced, nothing is removed.
  - Under I(replaced) and I(overridden), route targets and the route
    distinguisher of a listed VNI that are not in I(config) are removed.
  - Layer 3 VNIs (C(vni <id> l3) under C(vrf context)) are not managed by this module.
  - This module works with connection C(network_cli) and C(httpapi).
  - The I(parsed) state reads configuration from C(running_config) and does
    not connect to the device.
author:
  - Jorgen Spange (@jorgenspange)
options:
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device
        by executing the command B(show running-config | section ^evpn).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description:
      - A list of EVPN VNI configurations.
    type: list
    elements: dict
    suboptions:
      vni:
        description:
          - The Layer 2 VNI identifier.
        type: int
        required: true
      route_distinguisher:
        description:
          - Route distinguisher of the VNI, either C(auto) or in the form C(ASN:NN) or C(IP:NN).
        type: str
      route_target_import:
        description:
          - Route targets to import, C(auto) or in the form C(ASN:NN) or C(IP:NN).
        type: list
        elements: str
      route_target_export:
        description:
          - Route targets to export, C(auto) or in the form C(ASN:NN) or C(IP:NN).
        type: list
        elements: str
      route_target_both:
        description:
          - Route targets to both import and export, C(auto) or in the form C(ASN:NN) or C(IP:NN).
          - Merged into I(route_target_import) and I(route_target_export).
        type: list
        elements: str
  state:
    description:
      - The state the configuration should be left in.
      - With I(deleted), the VNIs listed in I(config) are removed, or all VNIs when I(config) is not given.
      - With I(overridden), VNIs that are not listed in I(config) are removed.
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
# nxos# show running-config | section ^evpn
# evpn
#   vni 10100 l2
#     rd auto

- name: Merge the provided configuration with the existing running configuration
  cisco.nxos.nxos_evpn_vnis:
    config:
      - vni: 10100
        route_target_both:
          - auto
      - vni: 10200
        route_distinguisher: 65000:10200
        route_target_import:
          - 65000:10200
        route_target_export:
          - 65000:10200
    state: merged

# Task output:
# ------------
# commands:
#   - evpn
#   - vni 10100 l2
#   - route-target import auto
#   - route-target export auto
#   - vni 10200 l2
#   - rd 65000:10200
#   - route-target import 65000:10200
#   - route-target export 65000:10200

# After state:
# ------------
# nxos# show running-config | section ^evpn
# evpn
#   vni 10100 l2
#     rd auto
#     route-target import auto
#     route-target export auto
#   vni 10200 l2
#     rd 65000:10200
#     route-target import 65000:10200
#     route-target export 65000:10200

# Using replaced

# Before state:
# -------------
# evpn
#   vni 10100 l2
#     rd auto
#     route-target import auto
#     route-target export auto
#   vni 10200 l2
#     rd 65000:10200

- name: Replace the configuration of the listed VNIs only
  cisco.nxos.nxos_evpn_vnis:
    config:
      - vni: 10100
        route_distinguisher: auto
        route_target_import:
          - 65000:10100
    state: replaced

# Task output:
# ------------
# commands:
#   - evpn
#   - vni 10100 l2
#   - no route-target import auto
#   - no route-target export auto
#   - route-target import 65000:10100

# Using overridden

# Before state:
# -------------
# evpn
#   vni 10100 l2
#     rd auto
#   vni 10200 l2
#     rd 65000:10200

- name: Override all VNIs with the provided configuration
  cisco.nxos.nxos_evpn_vnis:
    config:
      - vni: 10100
        route_distinguisher: auto
    state: overridden

# Task output:
# ------------
# commands:
#   - evpn
#   - no vni 10200 l2

# Using deleted

# Before state:
# -------------
# evpn
#   vni 10100 l2
#     rd auto
#   vni 10200 l2
#     rd 65000:10200

- name: Delete the listed VNIs (omit config to delete all of them)
  cisco.nxos.nxos_evpn_vnis:
    config:
      - vni: 10100
    state: deleted

# Task output:
# ------------
# commands:
#   - evpn
#   - no vni 10100 l2

# Using rendered

- name: Render platform specific configuration lines (without connecting to the device)
  cisco.nxos.nxos_evpn_vnis:
    config:
      - vni: 10100
        route_distinguisher: auto
        route_target_both:
          - auto
    state: rendered

# Task Output (redacted)
# -----------------------
# rendered:
#   - evpn
#   - vni 10100 l2
#   - rd auto
#   - route-target import auto
#   - route-target export auto

# Using parsed

# parsed.cfg
# ------------
# evpn
#   vni 10100 l2
#     rd auto
#     route-target import auto
#     route-target export auto

- name: Parse the provided configuration
  cisco.nxos.nxos_evpn_vnis:
    running_config: "{{ lookup('file', 'parsed.cfg') }}"
    state: parsed

# Task output (redacted)
# -----------------------
# parsed:
#   - vni: 10100
#     route_distinguisher: auto
#     route_target_import:
#       - auto
#     route_target_export:
#       - auto

# Using gathered

- name: Gather the VNI configuration from the device
  cisco.nxos.nxos_evpn_vnis:
    state: gathered

# Task output (redacted)
# -----------------------
# gathered:
#   - vni: 10100
#     route_distinguisher: auto
#     route_target_import:
#       - auto
#     route_target_export:
#       - auto
"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
commands:
  description: The set of commands pushed to the remote device.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - evpn
    - vni 10100 l2
    - rd auto
    - route-target import auto
rendered:
  description: The provided configuration rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - evpn
    - vni 10100 l2
    - rd auto
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when I(state) is C(gathered)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
parsed:
  description: The device native config provided in I(running_config) option, parsed into structured data.
  returned: when I(state) is C(parsed)
  type: list
  sample: >
    This output will always be in the same format as the module argspec.
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.evpn_vnis.evpn_vnis import (
    Evpn_vnisArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.evpn_vnis.evpn_vnis import (
    Evpn_vnis,
)


def main():
    """
    Main entry point for module execution.

    :returns: the result from module invocation
    """
    module = AnsibleModule(
        argument_spec=Evpn_vnisArgs.argument_spec,
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

    result = Evpn_vnis(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
