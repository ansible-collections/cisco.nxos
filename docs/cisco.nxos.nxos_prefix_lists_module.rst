.. _cisco.nxos.nxos_prefix_lists_module:


****************************
cisco.nxos.nxos_prefix_lists
****************************

**Prefix-Lists resource module.**


Version added: 2.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module manages prefix-lists configuration on devices running Cisco NX-OS.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
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
                        <div>A list of prefix-list configuration.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
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
                        <div>The Address Family Identifier (AFI) for the prefix-lists.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix_lists</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of prefix-list configurations.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Description of the prefix list</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>entries</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of configurations for the specified prefix-list</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>permit</li>
                                    <li>deny</li>
                        </ul>
                </td>
                <td>
                        <div>Prefix-List permit or deny.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eq</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Exact prefix length to be matched.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ge</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Minimum prefix length to be matched.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>le</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Maximum prefix length to be matched.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mask</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Explicit match mask.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>prefix</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP or IPv6 prefix in A.B.C.D/LEN or A:B::C:D/LEN format.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sequence</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Sequence Number.</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
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
                        <div>Name of the prefix-list.</div>
                </td>
            </tr>


            <tr>
                <td colspan="4">
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
                        <div>The value of this option should be the output received from the NX-OS device by executing the command <b>show running-config | section &#x27;^ip(.*</b> prefix-list&#x27;).</div>
                        <div>The state <em>parsed</em> reads the configuration from <code>running_config</code> option and transforms it into Ansible structured data as per the resource module&#x27;s argspec and the value is then returned in the <em>parsed</em> key within the result.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
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
                                    <li>parsed</li>
                                    <li>gathered</li>
                                    <li>rendered</li>
                        </ul>
                </td>
                <td>
                        <div>The state the configuration should be left in.</div>
                        <div>Refer to examples for more details.</div>
                        <div>With state <em>replaced</em>, for the listed prefix-lists, sequences that are in running-config but not in the task are negated.</div>
                        <div>With state <em>overridden</em>, all prefix-lists that are in running-config but not in the task are negated.</div>
                        <div>Please refer to examples for more details.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against NX-OS 9.3.6.
   - Unsupported for Cisco MDS
   - This module works with connection ``network_cli`` and ``httpapi``.



Examples
--------

.. code-block:: yaml

    # Using merged

    # Before state:
    # -------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # nxos-9k-rdo#

    - name: Merge the provided configuration with the existing running configuration
      cisco.nxos.nxos_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: AllowPrefix
                description: allows engineering IPv4 networks
                entries:
                  - sequence: 10
                    action: permit
                    prefix: 192.0.2.0/23
                    eq: 24
                  - sequence: 20
                    action: permit
                    prefix: 198.51.100.128/26
              - name: DenyPrefix
                description: denies lab IPv4 networks
                entries:
                  - sequence: 20
                    action: deny
                    prefix: 203.0.113.0/24
                    le: 25

          - afi: ipv6
            prefix_lists:
              - name: AllowIPv6Prefix
                description: allows engineering IPv6 networks
                entries:
                  - sequence: 8
                    action: permit
                    prefix: "2001:db8:400::/38"
                  - sequence: 20
                    action: permit
                    prefix: "2001:db8:8000::/35"
                    le: 37

    # Task output
    # -------------
    # before: []
    #
    # commands:
    #   - "ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks"
    #   - "ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38"
    #   - "ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37"
    #   - "ip prefix-list AllowPrefix description allows engineering IPv4 networks"
    #   - "ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24"
    #   - "ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26"
    #   - "ip prefix-list DenyPrefix description denies lab IPv4 networks"
    #   - "ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25"
    #
    # after:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix

    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    # Using replaced

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Replace prefix-lists configurations of listed prefix-lists with provided configurations
      cisco.nxos.nxos_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: AllowPrefix
                description: allows engineering IPv4 networks
                entries:
                  - sequence: 10
                    action: permit
                    prefix: 203.0.113.64/27

                  - sequence: 30
                    action: permit
                    prefix: 203.0.113.96/27
              - name: AllowPrefix2Stub
                description: allow other engineering IPv4 network
        state: replaced

    # Task output
    # -------------
    # before:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # commands:
    #   - "no ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24"
    #   - "ip prefix-list AllowPrefix seq 10 permit 203.0.113.64/27"
    #   - "ip prefix-list AllowPrefix seq 30 permit 203.0.113.96/27"
    #   - "no ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26"
    #   - "ip prefix-list AllowPrefix2Stub description allow other engineering IPv4 network"
    #
    # after:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 203.0.113.64/27
    #           - sequence: 30
    #             action: permit
    #             prefix: 203.0.113.96/27
    #          name: AllowPrefix
    #       - description: allow other engineering IPv4 network
    #         name: AllowPrefix2Stub
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 203.0.113.64/27
    # ip prefix-list AllowPrefix seq 30 permit 203.0.113.96/27
    # ip prefix-list AllowPrefix2Stub description allow other engineering IPv4 network
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    # Using overridden

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Override all prefix-lists configuration with provided configuration
      cisco.nxos.nxos_prefix_lists: &id003
        config:
          - afi: ipv4
            prefix_lists:
              - name: AllowPrefix
                description: allows engineering IPv4 networks
                entries:
                  - sequence: 10
                    action: permit
                    prefix: 203.0.113.64/27

                  - sequence: 30
                    action: permit
                    prefix: 203.0.113.96/27
              - name: AllowPrefix2Stub
                description: allow other engineering IPv4 network
        state: overridden

    # Task output
    # -------------
    # before:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # commands:
    #   - "no ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24"
    #   - "ip prefix-list AllowPrefix seq 10 permit 203.0.113.64/27"
    #   - "ip prefix-list AllowPrefix seq 30 permit 203.0.113.96/27"
    #   - "no ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26"
    #   - "ip prefix-list AllowPrefix2Stub description allow other engineering IPv4 network"
    #   - "no ip prefix-list DenyPrefix"
    #   - "no ipv6 prefix-list AllowIPv6Prefix"
    #
    # after:
    #   - afi: ipv4
    #     prefix_lists:
    #       - name: AllowPrefix
    #         description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 203.0.113.64/27
    #
    #           - sequence: 30
    #             action: permit
    #             prefix: 203.0.113.96/27
    #       - name: AllowPrefix2Stub
    #         description: allow other engineering IPv4 network
    #
    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 203.0.113.64/27
    # ip prefix-list AllowPrefix seq 30 permit 203.0.113.96/27
    # ip prefix-list AllowPrefix2Stub description allow other engineering IPv4 network

    # Using deleted to delete a all prefix lists for an AFI

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Delete all prefix-lists for an AFI
      cisco.nxos.nxos_prefix_lists:
        config:
          - afi: ipv4
        state: deleted
      register: result

    # Task output
    # -------------
    # before:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # commands:
    #   - "no ip prefix-list AllowPrefix"
    #   - "no ip prefix-list DenyPrefix"
    #
    # after:
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    # Using deleted to delete a single prefix-list

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Delete a single prefix-list
      cisco.nxos.nxos_prefix_lists:
        config:
          - afi: ipv4
            prefix_lists:
              - name: AllowPrefix
        state: deleted

    # Task output
    # -------------
    # before:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # commands:
    #   - "no ip prefix-list AllowPrefix"
    #
    # after:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    # Using deleted to delete all prefix-lists from the device

    # Before state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Delete all prefix-lists
      cisco.nxos.nxos_prefix_lists:
        state: deleted

    # Task output
    # -------------
    # before:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix
    #
    # commands:
    #   - "no ip prefix-list AllowPrefix"
    #   - "no ip prefix-list DenyPrefix"
    #   - "no ipv6 prefix-list AllowIPv6Prefix"
    #
    # after: []
    #
    # After state:
    # ------------
    # nxos-9k-rdo# show running-config | section 'ip(.*) prefix-list'
    # nxos-9k-rdo#

    # Using rendered

    - name: Render platform specific configuration lines with state rendered (without connecting to the device)
      cisco.nxos.nxos_prefix_lists: &id001
        config:
          - afi: ipv4
            prefix_lists:
              - name: AllowPrefix
                description: allows engineering IPv4 networks
                entries:
                  - sequence: 10
                    action: permit
                    prefix: 192.0.2.0/23
                    eq: 24
                  - sequence: 20
                    action: permit
                    prefix: 198.51.100.128/26
              - name: DenyPrefix
                description: denies lab IPv4 networks
                entries:
                  - sequence: 20
                    action: deny
                    prefix: 203.0.113.0/24
                    le: 25

          - afi: ipv6
            prefix_lists:
              - name: AllowIPv6Prefix
                description: allows engineering IPv6 networks
                entries:
                  - sequence: 8
                    action: permit
                    prefix: "2001:db8:400::/38"
                  - sequence: 20
                    action: permit
                    prefix: "2001:db8:8000::/35"
                    le: 37
        state: rendered

    # Task Output (redacted)
    # -----------------------
    # rendered:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix

    # Using parsed

    # parsed.cfg
    # ------------
    # ip prefix-list AllowPrefix description allows engineering IPv4 networks
    # ip prefix-list AllowPrefix seq 10 permit 192.0.2.0/23 eq 24
    # ip prefix-list AllowPrefix seq 20 permit 198.51.100.128/26
    # ip prefix-list DenyPrefix description denies lab IPv4 networks
    # ip prefix-list DenyPrefix seq 20 deny 203.0.113.0/24 le 25
    # ipv6 prefix-list AllowIPv6Prefix description allows engineering IPv6 networks
    # ipv6 prefix-list AllowIPv6Prefix seq 8 permit 2001:db8:400::/38
    # ipv6 prefix-list AllowIPv6Prefix seq 20 permit 2001:db8:8000::/35 le 37

    - name: Parse externally provided prefix-lists configuration
      register: result
      cisco.nxos.nxos_prefix_lists:
        running_config: "{{ lookup('file', './parsed.cfg') }}"
        state: parsed

    # Task output (redacted)
    # -----------------------
    # parsed:
    #   - afi: ipv4
    #     prefix_lists:
    #       - description: allows engineering IPv4 networks
    #         entries:
    #           - sequence: 10
    #             action: permit
    #             prefix: 192.0.2.0/23
    #             eq: 24
    #           - sequence: 20
    #             action: permit
    #             prefix: 198.51.100.128/26
    #         name: AllowPrefix
    #       - description: denies lab IPv4 networks
    #         entries:
    #           - sequence: 20
    #             action: deny
    #             prefix: 203.0.113.0/24
    #             le: 25
    #         name: DenyPrefix
    #
    #   - afi: ipv6
    #     prefix_lists:
    #       - description: allows engineering IPv6 networks
    #         entries:
    #           - sequence: 8
    #             action: permit
    #             prefix: "2001:db8:400::/38"
    #           - sequence: 20
    #             action: permit
    #             prefix: "2001:db8:8000::/35"
    #             le: 37
    #         name: AllowIPv6Prefix




Status
------


Authors
~~~~~~~

- Nilashish Chakraborty (@NilashishC)
