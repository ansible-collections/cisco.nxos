.. _cisco.nxos.nxos_lldp_module:


********************
cisco.nxos.nxos_lldp
********************

**(deprecated, removed after 2022-06-01) Manage LLDP configuration on Cisco NXOS network devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2022-06-01
:Why: Updated modules released with more functionality
:Alternative: nxos_lldp_global



Synopsis
--------
- This module provides declarative management of LLDP service on Cisco NXOS network devices.




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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                                    <li>enabled</li>
                                    <li>disabled</li>
                        </ul>
                </td>
                <td>
                        <div>State of the LLDP configuration. If value is <em>present</em> lldp will be enabled else if it is <em>absent</em> it will be disabled.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOSv 7.0(3)I5(1).
   - Unsupported for Cisco MDS



Examples
--------

.. code-block:: yaml

    - name: Enable LLDP service
      cisco.nxos.nxos_lldp:
        state: present

    - name: Disable LLDP service
      cisco.nxos.nxos_lldp:
        state: absent



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
                <td>always, except for the platforms that use Netconf transport to manage the device.</td>
                <td>
                            <div>The list of configuration mode commands to send to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;feature lldp&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in a release after 2022-06-01. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
