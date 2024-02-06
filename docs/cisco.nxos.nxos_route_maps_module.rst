.. _cisco.nxos.nxos_route_maps_module:


**************************
cisco.nxos.nxos_route_maps
**************************

**Route Maps resource module.**


Version added: 2.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages route maps configuration on devices running Cisco NX-OS.




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
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of route-map configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>entries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of entries (identified by sequence number) for this route-map.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>deny</li>
                                    <li>permit</li>
                        </ul>
                </td>
                <td>
                        <div>Route map denies or permits set operations.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>continue_sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Continue on a different entry within the route-map.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Description of the route-map.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match values from routing table.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match BGP peer AS number.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_path_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AS path access list name.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>asn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AS number.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match BGP AS path access-list.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>community</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match BGP community list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>community_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Community list.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exact_match</b>
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
                        <div>Do exact matching of communities.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evpn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match BGP EVPN Routes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_types</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match route type for evpn route.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extcommunity</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match BGP community list.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exact_match</b>
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
                        <div>Do exact matching of extended communities.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extcommunity_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Extended Community list.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interfaces</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match first hop interface of route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure IP specific information.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match address of route or match packet.</div>
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
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP access-list name (for use in route-maps for PBR only).</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multicast</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match multicast attributes.</div>
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
                    <b>group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast Group prefix.</div>
                        <div>Mutually exclusive with group_range.</div>
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
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 group prefix.</div>
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
                    <b>group_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast Group address range.</div>
                        <div>Mutually exclusive with group.</div>
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
                    <b>first</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>First Group address.</div>
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
                    <b>last</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Last Group address.</div>
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
                    <b>rp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Rendezvous point.</div>
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
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 rendezvous prefix.</div>
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
                    <b>rp_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ASM</li>
                                    <li>Bidir</li>
                        </ul>
                </td>
                <td>
                        <div>Multicast rendezvous point type.</div>
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
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast source address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match next-hop address of route.</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match advertising source address of route.</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure IPv6 specific information.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match address of route or match packet.</div>
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
                    <b>access_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP access-list name (for use in route-maps for PBR only).</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multicast</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match multicast attributes.</div>
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
                    <b>group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast Group prefix.</div>
                        <div>Mutually exclusive with group_range.</div>
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
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 group prefix.</div>
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
                    <b>group_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast Group address range.</div>
                        <div>Mutually exclusive with group.</div>
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
                    <b>first</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>First Group address.</div>
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
                    <b>last</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Last Group address.</div>
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
                    <b>rp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Rendezvous point.</div>
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
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IPv4 rendezvous prefix.</div>
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
                    <b>rp_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ASM</li>
                                    <li>Bidir</li>
                        </ul>
                </td>
                <td>
                        <div>Multicast rendezvous point type.</div>
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
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast source address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match next-hop address of route.</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match advertising source address of route.</div>
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
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of prefix-lists.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match entries of mac-lists.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match metric of route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ospf_area</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match ospf area.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_types</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>external</li>
                                    <li>inter-area</li>
                                    <li>internal</li>
                                    <li>intra-area</li>
                                    <li>level-1</li>
                                    <li>level-2</li>
                                    <li>local</li>
                                    <li>nssa-external</li>
                                    <li>type-1</li>
                                    <li>type-2</li>
                        </ul>
                </td>
                <td>
                        <div>Match route-type of route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match source protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Match tag of route.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>Sequence to insert to/delete from existing route-map entry.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set values in destination routing protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>as_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Prepend string for a BGP AS-path attribute.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prepend</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Prepend to the AS-Path.</div>
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
                    <b>as_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AS number.</div>
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
                    <b>last_as</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of last-AS prepends.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
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
                        <div>Set the tag as an AS-path attribute.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>comm_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP community list (for deletion).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>community</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP community attribute.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>additive</b>
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
                        <div>Add to existing community.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>graceful_shutdown</b>
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
                        <div>Graceful Shutdown (well-known community).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>internet</b>
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
                        <div>Internet (well-known community).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>local_as</b>
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
                        <div>Do not send outside local AS (well-known community).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_advertise</b>
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
                        <div>Do not advertise to any peer (well-known community).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_export</b>
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
                        <div>Do not export to next AS (well-known community).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Community number aa:nn format</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dampening</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP route flap dampening parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>half_life</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Half-life time for the penalty.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_suppress_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum suppress time for stable route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start_reuse_route</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Value to start reusing a route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start_suppress_route</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Value to start suppressing a route.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>distance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure administrative distance.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igp_ebgp_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Administrative distance for IGP or EBGP routes</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>internal_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for internal routes.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>local_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Distance for local routes.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>evpn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP EVPN Routes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gateway_ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set gateway IP for type 5 EVPN routes.</div>
                        <div>Cannot set ip and use-nexthop in the same route-map sequence.</div>
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
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Gateway IP address.</div>
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
                    <b>use_nexthop</b>
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
                        <div>Use nexthop address as gateway IP.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extcomm_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP extcommunity list (for deletion).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>extcommunity</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set BGP extcommunity attribute.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-Target.</div>
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
                    <b>additive</b>
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
                        <div>Add to existing rt extcommunity.</div>
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
                    <b>extcommunity_numbers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Extcommunity number.</div>
                        <div>Supported formats are ASN2:NN, ASN4:NN, IPV4:NN.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>forwarding_address</b>
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
                        <div>Set the forwarding address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure IP features.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify IP address.</div>
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
                    <b>prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of prefix list (Max Size 63).</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>next_hop</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set next-hop IP address (for policy-based routing)</div>
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
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set space-separated list of next-hop IP addresses. Address ordering is important. Also don`t use unnecessary spaces.</div>
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
                    <b>drop_on_fail</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Drop packets instead of using default routing when the configured next hop becomes unreachable</div>
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
                    <b>force_order</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable next-hop ordering as specified in the address parameter.</div>
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
                    <b>load_share</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable traffic load balancing across a maximum of 32 next-hop addresses</div>
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
                    <b>peer_address</b>
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
                        <div>BGP prefix next hop is set to the local address of the peer.</div>
                        <div>If no next hop is set in the route map, the next hop is set to the one stored in the path.</div>
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
                    <b>redist_unchanged</b>
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
                        <div>Set for next-hop address conservation for non-local generated routes.</div>
                        <div>Used with redistribute command. Available to maintain BGP routing compliant with RFC 4271 on Nexus OS.</div>
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
                    <b>unchanged</b>
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
                        <div>Set for next-hop address conservation in eBGP outgoing updates</div>
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
                    <b>verify_availability</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set next-hop ip address tracking with IP SLA</div>
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
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set one next-hop address</div>
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
                    <b>drop_on_fail</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Drop packets instead of using default routing when the configured next hop becomes unreachable</div>
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
                    <b>force_order</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable next-hop ordering as specified in the address parameter.</div>
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
                    <b>load_share</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enable traffic load balancing across a maximum of 32 next-hop addresses</div>
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
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set track number</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>precedence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set precedence field.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure IPv6 features.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify IP address.</div>
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
                    <b>prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of prefix list (Max Size 63).</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>precedence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set precedence field.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>label_index</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set Segment Routing (SR) label index of route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>level-1</li>
                                    <li>level-1-2</li>
                                    <li>level-2</li>
                        </ul>
                </td>
                <td>
                        <div>Where to import route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>local_preference</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>BGP local preference path attribute.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set metric for destination routing protocol.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bandwidth</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Metric value or Bandwidth in Kbits per second (Max Size 11).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igrp_delay_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGRP delay metric.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igrp_effective_bandwidth_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGRP Effective bandwidth metric (Loading) 255 is 100%.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igrp_mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGRP MTU of the path.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igrp_reliability_metric</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGRP reliability metric where 255 is 100 percent reliable.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>metric_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>external</li>
                                    <li>internal</li>
                                    <li>type-1</li>
                                    <li>type-2</li>
                        </ul>
                </td>
                <td>
                        <div>Type of metric for destination routing protocol.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nssa_only</b>
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
                        <div>OSPF NSSA Areas.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>null_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Output Null interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>origin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>egp</li>
                                    <li>igp</li>
                                    <li>incomplete</li>
                        </ul>
                </td>
                <td>
                        <div>BGP origin code.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path_selection</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>all</li>
                                    <li>backup</li>
                                    <li>best2</li>
                                    <li>multipaths</li>
                        </ul>
                </td>
                <td>
                        <div>Path selection criteria for BGP.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Tag value for destination routing protocol.</div>
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
                        <div>BGP weight for routing table.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="6">
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
                        <div>Route-map name.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^route-map&#x27;</b>.</div>
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
                        <div>With state <em>replaced</em>, for the listed route-maps, sequences that are in running-config but not in the task are negated.</div>
                        <div>With state <em>overridden</em>, all route-maps that are in running-config but not in the task are negated.</div>
                        <div>Please refer to examples for more details.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - Unsupported for Cisco MDS
   - This module works with connection ``network_cli`` and ``httpapi``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # nxos-9k-rdo#

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_route_maps:
        config:
          - route_map: rmap1
            entries:
              - sequence: 10
                action: permit
                description: rmap1-10-permit
                match:
                  ip:
                    address:
                      access_list: acl_1
                  as_path: Allow40
                  as_number:
                    asn: 65564

              - sequence: 20
                action: deny
                description: rmap1-20-deny
                match:
                  community:
                    community_list:
                      - BGPCommunity1
                      - BGPCommunity2
                  ip:
                    address:
                      prefix_lists:
                        - AllowPrefix1
                        - AllowPrefix2
                set:
                  dampening:
                    half_life: 30
                    start_reuse_route: 1500
                    start_suppress_route: 10000
                    max_suppress_time: 120

          - route_map: rmap2
            entries:
              - sequence: 20
                action: permit
                description: rmap2-20-permit
                continue_sequence: 40
                match:
                  ipv6:
                    address:
                      prefix_lists: AllowIPv6Prefix
                  interfaces: "{{ nxos_int1 }}"
                set:
                  as_path:
                    prepend:
                      as_number:
                        - 65563
                        - 65568
                        - 65569
                  comm_list: BGPCommunity

              - sequence: 40
                action: deny
                description: rmap2-40-deny
                match:
                  route_types:
                    - level-1
                    - level-2
                  tags: 2
                  ip:
                    multicast:
                      rp:
                        prefix: 192.0.2.0/24
                        rp_type: ASM
                      source: 203.0.113.0/24
                      group_range:
                        first: 239.0.0.1
                        last: 239.255.255.255

          - route_map: rmap3
            entries:
              - sequence: 10
                description: "*** first stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      verify_availability:
                        - address: 3.3.3.3
                          track: 1
                        - address: 4.4.4.4
                          track: 3

              - sequence: 20
                description: "*** second stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      address: 6.6.6.6 2.2.2.2
                      load_share: true
                      drop_on_fail: true

              - sequence: 30
                description: "*** third stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      peer_address: true

              - sequence: 40
                description: "*** fourth stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      unchanged: true
                      redist_unchanged: true
        state: merged

    # Task output
    # -------------
    #  before: []
    #
    #  commands:
    #    - "route-map rmap1 permit 10"
    #    - "match as-number 65564"
    #    - "match as-path Allow40"
    #    - "match ip address acl_1"
    #    - "description rmap1-10-permit"
    #    - "route-map rmap1 deny 20"
    #    - "match community BGPCommunity1 BGPCommunity2"
    #    - "match ip address prefix-list AllowPrefix1 AllowPrefix2"
    #    - "description rmap1-20-deny"
    #    - "set dampening 30 1500 10000 120"
    #    - "route-map rmap2 permit 20"
    #    - "match interface Ethernet1/1"
    #    - "match ipv6 address prefix-list AllowIPv6Prefix"
    #    - "set as-path prepend 65563 65568 65569"
    #    - "description rmap2-20-permit"
    #    - "continue 40"
    #    - "set comm-list BGPCommunity delete"
    #    - "route-map rmap2 deny 40"
    #    - "match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM"
    #    - "match route-type level-1 level-2"
    #    - "match tag 2"
    #    - "description rmap2-40-deny"
    #    - "route-map rmap3 permit 10"
    #    - "description *** first stanza ***"
    #    - "set ip next-hop verify-availability 3.3.3.3 track 1"
    #    - "set ip next-hop verify-availability 4.4.4.4 track 3"
    #    - "route-map rmap3 permit 20"
    #    - "description *** second stanza ***"
    #    - "set ip next-hop 6.6.6.6 2.2.2.2 load-share  drop-on-fail"
    #    - "route-map rmap3 permit 30"
    #    - "description *** third stanza ***"
    #    - "set ip next-hop peer-address"
    #    - "route-map rmap3 permit 40"
    #    - "description *** fourth stanza ***"
    #    - "set ip next-hop unchanged"
    #    - "set ip next-hop redist-unchanged"
    #
    #  after:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    #   - route_map: rmap3
    #     entries:
    #     - sequence: 10
    #       description: "*** first stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             verify_availability:
    #             - address: 3.3.3.3
    #               track: 1
    #             - address: 4.4.4.4
    #               track: 3
    #
    #     - sequence: 20
    #       description: "*** second stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             address: 6.6.6.6 2.2.2.2
    #             load_share: true
    #             drop_on_fail: true
    #
    #     - sequence: 30
    #       description: "*** third stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             peer_address: true
    #
    #     - sequence: 40
    #       description: "*** fourth stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             unchanged: true
    #             redist_unchanged: true

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny
    # route-map rmap3 permit 10
    #   description *** first stanza ***
    #   set ip next-hop verify-availability 3.3.3.3 track 1
    #   set ip next-hop verify-availability 4.4.4.4 track 3
    # route-map rmap3 permit 20
    #   description *** second stanza ***
    #   set ip next-hop 6.6.6.6 2.2.2.2 load-share  drop-on-fail
    # route-map rmap3 permit 30
    #   description *** third stanza ***
    #   set ip next-hop peer-address
    # route-map rmap3 permit 40
    #   description *** fourth stanza ***
    #   set ip next-hop unchanged
    #   set ip next-hop redist-unchanged
    #
    # Using replaced
    # (for the listed route-map(s), sequences that are in running-config but not in the task are negated)

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny
    # route-map rmap3 permit 10
    #   description *** first stanza ***
    #   set ip next-hop verify-availability 3.3.3.3 track 1
    #   set ip next-hop verify-availability 4.4.4.4 track 3
    # route-map rmap3 permit 20
    #   description *** second stanza ***
    #   set ip next-hop 6.6.6.6 2.2.2.2 load-share  drop-on-fail
    # route-map rmap3 permit 30
    #   description *** third stanza ***
    #   set ip next-hop peer-address
    # route-map rmap3 permit 40
    #   description *** fourth stanza ***
    #   set ip next-hop unchanged
    #   set ip next-hop redist-unchanged
    #
    - name: Replace route-maps configurations of listed route-maps with provided configurations
      cisco.nxos.nxos_route_maps:
        config:
          - route_map: rmap1
            entries:
              - sequence: 20
                action: deny
                description: rmap1-20-deny
                match:
                  community:
                    community_list:
                      - BGPCommunity4
                      - BGPCommunity5
                  ip:
                    address:
                      prefix_lists:
                        - AllowPrefix1
                set:
                  community:
                    local_as: true

          - route_map: rmap3
            entries:
              - sequence: 10
                description: "*** first stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      verify_availability:
                        - address: 3.3.3.3
                          track: 1
              - sequence: 20
                description: "*** second stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      peer_address: true
              - sequence: 30
                description: "*** third stanza ***"
                action: permit
                set:
                  ip:
                    next_hop:
                      address: 6.6.6.6 2.2.2.2
                      load_share: true
                      drop_on_fail: true
        state: replaced

    # Task output
    # -------------
    #  before:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    #   - route_map: rmap3
    #     entries:
    #     - sequence: 10
    #       description: "*** first stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             verify_availability:
    #             - address: 3.3.3.3
    #               track: 1
    #             - address: 4.4.4.4
    #               track: 3
    #
    #     - sequence: 20
    #       description: "*** second stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             address: 6.6.6.6 2.2.2.2
    #             load_share: true
    #             drop_on_fail: true
    #
    #     - sequence: 30
    #       description: "*** third stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             peer_address: true
    #
    #     - sequence: 40
    #       description: "*** fourth stanza ***"
    #       action: permit
    #       set:
    #         ip:
    #           next_hop:
    #             unchanged: true
    #             redist_unchanged: true
    #
    #  commands:
    #    - no route-map rmap1 permit 10
    #    - route-map rmap1 deny 20
    #    - no match community BGPCommunity1 BGPCommunity2
    #    - match community BGPCommunity4 BGPCommunity5
    #    - no match ip address prefix-list AllowPrefix1 AllowPrefix2
    #    - match ip address prefix-list AllowPrefix1
    #    - no set dampening 30 1500 10000 120
    #    - set community local-AS
    #    - route-map rmap3 permit 10
    #    - no set ip next-hop verify-availability 4.4.4.4 track 3
    #    - route-map rmap3 permit 20
    #    - no set ip next-hop 6.6.6.6 2.2.2.2 load-share drop-on-fail
    #    - set ip next-hop peer-address
    #    - route-map rmap3 permit 30
    #    - no set ip next-hop peer-address
    #    - set ip next-hop 6.6.6.6 2.2.2.2 load-share drop-on-fail
    #    - no route-map rmap3 permit 40
    #
    #  after:
    #    - route_map: rmap1
    #      entries:
    #        - sequence: 20
    #          action: deny
    #          description: rmap1-20-deny
    #          match:
    #            community:
    #              community_list:
    #                - BGPCommunity4
    #                - BGPCommunity5
    #            ip:
    #              address:
    #                prefix_lists:
    #                  - AllowPrefix1
    #          set:
    #            community:
    #              local_as: true
    #
    #    - route_map: rmap2
    #      entries:
    #        - action: permit
    #          continue_sequence: 40
    #          description: rmap2-20-permit
    #          match:
    #            interfaces:
    #            - Ethernet1/1
    #            ipv6:
    #              address:
    #                prefix_lists:
    #                - AllowIPv6Prefix
    #          sequence: 20
    #          set:
    #            as_path:
    #              prepend:
    #                as_number:
    #                - '65563'
    #                - '65568'
    #                - '65569'
    #            comm_list: BGPCommunity
    #
    #        - action: deny
    #          description: rmap2-40-deny
    #          match:
    #            ip:
    #              multicast:
    #                group_range:
    #                  first: 239.0.0.1
    #                  last: 239.255.255.255
    #                rp:
    #                  prefix: 192.0.2.0/24
    #                  rp_type: ASM
    #                source: 203.0.113.0/24
    #            route_types:
    #            - level-1
    #            - level-2
    #            tags:
    #            - 2
    #          sequence: 40
    #
    #    - route_map: rmap3
    #      entries:
    #      - sequence: 10
    #        description: "*** first stanza ***"
    #        action: permit
    #        set:
    #          ip:
    #            next_hop:
    #              verify_availability:
    #              - address: 3.3.3.3
    #                track: 1
    #      - sequence: 20
    #        description: "*** second stanza ***"
    #        action: permit
    #        set:
    #          ip:
    #            next_hop:
    #              peer_address: true
    #      - sequence: 30
    #        description: "*** third stanza ***"
    #        action: permit
    #        set:
    #          ip:
    #            next_hop:
    #              address: 6.6.6.6 2.2.2.2
    #              load_share: true
    #              drop_on_fail: true

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 deny 20
    #   description rmap1-20-deny
    #   match community BGPCommunity4 BGPCommunity5
    #   match ip address prefix-list AllowPrefix1
    #   set community local-AS
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny
    # route-map rmap3 permit 10
    #   description *** first stanza ***
    #   set ip next-hop verify-availability 3.3.3.3 track 1
    # route-map rmap3 permit 20
    #   description *** second stanza ***
    #   set ip next-hop peer-address
    # route-map rmap3 permit 30
    #   description *** third stanza ***
    #   set ip next-hop 6.6.6.6 2.2.2.2 load-share  drop-on-fail

    # Using overridden

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny

    - name: Override all route-maps configuration with provided configuration
      cisco.nxos.nxos_route_maps:
        config:
          - route_map: rmap1
            entries:
              - sequence: 20
                action: deny
                description: rmap1-20-deny
                match:
                  community:
                    community_list:
                      - BGPCommunity4
                      - BGPCommunity5
                  ip:
                    address:
                      prefix_lists:
                        - AllowPrefix1
                set:
                  community:
                    local_as: true
        state: overridden

    # Task output
    # -------------
    #  before:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    #  commands:
    #    - no route-map rmap1 permit 10
    #    - route-map rmap1 deny 20
    #    - no match community BGPCommunity1 BGPCommunity2
    #    - match community BGPCommunity4 BGPCommunity5
    #    - no match ip address prefix-list AllowPrefix1 AllowPrefix2
    #    - match ip address prefix-list AllowPrefix1
    #    - no set dampening 30 1500 10000 120
    #    - set community local-AS
    #    - no route-map rmap2 permit 20
    #    - no route-map rmap2 deny 40
    #
    #  after:
    #  - route_map: rmap1
    #    entries:
    #    - sequence: 20
    #      action: deny
    #      description: rmap1-20-deny
    #      match:
    #        community:
    #          community_list:
    #          - BGPCommunity4
    #          - BGPCommunity5
    #        ip:
    #          address:
    #            prefix_lists:
    #            - AllowPrefix1
    #      set:
    #        community:
    #          local_as: true
    #
    # After state:
    # ------------
    # nxos-9k-rdo# sh running-config | section "^route-map"
    # route-map rmap1 deny 20
    #   description rmap1-20-deny
    #   match community BGPCommunity4 BGPCommunity5
    #   match ip address prefix-list AllowPrefix1
    #   set community local-AS

    # Using deleted to delete a single route-map

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny

    - name: Delete single route-map
      cisco.nxos.nxos_route_maps:
        config:
          - route_map: rmap1
        state: deleted

    # Task output
    # -------------
    #  before:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    #  commands:
    #    - no route-map rmap1 permit 10
    #    - no route-map rmap1 deny 20
    #
    #  after:
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    # After state:
    # ------------
    # nxos-9k-rdo# sh running-config | section "^route-map"
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny

    # Using deleted to delete all route-maps from the device running-config

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny

    - name: Delete all route-maps
      cisco.nxos.nxos_route_maps:
        state: deleted

    # Task output
    # -------------
    #  before:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40
    #
    #  commands:
    #    - no route-map rmap1 permit 10
    #    - no route-map rmap1 deny 20
    #    - no route-map rmap2 permit 20
    #    - no route-map rmap2 deny 40
    #
    #  after: []
    #
    # After state:
    # ------------
    # nxos-9k-rdo# sh running-config | section "^route-map"

    - name: Render platform specific configuration lines with state rendered (without connecting to the device)
      cisco.nxos.nxos_route_maps:
        config:
          - route_map: rmap1
            entries:
              - sequence: 10
                action: permit
                description: rmap1-10-permit
                match:
                  ip:
                    address:
                      access_list: acl_1
                  as_path: Allow40
                  as_number:
                    asn: 65564

              - sequence: 20
                action: deny
                description: rmap1-20-deny
                match:
                  community:
                    community_list:
                      - BGPCommunity1
                      - BGPCommunity2
                  ip:
                    address:
                      prefix_lists:
                        - AllowPrefix1
                        - AllowPrefix2
                set:
                  dampening:
                    half_life: 30
                    start_reuse_route: 1500
                    start_suppress_route: 10000
                    max_suppress_time: 120

          - route_map: rmap2
            entries:
              - sequence: 20
                action: permit
                description: rmap2-20-permit
                continue_sequence: 40
                match:
                  ipv6:
                    address:
                      prefix_lists: AllowIPv6Prefix
                  interfaces: "{{ nxos_int1 }}"
                set:
                  as_path:
                    prepend:
                      as_number:
                        - 65563
                        - 65568
                        - 65569
                  comm_list: BGPCommunity

              - sequence: 40
                action: deny
                description: rmap2-40-deny
                match:
                  route_types:
                    - level-1
                    - level-2
                  tags: 2
                  ip:
                    multicast:
                      rp:
                        prefix: 192.0.2.0/24
                        rp_type: ASM
                      source: 203.0.113.0/24
                      group_range:
                        first: 239.0.0.1
                        last: 239.255.255.255
        state: rendered

    # Task Output (redacted)
    # -----------------------
    #  rendered:
    #    - "route-map rmap1 permit 10"
    #    - "match as-number 65564"
    #    - "match as-path Allow40"
    #    - "match ip address acl_1"
    #    - "description rmap1-10-permit"
    #    - "route-map rmap1 deny 20"
    #    - "match community BGPCommunity1 BGPCommunity2"
    #    - "match ip address prefix-list AllowPrefix1 AllowPrefix2"
    #    - "description rmap1-20-deny"
    #    - "set dampening 30 1500 10000 120"
    #    - "route-map rmap2 permit 20"
    #    - "match interface Ethernet1/1"
    #    - "match ipv6 address prefix-list AllowIPv6Prefix"
    #    - "set as-path prepend 65563 65568 65569"
    #    - "description rmap2-20-permit"
    #    - "continue 40"
    #    - "set comm-list BGPCommunity delete"
    #    - "route-map rmap2 deny 40"
    #    - "match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM"
    #    - "match route-type level-1 level-2"
    #    - "match tag 2"
    #    - "description rmap2-40-deny"

    # Using parsed

    # parsed.cfg
    # ------------
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap1 deny 20
    #   match community BGPCommunity1 BGPCommunity2
    #   match ip address prefix-list AllowPrefix1 AllowPrefix2
    #   description rmap1-20-deny
    #   set dampening 30 1500 10000 120
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete
    # route-map rmap2 deny 40
    #   match ip multicast source 203.0.113.0/24 group-range 239.0.0.1 to 239.255.255.255 rp 192.0.2.0/24 rp-type ASM
    #   match route-type level-1 level-2
    #   match tag 2
    #   description rmap2-40-deny

    - name: Parse externally provided route-maps configuration
      cisco.nxos.nxos_route_maps:
        running_config: "{{ lookup('file', './fixtures/parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    #  parsed:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #     - action: deny
    #       description: rmap1-20-deny
    #       match:
    #         community:
    #           community_list:
    #           - BGPCommunity1
    #           - BGPCommunity2
    #         ip:
    #           address:
    #             prefix_lists:
    #             - AllowPrefix1
    #             - AllowPrefix2
    #       sequence: 20
    #       set:
    #         dampening:
    #           half_life: 30
    #           max_suppress_time: 120
    #           start_reuse_route: 1500
    #           start_suppress_route: 10000
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #
    #     - action: deny
    #       description: rmap2-40-deny
    #       match:
    #         ip:
    #           multicast:
    #             group_range:
    #               first: 239.0.0.1
    #               last: 239.255.255.255
    #             rp:
    #               prefix: 192.0.2.0/24
    #               rp_type: ASM
    #             source: 203.0.113.0/24
    #         route_types:
    #         - level-1
    #         - level-2
    #         tags:
    #         - 2
    #       sequence: 40

    # Using gathered

    # Existing route-map config
    # ---------------------------
    # nxos-9k-rdo# show running-config | section "^route-map"
    # route-map rmap1 permit 10
    #   match as-number 65564
    #   match as-path Allow40
    #   match ip address acl_1
    #   description rmap1-10-permit
    # route-map rmap2 permit 20
    #   match interface Ethernet1/1
    #   match ipv6 address prefix-list AllowIPv6Prefix
    #   set as-path prepend 65563 65568 65569
    #   description rmap2-20-permit
    #   continue 40
    #   set comm-list BGPCommunity delete

    - name: Gather route-maps facts using gathered
      cisco.nxos.nxos_route_maps:
        state: gathered

    #  gathered:
    #   - route_map: rmap1
    #     entries:
    #     - action: permit
    #       description: rmap1-10-permit
    #       match:
    #         as_number:
    #           asn:
    #           - '65564'
    #         as_path:
    #           - Allow40
    #         ip:
    #           address:
    #             access_list: acl_1
    #       sequence: 10
    #
    #   - route_map: rmap2
    #     entries:
    #     - action: permit
    #       continue_sequence: 40
    #       description: rmap2-20-permit
    #       match:
    #         interfaces:
    #         - Ethernet1/1
    #         ipv6:
    #           address:
    #             prefix_lists:
    #             - AllowIPv6Prefix
    #         sequence: 20
    #         set:
    #           as_path:
    #             prepend:
    #               as_number:
    #               - '65563'
    #               - '65568'
    #               - '65569'
    #           comm_list: BGPCommunity
    #



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
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when changed</td>
                <td>
                            <div>The resulting configuration model invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The configuration prior to the model invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format
     of the parameters above.</div>
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
                <td>always</td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;route-map rmap1 permit 10&#x27;, &#x27;match as-number 65564&#x27;, &#x27;match as-path Allow40&#x27;, &#x27;match ip address acl_1&#x27;, &#x27;description rmap1-10-permit&#x27;, &#x27;route-map rmap1 deny 20&#x27;, &#x27;match community BGPCommunity1 BGPCommunity2&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
