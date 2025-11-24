.. _cisco.nxos.nxos_vrf_interfaces_module:


******************************
cisco.nxos.nxos_vrf_interfaces
******************************

**Resource module to configure VRF interfaces.**


Version added: 9.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module configures and manages the VRF configuration on interfaces on NX-OS platforms.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
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
                        <div>A list of interface VRF configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Full name of the interface excluding any logical unit number, i.e. Ethernet1/1.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Name of the VRF to be configured on the interface.</div>
                        <div>When configured, applies &#x27;vrf member &lt;vrf_name&gt;&#x27; under the interface.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config interface</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
   - Tested against Cisco NX-OS.
   - This module works with connection ``network_cli``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no switchport
    # interface Ethernet1/2
    #  description test
    #  no switchport
    #  no shutdown
    # interface Ethernet1/3
    # interface Ethernet1/4
    #  no switchport
    #  speed 1000
    #  no shutdown

    - name: Merge provided configuration with device configuration
      cisco.nxos.nxos_vrf_interfaces:
        config:
          - name: Ethernet1/1
          - name: Ethernet1/2
            vrf_name: test
          - name: Ethernet1/3
          - name:Ethernet1/4
        state: merged

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #
    # commands:
    #   - interface Ethernet1/2
    #   - vrf member test
    #
    # after:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #     vrf_name: "test2"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"

    # After state:
    # ------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no ip address
    # interface Ethernet1/2
    #  vrf member test
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Ethernet1/3
    #  no ip address
    #  negotiation auto
    # interfaceEthernet1/4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using overridden

    # Before state:
    # -------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no ip address
    # interface Ethernet1/1
    #  ip address dhcp
    #  negotiation auto
    # interface Ethernet1/2
    #  vrf member vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Ethernet1/3
    #  no ip address
    #  negotiation auto
    # interface Ethernet1/4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Override device configuration with provided configuration
      cisco.nxos.nxos_vrf_interfaces:
        config:
          - name: Ethernet1/1
          - name: Ethernet1/2
          - name: Ethernet1/3
          - name: Ethernet1/4
        state: overridden

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #     vrf_name: "vrf_B"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #
    # commands:
    #   - interface Ethernet1/2
    #   - no vrf member vrf_B
    #
    # after:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"

    # After state:
    # ------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no ip address
    # interface Ethernet1/2
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Ethernet1/3
    #  no ip address
    #  negotiation auto
    # interface Ethernet1/4
    #  no ip address
    #  shutdown
    #  negotiation auto

    # Using gathered

    # Before state:
    # -------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no ip address
    # interface Ethernet1/2
    #  vrf member vrf_B
    #  no ip address
    #  shutdown
    #  negotiation auto
    # interface Ethernet1/3
    #  no ip address
    #  negotiation auto
    # interfaceEthernet1/4
    #  no ip address
    #  shutdown
    #  negotiation auto

    - name: Gather listed VRF interfaces
      cisco.nxos.nxos_vrf_interfaces:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #     vrf_name: "vrf_B"
    #   - name: "Ethernet1/3"

    # Using rendered

    - name: Render VRF configuration
      cisco.nxos.nxos_vrf_interfaces:
        config:
          - name: Ethernet1/1
          - name: Ethernet1/2
            vrf_name: test
          - name: Ethernet1/3
          - name: Ethernet1/4
        state: rendered

    # Task Output:
    # ------------
    #
    # rendered:
    #   - interface Ethernet1/2
    #   - vrf member test

    # Using parsed

    # File: parsed.cfg
    # ---------------
    #
    # interface Ethernet1/2
    #   no switchport
    #   vrf member VRF1
    # interface Ethernet1/6
    #   no switchport
    #   speed 1000
    #   vrf member TEST_VRF

    - name: Parse configuration from device running config
      cisco.nxos.nxos_vrf_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    #
    # parsed:
    #   - name: "Ethernet1/2"
    #     vrf_name: "VRF1"
    #   - name: "Ethernet1/6"
    #     vrf_name: "TEST_VRF"

    # Using replaced

    # Before state:
    # -------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  no ip address
    # interface Ethernet1/2
    #  vrf member vrf_B
    #  no ip address
    #  shutdown
    # interface Ethernet1/3
    #  no ip address
    # interfaceEthernet1/4
    #  vrf member vrf_C
    #  no ip address
    #  shutdown

    - name: Replace device configuration of listed VRF interfaces with provided configuration
      cisco.nxos.nxos_vrf_interfaces:
        config:
          - name: Ethernet1/1
            vrf_name: test
          - name: Ethernet1/2
            vrf_name: vrf_E
        state: replaced

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Ethernet1/1"
    #     vrf_name: "vrf_A"
    #   - name: "Ethernet1/2"
    #     vrf_name: "vrf_B"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #     vrf_name: "vrf_C"
    #
    # commands:
    #   - interface Ethernet1/1
    #   - no vrf member vrf_A
    #   - vrf member test
    #   - interface Ethernet1/2
    #   - no vrf member vrf_B
    #   - vrf member vrf_E
    #
    # after:
    #   - name: "Ethernet1/1"
    #     vrf_name: "test"
    #   - name: "Ethernet1/2"
    #     vrf_name: "vrf_E"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #     vrf_name: "vrf_C"

    # Using deleted

    # Before state:
    # -------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  vrf member vrf_A
    #  ip address dhcp
    # interface Ethernet1/2
    #  vrf member vrf_B
    #  no ip address
    #  shutdown
    # interface Ethernet1/3
    #  no ip address
    # interfaceEthernet1/4
    #  vrf member vrf_C
    #  no ip address
    #  shutdown

    - name: Delete VRF configuration of specified interfaces
      cisco.nxos.nxos_vrf_interfaces:
        config:
          - name: Ethernet1/1
          - name: Ethernet1/2
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    #   - name: "Ethernet1/1"
    #     vrf_name: "vrf_A"
    #   - name: "Ethernet1/2"
    #     vrf_name: "vrf_B"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #     vrf_name: "vrf_C"
    #
    # commands:
    #   - interface Ethernet1/1
    #   - no vrf member vrf_A
    #   - interface Ethernet1/2
    #   - no vrf member vrf_B
    #
    # after:
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/1"
    #   - name: "Ethernet1/2"
    #   - name: "Ethernet1/3"
    #   - name: "Ethernet1/4"
    #     vrf_name: "vrf_C"

    # After state:
    # ------------
    #
    # nxos#show running-config interface
    # interface Ethernet1/1
    #  ip address dhcp
    # interface Ethernet1/2
    #  no ip address
    #  shutdown
    # interface Ethernet1/3
    #  no ip address
    # interfaceEthernet1/4
    #  vrf member vrf_C
    #  no ip address
    #  shutdown



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Ethernet1/1&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/2&quot;,
            &quot;vrf_name&quot;: &quot;test&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/3&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/4&quot;
        }
    ]</div>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code></td>
                <td>
                            <div>The configuration prior to the module execution.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Ethernet1/1&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/2&quot;,
            &quot;vrf_name&quot;: &quot;test&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/3&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/4&quot;
        }
    ]</div>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/2&#x27;, &#x27;vrf member test&#x27;, &#x27;no vrf member vrf_B&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Ethernet1/1&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/2&quot;,
            &quot;vrf_name&quot;: &quot;vrf_B&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/3&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/4&quot;
        }
    ]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[
        {
            &quot;name&quot;: &quot;Ethernet1/1&quot;,
            &quot;vrf_name&quot;: &quot;vrf_C&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/2&quot;,
            &quot;vrf_name&quot;: &quot;test&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/3&quot;
        },
        {
            &quot;name&quot;: &quot;Ethernet1/4&quot;
        }
    ]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;vrf member vrf_C&#x27;, &#x27;interface Ethernet1/2&#x27;, &#x27;vrf member test&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ruchi Pakhle (@Ruchip16)
