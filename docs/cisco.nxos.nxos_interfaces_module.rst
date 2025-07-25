.. _cisco.nxos.nxos_interfaces_module:


**************************
cisco.nxos.nxos_interfaces
**************************

**Interfaces resource module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes of NX-OS interfaces.




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
                        <div>A dictionary of interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Interface description.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>duplex</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>full</li>
                                    <li>half</li>
                                    <li>auto</li>
                        </ul>
                </td>
                <td>
                        <div>Interface link status. Applicable for Ethernet interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enabled</b>
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
                        <div>Administrative state of the interface. Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fabric_forwarding_anycast_gateway</b>
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
                        <div>Associate SVI with anycast gateway under VLAN configuration mode. Applicable for SVI interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip_forward</b>
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
                        <div>Enable or disable IP forward feature on SVIs. Set the value to <code>true</code> to enable  or <code>false</code> to disable.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>logging</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Logging interface events</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link_status</b>
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
                        <div>UPDOWN and CHANGE messages</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trunk_status</b>
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
                        <div>TRUNK status messages</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>E.E.E  MAC address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>layer2</li>
                                    <li>layer3</li>
                        </ul>
                </td>
                <td>
                        <div>Manage Layer2 or Layer3 state of the interface. Applicable for Ethernet and port channel interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mtu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MTU for a specific interface. Must be an even number between 576 and 9216. Applicable for Ethernet interfaces only.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
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
                        <div>Full name of interface, e.g. Ethernet1/1, port-channel10.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>service_policy</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Service policy configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>input</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the input of an interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the output of an interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the type of this policy</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>qos</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure qos Service Policy</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>input</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the input of an interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the output of an interface</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>queuing</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure queuing Service Policy</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>input</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the input of an interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Assign policy-map to the output of an interface</div>
                </td>
            </tr>



            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>snmp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Modify SNMP interface parameters</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trap</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Allow a specific SNMP trap</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link_status</b>
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
                        <div>Allow SNMP LINKUP and LINKDOWN traps (snmp trap link-status permit duplicates)</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>speed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface link speed. Applicable for Ethernet interfaces only.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^interface</b></div>
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
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>overridden</li>
                                    <li>deleted</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                                    <li>purged</li>
                        </ul>
                </td>
                <td>
                        <div>The state of the configuration after module completion</div>
                        <div>The state <em>rendered</em> considers the system default mode for interfaces to be &quot;Layer 3&quot; and the system default state for interfaces to be shutdown.</div>
                        <div>The state <em>purged</em> negates virtual interfaces that are specified in task from running-config.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOS 10.4(2) on CML
   - Unsupported for Cisco MDS



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description testing
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    - name: Merge provided configuration with device configuration
      cisco.nxos.nxos_interfaces:
        config:
          - name: Ethernet1/1
            description: Configured by Ansible
            enabled: true
          - name: Ethernet1/2
            description: Configured by Ansible Network
            enabled: false
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - description: testing
    #   name: Ethernet1/1
    # - description: mgmt interface
    #   name: mgmt0
    # commands:
    # - interface Ethernet1/1
    # - description Configured by Ansible
    # - interface Ethernet1/2
    # - description Configured by Ansible Network
    # - shutdown
    # after:
    # - description: Configured by Ansible
    #   name: Ethernet1/1
    # - description: Configured by Ansible Network
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description Configured by Ansible
    # interface Ethernet1/2
    #   description Configured by Ansible Network
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    # Using replaced

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description Updated by Ansible
    # interface Ethernet1/2
    #   description Configured by Ansible Network
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.nxos.nxos_interfaces:
        config:
          - name: Ethernet1/1
            description: Configured by Ansible
            enabled: true
            mtu: 9000
          - name: Ethernet1/2
            description: Configured by Ansible Network
            enabled: false
            mode: layer2
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    # - description: Updated by Ansible
    #   name: Ethernet1/1
    # - description: Configured by Ansible Network
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0
    # commands:
    # - interface Ethernet1/1
    # - mtu 1500
    # - interface Ethernet1/2
    # - description Updated by Ansible
    # after:
    # - description: Updated by Ansible
    #   name: Ethernet1/1
    # - description: Updated by Ansible
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description Updated by Ansible
    # interface Ethernet1/2
    #   description Updated by Ansible
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    # Using overridden

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description Updated by Ansible
    # interface Ethernet1/2
    #   description Updated by Ansible
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    - name: Override device configuration of all interfaces with provided configuration
      cisco.nxos.nxos_interfaces:
        config:
          - name: Ethernet1/1
            enabled: true
          - name: Ethernet1/2
            description: Configured by Ansible Network
            enabled: false
          - description: mgmt interface
            name: mgmt0
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    # - description: Updated by Ansible
    #   name: Ethernet1/1
    # - description: Updated by Ansible
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0
    # commands:
    # - interface Ethernet1/1
    # - no description
    # - interface Ethernet1/2
    # - description Configured by Ansible Network
    # after:
    # - name: Ethernet1/1
    # - description: Configured by Ansible Network
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    # interface Ethernet1/2
    #   description Configured by Ansible Network
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    # Using deleted

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    # interface Ethernet1/2
    #   description Configured by Ansible Network
    #   shutdown
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    - name: Delete or return interface parameters to default settings
      cisco.nxos.nxos_interfaces:
        config:
          - name: Ethernet1/2
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - name: Ethernet1/1
    # - description: Configured by Ansible Network
    #   enabled: false
    #   name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0
    # commands:
    # - interface Ethernet1/2
    # - no description
    # - no shutdown
    # after:
    # - name: Ethernet1/1
    # - name: Ethernet1/2
    # - description: mgmt interface
    #   name: mgmt0

    # After state:
    # ------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface mgmt0
    #   description mgmt interface
    #   ip address dhcp
    #   vrf member management

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_interfaces:
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
    #   - "interface Ethernet1/1"
    #   - "description outbound-intf"
    #   - "speed 100"
    #   - "interface Ethernet1/2"
    #   - "switchport"
    #   - "duplex full"
    #   - "no shutdown"

    # Using parsed

    # parsed.cfg
    # ------------
    #
    # interface Ethernet1/800
    #   description test-1
    #   speed 1000
    #   shutdown
    #   no switchport
    #   duplex half
    # interface Ethernet1/801
    #   description test-2
    #   switchport
    #   no shutdown
    #   mtu 1800

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output
    # -----------
    #
    #  parsed:
    #    - description: "test-1"
    #      duplex: "half"
    #      enabled: false
    #      mode: "layer3"
    #      name: "Ethernet1/800"
    #      speed: "1000"
    #    - description: "test-2"
    #      enabled: true
    #      mode: "layer2"
    #      mtu: "1800"
    #      name: "Ethernet1/801"

    # Using gathered

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Ethernet1/1
    #   description outbound-intf
    #   switchport
    #   no shutdown
    # interface Ethernet1/2
    #   description intf-l3
    #   speed 1000
    # interface Ethernet1/3
    # interface Ethernet1/4
    # interface Ethernet1/5

    - name: Gather interfaces facts from the device using nxos_interfaces
      cisco.nxos.nxos_interfaces:
        state: gathered

    # Task output
    # -----------
    #
    # - name: Ethernet1/1
    #   description: outbound-intf
    #   mode: layer2
    #   enabled: True
    # - name: Ethernet1/2
    #   description: intf-l3
    #   speed: "1000"

    # Using purged

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface Vlan42
    #   mtu 1800
    # interface port-channel10
    # interface port-channel11
    # interface Ethernet1/1
    # interface Ethernet1/2
    # interface Ethernet1/2.100
    #   description sub-intf

    - name: Purge virtual interfaces from running-config
      cisco.nxos.nxos_interfaces:
        config:
          - name: Vlan42
          - name: port-channel10
          - name: Ethernet1/2.100
        state: purged

    # Task output
    # ------------
    #
    # before:
    #   - name: Vlan1
    #   - mtu: '1800'
    #     name: Vlan42
    #   - name: port-channel10
    #   - name: port-channel11
    #   - name: Ethernet1/1
    #   - name: Ethernet1/2
    #   - description: sub-intf
    #     name: Ethernet1/2.100
    # commands:
    #   - no interface port-channel10
    #   - no interface Ethernet1/2.100
    #   - no interface Vlan42
    # after:
    #   - name: Vlan1
    #   - name: port-channel11
    #   - name: Ethernet1/1
    #   - name: Ethernet1/2

    # After state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface Vlan1
    # interface port-channel11
    # interface Ethernet1/1
    # interface Ethernet1/2



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
                            <div>The configuration as structured data after module completion.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                <td>always</td>
                <td>
                            <div>The configuration as structured data prior to module invocation.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">The configuration returned will always be in the same format of the parameters above.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;mtu 1800&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
- Vinay Mulugund (@roverflow)
