#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_bgp_templates
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
module: nxos_bgp_templates
short_description: BGP Templates resource module.
description:
- This module manages BGP templates on devices running Cisco NX-OS.
version_added: 4.2.0
notes:
- Tested against NX-OS 9.3.6.
- Unsupported for Cisco MDS
- This module works with connection C(network_cli) and C(httpapi).
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config bgp | section 'template').
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of BGP templates.
    type: dict
    suboptions:
      peers:
        description: Configure BGP peer templates.
        type: list
        elements: dict
        suboptions:
          name:
            description: Name of the BGP peer template.
            type: str
          address_family:
            description: Configure an address-family for peer.
            type: list
            elements: dict
            suboptions:
              afi:
                description: Address Family indicator.
                type: str
                choices: ["ipv4", "ipv6", "link-state", "l2vpn"]
                required: True
              safi:
                description: Sub Address Family indicator.
                type: str
                choices: ["unicast", "multicast", "mvpn"]
              advertise_map:
                description: Specify route-map for conditional advertisement.
                type: dict
                suboptions:
                  route_map:
                    description: Route-map name.
                    type: str
                    required: True
                  exist_map:
                    description: Condition route-map to advertise only when prefix in condition exists.
                    type: str
                  non_exist_map:
                    description: Condition route-map to advertise only when prefix in condition does not exist.
                    type: str
              advertisement_interval:
                description: Minimum interval between sending BGP routing updates.
                type: int
              allowas_in:
                description: Accept as-path with my AS present in it.
                type: dict
                suboptions:
                  set:
                    description: Activate allowas-in property.
                    type: bool
                  max_occurences:
                    description: Number of occurrences of AS number, default is 3.
                    type: int
              as_override:
                description: Override matching AS-number while sending update.
                type: bool
              capability:
                description: Advertise capability to the peer.
                type: dict
                suboptions:
                  additional_paths:
                    description: Additional paths capability.
                    type: dict
                    suboptions:
                      receive:
                        description: Additional paths Receive capability.
                        type: str
                        choices: ["enable", "disable"]
                      send:
                        description: Additional paths Send capability.
                        type: str
                        choices: ["enable", "disable"]
              default_originate:
                description: Originate a default toward this peer.
                type: dict
                suboptions:
                  set:
                    description: Set default-originate attribute.
                    type: bool
                  route_map:
                    description: Route-map to specify criteria for originating default.
                    type: str
              disable_peer_as_check:
                description: Disable checking of peer AS-number while advertising.
                type: bool
              filter_list:
                description: Name of filter-list.
                type: dict
                suboptions:
                  inbound:
                    description: Apply policy to incoming routes.
                    type: str
                  outbound:
                    description: Apply policy to outgoing routes.
                    type: str
              inherit:
                description: Inherit a template.
                type: dict
                suboptions:
                  peer_session:
                    description: Peer-session template to inherit.
                    type: str
              maximum_prefix:
                description: Maximum number of prefixes from this neighbor.
                type: dict
                suboptions:
                  max_prefix_limit:
                    description: Maximum prefix limit.
                    type: int
                  generate_warning_threshold:
                    description: Threshold percentage at which to generate a warning.
                    type: int
                  restart_interval:
                    description: Restart bgp connection after limit is exceeded.
                    type: int
                  warning_only:
                    description: Only give a warning message when limit is exceeded.
                    type: bool
              next_hop_self:
                description: Set our address as nexthop (non-reflected).
                type: dict
                suboptions:
                  set:
                    description: Set next-hop-self attribute.
                    type: bool
                  all_routes:
                    description: Set our address as nexthop for all routes.
                    type: bool
              next_hop_third_party:
                description: Compute a third-party nexthop if possible.
                type: bool
              prefix_list:
                description: Apply prefix-list.
                type: dict
                suboptions:
                  inbound:
                    description: Apply policy to incoming routes.
                    type: str
                  outbound:
                    description: Apply policy to outgoing routes.
                    type: str
              route_map:
                description: Apply route-map to neighbor.
                type: dict
                suboptions:
                  inbound:
                    description: Apply policy to incoming routes.
                    type: str
                  outbound:
                    description: Apply policy to outgoing routes.
                    type: str
              route_reflector_client:
                description: Configure a neighbor as Route reflector client.
                type: bool
              send_community:
                description: Send Community attribute to this neighbor.
                type: dict
                suboptions:
                  set:
                    description: Set send-community attribute.
                    type: bool
                  extended:
                    description: Send Extended Community attribute.
                    type: bool
                  standard:
                    description: Send Standard Community attribute.
                    type: bool
                  both:
                    description: Send Standard and Extended Community attributes.
                    type: bool
              soft_reconfiguration_inbound:
                description: Soft reconfiguration.
                type: dict
                suboptions:
                  set:
                    description: Set soft-reconfiguration inbound attribute.
                    type: bool
                  always:
                    description: Always perform inbound soft reconfiguration.
                    type: bool
              soo:
                description: Specify Site-of-origin extcommunity.
                type: str
              suppress_inactive:
                description: Advertise only active routes to peer.
                type: bool
              unsuppress_map:
                description: Route-map to selectively unsuppress suppressed routes.
                type: str
              weight:
                description: Set default weight for routes from this neighbor.
                type: int
          bfd:
            description: Bidirectional Fast Detection for the neighbor.
            type: dict
            suboptions:
              set:
                description: Set BFD for this neighbor.
                type: bool
              singlehop:
                description: Single-hop session.
                type: bool
              multihop:
                description: Multihop session.
                type: dict
                suboptions:
                  set:
                    description: Set BFD multihop.
                    type: bool
                  interval:
                    description: Configure BFD session interval parameters.
                    type: dict
                    suboptions:
                      tx_interval:
                        description: TX interval in milliseconds.
                        type: int
                      min_rx_interval:
                        description: Minimum RX interval.
                        type: int
                      multiplier:
                        description: Detect Multiplier.
                        type: int
          bmp_activate_server:
            description: Specify server ID for activating BMP monitoring for the peer.
            type: int
          capability:
            description: Capability.
            type: dict
            suboptions:
              suppress_4_byte_as:
                description: Suppress 4-byte AS Capability.
                type: bool
          description:
            description: Neighbor specific descripion.
            type: str
          disable_connected_check:
            description: Disable check for directly connected peer.
            type: bool
          dont_capability_negotiate:
            description: Don't negotiate capability with this neighbor.
            type: bool
          dscp:
            description: Set dscp value for tcp transport.
            type: str
          dynamic_capability:
            description: Dynamic Capability
            type: bool
          ebgp_multihop:
            description: Specify multihop TTL for remote peer.
            type: int
          graceful_shutdown:
            description: Graceful-shutdown for this neighbor.
            type: dict
            suboptions:
              activate:
                description: Send graceful-shutdown community.
                type: dict
                suboptions:
                  set:
                    description: Set activate.
                    type: bool
                  route_map:
                    description: Apply route-map to modify attributes for outbound.
                    type: str
          inherit:
            description: Inherit a template.
            type: dict
            suboptions:
              peer_session:
                description: Peer-session template to inherit.
                type: str
          local_as:
            description: Specify the local-as number for the eBGP neighbor.
            type: str
          log_neighbor_changes:
            description: Log message for neighbor up/down event.
            type: dict
            suboptions:
              set:
                description:
                - Set log-neighbor-changes.
                type: bool
              disable:
                description:
                - Disable logging of neighbor up/down event.
                type: bool
          low_memory:
            description: Behaviour in low memory situations.
            type: dict
            suboptions:
              exempt:
                description: Do not shutdown this peer when under memory pressure.
                type: bool
          password:
            description: Configure a password for neighbor.
            type: dict
            suboptions:
              encryption:
                description:
                - 0 specifies an UNENCRYPTED neighbor password.
                - 3 specifies an 3DES ENCRYPTED neighbor password will follow.
                - 7 specifies a Cisco type 7  ENCRYPTED neighbor password will follow.
                type: int
              key:
                description: Authentication password.
                type: str
          path_attribute:
            description: BGP path attribute optional filtering.
            type: list
            elements: dict
            suboptions:
              action:
                description: Action.
                type: str
                choices: ["discard", "treat-as-withdraw"]
              type:
                description: Path attribute type
                type: int
              range:
                description: Path attribute range.
                type: dict
                suboptions:
                  start:
                    description: Path attribute range start value.
                    type: int
                  end:
                    description: Path attribute range end value.
                    type: int
          remote_as:
            description: Specify Autonomous System Number of the neighbor.
            type: str
          remove_private_as:
            description: Remove private AS number from outbound updates.
            type: dict
            suboptions:
              set:
                description: Remove private AS.
                type: bool
              replace_as:
                description: Replace.
                type: bool
              all:
                description: All.
                type: bool
          shutdown:
            description: Administratively shutdown this neighbor.
            type: bool
          timers:
            description: Configure keepalive and hold timers.
            type: dict
            suboptions:
              keepalive:
                description: Keepalive interval (seconds).
                type: int
              holdtime:
                description: Holdtime (seconds).
                type: int
          transport:
            description: BGP transport connection.
            type: dict
            suboptions:
              connection_mode:
                description: Specify type of connection.
                type: dict
                suboptions:
                  passive:
                    description: Allow passive connection setup only.
                    type: bool
          ttl_security:
            description: Enable TTL Security Mechanism.
            type: dict
            suboptions:
              hops:
                description: Specify hop count for remote peer.
                type: int
          update_source:
            description: Specify source of BGP session and updates.
            type: str
  state:
    description:
    - The state the configuration should be left in.
    - Refer to examples for more details.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - purged
    - parsed
    - gathered
    - rendered
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

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_templates.bgp_templates import (
    Bgp_templatesArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.bgp_templates.bgp_templates import (
    Bgp_templates,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_templatesArgs.argument_spec,
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

    result = Bgp_templates(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
