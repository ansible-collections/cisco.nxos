.. _cisco.nxos.nxos_nxapi_module:


*********************
cisco.nxos.nxos_nxapi
*********************

**Manage NXAPI configuration on an NXOS device.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Configures the NXAPI feature on devices running Cisco NXOS.  The NXAPI feature is absent from the configuration by default.  Since this module manages the NXAPI feature it only supports the use of the ``Cli`` transport.




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
                    <b>http</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Controls the operating state of the HTTP protocol as one of the underlying transports for NXAPI.  By default, NXAPI will enable the HTTP transport when the feature is first configured.  To disable the use of the HTTP transport, set the value of this argument to False.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: enable_http</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>http_port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">80</div>
                </td>
                <td>
                        <div>Configure the port with which the HTTP server will listen on for requests.  By default, NXAPI will bind the HTTP service to the standard HTTP port 80.  This argument accepts valid port values in the range of 1 to 65535.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>https</b>
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
                        <div>Controls the operating state of the HTTPS protocol as one of the underlying transports for NXAPI.  By default, NXAPI will disable the HTTPS transport when the feature is first configured.  To enable the use of the HTTPS transport, set the value of this argument to True.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: enable_https</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>https_port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">443</div>
                </td>
                <td>
                        <div>Configure the port with which the HTTPS server will listen on for requests.  By default, NXAPI will bind the HTTPS service to the standard HTTPS port 443.  This argument accepts valid port values in the range of 1 to 65535.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sandbox</b>
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
                        <div>The NXAPI feature provides a web base UI for developers for entering commands.  This feature is initially disabled when the NXAPI feature is configured for the first time.  When the <code>sandbox</code> argument is set to True, the developer sandbox URL will accept requests and when the value is set to False, the sandbox URL is unavailable. This is supported on NX-OS 7K series.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: enable_sandbox</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssl_strong_ciphers</b>
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
                        <div>Controls the use of whether strong or weak ciphers are configured. By default, this feature is disabled and weak ciphers are configured.  To enable the use of strong ciphers, set the value of this argument to True.</div>
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
                        <div>The <code>state</code> argument controls whether or not the NXAPI feature is configured on the remote device.  When the value is <code>present</code> the NXAPI feature configuration is present in the device running-config.  When the values is <code>absent</code> the feature configuration is removed from the running-config.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tlsv1_0</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Controls the use of the Transport Layer Security version 1.0 is configured.  By default, this feature is enabled.  To disable the use of TLSV1.0, set the value of this argument to True.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tlsv1_1</b>
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
                        <div>Controls the use of the Transport Layer Security version 1.1 is configured.  By default, this feature is disabled.  To enable the use of TLSV1.1, set the value of this argument to True.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tlsv1_2</b>
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
                        <div>Controls the use of the Transport Layer Security version 1.2 is configured.  By default, this feature is disabled.  To enable the use of TLSV1.2, set the value of this argument to True.</div>
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

    - name: Enable NXAPI access with default configuration
      cisco.nxos.nxos_nxapi:
        state: present

    - name: Enable NXAPI with no HTTP, HTTPS at port 9443 and sandbox disabled
      cisco.nxos.nxos_nxapi:
        enable_http: false
        https_port: 9443
        https: true
        enable_sandbox: false

    - name: remove NXAPI configuration
      cisco.nxos.nxos_nxapi:
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
                    <b>updates</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>Returns the list of commands that need to be pushed into the remote device to satisfy the arguments</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;no feature nxapi&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Peter Sprygada (@privateip)
