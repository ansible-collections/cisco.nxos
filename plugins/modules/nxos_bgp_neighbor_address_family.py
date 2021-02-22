#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_bgp_neighbor_address_family
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_bgp_neighbor_address_family
short_description: BGP Neighbor Address Family resource module.
description:
- This module manages BGP Neighbor Address Family configuration on devices running Cisco NX-OS.
version_added: 2.0.0
notes:
- Tested against NX-OS 9.3.6.
- For managing BGP address family configurations please use
  the M(cisco.nxos.nxos_bgp_address_family) module.
- This module works with connection C(network_cli) and C(httpapi).
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section '^router bgp').
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: BGP Neighbor AF configuration.
    type: dict
    suboptions:
      as_number:
        description: Autonomous System Number of the router.
        type: str
      neighbors: &nbr
        description: A list of BGP Neighbor AF configuration.
        type: list
        elements: dict
        suboptions:
          neighbor:
            description: IP/IPv6 address of the neighbor.
            type: str
            required: True
          address_family:
            description: BGP Neighbor Address Family related configurations.
            type: list
            elements: dict
            suboptions:
              afi:
                description: Address Family indicator.
                type: str
                choices: ["ipv4", "ipv6", "link-state", "vpnv4", "vpnv6", "l2vpn"]
                required: True
              safi:
                description: Sub Address Family indicator.
                type: str
                choices: ["unicast", "multicast", "mvpn", "evpn"]
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
                  in:
                    description: Apply policy to incoming routes.
                    type: str
                  out:
                    description: Apply policy to outgoing routes.
                    type: str
              inherit:
                description: Inherit a template.
                type: dict
                suboptions:
                  template:
                    description: Template name.
                    type: str
                  sequence:
                    description: Sequence number.
                    type: int
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
                  in:
                    description: Apply policy to incoming routes.
                    type: str
                  out:
                    description: Apply policy to outgoing routes.
                    type: str
              rewrite_evpn_rt_asn:
                description: Auto generate RTs for EBGP neighbor.
                type: bool
              route_map:
                description: Apply route-map to neighbor.
                type: dict
                suboptions:
                  in:
                    description: Apply policy to incoming routes.
                    type: str
                  out:
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
      vrfs:
        description: Virtual Router Context.
        type: list
        elements: dict
        suboptions:
          vrf:
            description: VRF name.
            type: str
          neighbors: *nbr
  state:
    description:
    - The state the configuration should be left in.
    - State I(deleted) only removes BGP attributes that this modules
      manages and does not negate the BGP process completely.
    - Refer to examples for more details.
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - parsed
    - gathered
    - rendered
    default: merged
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_neighbor_address_family.bgp_neighbor_address_family import (
    Bgp_neighbor_address_familyArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.bgp_neighbor_address_family.bgp_neighbor_address_family import (
    Bgp_neighbor_address_family,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_neighbor_address_familyArgs.argument_spec,
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

    result = Bgp_neighbor_address_family(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
