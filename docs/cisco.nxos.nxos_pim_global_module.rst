.. _cisco.nxos.nxos_pim_global_module:


**************************
cisco.nxos.nxos_pim_global
**************************

**PIM global resource module.**


Version added: 14.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages the global Protocol Independent Multicast (PIM) configuration of a device running Cisco NX-OS, the ``ip pim`` commands of the global configuration.
- It covers the SSM range, the static RP addresses and the anycast RP sets, together with a few simple global options.




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
                        <div>The global PIM configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>anycast_rps</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The anycast RP sets (<code>ip pim anycast-rp</code>).</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>anycast_rp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 address of the anycast RP.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>members</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 addresses of the set members, one <code>ip pim anycast-rp</code> line for each member.</div>
                        <div>The own address of the device is also a member of the set.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bfd</b>
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
                        <div>Enable BFD on all PIM interfaces (<code>ip pim bfd</code>).</div>
                        <div>Needs <code>feature bfd</code>, the device rejects the command without it.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>flush_routes</b>
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
                        <div>Remove the routes when PIM is restarted (<code>ip pim flush-routes</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>log_neighbor_changes</b>
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
                        <div>Log the PIM neighbor state changes (<code>ip pim log-neighbor-changes</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>register_rate_limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Rate limit of the PIM data registers in packets per second (<code>ip pim register-rate-limit</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rp_addresses</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The static RP addresses (<code>ip pim rp-address</code>), one entry for each line.</div>
                        <div>An RP can have several entries with different group lists.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>bidir</b>
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
                        <div>The groups are handled in PIM bidirectional mode (<code>bidir</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The multicast group range of the RP (<code>group-list</code>).</div>
                        <div>When none of <em>group_list</em>, <em>prefix_list</em> and <em>route_map</em> is given the RP is configured for all groups, which NX-OS displays as <code>group-list 224.0.0.0/4</code>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The prefix list that defines the groups of the RP (<code>prefix-list</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The route map that defines the groups of the RP (<code>route-map</code>).</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>rp_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The IPv4 address of the RP.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssm_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The group ranges for Source Specific Multicast (<code>ip pim ssm range</code>).</div>
                        <div>NX-OS keeps these in one line, so the list is configured as a whole. The keyword <code>none</code> removes all SSM ranges and must be the only item.</div>
                        <div>With <em>state</em> <code>merged</code> the ranges are added to the configured ranges.</div>
                        <div>A list that is only <code>232.0.0.0/8</code> resets the line to the default.</div>
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | include &quot;^ip pim &quot;</b>.</div>
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
                                    <li>rendered</li>
                                    <li>gathered</li>
                                    <li>parsed</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>With <em>merged</em> what is given is added to the device, nothing is removed. The static RP lines and anycast RP members are added, the SSM range list is extended.</div>
                        <div>With <em>replaced</em> and <em>overridden</em> the global PIM configuration of the device is made identical to <em>config</em>. The module manages a single global configuration, so both states behave the same. Everything that is not given is removed, also the static RPs and the anycast RP members.</div>
                        <div>With <em>deleted</em> the settings listed in <em>config</em> are removed. Without <em>config</em> all global PIM configuration that the module manages is removed.</div>
                        <div>With <em>rendered</em> the commands for <em>config</em> are returned and nothing is sent to the device.</div>
                        <div>With <em>gathered</em> the configuration is read from the device and returned in <em>gathered</em>.</div>
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
   - The feature ``pim`` must be enabled, for example with :ref:`cisco.nxos.nxos_feature <cisco.nxos.nxos_feature_module>`.
   - The configuration of the PIM interfaces (``ip pim sparse-mode``) and of the VRFs is not managed.
   - NX-OS replaces the default SSM range ``232.0.0.0/8`` when another range is configured. Add ``232.0.0.0/8`` to *ssm_range* to keep it. The default is not displayed in the running configuration and is not returned by the module.
   - A static RP without *group_list*, *prefix_list* and *route_map* is stored by NX-OS with the group list ``224.0.0.0/4``, which the module returns and expects in *replaced* and *overridden*.
   - :ref:`cisco.nxos.nxos_pim <cisco.nxos.nxos_pim_module>` and :ref:`cisco.nxos.nxos_pim_rp_address <cisco.nxos.nxos_pim_rp_address_module>` manage a part of the same configuration. Prefer this module for declarative management, including *replaced*, *overridden* and *gathered*. Do not manage the same settings with both in one play.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # switch# show running-config | include "^ip pim "
    # switch#

    - name: Merge the provided PIM configuration with the existing running configuration.
      cisco.nxos.nxos_pim_global:
        config:
          log_neighbor_changes: true
          register_rate_limit: 100
          ssm_range:
            - 232.0.0.0/8
            - 239.255.250.0/24
          rp_addresses:
            - rp_address: 192.0.2.1
              group_list: 239.255.0.0/16
            - rp_address: 192.0.2.2
              group_list: 239.254.0.0/16
              bidir: true
            - rp_address: 192.0.2.3
              prefix_list: PL_RP3
            - rp_address: 192.0.2.4
              route_map: RM_RP4
          anycast_rps:
            - anycast_rp: 192.0.2.10
              members:
                - 192.0.2.11
                - 192.0.2.12
        state: merged

    # Task output:
    # ------------
    # before: {}
    #
    # commands:
    #   - ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    #   - ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
    #   - ip pim rp-address 192.0.2.3 prefix-list PL_RP3
    #   - ip pim rp-address 192.0.2.4 route-map RM_RP4
    #   - ip pim anycast-rp 192.0.2.10 192.0.2.11
    #   - ip pim anycast-rp 192.0.2.10 192.0.2.12
    #   - ip pim log-neighbor-changes
    #   - ip pim register-rate-limit 100
    #   - ip pim ssm range 232.0.0.0/8 239.255.250.0/24
    #
    # after:
    #   log_neighbor_changes: true
    #   register_rate_limit: 100
    #   ssm_range:
    #     - 232.0.0.0/8
    #     - 239.255.250.0/24
    #   rp_addresses:
    #     - rp_address: 192.0.2.1
    #       group_list: 239.255.0.0/16
    #     - rp_address: 192.0.2.2
    #       group_list: 239.254.0.0/16
    #       bidir: true
    #     - rp_address: 192.0.2.3
    #       prefix_list: PL_RP3
    #     - rp_address: 192.0.2.4
    #       route_map: RM_RP4
    #   anycast_rps:
    #     - anycast_rp: 192.0.2.10
    #       members:
    #         - 192.0.2.11
    #         - 192.0.2.12

    # After state:
    # ------------
    # switch# show running-config | include "^ip pim "
    # ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    # ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
    # ip pim rp-address 192.0.2.3 prefix-list PL_RP3
    # ip pim rp-address 192.0.2.4 route-map RM_RP4
    # ip pim ssm range 232.0.0.0/8 239.255.250.0/24
    # ip pim log-neighbor-changes
    # ip pim register-rate-limit 100
    # ip pim anycast-rp 192.0.2.10 192.0.2.11
    # ip pim anycast-rp 192.0.2.10 192.0.2.12

    # Using replaced

    # Before state:
    # -------------
    # switch# show running-config | include "^ip pim "
    # ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    # ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
    # ip pim log-neighbor-changes
    # ip pim anycast-rp 192.0.2.10 192.0.2.11

    - name: Replace the global PIM configuration.
      cisco.nxos.nxos_pim_global:
        config:
          rp_addresses:
            - rp_address: 192.0.2.1
              group_list: 239.255.0.0/16
            - rp_address: 192.0.2.5
              group_list: 239.253.0.0/16
        state: replaced

    # Task output:
    # ------------
    # commands:
    #   - no ip pim rp-address 192.0.2.2 group-list 239.254.0.0/16 bidir
    #   - no ip pim anycast-rp 192.0.2.10 192.0.2.11
    #   - no ip pim log-neighbor-changes
    #   - ip pim rp-address 192.0.2.5 group-list 239.253.0.0/16

    # Using deleted

    # Before state:
    # -------------
    # switch# show running-config | include "^ip pim "
    # ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    # ip pim ssm range 232.0.0.0/8 239.255.250.0/24
    # ip pim anycast-rp 192.0.2.10 192.0.2.11

    - name: Remove the SSM range and the anycast RP set.
      cisco.nxos.nxos_pim_global:
        config:
          ssm_range:
            - 232.0.0.0/8
          anycast_rps:
            - anycast_rp: 192.0.2.10
              members:
                - 192.0.2.11
        state: deleted

    # Task output:
    # ------------
    # commands:
    #   - no ip pim anycast-rp 192.0.2.10 192.0.2.11
    #   - no ip pim ssm range 232.0.0.0/8

    # Using rendered

    - name: Render the commands without a device connection.
      cisco.nxos.nxos_pim_global:
        config:
          bfd: true
          rp_addresses:
            - rp_address: 192.0.2.1
        state: rendered

    # Task output:
    # ------------
    # rendered:
    #   - ip pim rp-address 192.0.2.1 group-list 224.0.0.0/4
    #   - ip pim bfd

    # Using gathered

    - name: Gather the global PIM configuration.
      cisco.nxos.nxos_pim_global:
        state: gathered

    # Task output:
    # ------------
    # gathered:
    #   log_neighbor_changes: true
    #   ssm_range:
    #     - 232.0.0.0/8
    #     - 239.255.250.0/24
    #   rp_addresses:
    #     - rp_address: 192.0.2.1
    #       group_list: 239.255.0.0/16

    # Using parsed

    # parsed.cfg
    # ----------
    # ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16
    # ip pim anycast-rp 192.0.2.10 192.0.2.11

    - name: Parse the text of the running configuration.
      cisco.nxos.nxos_pim_global:
        running_config: "{{ lookup('ansible.builtin.file', 'parsed.cfg') }}"
        state: parsed

    # Task output:
    # ------------
    # parsed:
    #   rp_addresses:
    #     - rp_address: 192.0.2.1
    #       group_list: 239.255.0.0/16
    #   anycast_rps:
    #     - anycast_rp: 192.0.2.10
    #       members:
    #         - 192.0.2.11



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
                      <span style="color: purple">dictionary</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16&#x27;, &#x27;ip pim anycast-rp 192.0.2.10 192.0.2.11&#x27;, &#x27;ip pim ssm range 232.0.0.0/8 239.255.250.0/24&#x27;]</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip pim rp-address 192.0.2.1 group-list 239.255.0.0/16&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jørgen Spange (@jorgenspange)
