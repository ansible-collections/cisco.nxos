.. _cisco.nxos.nxos_features_module:


************************
cisco.nxos.nxos_features
************************

**Features resource module.**


Version added: 14.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the features of a device running Cisco NX-OS, the ``feature`` commands of the global configuration, for example ``feature bgp`` or ``feature nv overlay``.
- It enables and disables several features in one task and makes the set of enabled features declarative, with the states *overridden* and *deleted*.




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
                        <div>The features.</div>
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
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Enable (<code>true</code>) or disable (<code>false</code>) the feature.</div>
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
                        <div>The name of the feature as written in the <code>feature</code> command, for example <code>bgp</code>, <code>interface-vlan</code>, <code>nv overlay</code> or <code>tacacs+</code>.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config all | include &#x27;^feature|^no feature&#x27;</b>, or the full running configuration.</div>
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>With <em>merged</em> and <em>replaced</em> the features of <em>config</em> are enabled or disabled. Other features are not touched.</div>
                        <div>With <em>overridden</em> the features of <em>config</em> are enabled or disabled and every other enabled feature is disabled. This removes the configuration that depends on those features.</div>
                        <div>With <em>deleted</em> the features listed in <em>config</em> are disabled, the value of <em>enabled</em> is ignored. Without <em>config</em> <b>every enabled feature is disabled</b>, also those that give access to the device.</div>
                        <div>With <em>rendered</em> the commands for <em>config</em> are returned and nothing is sent to the device.</div>
                        <div>With <em>gathered</em> the features are read from the device and returned in <em>gathered</em>.</div>
                        <div>With <em>parsed</em> the text of <em>running_config</em> is converted to structured data.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
   - Unsupported for Cisco MDS.
   - **Disabling a feature removes all configuration that depends on it.** Disabling ``bgp`` removes the BGP configuration, disabling ``interface-vlan`` removes the SVIs. A feature that provides the access to the device, for example ``ssh``, ``tacacs+`` or ``nxapi``, can lock you out. Use the check mode before *overridden* and *deleted*.
   - The module reads the ``feature`` and ``no feature`` lines of ``show running-config all``. The plain running configuration hides the features that are enabled by default, for example ``ssh``. The device lists only the features that have such a line, so *gathered* does not return every feature of ``show feature``. The names of ``show feature`` are internal and differ from the names of the commands, for example ``nve`` for ``feature nv overlay`` and ``vnseg_vlan`` for ``feature vn-segment-vlan-based``, so they cannot be used.
   - The names are the ones of the ``feature`` command, exactly as they are written in the configuration, for example ``nv overlay``, ``vn-segment-vlan-based``, ``tacacs+`` or ``password encryption aes``. The set of features depends on the platform and the license, so the names are not restricted.
   - A feature is either enabled or disabled, so *merged* and *replaced* behave the same.
   - The commands that enable a feature are sent in the order of *config*, the commands that disable a feature after them. List a feature before the features that depend on it, for example ``nv overlay`` before ``vn-segment-vlan-based``.
   - The feature sets (``install feature-set`` and ``feature-set``) are not managed.
   - :ref:`cisco.nxos.nxos_feature <cisco.nxos.nxos_feature_module>` manages one feature per task and stays available.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # switch# show running-config | include ^feature
    # feature bgp
    # feature interface-vlan

    - name: Enable and disable features
      cisco.nxos.nxos_features:
        config:
          - name: nv overlay
            enabled: true
          - name: vn-segment-vlan-based
            enabled: true
          - name: interface-vlan
            enabled: false
        state: merged

    # Task output:
    # ------------
    # before:
    #   - name: bgp
    #     enabled: true
    #   - name: interface-vlan
    #     enabled: true
    #
    # commands:
    #   - feature nv overlay
    #   - feature vn-segment-vlan-based
    #   - no feature interface-vlan
    #
    # after:
    #   - name: bgp
    #     enabled: true
    #   - name: nv overlay
    #     enabled: true
    #   - name: vn-segment-vlan-based
    #     enabled: true

    # Using replaced

    # Before state:
    # -------------
    # switch# show running-config | include ^feature
    # feature bgp
    # feature interface-vlan
    # feature lacp

    - name: Set the state of the listed features, a feature that is not listed stays as it is
      cisco.nxos.nxos_features:
        config:
          - name: bgp
            enabled: true
          - name: interface-vlan
            enabled: false
          - name: nv overlay
            enabled: true
        state: replaced

    # Task output:
    # ------------
    # before:
    #   - name: bgp
    #     enabled: true
    #   - name: interface-vlan
    #     enabled: true
    #   - name: lacp
    #     enabled: true
    #
    # commands:
    #   - feature nv overlay
    #   - no feature interface-vlan
    #
    # after:
    #   - name: bgp
    #     enabled: true
    #   - name: lacp
    #     enabled: true
    #   - name: nv overlay
    #     enabled: true

    # Using overridden

    # Before state:
    # -------------
    # switch# show running-config | include ^feature
    # feature bgp
    # feature interface-vlan
    # feature lacp

    - name: Make bgp and lacp the only enabled features
      cisco.nxos.nxos_features:
        config:
          - name: bgp
            enabled: true
          - name: lacp
            enabled: true
        state: overridden

    # Task output:
    # ------------
    # commands:
    #   - no feature interface-vlan

    # Using deleted

    - name: Disable the listed features
      cisco.nxos.nxos_features:
        config:
          - name: bash-shell
          - name: scp-server
        state: deleted

    # Using gathered

    - name: Gather the features
      cisco.nxos.nxos_features:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   - name: bgp
    #     enabled: true
    #   - name: nxapi
    #     enabled: false
    #   - name: ssh
    #     enabled: true

    # Using rendered

    - name: Render the commands
      cisco.nxos.nxos_features:
        config:
          - name: bgp
            enabled: true
          - name: bash-shell
            enabled: false
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - feature bgp
    #   - no feature bash-shell

    # Using parsed

    - name: Parse the feature lines
      cisco.nxos.nxos_features:
        running_config: |
          feature ssh
          no feature nxapi
          feature nv overlay
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   - name: nv overlay
    #     enabled: true
    #   - name: nxapi
    #     enabled: false
    #   - name: ssh
    #     enabled: true



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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code> or <code>deleted</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;feature nv overlay&#x27;, &#x27;feature vn-segment-vlan-based&#x27;, &#x27;no feature interface-vlan&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;feature bgp&#x27;, &#x27;no feature bash-shell&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørgen Spange (@jorgenspange)
