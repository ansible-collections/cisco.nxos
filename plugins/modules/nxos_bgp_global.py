#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for nxos_bgp_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: nxos_bgp_global
short_description: BGP Global resource module.
description:
- This module manages global BGP configuration on devices running Cisco NX-OS.
version_added: 1.4.0
notes:
- Tested against NX-OS 9.3.3.
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
      asn:
        description: Autonomous System Number of the router.
        type: str
      bestpath: &bestpath
        description: Define the default bestpath selection algorithm.
        type: dict
        suboptions:
          always_compare_med:
            description: Compare MED on paths from different AS.
            type: bool
          as_path:
            description: AS-Path.
            type: dict
            suboptions:
              ignore:
                description: Ignore AS-Path during bestpath selection.
                type: bool
              multipath_relax:
                description: Relax AS-Path restriction when choosing multipaths.
                type: bool
          compare_neighborid:
            description: When more paths are available than max path config, use neighborid as tie-breaker.
            type: bool
          compare_routerid:
            description: Compare router-id for identical EBGP paths.
            type: bool
          cost_community_ignore:
            description: Ignore cost communities in bestpath selection.
            type: bool
          igp_metric_ignore:
            description: Ignore IGP metric for next-hop during bestpath selection.
            type: bool
          med:
            description: MED
            type: dict
            suboptions:
              confed:
                description: Compare MED only from paths originated from within a confederation.
                type: bool
              missing_as_worst:
                description: Treat missing MED as highest MED.
                type: bool
              non_deterministic:
                description: Not always pick the best-MED path among paths from same AS.
                type: bool
      cluster_id: &cluster_id
        description: Configure Route Reflector Cluster-ID.
        type: str
      confederation: &confederation
        description: AS confederation parameters.
        type: dict
        suboptions:
          identifier:
            description: Set routing domain confederation AS.
            type: str
          peers:
            description: Peer ASs in BGP confederation.
            type: list
            elements: str
      disable_policy_batching:
        description: Disable batching evaluation of outbound policy for a peer.
        type: dict
        suboptions:
          set:
            description: Set policy batching.
            type: bool
          ipv4:
            description: IPv4 address-family settings.
            type: dict
            suboptions:
              prefix_list:
                description: Name of prefix-list to apply.
                type: str
          ipv6:
            description: IPv6 address-family settings.
            type: dict
            suboptions:
              prefix_list:
                description: Name of prefix-list to apply.
                type: str
          nexthop:
            description: Batching based on nexthop.
            type: bool
      dynamic_med_interval:
        description: Sets the interval for dampening of med changes.
        type: int
      enforce_first_as:
        description: Enforce neighbor AS is the first AS in AS-PATH attribute (EBGP).
        type: bool
      enhanced_error:
        description: Enable BGP Enhanced error handling.
        type: bool
      fast_external_fallover:
        description: Immediately reset the session if the link to a directly connected BGP peer goes down.
        type: bool
      flush_routes:
        description: Flush routes in RIB upon controlled restart.
        type: bool
      graceful_restart:
        description: Configure Graceful Restart functionality.
        type: dict
        suboptions:
          set:
            description: Enable graceful-restart.
            type: bool
          restart_time:
            description: Maximum time for restart advertised to peers.
            type: int
          stalepath_time:
            description: Maximum time to keep a restarting peer's stale routes.
            type: int
          helper:
            description: Configure Graceful Restart Helper mode functionality.
            type: bool
          shutdown:
            description: Graceful-shutdown for BGP protocol.
            type: dict
            suboptions:
              activate:
                description: Send graceful-shutdown community on all routes.
                type: dict
                suboptions:
                  set:
                    description: Activiate graceful-shutdown.
                    type: bool
                  route_map:
                    description: Apply route-map to modify attributes for outbound.
                    type: str
              aware:
                description: Lower preference of routes carrying graceful-shutdown community.
                type: bool
      isolate:
        description: Isolate this router from BGP perspective.
        type: bool
      log_neighbor_changes: &log_nbr
        description: Log a message for neighbor up/down event.
        type: bool
      maxas_limit: &maxas_limit
        description: Allow AS-PATH attribute from EBGP neighbor imposing a limit on number of ASes.
        type: int
      neighbors: &nbr
        description: Configure BGP neighbors.
        type: list
        elements: dict
        suboptions:
          neighbor_address: 
            description: IP address/Prefix of the neighbor or interface.
            type: str
            required: True
          remote_as:
            description: Remote ASN.
            type: str
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
              peer:
                description: Peer template to inherit.
                type: str
              peer_session:
                description: Peer-session template to inherit.
                type: str
          local_as:
            description: Specify the local-as number for the eBGP neighbor.
            type: str
          log_neighbor_changes:
            description: Log message for neighbor up/down event.
            type: str
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
              key:
                description: Authentication password.
                type: str
          path_attribute:
            description: BGP path attribute optional filtering.
            type: dict
            suboptions:
              action:
                description: Action.
                type: str
                choices: ["discard", "treat-as-withdraw"]
              path_attribute_type:
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
            type: str
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
      neighbor_down: &nbr_down
        description: Handle BGP neighbor down event, due to various reasons.
        type: dict
        suboptions:
          fib_accelerate:
            description: Accelerate the hardware updates for IP/IPv6 adjacencies for neighbor.
            type: bool
      nexthop:
        description: Nexthop resolution options.
        type: dict
        suboptions:
          suppress_default_resolution:
            description: Prohibit use of default route for nexthop address resolution.
            type: bool
      reconnect_interval: &reconn_intv
        description: Configure connection reconnect interval.
        type: int
      router_id: &rtr_id
        description: Specify the IP address to use as router-id.
        type: str
      shutdown: &shtdwn
        description: Administratively shutdown BGP protocol.
        type: bool
      suppress_fib_pending: &suppr
        description: Advertise only routes that are programmed in hardware to peers.
        type: bool
      timers: &timers
        description: Configure bgp related timers.
        type: dict
        suboptions:
          bestpath_limit:
            description: Configure timeout for first bestpath after restart.
            type: dict
            suboptions:
              timeout:
                description: Bestpath timeout (seconds).
                type: int
              always:
                description: Configure update-delay-always option.
                type: bool
          bgp:
            description: Configure different bgp keepalive and holdtimes.
            type: dict
            suboptions:
              keepalive:
                description: Keepalive interval (seconds).
                type: int
              holdtime:
                description: Holdtime (seconds).
                type: int
          prefix_peer_timeout:
            description: Prefix Peer timeout (seconds).
            type: int
          prefix_peer_wait:
            description: Configure wait timer for a prefix peer.
            type: int
      vrfs:
        description: Virtual Router Context configurations.
        type: list
        elements: dict
        suboptions:
          vrf: 
            description: VRF name.
            type: str
          bestpath: *bestpath
          cluster_id: *cluster_id
          confederation: *confederation
          graceful_restart:
            description: Configure Graceful Restart functionality.
            type: dict
            suboptions:
              set:
                description: Enable graceful-restart.
                type: bool
              restart_time:
                description: Maximum time for restart advertised to peers.
                type: int
              stalepath_time:
                description: Maximum time to keep a restarting peer's stale routes.
                type: int
              helper:
                description: Configure Graceful Restart Helper mode functionality.
                type: bool
          local_as:
            description: Specify the local-as for this vrf.
            type: str
          log_neighbor_changes: *log_nbr
          maxas_limit: *maxas_limit
          neighbors: *nbr
          neighbor_down: *nbr_down
          reconnect_interval: *reconn_intv
          router_id: *rtr_id
          shutdown: *shtdwn
          timers: *timers
  state:
    description:
    - The state the configuration should be left in.
    type: str
    choices:
    - merged
    - replaced
    - deleted
    - parsed
    - gathered
    - parsed
    - rendered
    default: merged
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.argspec.bgp_global.bgp_global import (
    Bgp_globalArgs,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.bgp_global.bgp_global import (
    Bgp_global,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_globalArgs.argument_spec,
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

    result = Bgp_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
