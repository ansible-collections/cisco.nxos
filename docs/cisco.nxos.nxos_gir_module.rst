.. _cisco.nxos.nxos_gir_module:


*******************
cisco.nxos.nxos_gir
*******************

**Trigger a graceful removal or insertion (GIR) of the switch.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Trigger a graceful removal or insertion (GIR) of the switch.
- GIR processing may take more than 2 minutes. Timeout settings are automatically extended to 200s when user timeout settings are insufficient.




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
                        <div>Specify desired state of the resource.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>system_mode_maintenance</b>
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
                        <div>When <code>system_mode_maintenance=true</code> it puts all enabled protocols in maintenance mode (using the isolate command). When <code>system_mode_maintenance=false</code> it puts all enabled protocols in normal mode (using the no isolate command).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>system_mode_maintenance_dont_generate_profile</b>
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
                        <div>When <code>system_mode_maintenance_dont_generate_profile=true</code> it prevents the dynamic searching of enabled protocols and executes commands configured in a maintenance-mode profile. Use this option if you want the system to use a maintenance-mode profile that you have created. When <code>system_mode_maintenance_dont_generate_profile=false</code> it prevents the dynamic searching of enabled protocols and executes commands configured in a normal-mode profile. Use this option if you want the system to use a normal-mode profile that you have created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>system_mode_maintenance_on_reload_reset_reason</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>hw_error</li>
                                    <li>svc_failure</li>
                                    <li>kern_failure</li>
                                    <li>wdog_timeout</li>
                                    <li>fatal_error</li>
                                    <li>lc_failure</li>
                                    <li>match_any</li>
                                    <li>manual_reload</li>
                                    <li>any_other</li>
                                    <li>maintenance</li>
                        </ul>
                </td>
                <td>
                        <div>Boots the switch into maintenance mode automatically in the event of a specified system crash. Note that not all reset reasons are applicable for all platforms. Also if reset reason is set to match_any, it is not idempotent as it turns on all reset reasons. If reset reason is match_any and state is absent, it turns off all the reset reasons.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>system_mode_maintenance_shutdown</b>
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
                        <div>Shuts down all protocols, vPC domains, and interfaces except the management interface (using the shutdown command). This option is disruptive while <code>system_mode_maintenance</code> (which uses the isolate command) is not.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>system_mode_maintenance_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Keeps the switch in maintenance mode for a specified number of minutes. Range is 5-65535.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOSv 7.3.(0)D1(1) on VIRL
   - Unsupported for Cisco MDS
   - ``state`` has effect only in combination with ``system_mode_maintenance_timeout`` or ``system_mode_maintenance_on_reload_reset_reason``.
   - Using ``system_mode_maintenance`` and ``system_mode_maintenance_dont_generate_profile`` would make the module fail, but the system mode will be triggered anyway.
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    # Trigger system maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance: true
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Trigger system normal mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance: false
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Configure on-reload reset-reason for maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance_on_reload_reset_reason: manual_reload
        state: present
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Add on-reload reset-reason for maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance_on_reload_reset_reason: hw_error
        state: present
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Remove on-reload reset-reason for maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance_on_reload_reset_reason: manual_reload
        state: absent
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Set timeout for maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance_timeout: 30
        state: present
        host: '{{ inventory_hostname }}'
        username: '{{ un }}'
        password: '{{ pwd }}'
    # Remove timeout for maintenance mode
    - cisco.nxos.nxos_gir:
        system_mode_maintenance_timeout: 30
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
                    <b>final_system_mode</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>verbose mode</td>
                <td>
                            <div>describe the last system mode</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">normal</div>
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
                <td>verbose mode</td>
                <td>
                            <div>commands sent to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;terminal dont-ask&#x27;, &#x27;system mode maintenance timeout 10&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Gabriele Gerbino (@GGabriele)
