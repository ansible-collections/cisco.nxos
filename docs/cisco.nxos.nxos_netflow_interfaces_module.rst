.. _cisco.nxos.nxos_netflow_interfaces_module:


**********************************
cisco.nxos.nxos_netflow_interfaces
**********************************

**NetFlow interfaces resource module.**


Version added: 14.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the assignment of flow monitors to the interfaces of Cisco NX-OS devices.
- It manages the ``ip flow monitor``, ``ipv6 flow monitor`` and ``layer2-switched flow monitor`` commands of an interface.
- The flow monitors themselves must already exist on the device, they are managed by ``cisco.nxos.nxos_netflow_global``.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="3">
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
                        <div>A list of the flow monitor assignments of interfaces.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>flow_monitors</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The flow monitors that are applied on the interface.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>direction</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>input</li>
                                    <li>output</li>
                        </ul>
                </td>
                <td>
                        <div>The direction of the traffic that the flow monitor is applied on.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>monitor</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the flow monitor.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>protocol</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>ipv4</b>&nbsp;&larr;</div></li>
                                    <li>ipv6</li>
                                    <li>layer2_switched</li>
                        </ul>
                </td>
                <td>
                        <div>The protocol, <code>ipv4</code> is <code>ip flow monitor</code>, <code>ipv6</code> is <code>ipv6 flow monitor</code> and <code>layer2_switched</code> is <code>layer2-switched flow monitor</code>.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>The name of the interface, for example <code>Ethernet1/1</code>, <code>port-channel10</code> or <code>Vlan100</code>. Interface names are normalised.</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | include &quot;^interface|^  (ip|ipv6|layer2-switched</b> flow monitor&quot;).</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
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
                        <div>The state the configuration should be left in.</div>
                        <div>With <em>merged</em> the flow monitors are added, a flow monitor with another name for the same protocol and direction is replaced.</div>
                        <div>With <em>replaced</em> the flow monitors of the interfaces in <em>config</em> are replaced by the given ones.</div>
                        <div>With <em>overridden</em> the flow monitors of all the interfaces are replaced, the interfaces not in <em>config</em> lose theirs.</div>
                        <div>With <em>deleted</em> the flow monitors of the interfaces in <em>config</em> are removed, without <em>config</em> those of all the interfaces.</div>
                        <div>With <em>gathered</em>, <em>rendered</em> and <em>parsed</em> nothing is changed on the device.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
   - Unsupported for Cisco MDS.
   - The flow monitor commands need ``feature netflow``, and the flow monitors must already exist with an exporter.
   - The ``layer2_switched`` protocol is only accepted on a switchport.
   - The direction ``output`` needs the ``egr-netflow`` TCAM region to be carved, ``ipv6`` only accepts ``input`` on the tested platform.
   - The ``sampler`` option of the flow monitor commands is not available on the tested platform.
   - This module works with connection ``network_cli`` and ``httpapi``.
   - The *parsed* state reads configuration from ``running_config`` and does not connect to the device.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
    # interface Ethernet1/1
    # interface Ethernet1/2

    - name: Apply flow monitors on the interfaces
      cisco.nxos.nxos_netflow_interfaces:
        config:
          - name: Ethernet1/1
            flow_monitors:
              - monitor: MON_V4
                direction: input
              - monitor: MON_V6
                protocol: ipv6
                direction: input
          - name: Ethernet1/2
            flow_monitors:
              - monitor: MON_L2
                protocol: layer2_switched
                direction: input
        state: merged

    # Task output:
    # ------------
    # before: []
    # commands:
    #   - interface Ethernet1/1
    #   - ip flow monitor MON_V4 input
    #   - ipv6 flow monitor MON_V6 input
    #   - interface Ethernet1/2
    #   - layer2-switched flow monitor MON_L2 input
    # after:
    #   - name: Ethernet1/1
    #     flow_monitors:
    #       - monitor: MON_V4
    #         direction: input
    #         protocol: ipv4
    #       - monitor: MON_V6
    #         direction: input
    #         protocol: ipv6
    #   - name: Ethernet1/2
    #     flow_monitors:
    #       - monitor: MON_L2
    #         direction: input
    #         protocol: layer2_switched

    # Using replaced

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
    # interface Ethernet1/1
    #   ip flow monitor MON_V4 input
    #   ipv6 flow monitor MON_V6 input

    - name: Replace the flow monitors of Ethernet1/1
      cisco.nxos.nxos_netflow_interfaces:
        config:
          - name: Ethernet1/1
            flow_monitors:
              - monitor: MON_V4_NEW
                direction: input
        state: replaced

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/1
    #   - no ip flow monitor MON_V4 input
    #   - ip flow monitor MON_V4_NEW input
    #   - no ipv6 flow monitor MON_V6 input

    # Using overridden

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
    # interface Ethernet1/1
    #   ip flow monitor MON_V4 input
    # interface Ethernet1/2
    #   layer2-switched flow monitor MON_L2 input

    - name: Override the flow monitors of all the interfaces
      cisco.nxos.nxos_netflow_interfaces:
        config:
          - name: Ethernet1/1
            flow_monitors:
              - monitor: MON_V4
                direction: input
        state: overridden

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/2
    #   - no layer2-switched flow monitor MON_L2 input

    # Using deleted

    - name: Remove the flow monitors of Ethernet1/1
      cisco.nxos.nxos_netflow_interfaces:
        config:
          - name: Ethernet1/1
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/1
    #   - no ip flow monitor MON_V4 input

    - name: Remove the flow monitors of all the interfaces
      cisco.nxos.nxos_netflow_interfaces:
        state: deleted

    # Using gathered

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  (ip|ipv6|layer2-switched) flow monitor"
    # interface Ethernet1/1
    #   ip flow monitor MON_V4 input
    # interface Ethernet1/2

    - name: Gather the flow monitors of the interfaces
      cisco.nxos.nxos_netflow_interfaces:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   - name: Ethernet1/1
    #     flow_monitors:
    #       - monitor: MON_V4
    #         direction: input
    #         protocol: ipv4

    # Using rendered

    - name: Render the commands for the provided configuration
      cisco.nxos.nxos_netflow_interfaces:
        config:
          - name: Eth1/3
            flow_monitors:
              - monitor: MON_V4
                direction: input
              - monitor: MON_V6
                protocol: ipv6
                direction: input
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - interface Ethernet1/3
    #   - ip flow monitor MON_V4 input
    #   - ipv6 flow monitor MON_V6 input

    # Using parsed

    # parsed.cfg
    # ----------
    # interface Ethernet1/1
    #   ip flow monitor MON_V4 input
    # interface Ethernet1/2

    - name: Parse the provided configuration
      cisco.nxos.nxos_netflow_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   - name: Ethernet1/1
    #     flow_monitors:
    #       - monitor: MON_V4
    #         direction: input
    #         protocol: ipv4



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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;ip flow monitor MON_V4 input&#x27;]</div>
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
                            <div>The device native config provided in <em>running_config</em> option, parsed into structured data.</div>
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
                            <div>The provided configuration rendered in device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;ip flow monitor MON_V4 input&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørgen Spange (@jorgenspange)
