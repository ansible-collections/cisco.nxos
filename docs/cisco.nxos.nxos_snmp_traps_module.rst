.. _cisco.nxos.nxos_snmp_traps_module:


**************************
cisco.nxos.nxos_snmp_traps
**************************

**(deprecated, removed after 2024-01-01) Manages SNMP traps.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2024-01-01
:Why: Updated modules released with more functionality
:Alternative: nxos_snmp_server



Synopsis
--------
- Manages SNMP traps configurations.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
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
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>aaa</li>
                                    <li>bfd</li>
                                    <li>bgp</li>
                                    <li>bridge</li>
                                    <li>callhome</li>
                                    <li>cfs</li>
                                    <li>config</li>
                                    <li>eigrp</li>
                                    <li>entity</li>
                                    <li>feature-control</li>
                                    <li>generic</li>
                                    <li>hsrp</li>
                                    <li>license</li>
                                    <li>link</li>
                                    <li>lldp</li>
                                    <li>mmode</li>
                                    <li>ospf</li>
                                    <li>pim</li>
                                    <li>rf</li>
                                    <li>rmon</li>
                                    <li>snmp</li>
                                    <li>storm-control</li>
                                    <li>stpx</li>
                                    <li>switchfabric</li>
                                    <li>syslog</li>
                                    <li>sysmgr</li>
                                    <li>system</li>
                                    <li>upgrade</li>
                                    <li>vtp</li>
                                    <li>all</li>
                        </ul>
                </td>
                <td>
                        <div>Case sensitive group.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>enabled</b>&nbsp;&larr;</div></li>
                                    <li>disabled</li>
                        </ul>
                </td>
                <td>
                        <div>Manage the state of the resource.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOSv 7.3.(0)D1(1) on VIRL
   - Limited Support for Cisco MDS
   - This module works at the group level for traps.  If you need to only enable/disable 1 specific trap within a group, use the :ref:`cisco.nxos.nxos_command <cisco.nxos.nxos_command_module>` module.
   - Be aware that you can set a trap only for an enabled feature.
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # ensure lldp trap configured
    - cisco.nxos.nxos_snmp_traps:
        group: lldp
        state: enabled

    # ensure lldp trap is not configured
    - cisco.nxos.nxos_snmp_traps:
        group: lldp
        state: disabled



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
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>command sent to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">snmp-server enable traps lldp ;</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in a release after 2024-01-01. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Jason Edelman (@jedelman8)
