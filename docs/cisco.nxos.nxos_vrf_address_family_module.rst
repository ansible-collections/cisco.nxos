.. _cisco.nxos.nxos_vrf_address_family_module:


**********************************
cisco.nxos.nxos_vrf_address_family
**********************************

**Resource module to configure VRF address family definitions.**


Version added: 9.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module provides declarative management of VRF definitions on Cisco NXOS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="6">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A list of device configurations for VRF address family.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>address_families</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Enable address family and enter its config mode - AFI/SAFI configuration</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>afi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>ipv4</li>
                                    <li>ipv6</li>
                        </ul>
                </td>
                <td>
                        <div>Address Family Identifier (AFI)</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>export</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF export</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map based VRF export</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Router Context</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>allow_vpn</b>
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
                        <div>Allow re-importation of VPN imported routes</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>map_import</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map based VRF import</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix limit</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>import</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>VRF import</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map based VRF export</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vrf</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Router Context</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>advertise_vpn</b>
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
                        <div>Allow leaked routes to be advertised to VPN</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>map_import</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Route-map based VRF import</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix limit</div>
                </td>
            </tr>


            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>maximum</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set a limit of routes</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_route_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure the options for maximum routes</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Configure threshold &amp; its options</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>reinstall_threshold</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Threshold value (%) at which to reinstall routes back to VRF</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>threshold_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Threshold value (%) at which to generate a warning msg</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>warning_only</b>
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
                        <div>Configure only give a warning message if limit is exceeded</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>max_routes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum number of routes allowed</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>route_target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify Target VPN Extended Communities</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>export</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Export Target-VPN community</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>import</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Import Target-VPN community</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>safi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>multicast</li>
                                    <li>unicast</li>
                        </ul>
                </td>
                <td>
                        <div>Address Family modifier</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="5">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the VRF.</div>
                </td>
            </tr>

            <tr>
                <td colspan="6">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section ^vrf</b>.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="6">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>deleted</li>
                                    <li>purged</li>
                                    <li><div style="color: blue"><b>merged</b>&nbsp;&larr;</div></li>
                                    <li>replaced</li>
                                    <li>rendered</li>
                                    <li>overridden</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in</div>
                        <div>The states <em>rendered</em>, <em>gathered</em> and <em>parsed</em> does not perform any change on the device.</div>
                        <div>The state <em>rendered</em> will transform the configuration in <code>config</code> option to platform specific CLI commands which will be returned in the <em>rendered</em> key within the result. For state <em>rendered</em> active connection to remote host is not required.</div>
                        <div>The state <em>gathered</em> will fetch the running configuration from device and transform it into structured data in the format as per the resource module argspec and the value is returned in the <em>gathered</em> key within the result.</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into JSON format as per the resource module parameters and the value is returned in the <em>parsed</em> key within the result. The value of <code>running_config</code> option should be the same format as the output of command <em>show running-config | section ^vrf</em>. connection to remote host is not required.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - This module works with connection ``network_cli`` and ``httpapi``. See https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf

    - name: Merge provided configuration with device configuration
      register: result
      cisco.nxos.nxos_vrf_address_family:
        config:
          - name: VRF1
            address_families:
              - afi: ipv4
                safi: unicast
                route_target:
                  - export: "65512:200"
                maximum:
                  max_routes: 500
                  max_route_options:
                    threshold:
                      threshold_value: 60
                      reinstall_threshold: 80
                export:
                  - map: "22"
                  - vrf:
                      allow_vpn: true
                      map_import: "44"
                  - vrf:
                      allow_vpn: true
              - afi: ipv6
                safi: unicast
                maximum:
                  max_routes: 1000
                route_target:
                  - import: "65512:200"
                import:
                  - map: "22"
                  - vrf:
                      advertise_vpn: true
                      map_import: "44"
                  - vrf:
                      advertise_vpn: true
        state: merged

    # Task Output:
    # ------------

    # before: {}
    # commands:
    #   - vrf context VRF1
    #   - address-family ipv4 unicast
    #   - maximum routes 500 60 reinstall 80
    #   - route-target export 65512:200
    #   - export map 22
    #   - export vrf default map 44 allow-vpn
    #   - export vrf allow-vpn
    #   - address-family ipv6 unicast
    #   - maximum routes 1000
    #   - route-target import 65512:200
    #   - import map 22
    #   - import vrf default map 44 advertise-vpn
    #   - import vrf advertise-vpn
    # after:
    #   - address_families:
    #       - afi: ipv4
    #         export:
    #           - map: "22"
    #           - vrf:
    #               allow_vpn: true
    #               map_import: "44"
    #           - vrf:
    #               allow_vpn: true
    #         maximum:
    #           max_route_options:
    #             threshold:
    #               reinstall_threshold: 80
    #               threshold_value: 60
    #           max_routes: 500
    #         route_target:
    #           - export: 65512:200
    #         safi: unicast
    #       - afi: ipv6
    #         import:
    #           - map: "22"
    #           - vrf:
    #               advertise_vpn: true
    #               map_import: "44"
    #           - vrf:
    #               advertise_vpn: true
    #         maximum:
    #           max_routes: 1000
    #         route_target:
    #           - import: 65512:200
    #         safi: unicast
    #     name: VRF1

    # After state:
    # ------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target export 65512:200
    #     export map 22
    #     export vrf default map 44 allow-vpn
    #     export vrf allow-vpn
    #     maximum routes 500 60 reinstall 80
    #   address-family ipv6 unicast
    #     route-target import 65512:200
    #     import map 22
    #     import vrf default map 44 advertise-vpn
    #     import vrf advertise-vpn
    #     maximum routes 1000

    # Using deleted

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #      route-target import 64512:200
    #      route-target export 64512:200
    #      export map 22
    #      export vrf default map 44 allow-vpn
    #      export vrf allow-vpn
    #      maximum routes 900 22 reinstall 44

    - name: Delete given vrf address family configuration
      register: result
      cisco.nxos.nxos_vrf_address_family:
        config:
          - name: VRF1
            address_families:
              - afi: ipv4
                safi: unicast
                route_target:
                  - import: 64512:200
                export:
                  - map: "22"
                maximum:
                  max_routes: 900
                  max_route_options:
                    threshold:
                      threshold_value: 22
                      reinstall_threshold: 44
        state: deleted

    # Task Output:
    # ------------
    #
    # before:
    #  - address_families:
    #      - afi: ipv4
    #        export:
    #          - map: "22"
    #          - vrf:
    #              allow_vpn: true
    #              map_import: "44"
    #          - vrf:
    #              allow_vpn: true
    #        maximum:
    #          max_route_options:
    #            threshold:
    #              reinstall_threshold: 44
    #              threshold_value: 22
    #          max_routes: 900
    #        route_target:
    #          - import: "64512:200"
    #          - export: "64512:200"
    #        safi: unicast
    #    name: VRF1

    # commands:
    #   - vrf context VRF1
    #   - address-family ipv4 unicast
    #   - no maximum routes 900 22 reinstall 44
    #   - no route-target import 64512:200
    #   - no export map 22
    # after:
    #   - address_families:
    #       - afi: ipv4
    #         export:
    #           - vrf:
    #               allow_vpn: true
    #               map_import: "44"
    #           - vrf:
    #               allow_vpn: true
    #         route_target:
    #           - export: "64512:200"
    #         safi: unicast
    #     name: VRF1

    # Using purged

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target export 65512:200
    #     export map 22
    #     export vrf default map 44 allow-vpn
    #     export vrf allow-vpn
    #     maximum routes 500 60 reinstall 80
    #   address-family ipv6 unicast
    #     route-target import 65512:200
    #     import map 22
    #     import vrf default map 44 advertise-vpn
    #     import vrf advertise-vpn
    #     maximum routes 1000

    - name: Purge the configuration of VRF address family
      register: result
      cisco.nxos.nxos_vrf_address_family:
        config:
          - name: VRF1
            address_families:
              - afi: ipv4
                safi: unicast
              - afi: ipv6
                safi: unicast
        state: purged

    # Task Output:
    # ------------
    #
    # before:
    #     - address_families:
    #           - afi: ipv4
    #             export:
    #                 - map: "22"
    #                 - vrf:
    #                       allow_vpn: true
    #                       map_import: "44"
    #                 - vrf:
    #                       allow_vpn: true
    #             maximum:
    #                 max_route_options:
    #                     threshold:
    #                         reinstall_threshold: 80
    #                         threshold_value: 60
    #                 max_routes: 500
    #             route_target:
    #                 - export: 65512:200
    #             safi: unicast
    #           - afi: ipv6
    #             import:
    #                 - map: "22"
    #                 - vrf:
    #                       advertise_vpn: true
    #                       map_import: "44"
    #                 - vrf:
    #                       advertise_vpn: true
    #             maximum:
    #                 max_routes: 1000
    #             route_target:
    #                 - import: 65512:200
    #             safi: unicast
    #       name: VRF1
    # commands:
    #   - vrf context VRF1
    #   - no address-family ipv4 unicast
    #   - no address-family ipv6 unicast
    # after: {}


    # Using overridden

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target import 64512:200
    #   address-family ipv6 unicast
    #     route-target import 554832:500

    - name: Override the provided configuration with the existing running configuration
      cisco.nxos.nxos_vrf_address_family:
        config:
          - name: VRF1
            address_families:
              - afi: ipv6
                safi: unicast
                route_target:
                  - export: 65512:200
                maximum:
                  max_routes: 500
                  max_route_options:
                    threshold:
                      threshold_value: 60
                      reinstall_threshold: 80
                export:
                  - map: "22"
                  - vrf:
                      allow_vpn: true
                      map_import: "44"
                  - vrf:
                      allow_vpn: true
          - name: temp
            address_families:
              - afi: ipv4
                safi: unicast
                route_target:
                  - import: 65512:200
                maximum:
                  max_routes: 1000
                export:
                  - map: "26"
                  - vrf:
                      allow_vpn: true
                      map_import: "46"
        state: overridden

    # Task Output:
    # ------------
    #
    # before:
    #  - address_families:
    #      - afi: ipv4
    #        route_target:
    #          - import: 64512:200
    #        safi: unicast
    #      - afi: ipv6
    #        route_target:
    #          - import: 554832:500
    #        safi: unicast
    #    name: VRF1
    #
    # commands:
    #  - vrf context VRF1
    #  - address-family ipv4 unicast
    #  - no route-target import 64512:200
    #  - address-family ipv6 unicast
    #  - maximum routes 500 60 reinstall 80
    #  - no route-target import 554832:500
    #  - route-target export 65512:200
    #  - export map 22
    #  - export vrf default map 44 allow-vpn
    #  - export vrf allow-vpn
    #  - vrf context temp
    #  - address-family ipv4 unicast
    #  - maximum routes 1000
    #  - route-target import 65512:200
    #  - export map 26
    #  - export vrf default map 46 allow-vpn
    # after:
    #  - address_families:
    #      - afi: ipv4
    #        safi: unicast
    #      - afi: ipv6
    #        export:
    #          - map: "22"
    #          - vrf:
    #              allow_vpn: true
    #              map_import: "44"
    #          - vrf:
    #              allow_vpn: true
    #        maximum:
    #          max_route_options:
    #            threshold:
    #              reinstall_threshold: 80
    #              threshold_value: 60
    #          max_routes: 500
    #        route_target:
    #          - export: 65512:200
    #        safi: unicast
    #    name: VRF1
    #  - address_families:
    #      - afi: ipv4
    #        export:
    #          - map: "26"
    #          - vrf:
    #              allow_vpn: true
    #              map_import: "46"
    #        maximum:
    #          max_routes: 1000
    #        route_target:
    #          - import: 65512:200
    #        safi: unicast
    #    name: temp

    # Using replaced

    # Before state:
    # -------------
    #
    # nxos# show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target import 64512:200
    #   address-family ipv6 unicast
    #     route-target import 554832:500

    - name: Replaced state for VRF configuration
      cisco.nxos.nxos_vrf_global:
        config:
          vrfs:
            - ip:
                name_server:
                  address_list:
                    - 192.168.255.1
                route:
                  - destination: 192.168.255.1
                    source: 0.0.0.0/0
              name: management
            - name: temp
              description: Test
              ip:
                auto_discard: true
                domain_list:
                  - invalid.com
                  - example.com
                domain_name: test.org
        state: replaced

    # Task Output:
    # ------------
    #
    # before:
    #  - address_families:
    #      - afi: ipv4
    #        route_target:
    #          - import: 64512:200
    #        safi: unicast
    #      - afi: ipv6
    #        route_target:
    #          - import: 554832:500
    #        safi: unicast
    #    name: VRF1
    # commands:
    #  - vrf context VRF1
    #  - address-family ipv4 unicast
    #  - no route-target import 64512:200
    #  - address-family ipv6 unicast
    #  - maximum routes 500 60 reinstall 80
    #  - no route-target import 554832:500
    #  - route-target export 65512:200
    #  - export map 22
    #  - export vrf default map 44 allow-vpn
    #  - export vrf allow-vpn
    #  - vrf context temp
    #  - address-family ipv4 unicast
    #  - maximum routes 1000
    #  - route-target import 65512:200
    #  - export map 26
    #  - export vrf default map 46 allow-vpn
    # after:
    #  - address_families:
    #      - afi: ipv4
    #        safi: unicast
    #      - afi: ipv6
    #        export:
    #          - map: "22"
    #          - vrf:
    #              allow_vpn: true
    #              map_import: "44"
    #          - vrf:
    #              allow_vpn: true
    #        maximum:
    #          max_route_options:
    #            threshold:
    #              reinstall_threshold: 80
    #              threshold_value: 60
    #          max_routes: 500
    #        route_target:
    #          - export: 65512:200
    #        safi: unicast
    #    name: VRF1
    #  - address_families:
    #      - afi: ipv4
    #        export:
    #          - map: "26"
    #          - vrf:
    #              allow_vpn: true
    #              map_import: "46"
    #        maximum:
    #          max_routes: 1000
    #        route_target:
    #          - import: 65512:200
    #        safi: unicast
    #    name: temp
    #
    # After state:
    # ------------
    # router-ios#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv6 unicast
    #     route-target export 65512:200
    #     export map 22
    #     export vrf default map 44 allow-vpn
    #     export vrf allow-vpn
    # vrf context temp
    #   address-family ipv4 unicast
    #     route-target import 65512:200
    #     export map 26
    #     export vrf default map 46 allow-vpn
    #     maximum routes 1000

    # Using gathered

    # Before state:
    # -------------
    #
    # nxos#show running-config | section ^vrf
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target export 65512:200
    #     export map 22
    #     export vrf default map 44 allow-vpn
    #     export vrf allow-vpn
    #     maximum routes 500 60 reinstall 80
    #   address-family ipv6 unicast
    #     route-target import 65512:200
    #     import map 22
    #     import vrf default map 44 advertise-vpn
    #     import vrf advertise-vpn
    #     maximum routes 1000

    - name: Gathered state for VRF configuration
      cisco.nxos.nxos_vrf_global:
        config:
        state: gathered

    # Task Output:
    # ------------
    #
    # gathered:
    #     - address_families:
    #           - afi: ipv4
    #             export:
    #                 - map: "22"
    #                 - vrf:
    #                       allow_vpn: true
    #                       map_import: "44"
    #                 - vrf:
    #                       allow_vpn: true
    #             maximum:
    #                 max_route_options:
    #                     threshold:
    #                         reinstall_threshold: 80
    #                         threshold_value: 60
    #                 max_routes: 500
    #             route_target:
    #                 - export: 65512:200
    #             safi: unicast
    #           - afi: ipv6
    #             import:
    #                 - map: "22"
    #                 - vrf:
    #                       advertise_vpn: true
    #                       map_import: "44"
    #                 - vrf:
    #                       advertise_vpn: true
    #             maximum:
    #                 max_routes: 1000
    #             route_target:
    #                 - import: 65512:200
    #             safi: unicast
    #       name: VRF1

    # Using rendered

    - name: Render provided configuration with device configuration
      register: result
      cisco.nxos.nxos_vrf_address_family:
        config:
          - name: VRF1
            address_families:
              - afi: ipv6
                safi: unicast
                route_target:
                  - export: 65512:200
                maximum:
                  max_routes: 500
                  max_route_options:
                    threshold:
                      threshold_value: 60
                      reinstall_threshold: 80
                export:
                  - map: "22"
                  - vrf:
                      allow_vpn: true
                      map_import: "44"
                  - vrf:
                      allow_vpn: true
          - name: temp
            address_families:
              - afi: ipv4
                safi: unicast
                route_target:
                  - import: 65512:200
                maximum:
                  max_routes: 1000
                export:
                  - map: "26"
                  - vrf:
                      allow_vpn: true
                      map_import: "46"
        state: rendered

    # Task Output:
    # ------------
    #
    # commands:
    #   - vrf context VRF1
    #   - address-family ipv6 unicast
    #   - maximum routes 500 60 reinstall 80
    #   - route-target export 65512:200
    #   - export map 22
    #   - export vrf default map 44 allow-vpn
    #   - export vrf allow-vpn
    #   - vrf context temp
    #   - address-family ipv4 unicast
    #   - maximum routes 1000
    #   - route-target import 65512:200
    #   - export map 26
    #   - export vrf default map 46 allow-vpn

    # Using Parsed

    # Parsed Config:
    # -------------
    # vrf context VRF1
    #   address-family ipv4 unicast
    #     route-target import 64512:200
    #     route-target export 64512:200
    #     export map 22
    #     export vrf default map 44 allow-vpn
    #     export vrf allow-vpn
    #     maximum routes 900 22 reinstall 44
    #   address-family ipv6 unicast
    #     route-target import 554832:500

    - name: Parse the commands for provided configuration
      register: result
      cisco.nxos.nxos_vrf_address_family:
        running_config: "{{ lookup('file', '_parsed.cfg') }}"
        state: parsed

    # Task Output:
    # ------------
    # parsed:
    #   - name: VRF1
    #     address_families:
    #       - afi: ipv4
    #         safi: unicast
    #         route_target:
    #           - import: 64512:200
    #           - export: 64512:200
    #         export:
    #           - map: "22"
    #           - vrf:
    #               allow_vpn: true
    #               map_import: "44"
    #           - vrf:
    #               allow_vpn: true
    #         maximum:
    #           max_routes: 900
    #           max_route_options:
    #             threshold:
    #               threshold_value: 22
    #               reinstall_threshold: 44
    #       - afi: ipv6
    #         safi: unicast
    #         route_target:
    #           - import: 554832:500



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
                      <span style="color: purple">list</span>
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
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
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
                <td>when <em>state</em> is <code>merged</code>, <code>replaced</code>, <code>overridden</code>, <code>deleted</code> or <code>purged</code></td>
                <td>
                            <div>The set of commands pushed to the remote device.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf context management&#x27;, &#x27;address-family ipv4 unicast&#x27;, &#x27;maximum routes 500 60 reinstall 80&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>gathered</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
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
                      <span style="color: purple">list</span>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;vrf context test1&#x27;, &#x27;address-family ipv6 unicast&#x27;, &#x27;route-target export 65512:200&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Vinay Mulugund (@roverflow)
