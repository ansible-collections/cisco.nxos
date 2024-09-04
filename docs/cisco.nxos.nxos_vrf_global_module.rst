.. _cisco.nxos.nxos_vrf_global_module:


**************************
cisco.nxos.nxos_vrf_global
**************************

**Resource module to configure VRF definitions.**


Version added: 8.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VRF definitions on Cisco NXOS.




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
                        <div>A list containing device configurations for VRF.</div>
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
                        <div>List of VRF definitions.</div>
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
                        <div>Description of the VRF.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>Configure IP features for the specified vrf.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>auto_discard</b>
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
                        <div>Auto 0.0.0.0/0 discard route.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>domain_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Add list domain names.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>domain_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify default domain name.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>icmp_err</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable ICMP error message.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure source-address for applications.</div>
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
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>loopback</li>
                                    <li>ethernet</li>
                                    <li>port-channel</li>
                        </ul>
                </td>
                <td>
                        <div>Source interface for ICMP error messages.</div>
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
                    <b>interface_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source interface value for ICMP error messages.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>igmp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGMP global configuration commands</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssm_translate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Translate IGMPv1/v2 reports to (S,G) route entries.</div>
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
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source address.</div>
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
                        <div>Group address.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mroutes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure multicast routes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast group address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>preference</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Preference value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Source address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Configure IP multicast global parameters.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_range_prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group range prefix-list policy for multicast boundary.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multipath</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure ECMP multicast load splitting.</div>
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
                    <b>resilient</b>
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
                        <div>Configure resilient RPF interface.</div>
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
                    <b>splitting_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure multicast load splitting type.</div>
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
                    <b>legacy</b>
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
                        <div>Configure hash based on source and group.</div>
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
                    <b>nbm</b>
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
                        <div>Configure NBM controlled RPF interface.</div>
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
                    <b>none</b>
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
                        <div>Disable multicast load splitting.</div>
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
                    <b>sg_hash</b>
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
                        <div>Configure hash based on source and group address.</div>
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
                    <b>sg_hash_next_hop</b>
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
                        <div>Configure hash based on source and group address and next-hop.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rpf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure RPF check.</div>
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
                    <b>group_list_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group range for RPF select.</div>
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
                    <b>vrf_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF for RPF lookup.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name_server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify nameserver address.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure multicast name server address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Display per-VRF information.</div>
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
                    <b>source_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>source address for configuring name server.</div>
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
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure static routes.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>destination</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Next-hop address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Destination prefix.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route tag.</div>
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
                    <b>route_pref</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route preference.</div>
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
                    <b>tag_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route tag value.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure track object.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>add vrf to the route.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>Configure IPv6 features for the specified vrf.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mld_ssm_translate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Translate MLDv1/v2 reports to (S,G) route entries.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>icmp</b>
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
                        <div>Configure ICMP parameters with mld.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>Group address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Configure IP multicast global parameters for ipv6.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_range_prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group range prefix-list policy for multicast boundary.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multipath</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure ECMP multicast load splitting.</div>
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
                    <b>resilient</b>
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
                        <div>Configure resilient RPF interface.</div>
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
                    <b>splitting_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure multicast load splitting type.</div>
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
                    <b>none</b>
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
                        <div>Disable multicast load splitting.</div>
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
                    <b>sg_hash</b>
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
                        <div>Configure hash based on source and group address.</div>
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
                    <b>sg_hash_next_hop</b>
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
                        <div>Configure hash based on source and group address and next-hop.</div>
                </td>
            </tr>




            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
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
                        <div>Configure IP multicast options.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>service_reflect</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure service reflect option.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>map_to</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map to interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>service_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>configure service interface.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the VRF..</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Network Identifier.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>layer_3</b>
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
                        <div>Configure Layer 3 VNI.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VNI number.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^vrf</b>.</div>
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
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>deleted</li>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>rendered</li>
                                    <li>overridden</li>
                                    <li>purged</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^vrf</em>. connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - This module works with connection ``network_cli`` and ``httpapi``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf

    - name: Merge provided VRF configuration
      cisco.nxos.vrf_global:
        config:
          vrfs:
            - name: testvrf
              description: this is description
              ip:
                auto_discard: true
                domain_list:
                  - example.net
                  - example.com
                domain_name: test.com
                icmp_err:
                  source_interface:
                    interface: port-channel
                    interface_value: '1'
                igmp:
                  ssm_translate:
                    - group: 232.0.0.0/8
                      source: 10.1.1.1
                    - group: 239.1.2.3/24
                      source: 192.168.1.1
                mroutes:
                  - group: 192.168.1.0/24
                    source: 192.168.1.1
                  - group: 192.168.1.0/24
                    preference: 2
                    source: 192.168.1.2
                    vrf: temp1
                multicast:
                  multipath:
                    resilient: true
                    splitting_type:
                      legacy: true
                  rpf:
                    - group_list_range: 238.1.0.0/24
                      vrf_name: temp1
                    - group_list_range: 239.1.0.0/24
                      vrf_name: temp1
                name_server:
                  address_list:
                    - 192.168.0.1
                    - 192.168.0.2
                    - 192.168.1.1
                    - 192.169.1.3
                  use_vrf:
                    source_address: 192.168.0.1
                    vrf: temp1
                route:
                  - destination: 192.0.2.22
                    source: 192.0.0.0/24
                  - destination: 192.0.2.22
                    source: 192.0.0.0/24
                    vrf: temp1
                  - destination: 192.0.2.22
                    source: 192.0.2.0/24
                    tags:
                      route_pref: 4
                      tag_value: 2
              ipv6:
                mld_ssm_translate:
                  - group: 'ff28::/16'
                    source: '2001:db8:0:abcd::2'
                  - group: 'ff30::/16'
                    source: '2001:db8:0:abcd::5'
                multicast:
                  group_range_prefix_list: temp2
                  multipath:
                    resilient: true
                    splitting_type:
                      none: true
              multicast:
                service_reflect:
                  - map_to: Ethernet2/2
                    service_interface: Ethernet1/1
                  - map_to: Ethernet4/2
                    service_interface: Ethernet2/1
              vni:
                vni_number: 5
        state: merged

    # Task Output:
    # ------------

    # before: {}
    # commands:
    #   - vrf context test1
    #   - description this is description
    #   - ip auto-discard
    #   - ip domain-name test.net
    #   - ip name-server 192.168.0.1 192.168.0.2 192.168.1.1 192.169.1.3
    #   - ip icmp-errors source-interface port-channel 1
    #   - ip multicast multipath resilient
    #   - ip multicast multipath legacy
    #   - ip name-server 192.168.0.1 use-vrf temp1
    #   - vni 5
    #   - ipv6 multicast group-range prefix-list temp2
    #   - ipv6 multicast multipath resilient
    #   - ipv6 multicast multipath none
    #   - ip domain-list test.org
    #   - ip domain-list example.com
    #   - ip domain-list example.net
    #   - ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #   - ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #   - ip mroute 192.168.1.0/24 192.168.1.1
    #   - ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #   - ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   - ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   - ip route 192.0.0.0/24 192.0.2.22
    #   - ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   - ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #   - multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2
    #   - multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2
    #   - ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2
    #   - ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::5

    # after:
    # 	vrfs:
    # 	 - name: testvrf
    # 	   description: this is description
    # 	   ip:
    # 	     auto_discard: true
    # 	     domain_list:
    # 	     - example.net
    # 	     - example.com
    # 	     domain_name: test.com
    # 	     icmp_err:
    # 	       source_interface:
    # 	         interface: port-channel
    # 	         interface_value: '1'
    # 	     igmp:
    # 	       ssm_translate:
    # 	       - group: 232.0.0.0/8
    # 	         source: 10.1.1.1
    # 	       - group: 239.1.2.3/24
    # 	         source: 192.168.1.1
    # 	     mroutes:
    # 	     - group: 192.168.1.0/24
    # 	       source: 192.168.1.1
    # 	     - group: 192.168.1.0/24
    # 	       preference: 2
    # 	       source: 192.168.1.2
    # 	       vrf: temp1
    # 	     multicast:
    # 	       multipath:
    # 	         resilient: true
    # 	         splitting_type:
    # 	           legacy: true
    # 	       rpf:
    # 	       - group_list_range: 238.1.0.0/24
    # 	         vrf_name: temp1
    # 	       - group_list_range: 239.1.0.0/24
    # 	         vrf_name: temp1
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.0.1
    # 	       - 192.168.0.2
    # 	       - 192.168.1.1
    # 	       - 192.169.1.3
    # 	       use_vrf:
    # 	         source_address: 192.168.0.1
    # 	         vrf: temp1
    # 	     route:
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.0.0/24
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.0.0/24
    # 	        vrf: temp1
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.2.0/24
    # 	       tags:
    # 	         route_pref: 4
    # 	         tag_value: 2
    # 	   ipv6:
    # 	     mld_ssm_translate:
    # 	     - group: ff28::/16
    # 	       source: 2001:db8:0:abcd::2
    # 	     - group: ff30::/16
    # 	       source: 2001:db8:0:abcd::5
    # 	     multicast:
    # 	       group_range_prefix_list: temp2
    # 	       multipath:
    # 	         resilient: true
    # 	         splitting_type:
    # 	           none: true
    # 	   multicast:
    # 	     service_reflect:
    # 	      - map_to: Ethernet2/2
    # 	        service_interface: Ethernet1/1
    # 	      - map_to: Ethernet4/2
    # 	        service_interface: Ethernet2/1
    # 	   vni:
    # 	     vni_number: 5

    # After state:
    # ------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context testvrf
    #   description this is description
    #   ip auto-discard
    #   ip domain-name test.net
    #   ip name-server 192.168.0.1 192.168.0.2 192.168.1.1 192.169.1.3
    #   ip icmp-errors source-interface port-channel 1
    #   ip multicast multipath resilient
    #   ip multicast multipath legacy
    #   ip name-server 192.168.0.1 use-vrf temp1
    #   vni 5
    #   ipv6 multicast group-range prefix-list temp2
    #   ipv6 multicast multipath resilient
    #   ipv6 multicast multipath none
    #   ip domain-list test.org
    #   ip domain-list example.com
    #   ip domain-list example.net
    #   ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #   ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #   ip mroute 192.168.1.0/24 192.168.1.1
    #   ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #   ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   ip route 192.0.0.0/24 192.0.2.22
    #   ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #   multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2
    #   multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2
    #   ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2
    #   ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::5

    # Using deleted

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context management
    #  ip name-server 192.168.255.1
    #  ip route 0.0.0.0/0 192.168.255.1
    # vrf context test1
    #  description this is description
    #  ip domain-name test.net
    #  ip domain-list example.net
    #  ip domain-list example.com
    #  ip domain-list test.org
    #  vni 5
    #  ip auto-discard
    #  ip route 192.0.0.0/24 192.0.2.22
    #  ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #  ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #  ip mroute 192.168.1.0/24 192.168.1.1
    #  ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #  ip icmp-errors source-interface po1
    #  ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #  ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #  ip multicast multipath legacy
    #  ip multicast multipath resilient
    #  ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #  ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #  ip multicast group-range prefix-list temp2

    - name: Delete VRF configuration
      cisco.nxos.vrf_global:
        config:
          vrfs:
            - name: test1
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1
    # 	   description: this is description
    # 	   ip:
    # 	     domain_name: test.net
    # 	     domain_list:
    # 	     - test.org
    # 	     - example.net
    # 	     - example.com
    # 	     auto_discard: true
    # 	     route:
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	       vrf: temp1
    # 	     - source: 192.0.2.0/24
    # 	       destination: 192.0.2.22
    # 	       tags:
    # 	         tag_value: 2
    # 	         route_pref: 4
    # 	     mroutes:
    # 	     - group: 192.168.1.0/24
    # 	       source: 192.168.1.1
    # 	     - group: 192.168.1.0/24
    # 	       source: 192.168.1.2
    # 	       preference: 2
    # 	       vrf: temp1
    # 	     icmp_err:
    # 	       source_interface:
    # 	         interface: port-channel
    # 	         interface_value: '1'
    # 	     igmp:
    # 	       ssm_translate:
    # 	       - group: 232.0.0.0/8
    # 	         source: 10.1.1.1
    # 	       - group: 239.1.2.3/24
    # 	         source: 192.168.1.1
    # 	     multicast:
    # 	       multipath:
    # 	         splitting_type:
    # 	           legacy: true
    # 	         resilient: true
    # 	       rpf:
    # 	       - vrf_name: temp1
    # 	         group_list_range: 238.1.0.0/24
    # 	       - vrf_name: temp1
    # 	         group_list_range: 239.1.0.0/24
    # 	   vni:
    # 	     vni_number: 5

    # commands:
    #   - vrf context test1
    #   - no description this is description
    #   - no ip auto-discard
    #   - no ip domain-name test.net
    #   - no ip icmp-errors source-interface port-channel 1
    #   - no ip multicast multipath resilient
    #   - no ip multicast multipath legacy
    #   - no vni 5
    #   - no ip domain-list example.net
    #   - no ip domain-list test.org
    #   - no ip domain-list example.com
    #   - no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #   - no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #   - no ip mroute 192.168.1.0/24 192.168.1.1
    #   - no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #   - no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   - no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   - no ip route 192.0.0.0/24 192.0.2.22
    #   - no ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   - no ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #
    # after:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1

    # Using deleted with empty config

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context management
    #  ip name-server 192.168.255.1
    #  ip route 0.0.0.0/0 192.168.255.1
    # vrf context test1
    #  description this is description
    #  ip domain-name test.net
    #  ip domain-list example.net
    #  ip domain-list example.com
    #  ip domain-list test.org
    #  vni 5

    - name: Delete VRF configuration
      cisco.nxos.vrf_global:
        config:
          vrfs:
            - name: test1
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1
    # 	   description: this is description
    # 	   ip:
    # 	     domain_name: test.net
    # 	     domain_list:
    # 	     - test.org
    # 	     - example.net
    # 	     - example.com
    # 	   vni:
    # 	     vni_number: 5

    # commands:
    #   - vrf context management
    #   - no ip name-server 192.168.255.1
    #   - no ip route 0.0.0.0/0 192.168.255.1
    #   - vrf context test1
    #   - no description this is description
    #   - no ip domain-name test.net
    #   - no vni 5
    #   - no ip domain-list example.net
    #   - no ip domain-list test.org
    #   - no ip domain-list example.com

    # after:
    # 	vrfs:
    # 	  - name: management
    # 	  - name: test1

    # Using purged

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context management
    #   ip name-server 192.168.255.1
    #   ip route 0.0.0.0/0 192.168.255.1
    # vrf context test1
    #   description this is description
    #   ip domain-name example.com
    #   ip domain-list example.net
    #   ip domain-list example.org
    #   vni 5
    #   ip auto-discard
    #   ip route 192.0.0.0/24 192.0.2.22
    #   ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    # vrf context test2
    #   description test description
    #   ip auto-discard
    #   ip domain-name test.com

    - name: Override VRF configuration
      cisco.nxos.vrf_global:
        config:
          vrfs:
            - name: test1
            - name: test2
        state: purged

    # Task Output:
    # ------------
    #
    # before:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1
    # 	   description: this is description
    # 	   ip:
    # 	     domain_name: example.com
    # 	     domain_list:
    # 	     - example.net
    # 	     - example.org
    # 	     auto_discard: true
    # 	     route:
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	       vrf: temp1
    # 	     - source: 192.0.2.0/24
    # 	       destination: 192.0.2.22
    # 	       tags:
    # 	         tag_value: 2
    # 	         route_pref: 4
    # 	  vni:
    # 	    vni_number: 5
    # 	 - name: test2
    # 	   description: test description
    # 	   ip:
    # 	     auto_discard: true
    # 	     domain_name: test.com
    #
    # commands:
    # - no vrf context test1
    # - no vrf context test2
    #
    # after:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1

    # Using overridden

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context management
    #   ip name-server 192.168.255.1
    #   ip route 0.0.0.0/0 192.168.255.1
    # vrf context test1
    #   description this is description
    #   ip domain-name example.com
    #   ip domain-list example.net
    #   ip domain-list example.org
    #   vni 5
    #   ip auto-discard
    #   ip route 192.0.0.0/24 192.0.2.22
    #   ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    # vrf context test2
    #   description test description
    #   ip auto-discard
    #   ip domain-name test.com

    - name: Override VRF configuration
      cisco.nxos.vrf_global:
        config:
          vrfs:
            - name: management
              ip:
                name_server:
                  address_list:
                    - 192.168.255.1
                route:
                  - source: 0.0.0.0/0
                    destination: 192.168.255.1
            - name: test1
              ip:
                auto_discard: false
                name_server:
                  address_list:
                    - 192.168.255.1
                route:
                  - source: 192.0.0.0/24
                    destination: 192.0.2.22
        state: overridden

    # Task Output:
    # ------------
    #
    # before:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1
    # 	   description: this is description
    # 	   ip:
    # 	     domain_name: example.com
    # 	     domain_list:
    # 	     - example.net
    # 	     - example.org
    # 	     auto_discard: true
    # 	     route:
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22
    # 	       vrf: temp1
    # 	     - source: 192.0.2.0/24
    # 	       destination: 192.0.2.22
    # 	       tags:
    # 	         tag_value: 2
    # 	         route_pref: 4
    # 	   vni:
    # 	     vni_number: 5
    # 	 - name: test2
    # 	   description: test description
    # 	   ip:
    # 	     auto_discard: true
    # 	     domain_name: test.com
    #
    # commands:
    # - vrf context test1
    # - no description this is description
    # - no ip domain-name example.com
    # - no ip domain-list example.net
    # - no ip domain-list example.org
    # - ip name-server 192.168.255.1
    # - no ip auto-discard
    # - no vni 5
    # - no ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    # - no ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    # - vrf context test2
    # - no description test description
    # - no ip auto-discard
    # - no ip domain-name test.com
    #
    # after:
    # 	vrfs:
    # 	 - name: management
    # 	   ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 0.0.0.0/0
    # 	       destination: 192.168.255.1
    # 	 - name: test1
    # 	   ip:
    # 	     auto_discard: false
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - source: 192.0.0.0/24
    # 	       destination: 192.0.2.22

    # Using replaced

    # Before state:
    # -------------
    #
    # nxos# show running-config | section ^vrf
    # vrf context management
    #   ip name-server 192.168.255.1
    #   ip route 0.0.0.0/0 192.168.255.1
    # vrf context temp
    #   ip domain-name test.org
    #   ip domain-list example.net
    #   ip domain-list example.com
    #   ip domain-list test.org
    #   ip name-server 192.168.0.1 192.169.1.3
    #   ip name-server 192.168.0.1 use-vrf temp1
    #   multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2
    #   multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2
    #   description this is descrition
    #   vni 5
    #   ip auto-discard
    #   ip route 192.0.0.0/24 192.0.2.22
    #   ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #   ip mroute 192.168.1.0/24 192.168.1.1
    #   ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #   ip icmp-errors source-interface po1
    #   ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #   ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #   ip multicast multipath legacy
    #   ip multicast multipath resilient
    #   ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   ip multicast group-range prefix-list temp2
    #   ipv6 multicast multipath none
    #   ipv6 multicast multipath resilient
    #   ipv6 multicast group-range prefix-list temp2
    #   ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2
    #   ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::1
    #   ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::2
    #   ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::3

    - name: Replaced state for VRF configuration
      cisco.nxos.nxos_vrf_global:
        config:
          vrfs:
            - ip:
                name_server:
                  address_list:
                    - 192.168.255.1
                route:
                  - destination: 192.168.255.1
                    source: 0.0.0.0/0
              name: management
            - name: temp
              description: Test
              ip:
                auto_discard: true
                domain_list:
                  - invalid.com
                  - example.com
                domain_name: test.org
        state: replaced

    # Task Output:
    # ------------
    #
    # before:
    # 	vrfs:
    # 	 - ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - destination: 192.168.255.1
    # 	       source: 0.0.0.0/0
    # 	   name: management
    # 	 - description: this is descrition
    # 	   ip:
    # 	     auto_discard: true
    # 	     domain_list:
    # 	     - example.net
    # 	     - test.org
    # 	     - example.com
    # 	     domain_name: test.org
    # 	     icmp_err:
    # 	       source_interface:
    # 	         interface: port-channel
    # 	         interface_value: '1'
    # 	     igmp:
    # 	       ssm_translate:
    # 	       - group: 232.0.0.0/8
    # 	         source: 10.1.1.1
    # 	       - group: 239.1.2.3/24
    # 	         source: 192.168.1.1
    # 	     mroutes:
    # 	     - group: 192.168.1.0/24
    # 	       source: 192.168.1.1
    # 	     - group: 192.168.1.0/24
    # 	       preference: 2
    # 	       source: 192.168.1.2
    # 	       vrf: temp1
    # 	     multicast:
    # 	       multipath:
    # 	         resilient: true
    # 	         splitting_type:
    # 	           legacy: true
    # 	       rpf:
    # 	       - group_list_range: 238.1.0.0/24
    # 	         vrf_name: temp1
    # 	       - group_list_range: 239.1.0.0/24
    # 	         vrf_name: temp1
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.0.1
    # 	       - 192.169.1.3
    # 	       use_vrf:
    # 	         source_address: 192.168.0.1
    # 	         vrf: temp1
    # 	     route:
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.0.0/24
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.0.0/24
    # 	       vrf: temp1
    # 	     - destination: 192.0.2.22
    # 	       source: 192.0.2.0/24
    # 	       tags:
    # 	         route_pref: 4
    # 	         tag_value: 2
    # 	   ipv6:
    # 	     mld_ssm_translate:
    # 	     - group: ff28::/16
    # 	       source: 2001:db8:0:abcd::2
    # 	     - group: ff30::/16
    # 	       source: 2001:db8:0:abcd::1
    # 	     - group: ff32::/16
    # 	       source: 2001:db8:0:abcd::2
    # 	     - group: ff32::/16
    # 	       source: 2001:db8:0:abcd::3
    # 	     multicast:
    # 	       group_range_prefix_list: temp2
    # 	       multipath:
    # 	         resilient: true
    # 	         splitting_type:
    # 	           none: true
    # 	   multicast:
    # 	     service_reflect:
    # 	     - map_to: Ethernet2/2
    # 	       service_interface: Ethernet1/1
    # 	     - map_to: Ethernet4/2
    # 	       service_interface: Ethernet2/1
    # 	   name: temp
    # 	   vni:
    # 	     vni_number: 5
    #
    # commands:
    #   - vrf context temp
    #   - description Test
    #   - no ip name-server 192.168.0.1 192.169.1.3
    #   - no ip icmp-errors source-interface port-channel 1
    #   - no ip multicast multipath resilient
    #   - no ip multicast multipath legacy
    #   - no ip name-server 192.168.0.1 use-vrf temp1
    #   - no vni 5
    #   - no ipv6 multicast group-range prefix-list temp2
    #   - no ipv6 multicast multipath resilient
    #   - no ipv6 multicast multipath none
    #   - ip domain-list invalid.com
    #   - no ip domain-list example.net
    #   - no ip domain-list test.org
    #   - no ip igmp ssm-translate 232.0.0.0/8 10.1.1.1
    #   - no ip igmp ssm-translate 239.1.2.3/24 192.168.1.1
    #   - no ip mroute 192.168.1.0/24 192.168.1.1
    #   - no ip mroute 192.168.1.0/24 192.168.1.2 2 vrf temp1
    #   - no ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   - no ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   - no ip route 192.0.0.0/24 192.0.2.22
    #   - no ip route 192.0.0.0/24 192.0.2.22 vrf temp1
    #   - no ip route 192.0.2.0/24 192.0.2.22 tag 2 4
    #   - no multicast service-reflect interface Ethernet1/1 map interface Ethernet2/2
    #   - no multicast service-reflect interface Ethernet2/1 map interface Ethernet4/2
    #   - no ipv6 mld ssm-translate ff28::/16 2001:db8:0:abcd::2
    #   - no ipv6 mld ssm-translate ff30::/16 2001:db8:0:abcd::1
    #   - no ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::2
    #   - no ipv6 mld ssm-translate ff32::/16 2001:db8:0:abcd::3
    #
    # after:
    # 	vrfs:
    # 	 - ip:
    # 	     name_server:
    # 	       address_list:
    # 	       - 192.168.255.1
    # 	     route:
    # 	     - destination: 192.168.255.1
    # 	       source: 0.0.0.0/0
    # 	   name: management
    # 	 - description: Test
    # 	   ip:
    # 	     auto_discard: true
    # 	     domain_list:
    # 	     - invalid.com
    # 	     - example.com
    # 	     domain_name: test.org
    # 	     multicast:
    # 	       rpf:
    # 	       - group_list_range: 238.1.0.0/24
    # 	         vrf_name: temp1
    # 	       - group_list_range: 239.1.0.0/24
    # 	         vrf_name: temp1
    #
    # After state:
    # ------------
    # router-ios#show running-config | section ^vrf
    # vrf context management
    #   ip name-server 192.168.255.1
    #   ip route 0.0.0.0/0 192.168.255.1
    # vrf context temp
    #   ip domain-name test.org
    #   ip domain-list example.com
    #   ip domain-list invalid.com
    #   description Test
    #   ip auto-discard
    #   ip multicast rpf select vrf temp1 group-list 238.1.0.0/24
    #   ip multicast rpf select vrf temp1 group-list 239.1.0.0/24
    #   ip multicast group-range prefix-list temp2



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
                      <span style="color: purple">dictionary</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf context management&#x27;, &#x27;description this is management vrf&#x27;, &#x27;ip domain-name example.com&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
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
                      <span style="color: purple">dictionary</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf context test1&#x27;, &#x27;description This is a test VRF&#x27;, &#x27;ip route 192.0.0.0/24 192.0.2.22&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Vinay Mulugund (@roverflow)
