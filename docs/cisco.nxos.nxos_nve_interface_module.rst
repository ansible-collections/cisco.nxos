.. _cisco.nxos.nxos_nve_interface_module:


*****************************
cisco.nxos.nxos_nve_interface
*****************************

**NVE interface resource module.**


Version added: 11.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of Network Virtualization Endpoint (NVE) overlay interface that terminates VXLAN tunnels.




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
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A List of NVE interface options.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise_virtual_rmac</b>
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
                        <div>Enable/disable virtual RMAC advertisement</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Interface description</div>
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
                        <div>Administrative state of the interface. Set the value to <code>true</code> to administratively enable the interface or <code>false</code> to disable it.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global_ingress_replication_bgp</b>
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
                        <div>Enable/disable global bgp ingress replication</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global_multicast_group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Global multicast group</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multicast address</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
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
                                    <li>L2</li>
                                    <li>L3</li>
                        </ul>
                </td>
                <td>
                        <div>VNI type.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global_suppress_arp</b>
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
                        <div>Enable/disable global ARP suppression</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_reachability_bgp</b>
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
                        <div>Enable/disable host reachability with bgp</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multisite_interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Multiste border gateway source interface</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_interface_hold_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source loopback interface hold-down-time in seconds</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_interface_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Source loopback interface name</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vnis</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure Virtual Network Identifier membership</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>associate_vrf</b>
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
                        <div>Associate L3VNI with VRF</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ingress_replication_bgp</b>
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
                        <div>Enable/disable bgp ingress replication for L2VNI</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>multisite_ingress_replication</b>
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
                        <div>Enable/disable multisite ingress replication for L2VNI</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suppress_arp</b>
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
                        <div>Enable/disable ARP suppression for L2VNI</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>suppress_arp_disable</b>
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
                        <div>Disable/enable the global setting for ARP suppression for L2VNI</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vni_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Network Identifier ID</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^router bgp&#x27;</b>.</div>
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
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state of the configuration after module completion.</div>
                        <div>States <code>replaced</code> and <code>overridden</code> have the same behaviour for this module.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOS 10.3(7)
   - Unsupported for Cisco MDS



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # switch# show running-config | section "^interface nve1"
    # switch#

    - name: Merge the provided NVE configuration with the existing running configuration.
      cisco.nxos.nxos_nve_interface:
        config:
          enabled: true
          description: vxlan vtep
          advertise_virtual_rmac: true
          host_reachability_bgp: true
          source_interface_name: loopback1
          source_interface_hold_time: 60
          global_multicast_group:
            address: 239.239.239.239
            mode: L2
          vnis:
            - associate_vrf: true
              vni_id: 11111
            - associate_vrf: false
              vni_id: 22222
            - suppress_arp: true
              vni_id: 33333
        state: merged

    # Task output:
    # ------------
    # before: {}
    #
    # commands:
    #   - interface nve1
    #   - description vxlan vtep
    #   - host-reachability protocol bgp
    #   - advertise virtual-rmac
    #   - source-interface loopback1
    #   - source-interface hold-down-time 60
    #   - member vni 11111 associate-vrf
    #   - member vni 22222
    #   - member vni 33333
    #   - suppress-arp
    #   - no shutdown
    #   - global mcast-group 239.239.239.239 L2
    #
    # after:
    #   enabled: true
    #   description: vxlan vtep
    #   advertise_virtual_rmac: true
    #   host_reacability_bgp: true
    #   source_interface_name: loopback1
    #   source_interface_hold_time: 60
    #   global_multicast_group:
    #     address: 239.239.239.239
    #     mode: L2
    #   vnis:
    #     - associate_vrf: true
    #       vni_id: 11111
    #     - vni_id: 22222
    #     - suppress_arp: true
    #       vni_id: 33333
    #
    # After state:
    # ------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   no shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   advertise virtual-rmac
    #   source-interface loopback1
    #   source-interface hold-down-time 60
    #   global mcast-group 239.239.239.239 L2
    #   member vni 11111 associate-vrf
    #   member vni 22222
    #   member vni 33333
    #     suppress-arp


    # Using gathered

    # Existing config:
    # ---------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   no shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   advertise virtual-rmac
    #   source-interface loopback1
    #   source-interface hold-down-time 60
    #   global mcast-group 239.239.239.239 L2
    #   member vni 11111 associate-vrf
    #   member vni 22222
    #   member vni 33333
    #     suppress-arp

    - name: Gather NVE interace facts using gathered
      cisco.nxos.nxos_nve_interface:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   enabled: true
    #   description: vxlan vtep
    #   advertise_virtual_rmac: true
    #   host_reacability_bgp: true
    #   source_interface_name: loopback1
    #   source_interface_hold_time: 60
    #   global_multicast_group:
    #     address: 239.239.239.239
    #     mode: L2
    #   vnis:
    #     - associate_vrf: true
    #       vni_id: 11111
    #     - vni_id: 22222
    #     - suppress_arp: true
    #       vni_id: 33333


    # Using overridden

    # Before state:
    # -------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   no shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   advertise virtual-rmac
    #   source-interface loopback1
    #   source-interface hold-down-time 60
    #   global mcast-group 239.239.239.239 L2
    #   member vni 11111 associate-vrf
    #   member vni 22222
    #   member vni 33333
    #     suppress-arp

    - name: Override NVE interface configuration with provided configuration.
      cisco.nxos.nxos_nve_interface:
        config:
          enabled: true
          advertise_virtual_rmac: true
          host_reachability_bgp: true
          source_interface_name: loopback1
          global_multicast_group:
            address: 230.230.230.230
            mode: L2
          vnis:
            - associate_vrf: false
              ingress_replication_bgp: true
              suppress_arp: true
              vni_id: 11111
            - associate_vrf: true
              vni_id: 22222
            - associate_vrf: true
              vni_id: 33333
        state: overridden

    # Task output:
    # ------------
    # before:
    #   enabled: true
    #   description: vxlan vtep
    #   advertise_virtual_rmac: true
    #   host_reacability_bgp: true
    #   source_interface_name: loopback1
    #   source_interface_hold_time: 60
    #   global_multicast_group:
    #     address: 239.239.239.239
    #     mode: L2
    #   vnis:
    #     - associate_vrf: true
    #       vni_id: 11111
    #     - vni_id: 22222
    #     - suppress_arp: true
    #       vni_id: 33333
    #
    # commands:
    #   - interface nve1
    #   - no description vxlan vtep
    #   - no source-interface hold-down-time 60
    #   - no member vni 11111
    #   - member vni 11111
    #   - suppress-arp
    #   - ingress-replication protocol bgp
    #   - no member vni 22222
    #   - member vni 22222 associate-vrf
    #   - no member vni 33333
    #   - member vni 33333 associate-vrf
    #   - global mcast-group 230.230.230.230 L2
    #
    # after:
    #   enabled: true
    #   advertise_virtual_rmac: true
    #   host_reachability_bgp: true
    #   source_interface_name: loopback1
    #   global_multicast_group:
    #     address: 230.230.230.230
    #     mode: L2
    #   vnis:
    #     - ingress_replication_bgp: true
    #       suppress_arp: true
    #       vni_id: 11111
    #     - associate_vrf: true
    #       vni_id: 22222
    #     - associate_vrf: true
    #       vni_id: 33333
    #
    # After state:
    # ------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   no shutdown
    #   host-reachability protocol bgp
    #   advertise virtual-rmac
    #   source-interface loopback1
    #   global mcast-group 239.230.230.230 L2
    #   member vni 11111
    #     suppress-arp
    #     ingress-replication protocol bgp
    #   member vni 22222 associate-vrf
    #   member vni 33333 associate-vrf


    # Using replaced

    # Before state:
    # -------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   no shutdown
    #   host-reachability protocol bgp
    #   advertise virtual-rmac
    #   source-interface loopback1
    #   global mcast-group 239.230.230.230 L2
    #   member vni 11111
    #     suppress-arp
    #     ingress-replication protocol bgp
    #   member vni 22222 associate-vrf
    #   member vni 33333 associate-vrf

    - name: Replace NVE interface configuration with provided configuration.
      cisco.nxos.nxos_nve_interface:
        config:
          description: vxlan vtep
          host_reachability_bgp: true
          source_interface_name: loopback1
        state: replaced

    # Task output:
    # ------------
    # before:
    #   enabled: true
    #   advertise_virtual_rmac: true
    #   host_reachability_bgp: true
    #   source_interface_name: loopback1
    #   global_multicast_group:
    #     address: 230.230.230.230
    #     mode: L2
    #   vnis:
    #     - ingress_replication_bgp: true
    #       suppress_arp: true
    #       vni_id: 11111
    #     - associate_vrf: true
    #       vni_id: 22222
    #     - associate_vrf: true
    #       vni_id: 33333
    #
    # commands:
    #   - interface nve1
    #   - description vxlan vtep
    #   - no advertise virtual-rmac
    #   - no member vni 11111
    #   - no member vni 22222 associate-vrf
    #   - no member vni 33333 associate-vrf
    #   - shutdown
    #   - no global mcast-group L2
    #
    # after:
    #   description: vxlan vtep
    #   host_reachability_bgp: true
    #   source_interface_name: loopback1
    #
    # After state:
    # ------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   source-interface loopback1


    # Using deleted

    # Before state:
    # -------------
    # switch# show running-config | section "^interface nve1"
    # interface nve1
    #   shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   source-interface loopback1

    - name: Delete NVE configurations handled by this module.
      cisco.nxos.nxos_nve_interface:
        state: deleted

    # Task output:
    # ------------

    # before:
    #   description: vxlan vtep
    #   host_reacability_bgp: true
    #   source_interface_name: loopback1
    #
    # commands:
    #   - no interface nve1
    #
    # after: {}
    #
    # After state:
    # ------------
    # switch# show running-config | section "^interface nve1"
    # switch#


    # Using rendered

    - name: Render platform specific configuration lines (without connecting to the device)
      cisco.nxos.nxos_nve_interface:
        config:
          enabled: true
          description: vxlan vtep
          advertise_virtual_rmac: true
          host_reacability_bgp: true
          source_interface_name: loopback1
          global_multicast_group:
            address: 239.239.239.239
            mode: L2
          vnis:
            - suppress_arp: true
              vni_id: 11111
            - suppress_arp_disable: true
              vni_id: 22222
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - interface nve1
    #   - description vxlan vtep
    #   - host-reachability protocol bgp
    #   - advertise virtual-rmac
    #   - source-interface loopback1
    #   - member vni 11111
    #   - suppress-arp
    #   - member vni 22222
    #   - suppress-arp disable
    #   - no shutdown
    #   - global mcast-group 239.239.239.239 L2


    # Using parsed

    # parsed.cfg
    # ----------
    # interface nve1
    #   no shutdown
    #   description vxlan vtep
    #   host-reachability protocol bgp
    #   source-interface loopback1
    #   global mcast-group 239.239.239.239 L2
    #   member vni 22222
    #   member vni 33333

    - name: Parse externally provided NVE interface config
      cisco.nxos.nxos_nve_interface:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   description: vxlan vtep
    #   enabled: true
    #   global_multicast_group:
    #     address: 239.239.239.239
    #     mode: L2
    #  host_reacability_bgp: true
    #  source_interface_name: loopback1
    #  vnis:
    #    - vni_id: 22222
    #    - vni_id: 33333



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;interface nve1&#x27;, &#x27;no shutdown&#x27;, &#x27;description vxlan vtep&#x27;, &#x27;host-reachability protocol bgp&#x27;, &#x27;advertise virtual-rmac&#x27;, &#x27;source-interface loopback1&#x27;, &#x27;global mcast-group 239.239.239.239 L2&#x27;, &#x27;member vni 11111 associate-vrf&#x27;, &#x27;member vni 22222&#x27;, &#x27;suppress-arp&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørn Ivar Holland (@jiholland)
