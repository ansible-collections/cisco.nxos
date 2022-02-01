.. _cisco.nxos.nxos_ntp_global_module:


**************************
cisco.nxos.nxos_ntp_global
**************************

**NTP Global resource module.**


Version added: 2.6.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages ntp configuration on devices running Cisco NX-OS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
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
                        <div>A dict of ntp configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>access_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NTP access-group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match_all</b>
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
                        <div>Scan ACLs present in all ntp access groups.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Access-group peer.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Name of access list.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Access-group query-only.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Name of access list.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serve</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Access-group serve.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Name of access list.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serve_only</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Access-group serve-only.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Name of access list.</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable/Disable the packets.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>control</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Control mode packets.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rate_limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Rate-limit delay.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>private</b>
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
                        <div>Enable/Disable Private mode packets.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authenticate</b>
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
                        <div>Enable/Disable authentication.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NTP authentication key.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>0 for Clear text</div>
                        <div>7 for Encrypted</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key number (range 1-65535).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication key.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>logging</b>
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
                        <div>Enable/Disable logging of NTPD Events.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>master</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Act as NTP master clock.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>stratum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Stratum number.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>passive</b>
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
                        <div>NTP passive command.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NTP Peers.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Keyid to be used while communicating to this server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maxpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum interval to poll a peer.</div>
                        <div>Poll interval in secs to a power of 2.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum interval to poll a peer.</div>
                        <div>Poll interval in secs to a power of 2.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hostname/IP address of the NTP Peer.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefer</b>
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
                        <div>Preferred Server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
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
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>servers</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NTP servers.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Keyid to be used while communicating to this server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maxpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum interval to poll a peer.</div>
                        <div>Poll interval in secs to a power of 2.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minpoll</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum interval to poll a peer.</div>
                        <div>Poll interval in secs to a power of 2.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefer</b>
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
                        <div>Preferred Server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hostname/IP address of the NTP Peer.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
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
                        <div>Source of NTP packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source interface sending NTP packets.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trusted_keys</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>NTP trusted-key number.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Trusted-Key number.</div>
                </td>
            </tr>


            <tr>
                <td colspan="4">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config ntp</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
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
                        <div>The states <em>replaced</em> and <em>overridden</em> have identical behaviour for this module.</div>
                        <div>Please refer to examples for more details.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - This module works with connection ``network_cli`` and ``httpapi``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos-9k-rdo# show running-config ntp
    # nxos-9k-rdo#

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_ntp_global: &id001
        config:
          access_group:
            peer:
              - access_list: PeerAcl1
            serve:
              - access_list: ServeAcl1
          authenticate: True
          authentication_keys:
            - id: 1001
              key: vagwwtKfkv
              encryption: 7
            - id: 1002
              key: vagwwtKfkvgthz
              encryption: 7
          logging: True
          master:
            stratum: 2
          peers:
            - peer: 192.0.2.1
              key_id: 1
              maxpoll: 15
              minpoll: 5
              use_vrf: default
            - peer: 192.0.2.2
              key_id: 2
              prefer: True
              use_vrf: siteA
          servers:
            - server: 198.51.100.1
              key_id: 2
              use_vrf: default
            - server: 203.0.113.1
              key_id: 1
              use_vrf: siteB

    # Task output
    # -------------
    #  before: {}
    #
    #  commands:
    #    - "ntp authenticate"
    #    - "ntp logging"
    #    - "ntp master 2"
    #    - "ntp authentication-keys 1001 md5 vagwwtKfkv 7"
    #    - "ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7"
    #    - "ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15"
    #    - "ntp peer 192.0.2.2 prefer use-vrf siteA key 2"
    #    - "ntp server 198.51.100.1 use-vrf default key 2"
    #    - "ntp server 203.0.113.1 use-vrf siteB key 1"
    #    - "ntp access-group peer PeerAcl1"
    #    - "ntp access-group serve ServeAcl1"
    #
    #  after:
    #    access_group:
    #      peer:
    #        - access_list: PeerAcl1
    #      serve:
    #       - access_list: ServeAcl1
    #    authenticate: True
    #    authentication_keys:
    #      - id: 1001
    #        key: vagwwtKfkv
    #        encryption: 7
    #      - id: 1002
    #        key: vagwwtKfkvgthz
    #        encryption: 7
    #    logging: True
    #    master:
    #     stratum: 2
    #    peers:
    #      - peer: 192.0.2.1
    #        key_id: 1
    #        maxpoll: 15
    #        minpoll: 5
    #        use_vrf: default
    #      - peer: 192.0.2.2
    #        key_id: 2
    #        prefer: True
    #        use_vrf: siteA
    #    servers:
    #      - server: 198.51.100.1
    #        key_id: 2
    #        use_vrf: default
    #      - server: 203.0.113.1
    #        key_id: 1
    #        use_vrf: siteB

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config ntp
    # ntp authenticate
    # ntp logging
    # ntp master 2
    # ntp authentication-keys 1001 md5 vagwwtKfkv 7
    # ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7
    # ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15
    # ntp peer 192.0.2.2 prefer use-vrf siteA key 2
    # ntp server 198.51.100.1 use-vrf default key 2
    # ntp server 203.0.113.1 use-vrf siteB key 1
    # ntp access-group peer PeerAcl1
    # ntp access-group serve ServeAcl1

    # Using replaced

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config ntp
    # ntp authenticate
    # ntp logging
    # ntp master 2
    # ntp authentication-keys 1001 md5 vagwwtKfkv 7
    # ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7
    # ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15
    # ntp peer 192.0.2.2 prefer use-vrf siteA key 2
    # ntp server 198.51.100.1 use-vrf default key 2
    # ntp server 203.0.113.1 use-vrf siteB key 1
    # ntp access-group peer PeerAcl1
    # ntp access-group serve ServeAcl1

    - name: Replace logging global configurations of listed logging global with provided configurations
      cisco.nxos.nxos_ntp_global:
        config:
          access_group:
            peer:
              - access_list: PeerAcl2
            serve:
              - access_list: ServeAcl2
          logging: True
          master:
            stratum: 2
          peers:
            - peer: 192.0.2.1
              key_id: 1
              maxpoll: 15
              minpoll: 5
              use_vrf: default
            - peer: 192.0.2.5
              key_id: 2
              prefer: True
              use_vrf: siteA
          servers:
            - server: 198.51.100.1
              key_id: 2
              use_vrf: default
        state: replaced

    # Task output
    # -------------
    #  before:
    #    access_group:
    #      peer:
    #        - access_list: PeerAcl1
    #      serve:
    #       - access_list: ServeAcl1
    #    authenticate: True
    #    authentication_keys:
    #      - id: 1001
    #        key: vagwwtKfkv
    #        encryption: 7
    #      - id: 1002
    #        key: vagwwtKfkvgthz
    #        encryption: 7
    #    logging: True
    #    master:
    #     stratum: 2
    #    peers:
    #      - peer: 192.0.2.1
    #        key_id: 1
    #        maxpoll: 15
    #        minpoll: 5
    #        use_vrf: default
    #      - peer: 192.0.2.2
    #        key_id: 2
    #        prefer: True
    #        use_vrf: siteA
    #    servers:
    #      - server: 198.51.100.1
    #        key_id: 2
    #        use_vrf: default
    #      - server: 203.0.113.1
    #        key_id: 1
    #        use_vrf: siteB
    #
    #  commands:
    #    - "no ntp authenticate"
    #    - "no ntp authentication-keys 1001 md5 vagwwtKfkv 7"
    #    - "no ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7"
    #    - "ntp peer 192.0.2.5 prefer use-vrf siteA key 2"
    #    - "no ntp peer 192.0.2.2 prefer use-vrf siteA key 2"
    #    - "no ntp server 203.0.113.1 use-vrf siteB key 1"
    #    - "ntp access-group peer PeerAcl2"
    #    - "no ntp access-group peer PeerAcl1"
    #    - "ntp access-group serve ServeAcl2"
    #    - "no ntp access-group serve ServeAcl1"
    #
    #  after:
    #    access_group:
    #      peer:
    #        - access_list: PeerAcl2
    #      serve:
    #        - access_list: ServeAcl2
    #    logging: True
    #    master:
    #      stratum: 2
    #    peers:
    #      - peer: 192.0.2.1
    #        key_id: 1
    #        maxpoll: 15
    #        minpoll: 5
    #        use_vrf: default
    #      - peer: 192.0.2.5
    #        key_id: 2
    #        prefer: True
    #        use_vrf: siteA
    #    servers:
    #      - server: 198.51.100.1
    #        key_id: 2
    #        use_vrf: default

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config ntp
    # ntp logging
    # ntp master 2
    # ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15
    # ntp peer 192.0.2.5 prefer use-vrf siteA key 2
    # ntp server 198.51.100.1 use-vrf default key 2
    # ntp access-group peer PeerAcl2
    # ntp access-group serve ServeAcl2

    # Using deleted to delete all logging configurations

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config ntp

    - name: Delete all logging configuration
      cisco.nxos.nxos_ntp_global:
        state: deleted

    # Task output
    # -------------
    #  before:
    #    access_group:
    #      peer:
    #        - access_list: PeerAcl1
    #      serve:
    #       - access_list: ServeAcl1
    #    authenticate: True
    #    authentication_keys:
    #      - id: 1001
    #        key: vagwwtKfkv
    #        encryption: 7
    #      - id: 1002
    #        key: vagwwtKfkvgthz
    #        encryption: 7
    #    logging: True
    #    master:
    #     stratum: 2
    #    peers:
    #      - peer: 192.0.2.1
    #        key_id: 1
    #        maxpoll: 15
    #        minpoll: 5
    #        use_vrf: default
    #      - peer: 192.0.2.2
    #        key_id: 2
    #        prefer: True
    #        use_vrf: siteA
    #    servers:
    #      - server: 198.51.100.1
    #        key_id: 2
    #        use_vrf: default
    #      - server: 203.0.113.1
    #        key_id: 1
    #        use_vrf: siteB
    #
    #  commands:
    #    - "no ntp authenticate"
    #    - "no ntp logging"
    #    - "no ntp master 2"
    #    - "no ntp authentication-keys 1001 md5 vagwwtKfkv 7"
    #    - "no ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7"
    #    - "no ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15"
    #    - "no ntp peer 192.0.2.2 prefer use-vrf siteA key 2"
    #    - "no ntp server 198.51.100.1 use-vrf default key 2"
    #    - "no ntp server 203.0.113.1 use-vrf siteB key 1"
    #    - "no ntp access-group peer PeerAcl1"
    #    - "no ntp access-group serve ServeAcl1"
    #
    #  after: {}

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config ntp
    # nxos-9k-rdo#

    # Using rendered

    - name: Render platform specific configuration lines with state rendered (without connecting to the device)
      cisco.nxos.nxos_ntp_global:
        config:
          access_group:
            peer:
              - access_list: PeerAcl1
            serve:
              - access_list: ServeAcl1
          authenticate: True
          authentication_keys:
            - id: 1001
              key: vagwwtKfkv
              encryption: 7
            - id: 1002
              key: vagwwtKfkvgthz
              encryption: 7
          logging: True
          master:
            stratum: 2
          peers:
            - peer: 192.0.2.1
              key_id: 1
              maxpoll: 15
              minpoll: 5
              use_vrf: default
            - peer: 192.0.2.2
              key_id: 2
              prefer: True
              use_vrf: siteA
          servers:
            - server: 198.51.100.1
              key_id: 2
              use_vrf: default
            - server: 203.0.113.1
              key_id: 1
              use_vrf: siteB
        state: rendered

    # Task Output (redacted)
    # -----------------------
    #  rendered:
    #    - "ntp authenticate"
    #    - "ntp logging"
    #    - "ntp master 2"
    #    - "ntp authentication-keys 1001 md5 vagwwtKfkv 7"
    #    - "ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7"
    #    - "ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15"
    #    - "ntp peer 192.0.2.2 prefer use-vrf siteA key 2"
    #    - "ntp server 198.51.100.1 use-vrf default key 2"
    #    - "ntp server 203.0.113.1 use-vrf siteB key 1"
    #    - "ntp access-group peer PeerAcl1"
    #    - "ntp access-group serve ServeAcl1"

    # Using parsed

    # parsed.cfg
    # ------------
    # ntp authenticate
    # ntp logging
    # ntp master 2
    # ntp authentication-keys 1001 md5 vagwwtKfkv 7
    # ntp authentication-keys 1002 md5 vagwwtKfkvgthz 7
    # ntp peer 192.0.2.1 use-vrf default key 1 minpoll 5 maxpoll 15
    # ntp peer 192.0.2.2 prefer use-vrf siteA key 2
    # ntp server 198.51.100.1 use-vrf default key 2
    # ntp server 203.0.113.1 use-vrf siteB key 1
    # ntp access-group peer PeerAcl1
    # ntp access-group serve ServeAcl1

    - name: Parse externally provided ntp configuration
      cisco.nxos.nxos_ntp_global:
        running_config: "{{ lookup('file', './fixtures/parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    # parsed:
    #    access_group:
    #      peer:
    #        - access_list: PeerAcl1
    #      serve:
    #       - access_list: ServeAcl1
    #    authenticate: True
    #    authentication_keys:
    #      - id: 1001
    #        key: vagwwtKfkv
    #        encryption: 7
    #      - id: 1002
    #        key: vagwwtKfkvgthz
    #        encryption: 7
    #    logging: True
    #    master:
    #     stratum: 2
    #    peers:
    #      - peer: 192.0.2.1
    #        key_id: 1
    #        maxpoll: 15
    #        minpoll: 5
    #        use_vrf: default
    #      - peer: 192.0.2.2
    #        key_id: 2
    #        prefer: True
    #        use_vrf: siteA
    #    servers:
    #      - server: 198.51.100.1
    #        key_id: 2
    #        use_vrf: default
    #      - server: 203.0.113.1
    #        key_id: 1
    #        use_vrf: siteB



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ntp master stratum 2&#x27;, &#x27;ntp peer 198.51.100.1 use-vrf test maxpoll 7&#x27;, &#x27;ntp authentication-key 10 md5 wawyhanx2 7&#x27;, &#x27;ntp access-group peer PeerAcl1&#x27;, &#x27;ntp access-group peer PeerAcl2&#x27;, &#x27;ntp access-group query-only QueryAcl1&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ntp master stratum 2&#x27;, &#x27;ntp peer 198.51.100.1 use-vrf test maxpoll 7&#x27;, &#x27;ntp authentication-key 10 md5 wawyhanx2 7&#x27;, &#x27;ntp access-group peer PeerAcl1&#x27;, &#x27;ntp access-group peer PeerAcl2&#x27;, &#x27;ntp access-group query-only QueryAcl1&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
