.. _cisco.nxos.nxos_hsrp_interfaces_module:


*******************************
cisco.nxos.nxos_hsrp_interfaces
*******************************

**HSRP interfaces resource module**


Version added: 10.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Resource module to configure HSRP on interfaces.




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
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary of HSRP configuration options to add to interface</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable/Disable HSRP Bidirectional Forwarding Detection (BFD) on the interface.</div>
                        <div><b>Deprecated</b>, Use standby.bfd instead, the facts would always render bfd information as a part of standby configuration</div>
                        <div>This option has been deprecated and will be removed in a release after 2028-06-01.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>standby</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Standby options generic, not idempotent when version 1 (HSRP)</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable HSRP BFD</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>HSRP initialization delay</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minimum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay at least this long</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reload</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay after reload</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_refresh</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Refresh MAC cache on switch by periodically sending packet from virtual mac address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_bia</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>HSRP uses interface&#x27;s burned in address (does not work with mac address)</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scope</b>
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
                        <div>Scope interface option (hsrp use-bia scope interface)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Set use-bia only</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>HSRP version</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>standby_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group number and group options for standby (HSRP)</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>authentication</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Authentication configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_chain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key chain</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key_string</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set key string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password_text</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password text valid for plain text and and key-string</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>follow</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Groups to be followed</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Redundancy name string</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_no</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group number</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable HSRP IPv4 and set the virtual IP address</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>secondary</b>
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
                        <div>Make this IP address a secondary virtual IP address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>virtual_ip</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual IP address</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual MAC address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>preempt</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Overthrow lower priority Active routers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>minimum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay at least this long</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reload</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delay after reload</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sync</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Wait for IP redundancy clients</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>priority</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority level</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority level value</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lower</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set lower threshold value (forwarding-threshold)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>upper</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set upper threshold value (forwarding-threshold)</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timer</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Overthrow lower priority Active routers</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hello_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hello interval in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hold_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hold time in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>msec</b>
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
                        <div>Specify hello interval in milliseconds</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>track</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority tracking</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>decrement</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Priority decrement</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>object_no</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Track object number</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^interface&#x27;</b>.</div>
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^interface</em> executed on device. For state <em>parsed</em> active connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 10.4(2) Nexus 9000v.
   - Feature bfd and hsrp, should be enabled for this module.
   - Unsupported for Cisco MDS



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    - name: Merge provided configuration with device configuration
      cisco.nxos.nxos_hsrp_interfaces:
        config:
          - name: Ethernet1/1
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_string: SECUREKEY10
                group_name: VLAN10-GROUP
                group_no: 10
                ip:
                  - secondary: true
                    virtual_ip: 10.10.10.2
                mac_address: 00CC.10DD.10EE
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    # - name: Ethernet1/2
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7
    #  commands:
    # - interface Ethernet1/1
    # - hsrp version 2
    # - hsrp mac-refresh 400
    # - hsrp 10
    # - mac-address 00CC.10DD.10EE
    # - name VLAN10-GROUP
    # - authentication md5 key-string SECUREKEY10
    # - ip 10.10.10.2 secondary
    # - interface Ethernet1/2
    # - hsrp bfd
    # - hsrp version 2
    # - hsrp mac-refresh 400
    # - hsrp 20
    # - mac-address 00CC.10DD.10EF
    # - name VLAN20-GROUP
    # - authentication md5 key-chain SECUREKEY20
    # - ip 10.10.10.3 secondary
    #  after:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN10-GROUP
    #       group_no: 10
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.2
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.3
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 10
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN10-GROUP
    #     mac-address 00CC.10DD.10EE
    #     ip 10.10.10.2 secondary
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    #     ip 10.10.10.3 secondary
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    # Using replaced

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 10
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN10-GROUP
    #     mac-address 00CC.10DD.10EE
    #     ip 10.10.10.2 secondary
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    #     ip 10.10.10.3 secondary
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.nxos.nxos_hsrp_interfaces:
        config:
          - name: Ethernet1/1
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_string: SECUREKEY10
                group_name: VLAN11-GROUP
                group_no: 11
                mac_address: 00CC.10DD.10EE
          - name: Ethernet1/2
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_chain: SECUREKEY20
                group_name: VLAN20-GROUP
                group_no: 20
                mac_address: 00CC.10DD.10EF
        state: replaced

    # Task Output
    # -----------
    #
    #  before:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN10-GROUP
    #       group_no: 10
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.2
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.3
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7
    #  commands:
    # - interface Ethernet1/1
    # - hsrp 11
    # - mac-address 00CC.10DD.10EE
    # - name VLAN11-GROUP
    # - authentication md5 key-string SECUREKEY10
    # - no hsrp 10
    # - interface Ethernet1/2
    # - hsrp 20
    # - no ip 10.10.10.3 secondary
    #  after:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN11-GROUP
    #       group_no: 11
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7


    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 11
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN11-GROUP
    #     mac-address 00CC.10DD.10EE
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    # Using overridden

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 10
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN10-GROUP
    #     mac-address 00CC.10DD.10EE
    #     ip 10.10.10.2 secondary
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    #     ip 10.10.10.3 secondary

    - name: Override device configuration of all interfaces with provided configuration
      cisco.nxos.nxos_hsrp_interfaces:
        config:
          - name: Ethernet1/1
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_string: SECUREKEY10
                group_name: VLAN11-GROUP
                group_no: 11
                mac_address: 00CC.10DD.10EE
          - name: Ethernet1/2
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_chain: SECUREKEY20
                group_name: VLAN20-GROUP
                group_no: 20
                mac_address: 00CC.10DD.10EF
        state: overridden

    # Task Output
    # -----------
    #
    #  before:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN10-GROUP
    #       group_no: 10
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.2
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.3
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7
    #  commands:
    # - interface Ethernet1/1
    # - hsrp 11
    # - mac-address 00CC.10DD.10EE
    # - name VLAN11-GROUP
    # - authentication md5 key-string SECUREKEY10
    # - no hsrp 10
    # - interface Ethernet1/2
    # - hsrp 20
    # - no ip 10.10.10.3 secondary
    #  after:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN11-GROUP
    #       group_no: 11
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 11
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN11-GROUP
    #     mac-address 00CC.10DD.10EE
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7


    # Using deleted

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 10
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN10-GROUP
    #     mac-address 00CC.10DD.10EE
    #     ip 10.10.10.2 secondary
    # interface Ethernet1/2
    #   no switchport
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 20
    #     authentication md5 key-chain SECUREKEY20
    #     name VLAN20-GROUP
    #     mac-address 00CC.10DD.10EF
    #     ip 10.10.10.3 secondary
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    - name: Delete or return interface parameters to default settings
      cisco.nxos.nxos_hsrp_interfaces:
        config:
          - name: Ethernet1/1
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_string: SECUREKEY10
                group_name: VLAN11-GROUP
                group_no: 11
                mac_address: 00CC.10DD.10EE
          - name: Ethernet1/2
            standby:
              bfd: true
              mac_refresh: 400
              version: 2
            standby_options:
              - authentication:
                  key_chain: SECUREKEY20
                group_name: VLAN20-GROUP
                group_no: 20
                mac_address: 00CC.10DD.10EF
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_string: SECUREKEY10
    #       group_name: VLAN10-GROUP
    #       group_no: 10
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.2
    #       mac_address: 00CC.10DD.10EE
    # - name: Ethernet1/2
    #   standby:
    #     bfd: true
    #     mac_refresh: 400
    #     version: 2
    #   standby_options:
    #     - authentication:
    #         key_chain: SECUREKEY20
    #       group_name: VLAN20-GROUP
    #       group_no: 20
    #       ip:
    #         - secondary: true
    #           virtual_ip: 10.10.10.3
    #       mac_address: 00CC.10DD.10EF
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6
    # - name: Ethernet1/7
    # commands:
    # - interface Ethernet1/1
    # - no hsrp bfd
    # - no hsrp version 2
    # - no hsrp mac-refresh 400
    # - no hsrp 10
    # - interface Ethernet1/2
    # - no hsrp bfd
    # - no hsrp version 2
    # - no hsrp mac-refresh 400
    # - no hsrp 20
    # after:
    # - name: Vlan1
    # - name: Vlan10
    # - name: Vlan14
    # - name: Vlan1000
    # - name: Ethernet1/1
    # - name: Ethernet1/2
    # - name: Ethernet1/3
    # - name: Ethernet1/4
    # - name: Ethernet1/5
    # - name: Ethernet1/6

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan10
    # interface Vlan14
    #   bandwidth 99999
    # interface Vlan1000
    # interface Ethernet1/1
    #   no switchport
    # interface Ethernet1/2
    #   no switchport
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5
    # interface Ethernet1/6
    # interface Ethernet1/7

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_hsrp_interfaces:
        config:
          - name: Ethernet1/1
            description: outbound-intf
            mode: layer3
            speed: 100
          - name: Ethernet1/2
            mode: layer2
            enabled: true
            duplex: full
        state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    #  - interface Vlan1
    #  - hsrp version 2
    #  - hsrp 10
    #  - timers msec 250 255
    #  - authentication md5 key-chain test
    #  - interface Vlan10
    #  - hsrp bfd
    #  - hsrp version 2
    #  - hsrp mac-refresh 400
    #  - hsrp 10
    #  - mac-address 00CC.10DD.10EE
    #  - name VLAN10-GROUP
    #  - preempt delay minimum 15 reload 120 sync 10
    #  - authentication md5 key-string SECUREKEY10
    #  - ip 10.10.10.2 secondary
    #  - interface Vlan14
    #  - hsrp bfd
    #  - hsrp version 2
    #  - hsrp delay 22 123
    #  - hsrp mac-refresh 300
    #  - hsrp 14
    #  - follow VLAN14-GROUP
    #  - mac-address 00AA.14BB.14CC
    #  - ip 192.168.14.1 secondary
    #  - ip 192.168.14.2 secondary
    #  - hsrp 15
    #  - mac-address 00BB.14CC.15DD
    #  - preempt delay minimum 10 reload 100 sync 5
    #  - priority 22 forwarding-threshold lower 12 upper 22
    #  - timers msec 456 33
    #  - authentication md5 key-string SECUREKEY14
    #  - interface Vlan1000
    #  - hsrp 10
    #  - mac-address 0423.4567.89AB
    #  - name testhsr
    #  - preempt delay minimum 33 reload 23 sync 22
    #  - priority 22 forwarding-threshold lower 12 upper 22
    #  - timers msec 456 33
    #  - authentication md5 key-string testmesecurte
    #  - ip 10.15.8.1 secondary


    # Using parsed

    # parsed.cfg
    # ------------
    #
    # interface Vlan1
    #   hsrp version 2
    #   hsrp 10
    #     authentication md5 key-chain test
    #     timers msec 250  255
    # interface Vlan10
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp mac-refresh 400
    #   hsrp 10
    #     authentication md5 key-string SECUREKEY10
    #     name VLAN10-GROUP
    #     mac-address 00CC.10DD.10EE
    #     preempt delay minimum 15 reload 120 sync 10
    #     ip 10.10.10.2 secondary
    # interface Vlan14
    #   bandwidth 99999
    #   hsrp bfd
    #   hsrp version 2
    #   hsrp delay minimum 22 reload 123
    #   hsrp mac-refresh 300
    #   hsrp 14
    #     follow VLAN14-GROUP
    #     mac-address 00AA.14BB.14CC
    #     ip 192.168.14.1 secondary
    #     ip 192.168.14.2 secondary
    #   hsrp 15
    #     authentication md5 key-string SECUREKEY14
    #     mac-address 00BB.14CC.15DD
    #     preempt delay minimum 10 reload 100 sync 5
    #     priority 22 forwarding-threshold lower 12 upper 22
    #     timers msec 456  33
    # interface Vlan1000
    #   hsrp 10
    #     authentication md5 key-string testmesecurte
    #     name testhsr
    #     mac-address 0423.4567.89AB
    #     preempt delay minimum 33 reload 23 sync 22
    #     priority 22 forwarding-threshold lower 12 upper 22
    #     timers msec 456  33
    #     ip 10.15.8.1 secondary

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_hsrp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output
    # -----------
    #
    # {"parsed": [
    #        {
    #            "name": "Vlan1",
    #            "standby": {
    #                "version": 2
    #            },
    #            "standby_options": [
    #                {
    #                    "authentication": {
    #                        "key_chain": "test"
    #                    },
    #                    "group_no": 10,
    #                    "timer": {
    #                        "hello_interval": 250,
    #                        "hold_time": 255,
    #                        "msec": true
    #                    }
    #                }
    #            ]
    #        },
    #        {
    #            "name": "Vlan10",
    #            "standby": {
    #                "bfd": true,
    #                "mac_refresh": 400,
    #                "version": 2
    #            },
    #            "standby_options": [
    #                {
    #                    "authentication": {
    #                        "key_string": "SECUREKEY10"
    #                    },
    #                    "group_name": "VLAN10-GROUP",
    #                    "group_no": 10,
    #                    "ip": [
    #                        {
    #                            "secondary": true,
    #                            "virtual_ip": "10.10.10.2"
    #                        }
    #                    ],
    #                    "mac_address": "00CC.10DD.10EE",
    #                    "preempt": {
    #                        "minimum": 15,
    #                        "reload": 120,
    #                        "sync": 10
    #                    }
    #                }
    #            ]
    #        },
    #        {
    #            "name": "Vlan14",
    #            "standby": {
    #                "bfd": true,
    #                "delay": {
    #                    "minimum": 22,
    #                    "reload": 123
    #                },
    #                "mac_refresh": 300,
    #                "version": 2
    #            },
    #            "standby_options": [
    #                {
    #                    "follow": "VLAN14-GROUP",
    #                    "group_no": 14,
    #                    "ip": [
    #                        {
    #                            "secondary": true,
    #                            "virtual_ip": "192.168.14.1"
    #                        },
    #                        {
    #                            "secondary": true,
    #                            "virtual_ip": "192.168.14.2"
    #                        }
    #                    ],
    #                    "mac_address": "00AA.14BB.14CC"
    #                },
    #                {
    #                    "authentication": {
    #                        "key_string": "SECUREKEY14"
    #                    },
    #                    "group_no": 15,
    #                    "mac_address": "00BB.14CC.15DD",
    #                    "preempt": {
    #                        "minimum": 10,
    #                        "reload": 100,
    #                        "sync": 5
    #                    },
    #                    "priority": {
    #                        "level": 22,
    #                        "lower": 12,
    #                        "upper": 22
    #                    },
    #                    "timer": {
    #                        "hello_interval": 456,
    #                        "hold_time": 33,
    #                        "msec": true
    #                    }
    #                }
    #            ]
    #        },
    #        {
    #            "name": "Vlan1000",
    #            "standby_options": [
    #                {
    #                    "authentication": {
    #                        "key_string": "testmesecurte"
    #                    },
    #                    "group_name": "testhsr",
    #                    "group_no": 10,
    #                    "ip": [
    #                        {
    #                            "secondary": true,
    #                            "virtual_ip": "10.15.8.1"
    #                        }
    #                    ],
    #                    "mac_address": "0423.4567.89AB",
    #                    "preempt": {
    #                        "minimum": 33,
    #                        "reload": 23,
    #                        "sync": 22
    #                    },
    #                    "priority": {
    #                        "level": 22,
    #                        "lower": 12,
    #                        "upper": 22
    #                    },
    #                    "timer": {
    #                        "hello_interval": 456,
    #                        "hold_time": 33,
    #                        "msec": true
    #                    }
    #                }
    #            ]}



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;hsrp 14&#x27;, &#x27;follow VLAN14-GROUP&#x27;, &#x27;mac-address 00AA.14BB.14CC&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;hsrp 14&#x27;, &#x27;follow VLAN14-GROUP&#x27;, &#x27;mac-address 00AA.14BB.14CC&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Chris Van Heuveln (@chrisvanheuveln)
- Sagar Paul (@KB-perByte)
