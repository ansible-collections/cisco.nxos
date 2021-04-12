#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_route_maps
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_route_maps
short_description: Route Maps resource module.
description:
- This module manages route maps configuration on devices running Cisco NX-OS.
version_added: 2.2.0
notes:
- Tested against NX-OS 9.3.6.
- This module works with connection C(network_cli) and C(httpapi).
author: Nilashish Chakraborty (@NilashishC)
options:
  running_config:
    description:
    - This option is used only with state I(parsed).
    - The value of this option should be the output received from the NX-OS device
      by executing the command B(show running-config | section '^route-map').
    - The state I(parsed) reads the configuration from C(running_config) option and
      transforms it into Ansible structured data as per the resource module's argspec
      and the value is then returned in the I(parsed) key within the result.
    type: str
  config:
    description: A list of route-map configuration.
    type: list
    elements: dict
    suboptions:
      route_map:
        description: Route-map name.
        type: str
      entries:
        description: List of entries (identified by sequence number) for this route-map.
        type: list
        elements: dict
        suboptions:
          sequence:
            description: Sequence to insert to/delete from existing route-map entry.
            type: int
          action:
            description: Route map denies or permits set operations.
            type: str
            choices: ["deny", "permit"]
          continue:
            description: Continue on a different entry within the route-map.
            type: int
          description:
            description: Description of the route-map.
            type: str
          match:
            description: Match values from routing table.
            type: dict
            suboptions:
              as_number:
                description: Match BGP peer AS number.
                type: dict
                suboptions:
                  asn:
                    description: AS number.
                    type: str
                  as_path_list:
                    description: AS path access list name.
                    type: str
              as_path:
                description: Match BGP AS path list.
                type: str
              community:
                description: Match BGP community list.
                type: dict
                suboptions:
                  community_list:
                    description: Community list.
                    type: list
                    elements: str
                  exact_match:
                    description: Do exact matching of communities.
                    type: bool
              evpn:
                description: Match BGP EVPN Routes.
                type: dict
                suboptions:
                  route_type:
                    description: Match route type for evpn route.
                    type: list
                    elements: str
              extcommunity:
                description: Match BGP community list.
                type: dict
                suboptions:
                  extcommunity_list:
                    description: Extended Community list.
                    type: list
                    elements: str
                  exact_match:
                    description: Do exact matching of extended communities.
                    type: bool
              interfaces:
                description: Match first hop interface of route.
                type: list
                elements: str
              ip:
                description: Configure IP specific information.
                type: dict
                suboptions: &id001
                  address:
                    description: Match address of route or match packet.
                    type: dict
                    suboptions:
                      access_list:
                        description: IP access-list name (for use in route-maps for PBR only).
                        type: str
                      prefix_lists:
                        description: Match entries of prefix-lists.
                        type: list
                        elements: str
                  multicast:
                    description: Match multicast attributes.
                    type: dict
                    suboptions:
                      group:
                        description: Multicast Group prefix.
                        type: dict
                        suboptions:
                          prefix:
                            description: IPv4 group prefix.
                            type: str
                          rp: &rp
                            description: Rendezvous point.
                            type: dict
                            suboptions:
                              prefix:
                                description: IPv4 rendezvous prefix.
                                type: str
                              rp_type:
                                description: Multicast rendezvous point type.
                                type: str
                                choices: ["ASM", "Bidir"]
                          source: &source
                            description: Multicast source address.
                            type: str
                      group_range:
                        description: Multicast Group address range.
                        type: dict
                        suboptions:
                          first:
                            description: First Group address.
                            type: str
                          last:
                            description: Last Group address.
                            type: str
                          rp: *rp
                          source: *source
                  next_hop:
                    description: Match next-hop address of route.
                    type: dict
                    suboptions:
                      prefix_lists:
                        description: Match entries of prefix-lists.
                        type: list
                        elements: str
                  route_source:
                    description: Match advertising source address of route.
                    type: dict
                    suboptions:
                      prefix_lists:
                        description: Match entries of prefix-lists.
                        type: list
                        elements: str
              ipv6:
                description: Configure IPv6 specific information.
                type: dict
                suboptions: *id001
              mac_list:
                description: Match entries of mac-lists.
                type: list
                elements: str
              metric:
                description: Match metric of route.
                type: list
                elements: int
              ospf_area:
                description: Match ospf area.
                type: list
                elements: int
              route_type:
                description: Match route-type of route.
                type: list
                elements: str
                choices: ["external", "inter-area", "internal", "intra-area", "level-1", "level-2", "local", "nssa-external", "type-1", "type-2"]
              source_protocol:
                description: Match source protocol.
                type: list
                elements: str
              tags:
                description: Match tag of route.
                type: list
                elements: int
          set:
            description: Set values in destination routing protocol.
            type: dict
            suboptions:
              as_path:
                description: Prepend string for a BGP AS-path attribute.
                type: dict
                suboptions:
                  prepend:
                    description: Prepend to the AS-Path.
                    type: dict
                    suboptions:
                      as_number:
                        description: AS number.
                        type: list
                        elements: str
                      last_as:
                        description: Number of last-AS prepends.
                        type: int
                  tag:
                    description: Set the tag as an AS-path attribute.
                    type: bool
              comm_list:
                description: Set BGP community list (for deletion).
                type: str
              community:
                description: Set BGP community attribute.
                type: dict
                suboptions:
                  additive:
                    description: Add to existing community.
                    type: bool
                  graceful_shutdown:
                    description: Graceful Shutdown (well-known community).
                    type: bool
                  internet:
                    description: Internet (well-known community).
                    type: bool
                  local_as:
                    description: Do not send outside local AS (well-known community).
                    type: bool
                  no_advertise:
                    description: Do not advertise to any peer (well-known community).
                    type: bool
                  no_export:
                    description: Do not export to next AS (well-known community).
                    type: bool
                  number:
                    description: "Community number aa:nn format"
                    type: list
                    elements: str
              dampening:
                description: Set BGP route flap dampening parameters.
                type: dict
                suboptions:
                  half_life:
                    description: Half-life time for the penalty.
                    type: int
                  start_reuse_route:
                    description: Value to start reusing a route.
                    type: int
                  start_suppress_route:
                    description: Value to start suppressing a route.
                    type: int
                  max_suppress_time:
                    description: Maximum suppress time for stable route.
                    type: int
              distance:
                description: Configure administrative distance.
                type: dict
                suboptions:
                  igp_ebgp_routes:
                    description: Administrative distance for IGP or EBGP routes
                    type: int
                  internal_routes:
                    description: Distance for internal routes.
                    type: int
                  local_routes:
                    description: Distance for local routes.
                    type: int
              evpn:
                description: Set BGP EVPN Routes.
                type: dict
                suboptions:
                  gateway_ip:
                    description:
                      - Set gateway IP for type 5 EVPN routes.
                      - Cannot set ip and use-nexthop gateway-ip in the same route-map sequence.
                    type: dict
                    suboptions:
                      ip:
                        description: Gateway IP address.
                        type: str
                      use_nexthop:
                        description: Use nexthop address as gateway IP.
                        type: bool
              extcomm_list:
                description: Set BGP extcommunity list (for deletion).
                type: str
              forwarding_address:
                description: Set the forwarding address.
                type: bool
              null_interface:
                description: Output Null interface.
                type: str
              ip:
                description: Configure IP features.
                type: dict
                suboptions: &id002
                  address:
                    description: Specify IP address.
                    type: dict
                    suboptions:
                      prefix_list:
                        description: Name of prefix list (Max Size 63).
                        type: str
                  precedence:
                    description: Set precedence field.
                    type: str
              ipv6:
                description: Configure IPv6 features.
                type: dict
                suboptions: *id002
              label_index:
                description: Set Segment Routing (SR) label index of route.
                type: int
              level:
                description: Where to import route.
                type: str
                choices: ["level-1", "level-1-2", "level-2"]
              local_preference:
                description: BGP local preference path attribute.
                type: int
              metric:
                description: Set metric for destination routing protocol.
                type: dict
                suboptions:
                  bandwidth:
                    description: Metric value or Bandwidth in Kbits per second (Max Size 11).
                    type: int
                  igrp_delay_metric:
                    description: IGRP delay metric.
                    type: int
                  igrp_reliability_metric:
                    description: IGRP reliability metric where 255 is 100 percent reliable.
                    type: int
                  igrp_effective_bandwidth_metric:
                    description: IGRP Effective bandwidth metric (Loading) 255 is 100%.
                    type: int
                  igrp_mtu:
                    description: IGRP MTU of the path.
                    type: int
              metric_type:
                description: Type of metric for destination routing protocol.
                type: str
                choices: ["external", "internal", "type-1", "type-2"]
              nssa_only:
                description: OSPF NSSA Areas.
                type: bool
              origin:
                description: BGP origin code.
                type: str
                choices: ["egp", "igp", "incomplete"]
              path_selection:
                description: Path selection criteria for BGP.
                type: str
                choices: ["all", "backup", "best2", "multipaths"]
              tag:
                description: Tag value for destination routing protocol.
                type: int
              weight:
                description: BGP weight for routing table.
                type: int
  state:
    description:
    - The state the configuration should be left in.
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.route_maps.route_maps import (
    Route_mapsArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.route_maps.route_maps import (
    Route_maps,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Route_mapsArgs.argument_spec,
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

    result = Route_maps(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
