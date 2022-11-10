.. _cisco.nxos.nxos_pim_module:


*******************
cisco.nxos.nxos_pim
*******************

**Manages configuration of a PIM instance.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manages configuration of a Protocol Independent Multicast (PIM) instance.




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
                    <b>bfd</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>enable</li>
                                    <li>disable</li>
                        </ul>
                </td>
                <td>
                        <div>Enables BFD on all PIM interfaces.</div>
                        <div>Dependency: &#x27;&#x27;feature bfd&#x27;&#x27;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssm_range</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>Configure group ranges for Source Specific Multicast (SSM). Valid values are multicast addresses or the keyword <code>none</code> or keyword <code>default</code>. <code>none</code> removes all SSM group ranges. <code>default</code> will set ssm_range to the default multicast address. If you set multicast address, please ensure that it is not the same as the <code>default</code>, otherwise use the <code>default</code> option.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Unsupported for Cisco MDS
   - For information on using CLI and NX-API see the :ref:`NXOS Platform Options guide <nxos_platform_options>`
   - For more information on using Ansible to manage network devices see the :ref:`Ansible Network Guide <network_guide>`
   - For more information on using Ansible to manage Cisco devices see the `Cisco integration page <https://www.ansible.com/integrations/networks/cisco>`_.



Examples
--------

.. code-block:: yaml

    - name: Configure ssm_range, enable bfd
      cisco.nxos.nxos_pim:
        bfd: enable
        ssm_range: 224.0.0.0/8

    - name: Set to default
      cisco.nxos.nxos_pim:
        ssm_range: default

    - name: Remove all ssm group ranges
      cisco.nxos.nxos_pim:
        ssm_range: none



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
                            <div>commands sent to the device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ip pim bfd&#x27;, &#x27;ip pim ssm range 224.0.0.0/8&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Gabriele Gerbino (@GGabriele)
