.. _cisco.nxos.nxos_vpc_interface_module:


*****************************
cisco.nxos.nxos_vpc_interface
*****************************

**VPC interface resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages VPC-related interface configuration on Cisco NX-OS devices.




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
                        <div>A list of VPC interface configurations.</div>
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
                        <div>Full name of the interface (e.g. <code>port-channel10</code> or <code>Ethernet1/3</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>orphan_port_suspend</b>
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
                        <div>When <code>true</code>, configure the interface as a VPC orphan-port that suspends when the VPC secondary peer-link goes down.</div>
                        <div>Supported on any interface type.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>peer_link</b>
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
                        <div>When <code>true</code>, configure this port-channel as the VPC peer-link.</div>
                        <div>Mutually exclusive with <em>vpc</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vpc</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VPC ID to assign to this port-channel.</div>
                        <div>Mutually exclusive with <em>peer_link</em>.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^interface</b>.</div>
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
                        <div>The state the configuration should be left in.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 10.5(5) on N9K-C93180YC-FX3H.
   - Unsupported for Cisco MDS.
   - ``vpc`` and ``peer_link`` are mutually exclusive for a given port-channel.
   - ``orphan_port_suspend`` applies to any interface type, including Ethernet interfaces.
   - This module works with connection ``network_cli`` and ``httpapi``.
   - The *parsed* state reads configuration from ``running_config`` and does not connect to the device.
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos# show running-config | section ^interface port-channel
    # interface port-channel10
    #   switchport
    # interface port-channel20
    #   switchport

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_vpc_interface:
        config:
          - name: port-channel10
            vpc: 100
          - name: port-channel20
            peer_link: true
          - name: Ethernet1/3
            orphan_port_suspend: true
        state: merged

    # Task output:
    # ------------
    # before: []
    #
    # commands:
    #   - interface port-channel10
    #   - vpc 100
    #   - interface port-channel20
    #   - vpc peer-link
    #   - interface Ethernet1/3
    #   - vpc orphan-port suspend
    #
    # after:
    #   - name: Ethernet1/3
    #     orphan_port_suspend: true
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true

    # After state:
    # ------------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link


    # Using replaced

    # Before state:
    # -------------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link

    - name: Replace the VPC configuration of listed port-channels
      cisco.nxos.nxos_vpc_interface:
        config:
          - name: port-channel10
            vpc: 200
        state: replaced

    # Task output:
    # ------------
    # before:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true
    #
    # commands:
    #   - interface port-channel10
    #   - no vpc
    #   - vpc 200
    #
    # after:
    #   - name: port-channel10
    #     vpc: "200"
    #   - name: port-channel20
    #     peer_link: true

    # Note: port-channel20 is unchanged because it is not in the config list.


    # Using overridden

    # Before state:
    # -------------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link
    # interface port-channel30
    #   vpc 300

    - name: Override all VPC interface configuration with provided configuration
      cisco.nxos.nxos_vpc_interface:
        config:
          - name: port-channel10
            vpc: 100
          - name: port-channel20
            peer_link: true
        state: overridden

    # Task output:
    # ------------
    # before:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true
    #   - name: port-channel30
    #     vpc: "300"
    #
    # commands:
    #   - interface port-channel30
    #   - no vpc
    #
    # after:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true

    # Note: port-channel30 is removed because it is not in the want list.


    # Using deleted

    # Before state:
    # -------------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link

    - name: Delete the VPC configuration of listed port-channels
      cisco.nxos.nxos_vpc_interface:
        config:
          - name: port-channel10
        state: deleted

    # Task output:
    # ------------
    # before:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true
    #
    # commands:
    #   - interface port-channel10
    #   - no vpc
    #
    # after:
    #   - name: port-channel20
    #     peer_link: true

    # Using deleted (no config — removes all VPC interface configuration)

    - name: Delete the VPC configuration of all port-channels
      cisco.nxos.nxos_vpc_interface:
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - interface port-channel10
    #   - no vpc
    #   - interface port-channel20
    #   - no vpc peer-link


    # Using gathered

    # Existing device config:
    # -----------------------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link

    - name: Gather VPC interface facts from the device
      cisco.nxos.nxos_vpc_interface:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true


    # Using rendered

    - name: Render platform specific configuration lines
      cisco.nxos.nxos_vpc_interface:
        config:
          - name: port-channel10
            vpc: 100
          - name: port-channel20
            peer_link: true
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - interface port-channel10
    #   - vpc 100
    #   - interface port-channel20
    #   - vpc peer-link


    # Using parsed

    # parsed.cfg
    # ----------
    # interface port-channel10
    #   vpc 100
    # interface port-channel20
    #   vpc peer-link

    - name: Parse externally supplied configuration into structured data
      cisco.nxos.nxos_vpc_interface:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   - name: port-channel10
    #     vpc: "100"
    #   - name: port-channel20
    #     peer_link: true



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface port-channel10&#x27;, &#x27;vpc 100&#x27;, &#x27;interface port-channel20&#x27;, &#x27;vpc peer-link&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface port-channel10&#x27;, &#x27;vpc 100&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jason Edelman (@jedelman8)
- Gabriele Gerbino (@GGabriele)
- Jorgen Spange (@jorgenspange)
