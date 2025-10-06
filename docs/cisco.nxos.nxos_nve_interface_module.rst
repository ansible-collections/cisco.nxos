.. Created with antsibull-docs 2.21.0

cisco.nxos.nxos_nve_interface module -- NVE interface resource module.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `cisco.nxos collection <https://galaxy.ansible.com/ui/repo/published/cisco/nxos/>`_ (version 11.0.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible\-galaxy collection install cisco.nxos`.

To use it in a playbook, specify: ``cisco.nxos.nxos_nve_interface``.

New in cisco.nxos 11.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides declarative management of Network Virtualization Endpoint (NVE) overlay interface that terminates VXLAN tunnels.


Aliases: nve_interface






Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="3"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config"></div>
      <p style="display: inline;"><strong>config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>A List of NVE interface options.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/advertise_virtual_rmac"></div>
      <p style="display: inline;"><strong>advertise_virtual_rmac</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/advertise_virtual_rmac" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable virtual RMAC advertisement</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/description"></div>
      <p style="display: inline;"><strong>description</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/description" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Interface description</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/enabled"></div>
      <p style="display: inline;"><strong>enabled</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/enabled" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Administrative state of the interface. Set the value to <code class='docutils literal notranslate'>true</code> to administratively enable the interface or <code class='docutils literal notranslate'>false</code> to disable it.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/global_ingress_replication_bgp"></div>
      <p style="display: inline;"><strong>global_ingress_replication_bgp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/global_ingress_replication_bgp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable global bgp ingress replication</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/global_multicast_group"></div>
      <p style="display: inline;"><strong>global_multicast_group</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/global_multicast_group" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Global multicast group</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/global_multicast_group/address"></div>
      <p style="display: inline;"><strong>address</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/global_multicast_group/address" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Multicast address</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/global_multicast_group/mode"></div>
      <p style="display: inline;"><strong>mode</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/global_multicast_group/mode" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>VNI type.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;L2&#34;</code></p></li>
        <li><p><code>&#34;L3&#34;</code></p></li>
      </ul>

    </td>
  </tr>

  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/global_suppress_arp"></div>
      <p style="display: inline;"><strong>global_suppress_arp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/global_suppress_arp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable global ARP suppression</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/host_reachability_bgp"></div>
      <p style="display: inline;"><strong>host_reachability_bgp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/host_reachability_bgp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable host reachability with bgp</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/multisite_interface"></div>
      <p style="display: inline;"><strong>multisite_interface</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/multisite_interface" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Multiste border gateway source interface</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/source_interface_hold_time"></div>
      <p style="display: inline;"><strong>source_interface_hold_time</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/source_interface_hold_time" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Source loopback interface hold-down-time in seconds</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/source_interface_name"></div>
      <p style="display: inline;"><strong>source_interface_name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/source_interface_name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Source loopback interface name</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis"></div>
      <p style="display: inline;"><strong>vnis</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Configure Virtual Network Identifier membership</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/associate_vrf"></div>
      <p style="display: inline;"><strong>associate_vrf</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/associate_vrf" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Associate L3VNI with VRF</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/ingress_replication_bgp"></div>
      <p style="display: inline;"><strong>ingress_replication_bgp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/ingress_replication_bgp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable bgp ingress replication for L2VNI</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/multisite_ingress_replication"></div>
      <p style="display: inline;"><strong>multisite_ingress_replication</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/multisite_ingress_replication" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable multisite ingress replication for L2VNI</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/suppress_arp"></div>
      <p style="display: inline;"><strong>suppress_arp</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/suppress_arp" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Enable/disable ARP suppression for L2VNI</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/suppress_arp_disable"></div>
      <p style="display: inline;"><strong>suppress_arp_disable</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/suppress_arp_disable" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Disable/enable the global setting for ARP suppression for L2VNI</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config/vnis/vni_id"></div>
      <p style="display: inline;"><strong>vni_id</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config/vnis/vni_id" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>Virtual Network Identifier ID</p>
    </td>
  </tr>


  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-running_config"></div>
      <p style="display: inline;"><strong>running_config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-running_config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option is used only with state <em>parsed</em>.</p>
      <p>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^router bgp&#x27;</b>.</p>
      <p>The state <em>parsed</em> reads the configuration from <code class='docutils literal notranslate'>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</p>
    </td>
  </tr>
  <tr>
    <td colspan="3" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The state of the configuration after module completion.</p>
      <p>States <code class='docutils literal notranslate'>replaced</code> and <code class='docutils literal notranslate'>overridden</code> have the same behaviour for this module.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;merged&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;replaced&#34;</code></p></li>
        <li><p><code>&#34;overridden&#34;</code></p></li>
        <li><p><code>&#34;deleted&#34;</code></p></li>
        <li><p><code>&#34;parsed&#34;</code></p></li>
        <li><p><code>&#34;gathered&#34;</code></p></li>
        <li><p><code>&#34;rendered&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

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
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-after"></div>
      <p style="display: inline;"><strong>after</strong></p>
      <a class="ansibleOptionLink" href="#return-after" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration as structured data after module completion.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when changed</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;The configuration returned will always be in the same format of the parameters above.\n&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-before"></div>
      <p style="display: inline;"><strong>before</strong></p>
      <a class="ansibleOptionLink" href="#return-before" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The configuration as structured data prior to module invocation.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;The configuration returned will always be in the same format of the parameters above.\n&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-commands"></div>
      <p style="display: inline;"><strong>commands</strong></p>
      <a class="ansibleOptionLink" href="#return-commands" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The set of commands pushed to the remote device.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;interface nve1&#34;, &#34;no shutdown&#34;, &#34;description vxlan vtep&#34;, &#34;host-reachability protocol bgp&#34;, &#34;advertise virtual-rmac&#34;, &#34;source-interface loopback1&#34;, &#34;global mcast-group 239.239.239.239 L2&#34;, &#34;member vni 11111 associate-vrf&#34;, &#34;member vni 22222&#34;, &#34;suppress-arp&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Jørn Ivar Holland (@jiholland)


Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible\-collections/cisco.nxos/issues>`__
* `Repository (Sources) <https://github.com/ansible\-collections/cisco.nxos>`__
