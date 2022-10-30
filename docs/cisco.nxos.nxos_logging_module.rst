.. _cisco.nxos.nxos_logging_module:


***********************
cisco.nxos.nxos_logging
***********************

**Manage logging on network devices**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2023-08-01
:Why: Updated module released with more functionality.
:Alternative: nxos_logging_global



Synopsis
--------
- This module provides declarative management of logging on Cisco NX-OS devices.




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
                    <b>aggregate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of logging definitions.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>console</li>
                                    <li>logfile</li>
                                    <li>module</li>
                                    <li>monitor</li>
                                    <li>server</li>
                        </ul>
                </td>
                <td>
                        <div>Destination of the logs.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dest_level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set logging severity levels.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: level</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>event</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>link-enable</li>
                                    <li>link-default</li>
                                    <li>trunk-enable</li>
                                    <li>trunk-default</li>
                        </ul>
                </td>
                <td>
                        <div>Link/trunk enable/default interface configuration logging</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Facility name for logging.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility_level</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set logging severity levels for facility based log messages.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>facility_link_status</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>link-down-notif</li>
                                    <li>link-down-error</li>
                                    <li>link-up-notif</li>
                                    <li>link-up-error</li>
                        </ul>
                </td>
                <td>
                        <div>Set logging facility ethpm link status. Not idempotent with version 6.0 images.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>file_size</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set logfile size</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Interface to be used while configuring source-interface for logging (e.g., &#x27;Ethernet1/2&#x27;, &#x27;mgmt0&#x27;)</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interface_message</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>add-interface-description</li>
                        </ul>
                </td>
                <td>
                        <div>Add interface description to interface syslogs. Does not work with version 6.0 images using nxapi as a transport.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>If value of <code>dest</code> is <em>logfile</em> it indicates file-name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>purge</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Remove any switch logging configuration that does not match what has been configured Not supported for ansible_connection local. All nxos_logging tasks must use the same ansible_connection type.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remote_server</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hostname or IP Address for remote logging (when dest is &#x27;server&#x27;).</div>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>State of the logging configuration.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timestamp</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>microseconds</li>
                                    <li>milliseconds</li>
                                    <li>seconds</li>
                        </ul>
                </td>
                <td>
                        <div>Set logging timestamp format</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF to be used while configuring remote logging (when dest is &#x27;server&#x27;).</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Limited Support for Cisco MDS
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    - name: configure console logging with level
      cisco.nxos.nxos_logging:
        dest: console
        level: 2
        state: present
    - name: remove console logging configuration
      cisco.nxos.nxos_logging:
        dest: console
        level: 2
        state: absent
    - name: configure file logging with level
      cisco.nxos.nxos_logging:
        dest: logfile
        name: testfile
        dest_level: 3
        state: present
    - name: Configure logging logfile with size
      cisco.nxos.nxos_logging:
        dest: logfile
        name: testfile
        dest_level: 3
        file_size: 16384
    - name: configure facility level logging
      cisco.nxos.nxos_logging:
        facility: daemon
        facility_level: 0
        state: present
    - name: remove facility level logging
      cisco.nxos.nxos_logging:
        facility: daemon
        facility_level: 0
        state: absent
    - name: Configure Remote Logging
      cisco.nxos.nxos_logging:
        dest: server
        remote_server: test-syslogserver.com
        facility: auth
        facility_level: 1
        use_vrf: management
        state: present
    - name: Configure Source Interface for Logging
      cisco.nxos.nxos_logging:
        interface: mgmt0
        state: present
    - name: Purge nxos_logging configuration not managed by this playbook
      cisco.nxos.nxos_logging:
        purge: true
    - name: Configure logging timestamp
      cisco.nxos.nxos_logging:
        timestamp: milliseconds
        state: present
    - name: Configure logging facility ethpm link status
      cisco.nxos.nxos_logging:
        facility: ethpm
        facility_link_status: link-up-notif
        state: present
    - name: Configure logging message ethernet description
      cisco.nxos.nxos_logging:
        interface_message: add-interface-description
        state: present
    - name: Configure logging event link enable
      cisco.nxos.nxos_logging:
        event: link-enable
        state: present
    - name: Configure logging using aggregate
      cisco.nxos.nxos_logging:
        aggregate:
        - {dest: console, dest_level: 2}
        - {dest: logfile, dest_level: 2, name: testfile}
        - {facility: daemon, facility_level: 0}
        state: present



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
                            <div>The list of configuration mode commands to send to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;logging console 2&#x27;, &#x27;logging logfile testfile 3&#x27;, &#x27;logging level daemon 0&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in a release after 2023-08-01. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Trishna Guha (@trishnaguha)
