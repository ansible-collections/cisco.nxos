.. _cisco.nxos.nxos_igmp_snooping_module:


*****************************
cisco.nxos.nxos_igmp_snooping
*****************************

**IGMP snooping resource module.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the global IGMP snooping configuration and the static groups of the per-VLAN snooping context (``vlan configuration <id>``) on devices running Cisco NX-OS.




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
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IGMP snooping configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disable_nve_static_router_port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 13.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Do not include the NVE interface as a static router port in the VXLAN VLANs (<code>ip igmp snooping disable-nve-static-router-port</code>).</div>
                        <div>Defaults to <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Group membership timeout for all VLANs on the device (<code>ip igmp snooping group-timeout</code>).</div>
                        <div>Accepted values are an integer in the range 1-10080 (minutes) and <code>never</code>.</div>
                        <div>It is removed by <em>state</em> <code>deleted</code>, and by <em>state</em> <code>replaced</code> and <code>overridden</code> when it is not given.</div>
                        <div>It cannot be set while <em>snooping</em> is, or is being set to, <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>link_local_groups_suppression</b>
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
                        <div>Global link-local groups suppression (<code>ip igmp snooping link-local-groups-suppression</code>).</div>
                        <div>Defaults to <code>true</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>report_suppression</b>
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
                        <div>Global IGMPv1/IGMPv2 report suppression (<code>ip igmp snooping report-suppression</code>).</div>
                        <div>Defaults to <code>true</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>snooping</b>
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
                        <div>Enables or disables IGMP snooping on the switch (<code>ip igmp snooping</code>).</div>
                        <div>Defaults to <code>true</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>v3_report_suppression</b>
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
                        <div>Global IGMPv3 report suppression and proxy reporting (<code>ip igmp snooping v3-report-suppression</code>).</div>
                        <div>Defaults to <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlans</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 13.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>The VLANs with a <code>vlan configuration</code> block.</div>
                        <div>With <em>state</em> <code>replaced</code> the static groups of a listed VLAN are made identical to the ones given, VLANs that are not listed are left alone.</div>
                        <div>With <em>state</em> <code>overridden</code> the VLANs that are not listed are removed.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>static_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Static multicast groups of the VLAN (<code>ip igmp snooping static-group</code>).</div>
                        <div>A VLAN without static groups has no <code>vlan configuration</code> block under <em>state</em> <code>replaced</code> and <code>overridden</code>.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 multicast group address.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interfaces</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The interfaces on which the group is statically joined.</div>
                        <div>One <code>ip igmp snooping static-group</code> line is configured for each interface.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 source address of the group, for IGMPv3.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vlan_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The VLAN ID, in the range 1-4094.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vxlan</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 13.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Enables IGMP snooping for VXLAN VLANs (<code>ip igmp snooping vxlan</code>).</div>
                        <div>Defaults to <code>false</code>.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the commands <b>show running-config | section &quot;^vlan configuration&quot;</b> and <b>show running-config | include &quot;ip igmp snooping&quot;</b>, or the full running configuration.</div>
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
                                    <li>gathered</li>
                                    <li>rendered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>With <em>merged</em> what is given is added to the device, nothing is removed. A setting that is not given is not touched.</div>
                        <div>With <em>replaced</em> the global settings that are not given are reset to their default, the listed VLANs are made identical to the given ones and the other VLANs are not touched.</div>
                        <div>With <em>overridden</em> the same applies and the VLANs that are not listed are removed.</div>
                        <div>With <em>deleted</em> and without <em>config</em> all global settings are reset to their default and all <code>vlan configuration</code> blocks are removed. With <em>config</em> the listed global settings are reset, a listed VLAN without <em>static_groups</em> is removed, and for a listed VLAN with <em>static_groups</em> only these are removed.</div>
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
   - This module was rewritten as a resource module. The former flat parameters and the ``present`` and ``default`` states are gone, use *config* with the *state* ``merged`` or ``deleted`` instead.
   - The IGMP snooping configuration must be identical on both vPC peers.
   - IGMP snooping over VXLAN is supported with BGP EVPN only, not with flood-and-learn, and not on VLANs with FEX member ports. The global *vxlan* setting (``ip igmp snooping vxlan``) must be enabled for snooping to be active on VXLAN VLANs.
   - A VLAN without PIM needs an IGMP querier. The querier is not managed by this module.
   - The settings of a VLAN do not apply until the VLAN exists. NX-OS keeps a ``vlan configuration`` block when the VLAN itself is removed, use *state* ``deleted``, ``replaced`` or ``overridden`` to remove such blocks.
   - NX-OS does not show a setting that has its default value in the running configuration. The facts therefore report every boolean setting with its effective value, which means that ``gathered`` and ``parsed`` return ``snooping``, ``link_local_groups_suppression``, ``report_suppression``, ``v3_report_suppression``, ``vxlan`` and ``disable_nve_static_router_port`` even when they are not configured. The group timeout is only returned when it is configured.
   - The default values are ``snooping=true``, ``link_local_groups_suppression=true``, ``report_suppression=true``, ``v3_report_suppression=false``, ``vxlan=false``, ``disable_nve_static_router_port=false`` and no group timeout. Setting an option to its default value is a no-op when the device already has it.
   - NX-OS rejects ``group-timeout`` while snooping is disabled. The module fails before changing anything when *group_timeout* is given and *snooping* is, or is becoming, ``false``. The group timeout is sent after the other global settings, except when it is removed because snooping is being disabled.
   - Only the static groups of a VLAN are managed. A ``vlan configuration`` block with any other content is parsed as a VLAN without static groups. It is removed completely, together with that content, by ``deleted`` and ``overridden``, and by ``replaced`` when the listed VLAN has no *static_groups*.
   - A static group is accepted and stored for any interface, but ``show ip igmp snooping groups vlan <id>`` only lists it (type S) when the interface is a member port of that VLAN.
   - ``state=deleted`` without *config* and ``state=overridden`` remove every ``vlan configuration`` block on the switch that is not listed, including blocks created by other tools or roles. Run the task in check mode first.
   - A ``vlan configuration`` block that is not for a single VLAN (for example a range) is ignored.
   - A VLAN that is listed without *static_groups* is not created by ``merged``, because an empty ``vlan configuration`` block has no effect. It is reported by ``gathered`` when the device has one.
   - Interface names are normalised before they are compared, so ``Eth1/10``, ``ethernet1/10`` and ``Ethernet1/10`` are the same, as are ``Po20`` and ``port-channel20``.
   - This module works with connection ``network_cli`` and ``httpapi``.
   - The *parsed* state reads configuration from *running_config* and does not connect to the device.
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # (nothing is shown, the device has the default configuration)

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_igmp_snooping:
        config:
          vxlan: true
          v3_report_suppression: true
          group_timeout: "300"
          vlans:
            - vlan_id: 100
              static_groups:
                - group: 233.252.0.10
                  interfaces:
                    - Eth1/10
                    - Po20
                - group: 233.252.0.11
                  source: 192.0.2.10
                  interfaces:
                    - Ethernet1/10
        state: merged

    # Task output:
    # ------------
    # before:
    #   snooping: true
    #   link_local_groups_suppression: true
    #   report_suppression: true
    #   v3_report_suppression: false
    #   vxlan: false
    #   disable_nve_static_router_port: false
    # commands:
    #   - ip igmp snooping v3-report-suppression
    #   - ip igmp snooping vxlan
    #   - ip igmp snooping group-timeout 300
    #   - vlan configuration 100
    #   - ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    #   - ip igmp snooping static-group 233.252.0.10 interface port-channel20
    #   - ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10
    # after:
    #   snooping: true
    #   link_local_groups_suppression: true
    #   report_suppression: true
    #   v3_report_suppression: true
    #   vxlan: true
    #   disable_nve_static_router_port: false
    #   group_timeout: "300"
    #   vlans:
    #     - vlan_id: 100
    #       static_groups:
    #         - group: 233.252.0.10
    #           interfaces:
    #             - Ethernet1/10
    #             - port-channel20
    #         - group: 233.252.0.11
    #           source: 192.0.2.10
    #           interfaces:
    #             - Ethernet1/10

    # After state:
    # ------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # ip igmp snooping v3-report-suppression
    # ip igmp snooping group-timeout 300
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    #   ip igmp snooping static-group 233.252.0.10 interface port-channel20
    #   ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10

    # Using replaced

    # Before state:
    # -------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # ip igmp snooping v3-report-suppression
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    #   ip igmp snooping static-group 233.252.0.10 interface port-channel20
    # vlan configuration 200
    #   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

    - name: Replace the global settings and the listed VLANs
      cisco.nxos.nxos_igmp_snooping:
        config:
          vxlan: true
          vlans:
            - vlan_id: 100
              static_groups:
                - group: 233.252.0.10
                  interfaces:
                    - Ethernet1/10
        state: replaced

    # Task output:
    # ------------
    # commands:
    #   - no ip igmp snooping v3-report-suppression
    #   - vlan configuration 100
    #   - no ip igmp snooping static-group 233.252.0.10 interface port-channel20

    # After state:
    # ------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    # vlan configuration 200
    #   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

    # Using overridden

    # Before state:
    # -------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    # vlan configuration 200
    #   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

    # WARNING: every vlan configuration block that is not listed is removed, also the ones
    # created by other tools or roles. Run it with check_mode first.
    - name: Override the IGMP snooping configuration
      cisco.nxos.nxos_igmp_snooping:
        config:
          vxlan: true
          vlans:
            - vlan_id: 100
              static_groups:
                - group: 233.252.0.10
                  interfaces:
                    - Ethernet1/10
        state: overridden

    # Task output:
    # ------------
    # commands:
    #   - no vlan configuration 200

    # After state:
    # ------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10

    # Using deleted

    # Before state:
    # -------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # ip igmp snooping group-timeout 300
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    # vlan configuration 200
    #   ip igmp snooping static-group 233.252.0.20 interface Ethernet1/20

    - name: Delete the VLAN 200 configuration only
      cisco.nxos.nxos_igmp_snooping:
        config:
          vlans:
            - vlan_id: 200
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - no vlan configuration 200

    # Using deleted without config

    # Before state:
    # -------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # ip igmp snooping vxlan
    # ip igmp snooping group-timeout 300
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10

    # WARNING: this removes EVERY vlan configuration block on the switch, also the ones
    # created by other tools or roles. Run it with check_mode first.
    - name: Reset all global settings and remove all vlan configuration blocks
      cisco.nxos.nxos_igmp_snooping:
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - no ip igmp snooping vxlan
    #   - no ip igmp snooping group-timeout 300
    #   - no vlan configuration 100

    # After state:
    # ------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # (nothing is shown, the device has the default configuration)

    # Using rendered

    - name: Render platform specific configuration lines (without connecting to the device)
      cisco.nxos.nxos_igmp_snooping:
        config:
          snooping: true
          report_suppression: false
          vlans:
            - vlan_id: 100
              static_groups:
                - group: 233.252.0.10
                  source: 192.0.2.10
                  interfaces:
                    - Po20
        state: rendered

    # Task Output:
    # ------------
    # rendered:
    #   - ip igmp snooping
    #   - no ip igmp snooping report-suppression
    #   - vlan configuration 100
    #   - ip igmp snooping static-group 233.252.0.10 source 192.0.2.10 interface port-channel20

    # Using parsed

    # parsed.cfg
    # ----------
    # ip igmp snooping vxlan
    # ip igmp snooping group-timeout 300
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10
    #   ip igmp snooping static-group 233.252.0.10 interface port-channel20

    - name: Parse the provided configuration
      cisco.nxos.nxos_igmp_snooping:
        running_config: "{{ lookup('file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   snooping: true
    #   link_local_groups_suppression: true
    #   report_suppression: true
    #   v3_report_suppression: false
    #   vxlan: true
    #   disable_nve_static_router_port: false
    #   group_timeout: "300"
    #   vlans:
    #     - vlan_id: 100
    #       static_groups:
    #         - group: 233.252.0.10
    #           interfaces:
    #             - Ethernet1/10
    #             - port-channel20

    # Using gathered

    # Existing device config:
    # -----------------------
    # nxos# show running-config | section "^vlan configuration|^ip igmp snooping"
    # no ip igmp snooping link-local-groups-suppression
    # vlan configuration 100
    #   ip igmp snooping static-group 233.252.0.11 source 192.0.2.10 interface Ethernet1/10

    - name: Gather the IGMP snooping configuration from the device
      cisco.nxos.nxos_igmp_snooping:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   snooping: true
    #   link_local_groups_suppression: false
    #   report_suppression: true
    #   v3_report_suppression: false
    #   vxlan: false
    #   disable_nve_static_router_port: false
    #   vlans:
    #     - vlan_id: 100
    #       static_groups:
    #         - group: 233.252.0.11
    #           source: 192.0.2.10
    #           interfaces:
    #             - Ethernet1/10



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip igmp snooping vxlan&#x27;, &#x27;vlan configuration 100&#x27;, &#x27;ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
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
                      <span style="color: purple">dictionary</span>
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
                            <div>The provided configuration in the device-native format (offline).</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip igmp snooping vxlan&#x27;, &#x27;vlan configuration 100&#x27;, &#x27;ip igmp snooping static-group 233.252.0.10 interface Ethernet1/10&#x27;]</div>
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
