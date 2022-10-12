.. _cisco.nxos.nxos_smu_module:


*******************
cisco.nxos.nxos_smu
*******************

**(deprecated, removed after 2022-10-01) Perform SMUs on Cisco NX-OS devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in collection release after 2022-10-01
:Why: Updated modules released with more functionality.
:Alternative: nxos_rpm



Synopsis
--------
- Perform software maintenance upgrades (SMUs) on Cisco NX-OS devices.




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
                    <b>file_system</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"bootflash:"</div>
                </td>
                <td>
                        <div>The remote file system of the device. If omitted, devices that support a file_system parameter will use their default values.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pkg</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the remote package.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NXOSv 7.3.(0)D1(1) on VIRL
   - Unsupported for Cisco MDS
   - The module can only activate and commit a package, not remove or deactivate it.
   - Use ``transport=nxapi`` to avoid connection timeout



Examples
--------

.. code-block:: yaml

    - cisco.nxos.nxos_smu:
        pkg: nxos.CSCuz65185-n9k_EOR-1.0.0-7.0.3.I2.2d.lib32_n9000.rpm



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;install add bootflash:nxos.CSCuz65185-n9k_EOR-1.0.0-7.0.3.I2.2d.lib32_n9000.rpm&#x27;, &#x27;install activate bootflash:nxos.CSCuz65185-n9k_EOR-1.0.0-7.0.3.I2.2d.lib32_n9000.rpm force&#x27;, &#x27;install commit bootflash:nxos.CSCuz65185-n9k_EOR-1.0.0-7.0.3.I2.2d.lib32_n9000.rpm&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


- This module will be removed in a release after 2022-10-01. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Gabriele Gerbino (@GGabriele)
