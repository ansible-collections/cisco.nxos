.. _cisco.nxos.nxos_fc_interfaces_module:


*****************************
cisco.nxos.nxos_fc_interfaces
*****************************

**Fc Interfaces resource module**


Version added: 5.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the interface attributes of NX-OS fc interfaces.




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
                        <div>A dictionary of interface options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>analytics</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>fc-scsi</li>
                                    <li>fc-nvme</li>
                                    <li>fc-all</li>
                        </ul>
                </td>
                <td>
                        <div>Analytics type on the fc interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                <td colspan="1">
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
                        <div>Administrative state of the interface. Set the value to <code>true</code> to administratively enable the interface or <code>true</code> to disable it</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>auto</li>
                                    <li>E</li>
                                    <li>F</li>
                                    <li>Fx</li>
                                    <li>NP</li>
                                    <li>SD</li>
                        </ul>
                </td>
                <td>
                        <div>Port mode of the fc interface</div>
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
                        <div>Full name of interface, e.g. fc1/1, fc18/48</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>speed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>auto</li>
                                    <li>1000</li>
                                    <li>2000</li>
                                    <li>4000</li>
                                    <li>8000</li>
                                    <li>10000</li>
                                    <li>16000</li>
                                    <li>32000</li>
                                    <li>64000</li>
                                    <li>auto max 2000</li>
                                    <li>auto max 4000</li>
                                    <li>auto max 8000</li>
                                    <li>auto max 16000</li>
                                    <li>auto max 32000</li>
                                    <li>auto max 64000</li>
                        </ul>
                </td>
                <td>
                        <div>Interface link speed.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>trunk_mode</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>auto</li>
                                    <li>on</li>
                                    <li>off</li>
                        </ul>
                </td>
                <td>
                        <div>Trunk mode of the fc interface</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config interface</b></div>
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
                        <div>The state of the configuration after module completion</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOS 9.3(2) on Cisco MDS Switches



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # switch# show running-config interface all
    # interface fc18/10
    #     analytics type fc-nvme
    #     switchport speed auto max 16000
    #     switchport mode auto
    #     switchport description $
    #     switchport trunk mode on
    #     shutdown

    - name: Merge provided configuration with device configuration
      cisco.nxos.nxos_fc_interfaces:
        config:
          - name: fc18/10
            analytics: fc-scsi
        state: merged

    # Task Output
    # -----------
    #
    # before:
    # - name: fc18/10
    #   speed: auto max 16000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: $
    #   analytics: fc-nvme
    # commands:
    # - interface fc18/10
    # - analytics type fc-scsi
    # after:
    # - name: fc18/10
    #   speed: auto max 16000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: $
    #   analytics: fc-all

    # After state:
    # ------------
    #
    # switch# show running-config interface all
    # interface fc18/10
    #     analytics type fc-scsi
    #     analytics type fc-nvme
    #     switchport speed auto max 16000
    #     switchport mode auto
    #     switchport description $
    #     switchport trunk mode on
    #     shutdown

    # Using replaced

    # Before state:
    # -------------
    #
    # switch# show running-config interface all
    # interface fc18/12
    #     analytics type fc-scsi
    #     analytics type fc-nvme
    #     switchport speed auto max 64000
    #     switchport mode auto
    #     switchport description 1
    #     switchport trunk mode on
    #     no shutdown

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.nxos.nxos_fc_interfaces:
        config:
          - name: fc18/12
            speed: auto max 64000
            mode: auto
            trunk_mode: "on"
            enabled: true
            description: 1
            analytics: fc-scsi
        state: replaced

    # Task Output
    # -----------
    #
    # before:
    # - name: fc18/12
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: 1
    #   analytics: fc-all
    # commands:
    # - interface fc18/12
    # - no analytics type fc-all
    # - analytics type fc-scsi
    # after:
    # - name: fc18/12
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: 1
    #   analytics: fc-scsi

    # After state:
    # ------------
    #
    # switch# show running-config interface all
    # interface fc18/12
    #     analytics type fc-scsi
    #     switchport speed auto max 64000
    #     switchport mode auto
    #     switchport description 1
    #     switchport trunk mode on
    #     no shutdown


    # Using deleted

    # Before state:
    # -------------
    #
    # switch# show running-config interface all
    # interface fc1/2
    #     switchport speed 1000
    #     switchport mode E
    #     no switchport description
    #     switchport trunk mode off
    #     no shutdown

    - name: Delete or return interface parameters to default settings
      cisco.nxos.nxos_fc_interfaces:
        config:
          - name: fc1/2
        state: deleted

    # Task Output
    # -----------
    #
    # before:
    # - name: fc1/2
    #   speed: 1000
    #   mode: E
    #   trunk_mode: off
    #   enabled: true
    # commands:
    # - interface fc1/2
    # - no switchport speed 1000
    # - no switchport mode E
    # - switchport trunk mode on
    # - shutdown
    # after:
    # - name: fc1/2
    #   speed: auto
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true

    # After state:
    # ------------
    #
    # switch# show running-config interface all
    # interface fc1/2
    #     switchport speed auto
    #     switchport mode auto
    #     no switchport description
    #     switchport trunk mode on
    #     shutdown

    # Using overridden

    # Before state:
    # -------------
    #
    # switch# show running-config interface all
    # interface fc18/12
    #     analytics type fc-scsi
    #     analytics type fc-nvme
    #     switchport speed auto max 64000
    #     switchport mode auto
    #     switchport description 1
    #     switchport trunk mode on
    #     no shutdown
    # interface fc18/13
    #     analytics type fc-scsi
    #     analytics type fc-nvme
    #     switchport speed auto max 64000
    #     switchport mode auto
    #     switchport description 1
    #     switchport trunk mode on
    #     no shutdown

    - name: Replaces device configuration of listed interfaces with provided configuration
      cisco.nxos.nxos_fc_interfaces:
        config:
          - name: fc18/12
            speed: auto max 64000
            mode: auto
            trunk_mode: "on"
            enabled: true
            description: 1
            analytics: fc-scsi
        state: overridden

    # Task Output
    # -----------
    #
    # before:
    # - name: fc18/12
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: 1
    #   analytics: fc-all
    # - name: fc18/13
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: 1
    #   analytics: fc-all
    # commands:
    # - interface fc18/12
    #   no analytics type fc-all
    #   analytics type fc-scsi
    # - interface fc18/13
    #   no switchport description
    #   no switchport speed auto max 64000
    #   no switchport mode auto
    #   switchport trunk mode on
    #   shutdown
    # after:
    # - name: fc18/12
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: 1
    #   analytics: fc-scsi
    # - name: fc18/13
    #   speed: auto max 64000
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true

    # After state:
    # ------------
    #
    # switch# show running-config interface all
    # interface fc18/12
    #     analytics type fc-scsi
    #     switchport speed auto max 64000
    #     switchport mode auto
    #     switchport description 1
    #     switchport trunk mode on
    #     no shutdown
    # interface fc18/13
    #     switchport mode auto
    #     switchport trunk mode on
    #     shutdown

    # Using rendered

    - name: Use rendered state to convert task input to device specific commands
      cisco.nxos.nxos_fc_interfaces:
        config:
          - name: fc1/1
            speed: auto
            mode: auto
            trunk_mode: "on"
            enabled: true
            description: This is a sample line
          - name: fc1/2
            speed: 1000
            mode: E
            trunk_mode: "off"
            enabled: true
            state: rendered

    # Task Output
    # -----------
    #
    # rendered:
    # interface fc1/1
    #     switchport speed auto
    #     switchport mode auto
    #     switchport description This is a sample line
    #     switchport trunk mode on
    #     no shutdown
    #
    # interface fc1/2
    #     switchport speed 1000
    #     switchport mode E
    #     no switchport description
    #     switchport trunk mode off
    #     no shutdown

    # Using parsed

    # parsed.cfg
    # ------------
    #
    # interface fc1/1
    #     switchport speed auto
    #     switchport mode auto
    #     switchport description This is a sample line
    #     switchport trunk mode on
    #     no shutdown
    #
    # interface fc1/2
    #     switchport speed 1000
    #     switchport mode E
    #     no switchport description
    #     switchport trunk mode off
    #     no shutdown

    - name: Use parsed state to convert externally supplied config to structured format
      cisco.nxos.nxos_fc_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output
    # -----------
    #
    #  parsed:
    # - name: fc1/1
    #   speed: auto
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: This is a sample line
    # - name: fc1/2
    #   speed: 1000
    #   mode: E
    #   trunk_mode: off
    #   enabled: true

    # Using gathered

    # Before state:
    # -------------
    #
    # switch# show running-config | section interface
    # interface fc1/1
    #     switchport speed auto
    #     switchport mode auto
    #     switchport description This is a sample line
    #     switchport trunk mode on
    #     no shutdown
    #
    # interface fc1/2
    #     switchport speed 1000
    #     switchport mode E
    #     no switchport description
    #     switchport trunk mode off
    #     no shutdown
    #
    - name: Gather interfaces facts from the device using nxos_fc_interfaces
      cisco.nxos.nxos_fc_interfaces:
        state: gathered
    #
    # Task output
    # -----------
    #
    # - name: fc1/1
    #   speed: auto
    #   mode: auto
    #   trunk_mode: on
    #   enabled: true
    #   description: This is a sample line
    # - name: fc1/2
    #   speed: 1000
    #   mode: E
    #   trunk_mode: off
    #   enabled: true



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface fc1/1&#x27;, &#x27;description sample description&#x27;, &#x27;shutdown&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface fc1/1&#x27;, &#x27;description sample description&#x27;, &#x27;shutdown&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Suhas Bharadwaj (@srbharadwaj)
