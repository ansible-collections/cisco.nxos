#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_bgp_address_family
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_bgp_address_family
short_description: BGP Address Family resource module.
description:
- This module manages BGP Address Family configuration on devices running Cisco NX-OS.
version_added: 2.0.0
notes:
- Tested against NX-OS 9.3.6.
- For managing BGP neighbor address family configurations please use
  the M(cisco.nxos.nxos_bgp_neighbor_address_family) module.
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
    description: A list of BGP process configuration.
    type: dict
    suboptions:
      as_number:
        description: Autonomous System Number of the router.
        type: str
      address_family:
        description: Address Family related configurations.
        type: list
        elements: dict
        suboptions:
          afi:
            description: Address Family indicator.
            type: str
            choices: ["ipv4", "ipv6", "link-state", "vpnv4", "vpnv6"]
            required: True
          safi:
            description: Sub Address Family indicator.
            type: str
            choices: ["unicast", "multicast", "mvpn"]
          additional_paths:
            description: Additional paths configuration.
            type: dict
            suboptions:
              install_backup: 
                description: Install backup path.
                type: bool
              receive:
                description: Additional paths Receive capability.
                type: bool
              selection:
                description: Additional paths selection
                type: dict
                suboptions:
                  route_map:
                    description: Route-map for additional paths selection
                    type: str
              send:
                description: Additional paths Send capability
                type: bool
          aggregate_address:
            description: Configure BGP aggregate prefixes
            type: list
            elements: dict
            suboptions:
              prefix: 
                description: Aggregate prefix.
                type: str
              advertise_map:
                description: Select attribute information from specific routes.
                type: str
              as_set:
                description: Generate AS-SET information.
                type: bool
              attribute_map:
                description: Set attribute information of aggregate.
                type: str
              summary_only:
                description: Do not advertise more specifics.
                type: bool
              suppress_map:
                description: Conditionally filter more specific routes.
                type: str
          client_to_client:
            description: Configure client-to-client route reflection.
            type: dict
            suboptions:
              reflection:
                description: Reflection of routes permitted.
                type: bool
          dampen_igp_metric:
            description: Dampen IGP metric-related changes.
            type: int
          dampening:
            description: Configure route flap dampening.
            type: dict
            suboptions:
              set:
                description: Set route flap dampening.
                type: bool
              decay_half_life:
                description: Decay half life.
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
              route_map:
                description: Apply route-map to specify dampening criteria.
                type: str
          default_information:
            description: Control distribution of default information.
            type: dict
            suboptions:
              originate:
                description: Distribute a default route.
                type: bool
          default_metric:
            description: Set metric of redistributed routes.
            type: int
          distance:
            description: Configure administrative distance.
            type: dict
            suboptions:
              ebgp_routes:
                description: Distance for EBGP routes.
                type: int
              ibgp_routes:
                description: Distance for IBGP routes.
                type: int
              local_routes:
                description: Distance for local routes.
                type: int
          export_gateway_ip:
            description: Export Gateway IP to Type-5 EVPN routes for VRF
            type: bool
          inject_map:
            description: Routemap which specifies prefixes to inject.
            type: list
            elements: dict
            suboptions:
              route_map:
                description: Route-map name.
                type: str
              exist_map:
                description: Routemap which specifies exist condition.
                type: str
              copy_attributes:
                description: Copy attributes from aggregate.
                type: bool
          maximum_paths:
            description: Forward packets over multipath paths.
            type: dict
            suboptions:
              parallel_paths:
                description: Number of parallel paths.
                type: int
              ibgp:
                description: Configure multipath for IBGP paths.
                type: dict
                suboptions:
                  parallel_paths:
                    description:  Number of parallel paths.
                    type: int
              eibgp:
                description: Configure multipath for both EBGP and IBGP paths.
                type: dict
                suboptions:
                  parallel_paths:
                    description:  Number of parallel paths.
                    type: int
              local:
                description: Configure multipath for local paths.
                type: dict
                suboptions:
                  parallel_paths:
                    description:  Number of parallel paths.
                    type: int
              mixed:
                description: Configure multipath for local and remote paths.
                type: dict
                suboptions:
                  parallel_paths:
                    description:  Number of parallel paths.
                    type: int
          network:
            description: Configure an IP prefix to advertise.
            type: list
            elements: dict
            suboptions:
              prefix:
                description: IP prefix in CIDR format.
                type: str
              route_map:
                description: Route-map name.
                type: str
          nexthop:
            description: Nexthop tracking.
            type: dict
            suboptions:
              route_map:
                description: Route-map name.
                type: str
              trigger_delay:
                description: Set the delay to trigger nexthop tracking.
                type: dict
                suboptions:
                  critical_delay:
                    description:
                    - Nexthop changes affecting reachability.
                    - Delay value (miliseconds).
                    type: int
                  non_critical_delay:
                    description:
                    - Other nexthop changes.
                    - Delay value (miliseconds).
                    type: int
          redistribute:
            description: Configure redistribution.
            type: list
            elements: dict
            suboptions:
              protocol:
                description:
                - The name of the protocol.
                type: str
                choices: ["am", "direct", "eigrp", "isis", "lisp", "ospf", "rip", "static"]
                required: true
              id:
                description:
                - The identifier for the protocol specified.
                type: str
              route_map:
                description:
                - The route map policy to constrain redistribution.
                type: str
                required: true
          retain:
            description: Retain the routes based on Target VPN Extended Communities.
            type: dict
            suboptions:
              route_target:
                description: Specify Target VPN Extended Communities
                type: dict
                suboptions:
                  retain_all:
                    description: All the routes regardless of Target-VPN community
                    type: bool
                  route_map:
                    description: Apply route-map to filter routes.
                    type: str
          suppress_inactive:
            description: Advertise only active routes to peers.
            type: bool
          table_map:
            description:
            - Policy for filtering/modifying OSPF routes before sending them to RIB.
            type: dict
            suboptions:
              name:
                description:
                - The Route Map name.
                type: str
                required: true
              filter:
                description:
                - Block the OSPF routes from being sent to RIB.
                type: bool
          timers:
            description: Configure bgp related timers.
            type: dict
            suboptions:
              bestpath_defer:
                description: Configure bestpath defer timer value for batch prefix processing.
                type: dict
                suboptions:
                  defer_time:
                    description: Bestpath defer time (mseconds).
                    type: int
                  maximum_defer_time:
                    description: Maximum bestpath defer time (mseconds).
                    type: int
          wait_igp_convergence:
            description: Delay initial bestpath until redistributed IGPs have converged.
            type: bool
          vrf:
            description: Virtual Router Context.
            type: str
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
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_address_family.bgp_address_family import (
    Bgp_address_familyArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.bgp_address_family.bgp_address_family import (
    Bgp_address_family,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_address_familyArgs.argument_spec,
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

    result = Bgp_address_family(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
