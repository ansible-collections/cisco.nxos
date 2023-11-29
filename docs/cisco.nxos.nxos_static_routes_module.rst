.. _cisco.nxos.nxos_static_routes_module:


*****************************
cisco.nxos.nxos_static_routes
*****************************

**Static routes resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the attributes of static routes on Cisco NX-OS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="5">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of configurations for static routes</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_families</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary specifying the address family to which the static route(s) belong.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies the top level address family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary that specifies the static route configurations</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Destination prefix of static route</div>
                        <div>The address format is &lt;ipv4/v6 address&gt;/&lt;mask&gt;</div>
                        <div>The mask is number in range 0-32 for IPv4 and in range 0-128 for IPv6</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hops</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Details of route to be taken</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>admin_distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Preference or administrative distance of route (range 1-255)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest_vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF of the destination</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>forward_router_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP address of the next hop router</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Outgoing interface to take. For anything except &#x27;Null0&#x27;, then next hop IP address should also be configured.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the static route</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route tag value (numeric)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Track value (range 1 - 512). Track must already be configured on the device before adding the route.</div>
                </td>
            </tr>



            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The VRF to which the static route(s) belong</div>
                </td>
            </tr>

            <tr>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option is used only with state <em>parsed</em>.</div>
                        <div>The value of this option should be the output received from the NX-OS device by executing the following commands in order <b>show running-config | include &#x27;^ip(v6</b>* route&#x27;) and <b>show running-config | section &#x27;^vrf context&#x27;</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>deleted</li>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>overridden</li>
                                    <li>replaced</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Nexus 9300v running NX-OS 9.3.6 on CML.
   - Unsupported for Cisco MDS
   - When a route is configured for a non-existent VRF, the VRF is created and the route is added to it.
   - When deleting routes for a VRF, all routes inside the VRF are deleted, but the VRF is not deleted.



Examples
--------

.. code-block:: yaml

    # Using deleted - delete all

    # Before state:
    # -------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.32/28 192.0.2.12 name new_route
    # ip route 192.0.2.26/24 192.0.2.13 tag 12
    # switch# show running-config | section '^vrf context'

    - name: Delete all routes
      cisco.nxos.nxos_static_routes:
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.0/24
    #             next_hops:
    #               - forward_router_address: 192.0.2.13
    #                 tag: 12
    #           - dest: 192.0.2.32/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.12
    #                 route_name: new_route
    # commands:
    # - no ip route 192.0.2.0/24 192.0.2.13 tag 12
    # - no ip route 192.0.2.32/28 192.0.2.12 name new_route
    # after: []

    # After state:
    # ------------
    # switch# show running-config | include '^ip(v6)* route'
    # switch# show running-config | section '^vrf context'

    # Using deleted - vrf based

    # Before state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ip route 192.0.2.64/28 192.0.2.22 tag 4
    # ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
    # ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5

    - name: Delete routes based on VRF
      cisco.nxos.nxos_static_routes:
        config:
          - vrf: trial_vrf
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.64/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.22
    #                 tag: 4
    #               - admin_distance: 1
    #                 forward_router_address: 192.0.2.23
    #                 route_name: merged_route
    #       - afi: ipv6
    #         routes:
    #           - dest: '2200:10::/36'
    #             next_hops:
    #               - admin_distance: 5
    #                 dest_vrf: dest
    #                 forward_router_address: '2048:ae12::1'
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12
    # commands:
    # - vrf context trial_vrf
    # - no ip route 192.0.2.64/28 192.0.2.22 tag 4
    # - no ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
    # - no ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5
    # after:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12

    # After state:
    # -----------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf

    # Using deleted - afi based

    # Before state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ip route 192.0.2.64/28 192.0.2.22 tag 4
    # ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
    # ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5

    - name: Delete routes based on AFI in a VRF
      cisco.nxos.nxos_static_routes:
        config:
          - vrf: trial_vrf
            address_families:
              - afi: ipv4
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.64/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.22
    #                 tag: 4
    #               - admin_distance: 1
    #                 forward_router_address: 192.0.2.23
    #                 route_name: merged_route
    #       - afi: ipv6
    #         routes:
    #           - dest: '2200:10::/36'
    #             next_hops:
    #               - admin_distance: 5
    #                 dest_vrf: dest
    #                 forward_router_address: '2048:ae12::1'
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12
    # commands:
    # - vrf context trial_vrf
    # - no ip route 192.0.2.64/28 192.0.2.22 tag 4
    # - no ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
    # after:
    #   - address_families:
    #       - afi: ipv6
    #         routes:
    #           - dest: '2200:10::/36'
    #             next_hops:
    #               - admin_distance: 5
    #                 dest_vrf: dest
    #                 forward_router_address: '2048:ae12::1'
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12

    # After state:
    # -----------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ipv6 route 2200:10::/36 2048:ae12::1 vrf dest 5

    # Using merged

    # Before state:
    # -------------
    # switch# show running-config | include '^ip(v6)* route'
    # switch# show running-config | section '^vrf context'

    - name: Merge new static route configuration
      cisco.nxos.nxos_static_routes:
        config:
          - vrf: trial_vrf
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.64/24
                    next_hops:
                      - forward_router_address: 192.0.2.22
                        tag: 4
                        admin_distance: 2
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.16/24
                    next_hops:
                      - forward_router_address: 192.0.2.24
                        route_name: new_route
              - afi: ipv6
                routes:
                  - dest: '2001:db8::/64'
                    next_hops:
                      - interface: eth1/3
                        forward_router_address: '2001:db8::12'
        state: merged

    # Task Output
    # -----------
    #
    # before:[]
    # commands:
    # - vrf context trial_vrf
    # - ip route 192.0.2.64/24 192.0.2.22 tag 4 2
    # - ip route 192.0.2.16/24 192.0.2.24 name new_route
    # - ipv6 route 2001:db8::/64 Ethernet1/3 2001:db8::12
    # after:
    #     - vrf: trial_vrf
    #       address_families:
    #       - afi: ipv4
    #         routes:
    #         - dest: 192.0.2.64/24
    #           next_hops:
    #           - forward_router_address: 192.0.2.22
    #             tag: 4
    #             admin_distance: 2
    #     - address_families:
    #       - afi: ipv4
    #         routes:
    #         - dest: 192.0.2.16/24
    #           next_hops:
    #           - forward_router_address: 192.0.2.24
    #             route_name: new_route
    #       - afi: ipv6
    #         routes:
    #         - dest: 2001:db8::/64
    #           next_hops:
    #           - interface: eth1/3
    #             forward_router_address: 2

    # After state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/24 192.0.2.24 name new_route
    # ipv6 route 2001:db8::/64 Ethernet1/3 2001:db8::12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    #   ip route 192.0.2.0/24 192.0.2.22 tag 4 2

    # Using overridden

    # Before state:
    # -------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ip route 192.0.2.64/28 192.0.2.22 tag 4
    # ip route 192.0.2.64/28 192.0.2.23 name merged_route 1

    - name: Overridden existing static route configuration with new configuration
      cisco.nxos.nxos_static_routes:
        config:
          - vrf: trial_vrf
            address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.16/28
                    next_hops:
                      - forward_router_address: 192.0.2.23
                        route_name: overridden_route1
                        admin_distance: 3
                      - forward_router_address: 192.0.2.45
                        route_name: overridden_route2
                        dest_vrf: destinationVRF
                        interface: Ethernet1/2
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.64/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.22
    #                 tag: 4
    #               - admin_distance: 1
    #                 forward_router_address: 192.0.2.23
    #                 route_name: merged_route
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12
    # commands:
    # - no ip route 192.0.2.16/28 192.0.2.24 name new_route
    # - no ip route 192.0.2.80/28 192.0.2.26 tag 12
    # - vrf context trial_vrf
    # - no ip route 192.0.2.64/28 192.0.2.22 tag 4
    # - no ip route 192.0.2.64/28 192.0.2.23 name merged_route 1
    # - ip route 192.0.2.16/28 192.0.2.23 name overridden_route1 3
    # - ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name overridden_route2
    # after:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - admin_distance: 3
    #                 forward_router_address: 192.0.2.23
    #                 route_name: overridden_route1
    #               - dest_vrf: destinationVRF
    #                 forward_router_address: 192.0.2.45
    #                 interface: Ethernet1/2
    #                 route_name: overridden_route2
    #    vrf: trial_vrf

    # After state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    #   ip route 192.0.2.16/28 192.0.2.23 name overridden_route1 3
    #   ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name overridden_route2

    # Using replaced

    # Before state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.24 name new_route
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ip route 192.0.2.64/28 192.0.2.22 tag 4
    # ip route 192.0.2.64/28 192.0.2.23 name merged_route 1

    - name: Replaced the existing static configuration of a prefix with new configuration
      cisco.nxos.nxos_static_routes:
        config:
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.16/28
                    next_hops:
                      - forward_router_address: 192.0.2.23
                        route_name: replaced_route1
                        admin_distance: 3
                      - forward_router_address: 192.0.2.45
                        route_name: replaced_route2
                        dest_vrf: destinationVRF
                        interface: Ethernet1/2
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.64/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.22
    #                 tag: 4
    #               - admin_distance: 1
    #                 forward_router_address: 192.0.2.23
    #                 route_name: merged_route
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.24
    #                 route_name: new_route
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12
    # commands:
    # - no ip route 192.0.2.16/28 192.0.2.24 name new_route
    # - ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
    # - ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
    # after:
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.64/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.22
    #                 tag: 4
    #               - admin_distance: 1
    #                 forward_router_address: 192.0.2.23
    #                 route_name: merged_route
    #     vrf: trial_vrf
    #   - address_families:
    #       - afi: ipv4
    #         routes:
    #           - dest: 192.0.2.16/28
    #             next_hops:
    #               - admin_distance: 3
    #                 forward_router_address: 192.0.2.23
    #                 route_name: replaced_route1
    #               - dest_vrf: destinationVRF
    #                 forward_router_address: 192.0.2.45
    #                 interface: Ethernet1/2
    #                 route_name: replaced_route2
    #           - dest: 192.0.2.80/28
    #             next_hops:
    #               - forward_router_address: 192.0.2.26
    #                 tag: 12

    # After state:
    # ------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ip route 192.0.2.16/28 192.0.2.23 name replaced_route1 3
    # ip route 192.0.2.16/28 Ethernet1/2 192.0.2.45 vrf destinationVRF name replaced_route2
    # ip route 192.0.2.80/28 192.0.2.26 tag 12
    # switch# show running-config | section '^vrf context'
    # vrf context trial_vrf
    # ip route 192.0.2.64/28 192.0.2.22 tag 4
    # ip route 192.0.2.64/28 192.0.2.23 name merged_route 1


    # Using gathered

    # Before state:
    # -------------
    #
    # switch# show running-config | include '^ip(v6)* route'
    # ipv6 route 2001:db8:12::/32  2001:db8::12
    # switch# show running-config | section '^vrf context'
    # vrf context Test
    #    ip route 192.0.2.48/28 192.0.2.13
    #    ip route 192.0.2.48/28 192.0.2.14 5

    - name: Gather the existing configuration
      cisco.nxos.nxos_static_routes:
        state: gathered

    # Task Output
    # -----------
    #
    # gathered:
    #     - vrf: Test
    #       address_families:
    #         - afi: ipv4
    #           routes:
    #             - dest: 192.0.2.48/28
    #               next_hops:
    #                 - forward_router_address: 192.0.2.13
    #
    #                 - forward_router_address: 192.0.2.14
    #                   admin_distance: 5
    #
    #     - address_families:
    #         - afi: ipv6
    #           routes:
    #             - dest: 2001:db8:12::/32
    #               next_hops:
    #                 - forward_router_address: 2001:db8::12


    # Using rendered

    - name: Render required configuration to be pushed to the device
      cisco.nxos.nxos_static_routes:
        config:
          - address_families:
              - afi: ipv4
                routes:
                  - dest: 192.0.2.48/28
                    next_hops:
                      - forward_router_address: 192.0.2.13
              - afi: ipv6
                routes:
                  - dest: 2001:db8::/64
                    next_hops:
                      - interface: eth1/3
                        forward_router_address: 2001:db8::12
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    #   vrf context default
    #   ip route 192.0.2.48/28 192.0.2.13
    #   ipv6 route 2001:db8::/64 Ethernet1/3 2001:db8::12

    # Using parsed

    - name: Parse the config to structured data
      cisco.nxos.nxos_static_routes:
        state: parsed
        running_config: |
          ipv6 route 2002:db8:12::/32 2002:db8:12::1
          vrf context Test
            ip route 192.0.2.48/28 192.0.2.13
            ip route 192.0.2.48/28 192.0.2.14 5

    # Task Output
    # -----------
    #
    # parsed:
    #     - vrf: Test
    #       address_families:
    #         - afi: ipv4
    #           routes:
    #             - dest: 192.0.2.48/28
    #               next_hops:
    #                 - forward_router_address: 192.0.2.13
    #                 - forward_router_address: 192.0.2.14
    #                   admin_distance: 5
    #     - address_families:
    #         - afi: ipv6
    #           routes:
    #             - dest: 2002:db8:12::/32
    #               next_hops:
    #                 - forward_router_address: 2002:db8:12::1



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when changed</td>
                <td>
                            <div>The resulting configuration after module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The configuration prior to the module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip route 192.0.2.16/28 192.0.2.24 name new_route&#x27;, &#x27;vrf context trial_vrf&#x27;, &#x27;ip route 192.0.2.16/28 192.0.2.23 name overridden_route1 3&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>gathered</code></td>
                <td>
                            <div>Facts about the network resource gathered from the remote device as structured data.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>parsed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>parsed</code></td>
                <td>
                            <div>The device native config provided in <em>running_config</em> option parsed into structured data as per module argspec.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This output will always be in the same format as the module argspec.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>rendered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>rendered</code></td>
                <td>
                            <div>The provided configuration in the task rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip route 192.0.2.16/28 192.0.2.24 name new_route&#x27;, &#x27;vrf context trial_vrf&#x27;, &#x27;ip route 192.0.2.16/28 192.0.2.23 name overridden_route1 3&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Adharsh Srivats Rangarajan (@adharshsrivatsr)
- Sagar Paul (@KB-perByte)
