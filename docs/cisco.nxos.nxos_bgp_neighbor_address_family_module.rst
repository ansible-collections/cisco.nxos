.. _cisco.nxos.nxos_bgp_neighbor_address_family_module:


*******************************************
cisco.nxos.nxos_bgp_neighbor_address_family
*******************************************

**BGP Neighbor Address Family resource module.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages BGP Neighbor Address Family configuration on devices running Cisco NX-OS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="7">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="7">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>BGP Neighbor AF configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Autonomous System Number of the router.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbors</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of BGP Neighbor AF configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_family</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>BGP Neighbor Address Family related configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify route-map for conditional advertisement.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exist_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Condition route-map to advertise only when prefix in condition exists.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>non_exist_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Condition route-map to advertise only when prefix in condition does not exist.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map name.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertisement_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum interval between sending BGP routing updates.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                                    <li>link-state</li>
                                    <li>vpnv4</li>
                                    <li>vpnv6</li>
                                    <li>l2vpn</li>
                        </ul>
                </td>
                <td>
                        <div>Address Family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allowas_in</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Accept as-path with my AS present in it.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_occurences</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of occurrences of AS number, default is 3.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Activate allowas-in property.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_override</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Override matching AS-number while sending update.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>capability</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Advertise capability to the peer.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>additional_paths</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Additional paths capability.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>receive</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Additional paths Receive capability.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>send</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Additional paths Send capability.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_originate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Originate a default toward this peer.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map to specify criteria for originating default.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set default-originate attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable_peer_as_check</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Disable checking of peer AS-number while advertising.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of filter-list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inherit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Inherit a template.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Sequence number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Template name.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maximum_prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum number of prefixes from this neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>generate_warning_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Threshold percentage at which to generate a warning.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_prefix_limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix limit.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>restart_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Restart bgp connection after limit is exceeded.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>warning_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Only give a warning message when limit is exceeded.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop_self</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set our address as nexthop (non-reflected).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>all_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set our address as nexthop for all routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set next-hop-self attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop_third_party</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Compute a third-party nexthop if possible.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply prefix-list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rewrite_evpn_rt_asn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Auto generate RTs for EBGP neighbor.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply route-map to neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_reflector_client</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Configure a neighbor as Route reflector client.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>safi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>unicast</li>
                                    <li>multicast</li>
                                    <li>mvpn</li>
                                    <li>evpn</li>
                        </ul>
                </td>
                <td>
                        <div>Sub Address Family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>send_community</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Send Community attribute to this neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>both</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Standard and Extended Community attributes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extended</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Extended Community attribute.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set send-community attribute.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>standard</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Standard Community attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>soft_reconfiguration_inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Soft reconfiguration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>always</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Always perform inbound soft reconfiguration.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set soft-reconfiguration inbound attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>soo</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify Site-of-origin extcommunity.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suppress_inactive</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Advertise only active routes to peer.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unsuppress_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map to selectively unsuppress suppressed routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>weight</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set default weight for routes from this neighbor.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbor_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP/IPv6 address of the neighbor.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrfs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Router Context.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbors</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of BGP Neighbor AF configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_family</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>BGP Neighbor Address Family related configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify route-map for conditional advertisement.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exist_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Condition route-map to advertise only when prefix in condition exists.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>non_exist_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Condition route-map to advertise only when prefix in condition does not exist.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map name.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertisement_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum interval between sending BGP routing updates.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
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
                                    <li>link-state</li>
                                    <li>vpnv4</li>
                                    <li>vpnv6</li>
                                    <li>l2vpn</li>
                        </ul>
                </td>
                <td>
                        <div>Address Family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allowas_in</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Accept as-path with my AS present in it.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_occurences</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of occurrences of AS number, default is 3.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Activate allowas-in property.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_override</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Override matching AS-number while sending update.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>capability</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Advertise capability to the peer.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>additional_paths</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Additional paths capability.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>receive</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Additional paths Receive capability.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>send</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Additional paths Send capability.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_originate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Originate a default toward this peer.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map to specify criteria for originating default.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set default-originate attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable_peer_as_check</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Disable checking of peer AS-number while advertising.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of filter-list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inherit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Inherit a template.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Sequence number.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Template name.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maximum_prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum number of prefixes from this neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>generate_warning_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Threshold percentage at which to generate a warning.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_prefix_limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix limit.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>restart_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Restart bgp connection after limit is exceeded.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>warning_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Only give a warning message when limit is exceeded.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop_self</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set our address as nexthop (non-reflected).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>all_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set our address as nexthop for all routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set next-hop-self attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop_third_party</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Compute a third-party nexthop if possible.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply prefix-list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rewrite_evpn_rt_asn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Auto generate RTs for EBGP neighbor.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply route-map to neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to incoming routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>outbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Apply policy to outgoing routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_reflector_client</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Configure a neighbor as Route reflector client.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>safi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>unicast</li>
                                    <li>multicast</li>
                                    <li>mvpn</li>
                                    <li>evpn</li>
                        </ul>
                </td>
                <td>
                        <div>Sub Address Family indicator.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>send_community</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Send Community attribute to this neighbor.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>both</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Standard and Extended Community attributes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extended</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Extended Community attribute.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set send-community attribute.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>standard</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Send Standard Community attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>soft_reconfiguration_inbound</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Soft reconfiguration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>always</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Always perform inbound soft reconfiguration.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set soft-reconfiguration inbound attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>soo</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify Site-of-origin extcommunity.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suppress_inactive</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Advertise only active routes to peer.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>unsuppress_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map to selectively unsuppress suppressed routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>weight</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set default weight for routes from this neighbor.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>neighbor_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP/IPv6 address of the neighbor.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>VRF name.</div>
                </td>
            </tr>


            <tr>
                <td colspan="7">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^router bgp&#x27;</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="7">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>State <em>deleted</em> only removes BGP attributes that this modules manages and does not negate the BGP process completely.</div>
                        <div>Refer to examples for more details.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - Unsupported for Cisco MDS
   - For managing BGP address family configurations please use the :ref:`cisco.nxos.nxos_bgp_address_family <cisco.nxos.nxos_bgp_address_family_module>` module.
   - This module works with connection ``network_cli`` and ``httpapi``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # Nexus9000v#

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_bgp_neighbor_address_family: &id001
        config:
          as_number: 65536
          neighbors:
            - neighbor_address: 192.0.2.32
              address_family:
                - afi: ipv4
                  safi: unicast
                  maximum_prefix:
                    max_prefix_limit: 20
                    generate_warning_threshold: 75
                  weight: 100
                  prefix_list:
                    inbound: rmap1
                    outbound: rmap2
                - afi: ipv6
                  safi: unicast
            - neighbor_address: 192.0.2.33
              address_family:
                - afi: ipv4
                  safi: multicast
                  inherit:
                    template: BasePolicy
                    sequence: 200
          vrfs:
            - vrf: site-1
              neighbors:
                - neighbor_address: 203.0.113.1
                  address_family:
                    - afi: ipv4
                      safi: unicast
                      suppress_inactive: True
                      next_hop_self:
                        set: True
                - neighbor_address: 203.0.113.2
                  address_family:
                    - afi: ipv6
                      safi: unicast
                    - afi: ipv4
                      safi: multicast
                      send_community:
                        set: True

    # Task output
    # -------------
    #  before: {}
    #
    #  commands:
    #  - router bgp 65536
    #  - neighbor 192.0.2.32
    #  - address-family ipv4 unicast
    #  - maximum-prefix 20 75
    #  - weight 100
    #  - prefix-list rmap1 in
    #  - prefix-list rmap2 out
    #  - address-family ipv6 unicast
    #  - neighbor 192.0.2.33
    #  - address-family ipv4 multicast
    #  - inherit peer-policy BasePolicy 200
    #  - vrf site-1
    #  - neighbor 203.0.113.1
    #  - address-family ipv4 unicast
    #  - suppress-inactive
    #  - next-hop-self
    #  - neighbor 203.0.113.2
    #  - address-family ipv6 unicast
    #  - address-family ipv4 multicast
    #  - send-community
    #
    #  after:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #            weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast

    # After state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    # Using replaced

    # Before state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    - name: Replace specified neighbor AFs with given configuration
      cisco.nxos.nxos_bgp_neighbor_address_family: &replaced
        config:
          as_number: 65536
          neighbors:
            - neighbor_address: 192.0.2.32
              address_family:
                - afi: ipv4
                  safi: unicast
                  weight: 110
                - afi: ipv6
                  safi: unicast
            - neighbor_address: 192.0.2.33
              address_family:
                - afi: ipv4
                  safi: multicast
                  inherit:
                    template: BasePolicy
                    sequence: 200
          vrfs:
            - vrf: site-1
              neighbors:
                - neighbor_address: 203.0.113.1
                  address_family:
                    - afi: ipv4
                      safi: unicast
                - neighbor_address: 203.0.113.2
                  address_family:
                    - afi: ipv6
                      safi: unicast
                    - afi: ipv4
                      safi: multicast
                      send_community:
                        set: True
        state: replaced

    # Task output
    # -------------
    #  before:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #            weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast
    #
    #  commands:
    #    - router bgp 65536
    #    - neighbor 192.0.2.32
    #    - address-family ipv4 unicast
    #    - no maximum-prefix 20 75
    #    - weight 110
    #    - no prefix-list rmap1 in
    #    - no prefix-list rmap2 out
    #    - vrf site-1
    #    - neighbor 203.0.113.1
    #    - address-family ipv4 unicast
    #    - no suppress-inactive
    #    - no next-hop-self
    #
    #  after:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            weight: 110
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast

    # After state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       weight 110
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    # Using overridden

    # Before state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    - name: Override all BGP AF configuration with provided configuration
      cisco.nxos.nxos_bgp_neighbor_address_family:
        config:
          as_number: 65536
          neighbors:
            - neighbor_address: 192.0.2.32
              address_family:
                - afi: ipv4
                  safi: unicast
          vrfs:
            - vrf: site-1
              neighbors:
                - neighbor_address: 203.0.113.1
                  address_family:
                    - afi: ipv4
                      safi: unicast
                      suppress_inactive: True
                      next_hop_self:
                        set: True
        state: overridden

    # Task output
    # -------------
    #  before:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #            weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast
    #
    #  commands:
    #    - router bgp 65536
    #    - neighbor 192.0.2.32
    #    - address-family ipv4 unicast
    #    - no maximum-prefix 20 75
    #    - no weight 100
    #    - no prefix-list rmap1 in
    #    - no prefix-list rmap2 out
    #    - no address-family ipv6 unicast
    #    - neighbor 192.0.2.33
    #    - no address-family ipv4 multicast
    #    - vrf site-1
    #    - neighbor 203.0.113.2
    #    - no address-family ipv4 multicast
    #    - no address-family ipv6 unicast
    #
    #  after:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: True
    #                next_hop_self:
    #                  set: True

    # After state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self

    # Using deleted to remove specified neighbor AFs

    # Before state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    - name: Delete BGP configs handled by this module
      cisco.nxos.nxos_bgp_neighbor_address_family:
        config:
          as_number: 65536
          neighbors:
            - neighbor_address: 192.0.2.32
              address_family:
                - afi: ipv4
                  safi: unicast
          vrfs:
            - vrf: site-1
              neighbors:
                - neighbor_address: 203.0.113.2
                  address_family:
                    - afi: ipv6
                      safi: unicast
        state: deleted

    # Task output
    # -------------
    #  before:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #            weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast
    #
    #  commands:
    #    - router bgp 65536
    #    - neighbor 192.0.2.32
    #    - no address-family ipv4 unicast
    #    - vrf site-1
    #    - neighbor 203.0.113.2
    #    - no address-family ipv6 unicast
    #
    #  after:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #
    # After state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #

    # Using deleted to remove all neighbor AFs

    # Before state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast
    #

    - name: Delete all BGP neighbor AF configs handled by this module
      cisco.nxos.nxos_bgp_neighbor_address_family:
        state: deleted

    # Task output
    # -------------
    #  before:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #            safi: unicast
    #            maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #            weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast
    #
    #  commands:
    #    - router bgp 65536
    #    - neighbor 192.0.2.32
    #    - no address-family ipv4 unicast
    #    - no address-family ipv6 unicast
    #    - neighbor 192.0.2.33
    #    - no address-family ipv4 multicast
    #    - vrf site-1
    #    - neighbor 203.0.113.1
    #    - no address-family ipv4 unicast
    #    - neighbor 203.0.113.2
    #    - no address-family ipv6 unicast
    #    - no address-family ipv4 multicast
    #
    #  after:
    #    as_number: "65536"
    #
    # After state:
    # -------------
    # Nexus9000v# show running-config | section "^router bgp"
    # router bgp 65536
    #   neighbor 192.0.2.32
    #   neighbor 192.0.2.33
    #   vrf site-1
    #     neighbor 203.0.113.1
    #     neighbor 203.0.113.2
    #

    # Using rendered

    - name: Render platform specific configuration lines with state rendered (without connecting to the device)
      cisco.nxos.nxos_bgp_neighbor_address_family:
        config:
          as_number: 65536
          neighbors:
            - neighbor_address: 192.0.2.32
              address_family:
                - afi: ipv4
                  safi: unicast
                  maximum_prefix:
                    max_prefix_limit: 20
                    generate_warning_threshold: 75
                  weight: 100
                  prefix_list:
                    inbound: rmap1
                    outbound: rmap2
                - afi: ipv6
                  safi: unicast
            - neighbor_address: 192.0.2.33
              address_family:
                - afi: ipv4
                  safi: multicast
                  inherit:
                    template: BasePolicy
                    sequence: 200
          vrfs:
            - vrf: site-1
              neighbors:
                - neighbor_address: 203.0.113.1
                  address_family:
                    - afi: ipv4
                      safi: unicast
                      suppress_inactive: True
                      next_hop_self:
                        set: True
                - neighbor_address: 203.0.113.2
                  address_family:
                    - afi: ipv6
                      safi: unicast
                    - afi: ipv4
                      safi: multicast
                      send_community:
                        set: True
        state: rendered

    # Task Output (redacted)
    # -----------------------
    #  rendered:
    #    - router bgp 65536
    #    - neighbor 192.0.2.32
    #    - address-family ipv4 unicast
    #    - maximum-prefix 20 75
    #    - weight 100
    #    - prefix-list rmap1 in
    #    - prefix-list rmap2 out
    #    - address-family ipv6 unicast
    #    - neighbor 192.0.2.33
    #    - address-family ipv4 multicast
    #    - inherit peer-policy BasePolicy 200
    #    - vrf site-1
    #    - neighbor 203.0.113.1
    #    - address-family ipv4 unicast
    #    - suppress-inactive
    #    - next-hop-self
    #    - neighbor 203.0.113.2
    #    - address-family ipv6 unicast
    #    - address-family ipv4 multicast
    #    - send-community

    # Using parsed

    # parsed.cfg
    # ------------
    # router bgp 65536
    #   neighbor 192.0.2.32
    #     address-family ipv4 unicast
    #       maximum-prefix 20 75
    #       weight 100
    #       prefix-list rmap1 in
    #       prefix-list rmap2 out
    #     address-family ipv6 unicast
    #   neighbor 192.0.2.33
    #     address-family ipv4 multicast
    #       inherit peer-policy BasePolicy 200
    #   vrf site-1
    #     neighbor 203.0.113.1
    #       address-family ipv4 unicast
    #         suppress-inactive
    #         next-hop-self
    #     neighbor 203.0.113.2
    #       address-family ipv4 multicast
    #         send-community
    #       address-family ipv6 unicast

    - name: Parse externally provided BGP neighbor AF config
      register: result
      cisco.nxos.nxos_bgp_neighbor_address_family:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    #  parsed:
    #    as_number: "65536"
    #    neighbors:
    #      - neighbor_address: 192.0.2.32
    #        address_family:
    #          - afi: ipv4
    #           safi: unicast
    #           maximum_prefix:
    #              max_prefix_limit: 20
    #              generate_warning_threshold: 75
    #           weight: 100
    #            prefix_list:
    #              inbound: rmap1
    #              outbound: rmap2
    #          - afi: ipv6
    #            safi: unicast
    #      - neighbor_address: 192.0.2.33
    #        address_family:
    #          - afi: ipv4
    #            safi: multicast
    #            inherit:
    #              template: BasePolicy
    #              sequence: 200
    #    vrfs:
    #      - vrf: site-1
    #        neighbors:
    #          - neighbor_address: 203.0.113.1
    #            address_family:
    #              - afi: ipv4
    #                safi: unicast
    #                suppress_inactive: true
    #                next_hop_self:
    #                  set: true
    #          - neighbor_address: 203.0.113.2
    #            address_family:
    #              - afi: ipv4
    #                safi: multicast
    #                send_community:
    #                  set: True
    #              - afi: ipv6
    #                safi: unicast




Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
