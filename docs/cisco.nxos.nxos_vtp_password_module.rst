.. _cisco.nxos.nxos_vtp_password_module:


****************************
cisco.nxos.nxos_vtp_password
****************************

**Manages VTP password configuration.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manages VTP password configuration.




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
                        </ul>
                </td>
                <td>
                        <div>Manage the state of the resource</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vtp_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VTP password</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOSv 7.3.(0)D1(1) on VIRL
   - Unsupported for Cisco MDS
   - VTP feature must be active on the device to use this module.
   - This module is used to manage only VTP passwords.
   - Use this in combination with :ref:`cisco.nxos.nxos_vtp_domain <cisco.nxos.nxos_vtp_domain_module>` and :ref:`cisco.nxos.nxos_vtp_version <cisco.nxos.nxos_vtp_version_module>` to fully manage VTP operations.
   - You can set/remove password only if a VTP domain already exist.
   - If ``state=absent`` and no ``vtp_password`` is provided, it remove the current VTP password.
   - If ``state=absent`` and ``vtp_password`` is provided, the proposed ``vtp_password`` has to match the existing one in order to remove it.
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # ENSURE VTP PASSWORD IS SET
    - cisco.nxos.nxos_vtp_password:
        state: present
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'

    # ENSURE VTP PASSWORD IS REMOVED
    - cisco.nxos.nxos_vtp_password:
        state: absent
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'



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
                    <b>changed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>check to see if a change was made on the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>end_state</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>k/v pairs of vtp after module execution</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;domain&#x27;: &#x27;ntc&#x27;, &#x27;version&#x27;: &#x27;1&#x27;, &#x27;vtp_password&#x27;: &#x27;new_ntc&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>existing</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>k/v pairs of existing vtp</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;domain&#x27;: &#x27;ntc&#x27;, &#x27;version&#x27;: &#x27;1&#x27;, &#x27;vtp_password&#x27;: &#x27;ntc&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>proposed</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>k/v pairs of parameters passed into module</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;vtp_password&#x27;: &#x27;new_ntc&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>updates</b>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vtp password new_ntc&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Gabriele Gerbino (@GGabriele)
