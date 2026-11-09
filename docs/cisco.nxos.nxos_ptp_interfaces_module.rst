.. _cisco.nxos.nxos_ptp_interfaces_module:


******************************
cisco.nxos.nxos_ptp_interfaces
******************************

**PTP interfaces resource module.**


Version added: 14.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the Precision Time Protocol (PTP) configuration of the interfaces of Cisco NX-OS devices.
- The global PTP settings are managed by :ref:`cisco.nxos.nxos_ptp_global <cisco.nxos.nxos_ptp_global_module>`.




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
                        <div>A list of PTP interface configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>announce_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The announce interval, the logarithm of the number of seconds (<code>ptp announce interval</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>aes67</li>
                                    <li>smpte_2059_2</li>
                        </ul>
                </td>
                <td>
                        <div>The profile of the value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value. The range is 0-4 without a profile, 0-4 with <code>aes67</code> and -3 to 1 with <code>smpte_2059_2</code>. Defaults to <code>1</code> without a profile.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>announce_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The number of announce intervals before a timeout (<code>ptp announce timeout</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>aes67</li>
                                    <li>smpte_2059_2</li>
                        </ul>
                </td>
                <td>
                        <div>The profile of the value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value. The range is 2-4 without a profile and 2-10 with the profiles. Defaults to <code>3</code> without a profile.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>asymmetric_delay</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The asymmetric delay of the path in nanoseconds (<code>ptp asymmetric-delay</code>).</div>
                        <div>The device keeps one value, the direction and the value, the last one that is configured wins. Only one of <em>forward_path</em> and <em>reverse_path</em> can be given.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>forward_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The delay of the forward path, in the range 1-512000000.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reverse_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The delay of the reverse path, in the range 1-512000000.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delay_request_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The minimum delay request interval, the logarithm of the number of seconds (<code>ptp delay-request minimum interval</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>aes67</li>
                                    <li>smpte_2059_2</li>
                        </ul>
                </td>
                <td>
                        <div>The profile of the value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value. The range is -1 to 6 without a profile and -4 to 5 with the profiles. Defaults to <code>0</code> without a profile.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Enables PTP on the interface (<code>ptp</code>). <code>false</code> removes all PTP settings of the interface (<code>no ptp</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>master</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The unicast master addresses (<code>ptp master</code>), IPv4 or IPv6. Several can be configured on an interface.</div>
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
                        <div>The name of the interface, for example <code>Ethernet1/1</code>. Interface names are normalised.</div>
                </td>
            </tr>
            <tr>
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
                        <div>The unicast peer address (<code>ptp peer</code>), IPv4 or IPv6. The device accepts one peer on an interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>role</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>dynamic</li>
                                    <li>master</li>
                                    <li>slave</li>
                        </ul>
                </td>
                <td>
                        <div>The PTP role of the port (<code>ptp role</code>). Defaults to <code>dynamic</code>. <code>slave</code> needs the unicast transmission.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>slave</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The unicast slave addresses (<code>ptp slave</code>), IPv4 or IPv6. Several can be configured on an interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sync_interval</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The sync interval, the logarithm of the number of seconds (<code>ptp sync interval</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>aes67</li>
                                    <li>smpte_2059_2</li>
                        </ul>
                </td>
                <td>
                        <div>The profile of the value.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The value. The range is -3 to 1 without a profile, -4 to 1 with <code>aes67</code> and -7 to 0 with <code>smpte_2059_2</code>. Defaults to <code>-2</code> without a profile.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>transmission</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>unicast</li>
                                    <li>multicast</li>
                        </ul>
                </td>
                <td>
                        <div>The transmission mode of the port (<code>ptp transmission</code>). Defaults to <code>multicast</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>transport</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>The transport of the PTP messages (<code>ptp transport</code>). Defaults to <code>ipv4</code>. <code>ipv6</code> needs a global IPv6 PTP source.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ucast_source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The unicast source addresses (<code>ptp ucast-source</code>). The device accepts one for each address family.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv4</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ipv6</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv6 address.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The VLAN of the PTP messages (<code>ptp vlan</code>), in the range 1-4094. The reserved VLANs are rejected by the device.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | include &quot;^interface|^  ptp&quot;</b>.</div>
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
                        <div>With <em>merged</em> what is given is added to the interfaces and nothing is removed, except the settings that are given with their default value, which are removed.</div>
                        <div>With <em>replaced</em> the PTP settings of the listed interfaces are made identical to the given ones, the other interfaces are not touched.</div>
                        <div>With <em>overridden</em> the same applies and the PTP settings of the interfaces that are not listed are removed.</div>
                        <div>With <em>deleted</em> the PTP settings of the listed interfaces are removed (<code>no ptp</code>), without <em>config</em> those of all the interfaces. <code>feature ptp</code> is not touched.</div>
                        <div>With <em>gathered</em> the configuration is read from the device.</div>
                        <div>With <em>rendered</em> the commands for <em>config</em> are returned without connecting to the device.</div>
                        <div>With <em>parsed</em> <em>running_config</em> is returned as structured data.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 10.6(4) on N9K-C93180YC-FX.
   - Unsupported for Cisco MDS.
   - The PTP commands only exist when ``feature ptp`` is enabled, use :ref:`cisco.nxos.nxos_feature <cisco.nxos.nxos_feature_module>` for it.
   - PTP can only be enabled on an interface when a PTP source address is configured, see :ref:`cisco.nxos.nxos_ptp_global <cisco.nxos.nxos_ptp_global_module>`. Every other PTP setting of an interface needs PTP to be enabled on the interface first, so *enabled* must be ``true`` for an interface with other settings, unless *state* is ``merged`` and the interface already has PTP.
   - ``no ptp`` removes all the PTP settings of an interface, *enabled=false* and the states *deleted*, *replaced* and *overridden* use it for an interface that is not configured with *enabled=true*.
   - NX-OS does not display a setting that has its default value in the running configuration. The default values are *role* ``dynamic``, *transport* ``ipv4``, *transmission* ``multicast``, *announce_interval* ``1``, *announce_timeout* ``3``, *sync_interval* ``-2`` and *delay_request_interval* ``0``, without a profile. The values with a profile are always displayed, also when they are equal to the default of the plain form. A setting that is given with its default value is removed from the device, and the facts only return the settings that the device displays.
   - NX-OS only removes a setting with a value when the ``no`` command carries a value, the module sends the value that is configured on the device.
   - The values with the ``aes67`` and ``smpte_2059_2`` profiles of the interval settings cannot be mixed on one interface. When another profile is configured, the module removes the old line before it sets the new one.
   - The ``ptp cost`` command, the ``ptp ipv6 multicast scope`` command and the ``negotiation-schema`` of the ``ptp transmission``, ``ptp master`` and ``ptp slave`` commands of an interface are not managed by this module. N9K-C93180YC-FX with NX-OS 10.6(4) does not support ``ptp cost``, and a negotiation schema cannot be created with the CLI there.
   - This module works with connection ``network_cli`` and ``httpapi``.
   - The *parsed* state reads configuration from ``running_config`` and does not connect to the device.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  ptp"
    # interface Ethernet1/1
    # interface Ethernet1/2

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_ptp_interfaces:
        config:
          - name: Ethernet1/1
            enabled: true
            vlan: 100
            announce_interval:
              value: 3
              profile: aes67
            sync_interval:
              value: -2
              profile: aes67
            delay_request_interval:
              value: -2
              profile: aes67
          - name: Ethernet1/2
            enabled: true
            role: master
            transmission: unicast
        state: merged

    # Task output:
    # ------------
    # before: []
    # commands:
    #   - interface Ethernet1/1
    #   - ptp
    #   - ptp vlan 100
    #   - ptp delay-request minimum interval aes67 -2
    #   - ptp announce interval aes67 3
    #   - ptp sync interval aes67 -2
    #   - interface Ethernet1/2
    #   - ptp
    #   - ptp role master
    #   - ptp transmission unicast
    # after:
    #   - name: Ethernet1/1
    #     enabled: true
    #     vlan: 100
    #     announce_interval:
    #       value: 3
    #       profile: aes67
    #     sync_interval:
    #       value: -2
    #       profile: aes67
    #     delay_request_interval:
    #       value: -2
    #       profile: aes67
    #   - name: Ethernet1/2
    #     enabled: true
    #     role: master
    #     transmission: unicast

    # After state:
    # ------------
    # nxos# show running-config | include "^interface|^  ptp"
    # interface Ethernet1/1
    #   ptp
    #   ptp delay-request minimum interval aes67 -2
    #   ptp announce interval aes67 3
    #   ptp vlan 100
    #   ptp sync interval aes67 -2
    # interface Ethernet1/2
    #   ptp
    #   ptp role master
    #   ptp transmission unicast

    # Using replaced

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  ptp"
    # interface Ethernet1/1
    #   ptp
    #   ptp vlan 100
    #   ptp sync interval aes67 -2
    # interface Ethernet1/2
    #   ptp
    #   ptp role master

    - name: Replace the PTP configuration of Ethernet1/1
      cisco.nxos.nxos_ptp_interfaces:
        config:
          - name: Ethernet1/1
            enabled: true
            vlan: 200
        state: replaced

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/1
    #   - ptp vlan 200
    #   - no ptp sync interval aes67 -2

    # Using overridden

    - name: Override the PTP configuration of all the interfaces
      cisco.nxos.nxos_ptp_interfaces:
        config:
          - name: Ethernet1/1
            enabled: true
            vlan: 200
        state: overridden

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/2
    #   - no ptp

    # Using deleted

    - name: Remove the PTP configuration of Ethernet1/1
      cisco.nxos.nxos_ptp_interfaces:
        config:
          - name: Ethernet1/1
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - interface Ethernet1/1
    #   - no ptp

    # Using gathered

    # Before state:
    # -------------
    # nxos# show running-config | include "^interface|^  ptp"
    # interface Ethernet1/1
    #   ptp
    #   ptp vlan 200
    # interface Ethernet1/2

    - name: Gather the PTP configuration of the interfaces
      cisco.nxos.nxos_ptp_interfaces:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   - name: Ethernet1/1
    #     enabled: true
    #     vlan: 200

    # Using rendered

    - name: Render the commands for the provided configuration
      cisco.nxos.nxos_ptp_interfaces:
        config:
          - name: Eth1/3
            enabled: true
            master:
              - 192.0.2.10
            asymmetric_delay:
              forward_path: 100
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - interface Ethernet1/3
    #   - ptp
    #   - ptp asymmetric-delay forward-path 100
    #   - ptp master 192.0.2.10

    # Using parsed

    # parsed.cfg
    # ----------
    # interface Ethernet1/1
    #   ptp
    #   ptp vlan 200
    # interface Ethernet1/2

    - name: Parse the provided configuration
      cisco.nxos.nxos_ptp_interfaces:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   - name: Ethernet1/1
    #     enabled: true
    #     vlan: 200



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;ptp&#x27;, &#x27;ptp vlan 100&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface Ethernet1/1&#x27;, &#x27;ptp&#x27;, &#x27;ptp vlan 100&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jorgen Spange (@jorgenspange)
