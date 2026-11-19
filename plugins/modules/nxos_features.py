# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""The module file for nxos_features"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_features
short_description: Features resource module.
description:
  - This module manages the features of a device running Cisco NX-OS, the C(feature) commands of the
    global configuration, for example C(feature bgp) or C(feature nv overlay).
  - It enables and disables several features in one task and makes the set of enabled features
    declarative, with the states I(overridden) and I(deleted).
version_added: 14.1.0
author:
  - Jørgen Spange (@jorgenspange)
notes:
  - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
  - Unsupported for Cisco MDS.
  - B(Disabling a feature removes all configuration that depends on it.) Disabling C(bgp) removes
    the BGP configuration, disabling C(interface-vlan) removes the SVIs. A feature that provides the
    access to the device, for example C(ssh), C(tacacs+) or C(nxapi), can lock you out. Use the check mode
    before I(overridden) and I(deleted).
  - The module reads the C(feature) and C(no feature) lines of C(show running-config all). The plain
    running configuration hides the features that are enabled by default, for example C(ssh).
    The device lists only the features that have such a line, so I(gathered) does not return every feature
    of C(show feature). The names of C(show feature) are internal and differ from the names of the
    commands, for example C(nve) for C(feature nv overlay) and C(vnseg_vlan) for
    C(feature vn-segment-vlan-based), so they cannot be used.
  - The names are the ones of the C(feature) command, exactly as they are written in the
    configuration, for example C(nv overlay), C(vn-segment-vlan-based), C(tacacs+) or
    C(password encryption aes). The set of features depends on the platform and the license,
    so the names are not restricted.
  - A feature is either enabled or disabled, so I(merged) and I(replaced) behave the same.
  - The commands that enable a feature are sent in the order of I(config), the commands that disable a
    feature after them. List a feature before the features that depend on it, for example
    C(nv overlay) before C(vn-segment-vlan-based).
  - The feature sets (C(install feature-set) and C(feature-set)) are not managed.
  - M(cisco.nxos.nxos_feature) manages one feature per task and stays available.
options:
  config:
    description: The features.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The name of the feature as written in the C(feature) command, for example C(bgp),
            C(interface-vlan), C(nv overlay) or C(tacacs+).
        type: str
        required: true
      enabled:
        description:
          - Enable (C(true)) or disable (C(false)) the feature.
        type: bool
        default: true
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the NX-OS device by
        executing the command B(show running-config all | include '^feature|^no feature'),
        or the full running configuration.
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
    type: str
  state:
    description:
      - The state the configuration should be left in.
      - With I(merged) and I(replaced) the features of I(config) are enabled or disabled. Other features
        are not touched.
      - With I(overridden) the features of I(config) are enabled or disabled and every other enabled
        feature is disabled. This removes the configuration that depends on those features.
      - With I(deleted) the features listed in I(config) are disabled, the value of I(enabled) is ignored.
        Without I(config) B(every enabled feature is disabled), also those that give access to
        the device.
      - With I(rendered) the commands for I(config) are returned and nothing is sent to the device.
      - With I(gathered) the features are read from the device and returned in I(gathered).
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
# switch# show running-config | include ^feature
# feature bgp
# feature interface-vlan

- name: Enable and disable features
  cisco.nxos.nxos_features:
    config:
      - name: nv overlay
        enabled: true
      - name: vn-segment-vlan-based
        enabled: true
      - name: interface-vlan
        enabled: false
    state: merged

# Task output:
# ------------
# before:
#   - name: bgp
#     enabled: true
#   - name: interface-vlan
#     enabled: true
#
# commands:
#   - feature nv overlay
#   - feature vn-segment-vlan-based
#   - no feature interface-vlan
#
# after:
#   - name: bgp
#     enabled: true
#   - name: nv overlay
#     enabled: true
#   - name: vn-segment-vlan-based
#     enabled: true

# Using replaced

# Before state:
# -------------
# switch# show running-config | include ^feature
# feature bgp
# feature interface-vlan
# feature lacp

- name: Set the state of the listed features, a feature that is not listed stays as it is
  cisco.nxos.nxos_features:
    config:
      - name: bgp
        enabled: true
      - name: interface-vlan
        enabled: false
      - name: nv overlay
        enabled: true
    state: replaced

# Task output:
# ------------
# before:
#   - name: bgp
#     enabled: true
#   - name: interface-vlan
#     enabled: true
#   - name: lacp
#     enabled: true
#
# commands:
#   - feature nv overlay
#   - no feature interface-vlan
#
# after:
#   - name: bgp
#     enabled: true
#   - name: lacp
#     enabled: true
#   - name: nv overlay
#     enabled: true

# Using overridden

# Before state:
# -------------
# switch# show running-config | include ^feature
# feature bgp
# feature interface-vlan
# feature lacp

- name: Make bgp and lacp the only enabled features
  cisco.nxos.nxos_features:
    config:
      - name: bgp
        enabled: true
      - name: lacp
        enabled: true
    state: overridden

# Task output:
# ------------
# commands:
#   - no feature interface-vlan

# Using deleted

- name: Disable the listed features
  cisco.nxos.nxos_features:
    config:
      - name: bash-shell
      - name: scp-server
    state: deleted

# Using gathered

- name: Gather the features
  cisco.nxos.nxos_features:
    state: gathered

# Task output:
# ------------
# gathered:
#   - name: bgp
#     enabled: true
#   - name: nxapi
#     enabled: false
#   - name: ssh
#     enabled: true

# Using rendered

- name: Render the commands
  cisco.nxos.nxos_features:
    config:
      - name: bgp
        enabled: true
      - name: bash-shell
        enabled: false
    state: rendered

# Task output:
# ------------
# rendered:
#   - feature bgp
#   - no feature bash-shell

# Using parsed

- name: Parse the feature lines
  cisco.nxos.nxos_features:
    running_config: |
      feature ssh
      no feature nxapi
      feature nv overlay
    state: parsed

# Task output:
# ------------
# parsed:
#   - name: nv overlay
#     enabled: true
#   - name: nxapi
#     enabled: false
#   - name: ssh
#     enabled: true
"""

RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
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
  returned: when I(state) is C(merged), C(replaced), C(overridden) or C(deleted)
  type: list
  sample:
    - feature nv overlay
    - feature vn-segment-vlan-based
    - no feature interface-vlan
rendered:
  description: The provided configuration in the task rendered in device-native format (offline).
  returned: when I(state) is C(rendered)
  type: list
  sample:
    - feature bgp
    - no feature bash-shell
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

from ansible.module_utils.basic import (
    AnsibleModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.features.features import (
    FeaturesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.features.features import (
    Features,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=FeaturesArgs.argument_spec,
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

    result = Features(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
