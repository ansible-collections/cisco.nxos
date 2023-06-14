===================================
Cisco Nxos Collection Release Notes
===================================

.. contents:: Topics


v4.4.0
======

Minor Changes
-------------

- nxos_user - Add support for hashed passwords. (https://github.com/ansible-collections/cisco.nxos/issues/370).

Bugfixes
--------

- l3_interfaces - Append tag when updating IP address with state replaced (https://github.com/ansible-collections/cisco.nxos/issues/678).
- ntp_global - Fix incorrect handling of prefer option (https://github.com/ansible-collections/cisco.nxos/issues/670).
- nxos_banner - Add support for a custom multiline delimiter
- nxos_facts - Fix missing SVI facts (https://github.com/ansible-collections/cisco.nxos/issues/440).
- terminal - attempt privilege escalation only when prompt does not end with #

Documentation Changes
---------------------

- Fix docs of static-routes resource module.
- nxos_interfaces - Fixed module documentation and examples.
- nxos_l2_interfaces - Fixed module documentation and examples.
- nxos_l3_interfaces - Fixed module documentation and examples.

v4.3.0
======

Release Summary
---------------

Re-releasing v4.2.0 of this collection since the previously build failed to upload in Automation Hub.

v4.2.0
======

Minor Changes
-------------

- `nxos_route_maps` - add support for 'set ip next-hop <>' command in route-maps
- `nxos_vxlan_vtep` - add support for 'advertise virtual-rmac' command under nve interface

Bugfixes
--------

- `bgp` - Fix parsing remote-as for Nexus 3K (https://github.com/ansible-collections/cisco.nxos/issues/653).
- `facts` - Attempt to execute json output commands with | json-pretty first and fall back to | json if unsupported. This is a temporary workaround until https://github.com/ansible/pylibssh/issues/208 is fixed.
- `interfaces` - Correctly enable/disable VLAN interfaces (https://github.com/ansible-collections/cisco.nxos/issues/539).
- `route_maps` - resolve route-map description parameter idempotency
- `snmp_server` - fix community option to produce proper configuration with ipv4acl and ipv6acl.

v4.1.0
======

Minor Changes
-------------

- `nxos_acls` - Support ICMPv6 option. Please refer to module doc for all new options (https://github.com/ansible-collections/cisco.nxos/issues/624).
- `nxos_facts` - Update facts gathering logic to ensure that `gather_network_resources: all` does not fail for NX-OS on MDS switches.
- `nxos_l2_interfaces` - Add new mode dot1q-tunnel (https://github.com/ansible-collections/cisco.nxos/issues/600).

Bugfixes
--------

- `nxos_acls` - Fix how IPv6 prefixes are converted to hosts (https://github.com/ansible-collections/cisco.nxos/issues/623).
- `nxos_file_copy` - stop prepending redundant bootflash: to remote file names
- nxos_acls - Detect duplicate ACE error message from CLI and fail (https://github.com/ansible-collections/cisco.nxos/issues/611).
- nxos_command - Run & evaluate commands at least once even when retries is set to 0 (https://github.com/ansible-collections/cisco.nxos/issues/607).

v4.0.1
======

Bugfixes
--------

- `nxos_acls` - Parse ICMP echo-reply and echo options correctly (https://github.com/ansible-collections/cisco.nxos/issues/583).
- `nxos_acls` - Parse ICMP port-unreachable and unreachable options correctly (https://github.com/ansible-collections/cisco.nxos/issues/529).
- `nxos_acls` - Parse port-protocol options with hypenated names correctly (https://github.com/ansible-collections/cisco.nxos/issues/557).

v4.0.0
======

Major Changes
-------------

- Please use either of the following connection types - network_cli, httpapi or netconf.
- This release drops support for `connection: local` and provider dictionary.

Removed Features (previously deprecated)
----------------------------------------

- This release removes the following deprecated plugins that have reached their end-of-life.
- nxos_acl
- nxos_acl_interface
- nxos_interface
- nxos_interface_ospf
- nxos_l2_interface
- nxos_l3_interface
- nxos_linkagg
- nxos_lldp
- nxos_ospf
- nxos_ospf_vrf
- nxos_smu
- nxos_static_route
- nxos_vlan

v3.2.0
======

Minor Changes
-------------

- `nxos_l3_interfaces` - Add support for toggling ipv6 redirects (https://github.com/ansible-collections/cisco.nxos/issues/569).

Bugfixes
--------

- `nxos_telemetry` - Allow destination-group & sensor-group id to be strings.
- `nxos_telemetry` - Allow sensor-group paths to be generated without additional properties.

v3.1.2
======

Bugfixes
--------

- `nxos_facts` - Fixes parsing of module info json data when TABLE_modinfo entry is a list (https://github.com/ansible-collections/cisco.nxos/issues/559).

v3.1.1
======

Bugfixes
--------

- Fix issue with modules related to OSPF interfaces failing when the target NXOS device has subinterfaces.

v3.1.0
======

Minor Changes
-------------

- `nxos_snmp_server` - Add support for localizedV2key (https://github.com/ansible-collections/cisco.nxos/issues/415).
- `nxos_snmp_server` - Add support for sha-256 based based user authentication.

Bugfixes
--------

- `nxos_file_copy` - Skip `vrf` when running against MDS switches (https://github.com/ansible-collections/cisco.nxos/issues/508).
- `nxos_interfaces` - Enable all virtual interfaces with `enabled` set to True (https://github.com/ansible-collections/cisco.nxos/issues/335).
- `nxos_ntp_global` - Ensure idempotence for aliased keys (https://github.com/ansible-collections/cisco.nxos/issues/484).
- `nxos_snmp_server` - Fix typo for traps link cisco-xcvr-mon-status-chg.

Documentation Changes
---------------------

- Updated documentation in nxos_snmp_server, nxos_ntp_global and nxos_logging_global modules to reflect which options are unsupported on MDS switches.

v3.0.0
======

Major Changes
-------------

- The minimum required ansible.netcommon version has been bumped to v2.6.1.
- Updated base plugin references to ansible.netcommon.
- `nxos_facts` - change default gather_subset to `min` from `!config` (https://github.com/ansible-collections/cisco.nxos/issues/418).
- nxos_file_copy has been rewritten as a module. This change also removes the dependency on pexpect for file_pull operation. Since this now uses AnsibleModule class for argspec validation, the validation messages will be slighlty different. Expect changes in the return payload in some cases. All functionality remains unchanged.

Minor Changes
-------------

- `nxos_snmp_server` - add support for BGP, OSPF and OSPFv3 traps.

Bugfixes
--------

- `nxos_lag_interfaces` - Fix KeyError with state overridden when port-channel has no members (https://github.com/ansible-collections/cisco.nxos/issues/452).
- `nxos_ntp_global` - correctly propagate CLI failure for non-existent auth keys (https://github.com/ansible-collections/cisco.nxos/issues/467).
- `nxos_snmp_server` - Properly handle corner cases for snmp-server user (https://github.com/ansible-collections/cisco.nxos/issues/454).
- `snmp_server` - Snmp contact/location and location were not gathered if containing whitespaces.

v2.9.1
======

Bugfixes
--------

- Fix action plugin redirection to make module defaults work properly.
- Fix for nxos_vlans issue (https://github.com/ansible-collections/cisco.nxos/issues/425).
- `nxos_ntp_global` - Aliased `vrf` to `use_vrf` wherever applicable to maintain consistency with models for other platforms.
- nxos_snmp_server - Add alias for community (https://github.com/ansible-collections/cisco.nxos/issues/433)

Documentation Changes
---------------------

- Added notes in module docs to indicate supportability for Cisco MDS.

v2.9.0
======

Minor Changes
-------------

- Add nxos_hostname resource module.

Bugfixes
--------

- `nxos_bgp_address_family` -  Add hmm as valid option for redistribute protocol (https://github.com/ansible-collections/cisco.nxos/issues/385).
- `nxos_snmp_server` - Fix rendering context command (https://github.com/ansible-collections/cisco.nxos/issues/406).

New Modules
-----------

- nxos_hostname - Hostname resource module.

v2.8.2
======

Release Summary
---------------

The v2.8.1 of the cisco.nxos collection is not available on Ansible Automation Hub. Please download and use v2.8.2 which also contains an additional bug fix.

Bugfixes
--------

- `nxos_ntp_global` - In some cases, there is an extra whitespace in the source-interface line. This patch accounts for this behaviour in config (https://github.com/ansible-collections/cisco.nxos/issues/399).

v2.8.1
======

Bugfixes
--------

- nxos_acls - Fix incorrect parsing of remarks if it has 'ip/ipv6 access-list' in it.

v2.8.0
======

Minor Changes
-------------

- Add nxos_snmp_server resource module.

Deprecated Features
-------------------

- Deprecated nxos_snmp_community module.
- Deprecated nxos_snmp_contact module.
- Deprecated nxos_snmp_host module.
- Deprecated nxos_snmp_location module.
- Deprecated nxos_snmp_traps module.
- Deprecated nxos_snmp_user module.

New Modules
-----------

- nxos_snmp_server - SNMP Server resource module.

v2.7.1
======

Bugfixes
--------

- `nxos_acls` - Updating an existing ACE can only be done with states replaced or overridden. Using state merged will result in a failure.
- `nxos_logging_global` - Fix vlan_mgr not being gathered in facts (https://github.com/ansible-collections/cisco.nxos/issues/380).
- `nxos_vlans` - Fallback to json when json-pretty is not supported (https://github.com/ansible-collections/cisco.nxos/issues/377).

v2.7.0
======

Minor Changes
-------------

- `nxos_telemetry` - Add support for state gathered

Documentation Changes
---------------------

- Update README with information regarding MDS module testing.

v2.6.0
======

Minor Changes
-------------

- Add nxos_ntp_global module.

Deprecated Features
-------------------

- Deprecated `nxos_ntp`, `nxos_ntp_options`, `nxos_ntp_auth` modules.

Bugfixes
--------

- `nxos_acls` - Fix traceback with 'port_protocol' range (https://github.com/ansible-collections/cisco.nxos/issues/356)
- `nxos_facts` - Fix KeyError while gathering CDP neighbor facts (https://github.com/ansible-collections/cisco.nxos/issues/354).
- `nxos_ospf_interfaces` - Correctly sort interface names before rendering.
- `nxos_vlans` - switching to `| json-pretty` instead of `| json` as a workaround for the timeout issue with `libssh` (https://github.com/ansible/pylibssh/issues/208)

Documentation Changes
---------------------

- `ospf[v2, v3, _interfaces]` - Area ID should be in IP address format.

New Modules
-----------

- nxos_ntp_global - NTP Global resource module.

v2.5.1
======

Bugfixes
--------

- `nxos_facts` - Fix gathering CDP neighbor facts from certain N7Ks (https://github.com/ansible-collections/cisco.nxos/issues/329).
- `nxos_zone_zoneset` - zone member addition with smart zoning in an already existing zone should be a no-op (https://github.com/ansible-collections/cisco.nxos/issues/339).

Documentation Changes
---------------------

- Added notes in module docs to indicate supportability for Cisco MDS.

v2.5.0
======

Minor Changes
-------------

- Add nxos_logging_global resource module.

Deprecated Features
-------------------

- The nxos_logging module has been deprecated in favor of the new nxos_logging_global resource module and will be removed in a release after '2023-08-01'.

Bugfixes
--------

- Convert vlan lists to ranges in nxos_l2_interfaces (https://github.com/ansible-collections/cisco.nxos/issues/95).
- Do not expand direction 'both' into 'import' and 'export' for Nexus 9000 platforms (https://github.com/ansible-collections/cisco.nxos/issues/303).
- Prevent traceback when parsing unexpected line in nxos_static_routes.

Documentation Changes
---------------------

- Broken link in documentation fixed.

New Modules
-----------

- nxos_logging_global - Logging resource module.

v2.4.0
======

Minor Changes
-------------

- Add `advertise_l2vpn_evpn` option in `nxos_bgp_address_family` module (https://github.com/ansible-collections/cisco.nxos/issues/302).
- Add `nxos_prefix_lists` resource module.

Bugfixes
--------

- Render neighbor peer_type command correctly (https://github.com/ansible-collections/cisco.nxos/issues/308).

New Modules
-----------

- nxos_prefix_lists - Prefix-Lists resource module.

v2.3.0
======

Minor Changes
-------------

- Add `default_passive_interface` option in `nxos_ospf_interfaces`.
- Add a netconf subplugin to make netconf_* modules work with older NX-OS versions (https://github.com/ansible-collections/ansible.netcommon/issues/252).

Bugfixes
--------

- Fix how `send_community` attribute is handled in `nxos_bgp_neighbor_address_family` (https://github.com/ansible-collections/cisco.nxos/issues/281).
- Make `passive_interface` work properly when set to False.

New Plugins
-----------

Netconf
~~~~~~~

- nxos - Use nxos netconf plugin to run netconf commands on Cisco NX-OS platform.

v2.2.0
======

Minor Changes
-------------

- Add nxos_route_maps resource module.
- Add support for ansible_network_resources key allows to fetch the available resources for a platform (https://github.com/ansible-collections/cisco.nxos/issues/268).

New Modules
-----------

- nxos_route_maps - Route Maps resource module.

v2.1.1
======

Bugfixes
--------

- For versions >=2.1.0, this collection requires ansible.netcommon >=2.0.1.
- Re-releasing this collection with ansible.netcommon dependency requirements updated.

v2.1.0
======

Minor Changes
-------------

- Add support for state purged in nxos_interfaces.

Security Fixes
--------------

- Properly mask values of sensitive keys in module result.

Bugfixes
--------

- Allow commands to be properly generated with Jinja2 2.10.3 (workaround for https://github.com/pallets/jinja/issues/710).
- Allow integer values to be set for dscp key (https://github.com/ansible-collections/cisco.nxos/issues/253).
- Do not fail when parsing non rule entries in access-list config (https://github.com/ansible-collections/cisco.nxos/issues/262).

v2.0.0
======

Major Changes
-------------

- Please refer to ansible.netcommon `changelog <https://github.com/ansible-collections/ansible.netcommon/blob/main/changelogs/CHANGELOG.rst#ansible-netcommon-collection-release-notes>`_ for more details.
- Requires ansible.netcommon v2.0.0+ to support `ansible_network_single_user_mode` and `ansible_network_import_modules`.

Minor Changes
-------------

- Add bfd option for neighbors (https://github.com/ansible-collections/cisco.nxos/issues/241).
- Add hello_interval_ms option in nxos_pim_interface module to support sub-second intervals (https://github.com/ansible-collections/cisco.nxos/issues/226).
- Add nxos_bgp_address_family Resource Module.
- Add nxos_bgp_neighbor_address_family Resource Module.
- Add support df_bit and size option for nxos_ping (https://github.com/ansible-collections/cisco.nxos/pull/237).
- Adds support for `single_user_mode` command output caching.
- Move nxos_config idempotent warning message with the task response under `warnings` key if `changed` is `True`

Deprecated Features
-------------------

- Deprecated nxos_bgp_af in favour of nxos_bgp_address_family resource module.
- Deprecated nxos_bgp_neighbor_af in favour of nxos_bgp_neighbor_address_family resource module.

Bugfixes
--------

- Fail gracefully when BGP is already configured with a different ASN when states merged or replaced is used.
- Fixes to nxos_logging, nxos_igmp_snooping, nxos_l3_interfaces, nxos_ospf_interfaces and nxos_static_routes to conform with latest CLI behaviour.
- Properly configure neighbor timers and shutdown state (https://github.com/ansible-collections/cisco.nxos/issues/240).

New Modules
-----------

- nxos_bgp_address_family - BGP Address Family resource module.
- nxos_bgp_neighbor_address_family - BGP Neighbor Address Family resource module.

v1.4.0
======

Minor Changes
-------------

- Add `echo_request` option for ICMP.
- Add nxos_bgp_global resource module.

Deprecated Features
-------------------

- Deprecated `nxos_bgp` and `nxos_bgp_neighbor` modules in favor of `nxos_bgp_global` resource module.

Security Fixes
--------------

- Enable no_log for sensitive parameters in argspec.

Bugfixes
--------

- Add support for interfaces in mode 'fabricpath' to l2_interfaces (https://github.com/ansible-collections/cisco.nxos/issues/220).
- Allow enabling `fabric forwarding` feature through nxos_feature (https://github.com/ansible-collections/cisco.nxos/issues/213).
- Allow tag updates with state replaced (https://github.com/ansible-collections/cisco.nxos/issues/197).
- Fixes traceback while parsing power supply info in nxos_facts for newer NX-OS releases (https://github.com/ansible-collections/cisco.nxos/issues/192).
- Handle domain-name properly with vrf contexts (https://github.com/ansible-collections/cisco.nxos/issues/234).
- Parse interface contexts properly (https://github.com/ansible-collections/cisco.nxos/issues/195).
- Properly handle partial matches in community string (https://github.com/ansible-collections/cisco.nxos/issues/203).
- Update argspecs with default value for parameters.
- Update docs to clarify the idemptonecy releated caveat and add it in the output warnings (https://github.com/ansible-collections/ansible.netcommon/pull/189)
- config replace is actually supported for devices other than N9K and hence we should not fail, and instead let the device handle it (https://github.com/ansible-collections/cisco.nxos/issues/215).

Documentation Changes
---------------------

- Fix error in ``host_reachability`` parameter's example where a default value is used, which the ``host_reachability`` parameter does not support. Improve descriptions of some parameters to be more explicit. Correct spelling and grammar where errors were noticed.

New Modules
-----------

- nxos_bgp_global - BGP Global resource module.

v1.3.1
======

Bugfixes
--------

- Add version key to galaxy.yaml to work around ansible-galaxy bug
- Allow nxos_user to run with MDS (https://github.com/ansible-collections/cisco.nxos/issues/163).
- Fix for nxos_lag_interfaces issue (https://github.com/ansible-collections/cisco.nxos/pull/194).
- Make sure that the OSPF modules work properly when process_id is a string (https://github.com/ansible-collections/cisco.nxos/issues/198).

v1.3.0
======

Minor Changes
-------------

- Add nxos_ospf_interfaces resource module.

Deprecated Features
-------------------

- Deprecated `nxos_interface_ospf` in favor of `nxos_ospf_interfaces` Resource Module.

Bugfixes
--------

- Allow `fex-fabric` option for mode key (https://github.com/ansible-collections/cisco.nxos/issues/166).
- Fixes for nxos rpm issue (https://github.com/ansible-collections/cisco.nxos/pull/173).
- Update regex to accept the platform "N77" as supporting fabricpath.
- Vlan config diff was not removing default values

New Modules
-----------

- nxos_ospf_interfaces - OSPF Interfaces Resource Module.

v1.2.0
======

Minor Changes
-------------

- Add nxos_ospfv3 module.
- Allow other transfer protocols than scp to pull files from a NXOS device in nxos_file_copy module. sftp, http, https, tftp and ftp can be choosen as a transfer protocol, when the file_pull parameter is true..

Deprecated Features
-------------------

- Deprecated `nxos_smu` in favour of `nxos_rpm` module.
- The `nxos_ospf_vrf` module is deprecated by `nxos_ospfv2` and `nxos_ospfv3` Resource Modules.

Bugfixes
--------

- Correctly parse facts for lacp interfaces mode information (https://github.com/ansible-collections/cisco.nxos/pull/164).
- Fix for nxos smu issue (https://github.com/ansible-collections/cisco.nxos/pull/160).
- Fix regex for parsing configuration in nxos_lag_interfaces.
- Fix regexes in nxos_acl_interfaces facts and some code cleanup (https://github.com/ansible-collections/cisco.nxos/issues/149).
- Fix rendering of `log-adjacency-changes` commands.
- Preserve whitespaces in banner text (https://github.com/ansible-collections/cisco.nxos/pull/146).

New Modules
-----------

- nxos_ospfv3 - OSPFv3 resource module

v1.1.0
======

Minor Changes
-------------

- Add N9K multisite support(https://github.com/ansible-collections/cisco.nxos/pull/142)

Bugfixes
--------

- Allow facts round trip to work on nxos_vlans (https://github.com/ansible-collections/cisco.nxos/pull/141).

v1.0.2
======

Release Summary
---------------

Rereleased 1.0.1 with updated changelog.

v1.0.1
======

Minor Changes
-------------

- documentation - Use FQCN when refering to modules (https://github.com/ansible-collections/cisco.nxos/pull/116)

Bugfixes
--------

- Element type of `commands` key should be `raw` since it accepts both strings and dicts (https://github.com/ansible-collections/cisco.nxos/pull/126).
- Fix nxos_interfaces states replaced and overridden (https://github.com/ansible-collections/cisco.nxos/pull/102).
- Fixed force option in lag_interfaces.py (https://github.com/ansible-collections/cisco.nxos/pull/111).
- Make `src`, `backup` and `backup_options` in nxos_config work when module alias is used (https://github.com/ansible-collections/cisco.nxos/pull/121).
- Makes sure that docstring and argspec are in sync and removes sanity ignores (https://github.com/ansible-collections/cisco.nxos/pull/112).
- Update docs after sanity fixes to modules.
- nxos_user - do not fail when a custom role is used (https://github.com/ansible-collections/cisco.nxos/pull/130)

v1.0.0
======

New Plugins
-----------

Cliconf
~~~~~~~

- nxos - Use NX-OS cliconf to run commands on Cisco NX-OS platform

Httpapi
~~~~~~~

- nxos - Use NX-API to run commands on Cisco NX-OS platform

New Modules
-----------

- nxos_aaa_server - Manages AAA server global configuration.
- nxos_aaa_server_host - Manages AAA server host-specific configuration.
- nxos_acl - (deprecated, removed after 2022-06-01) Manages access list entries for ACLs.
- nxos_acl_interface - (deprecated, removed after 2022-06-01) Manages applying ACLs to interfaces.
- nxos_acl_interfaces - ACL interfaces resource module
- nxos_acls - ACLs resource module
- nxos_banner - Manage multiline banners on Cisco NXOS devices
- nxos_bfd_global - Bidirectional Forwarding Detection (BFD) global-level configuration
- nxos_bfd_interfaces - BFD interfaces resource module
- nxos_bgp - Manages BGP configuration.
- nxos_bgp_af - Manages BGP Address-family configuration.
- nxos_bgp_neighbor - Manages BGP neighbors configurations.
- nxos_bgp_neighbor_af - Manages BGP address-family's neighbors configuration.
- nxos_command - Run arbitrary command on Cisco NXOS devices
- nxos_config - Manage Cisco NXOS configuration sections
- nxos_evpn_global - Handles the EVPN control plane for VXLAN.
- nxos_evpn_vni - Manages Cisco EVPN VXLAN Network Identifier (VNI).
- nxos_facts - Gets facts about NX-OS switches
- nxos_feature - Manage features in NX-OS switches.
- nxos_file_copy - Copy a file to a remote NXOS device.
- nxos_gir - Trigger a graceful removal or insertion (GIR) of the switch.
- nxos_gir_profile_management - Create a maintenance-mode or normal-mode profile for GIR.
- nxos_hsrp - Manages HSRP configuration on NX-OS switches.
- nxos_hsrp_interfaces - HSRP interfaces resource module
- nxos_igmp - Manages IGMP global configuration.
- nxos_igmp_interface - Manages IGMP interface configuration.
- nxos_igmp_snooping - Manages IGMP snooping global configuration.
- nxos_install_os - Set boot options like boot, kickstart image and issu.
- nxos_interface - (deprecated, removed after 2022-06-01) Manages physical attributes of interfaces.
- nxos_interface_ospf - Manages configuration of an OSPF interface instance.
- nxos_interfaces - Interfaces resource module
- nxos_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco NXOS devices.
- nxos_l2_interfaces - L2 interfaces resource module
- nxos_l3_interface - (deprecated, removed after 2022-06-01) Manage L3 interfaces on Cisco NXOS network devices
- nxos_l3_interfaces - L3 interfaces resource module
- nxos_lacp - LACP resource module
- nxos_lacp_interfaces - LACP interfaces resource module
- nxos_lag_interfaces - LAG interfaces resource module
- nxos_linkagg - (deprecated, removed after 2022-06-01) Manage link aggregation groups on Cisco NXOS devices.
- nxos_lldp - (deprecated, removed after 2022-06-01) Manage LLDP configuration on Cisco NXOS network devices.
- nxos_lldp_global - LLDP resource module
- nxos_lldp_interfaces - LLDP interfaces resource module
- nxos_logging - Manage logging on network devices
- nxos_ntp - Manages core NTP configuration.
- nxos_ntp_auth - Manages NTP authentication.
- nxos_ntp_options - Manages NTP options.
- nxos_nxapi - Manage NXAPI configuration on an NXOS device.
- nxos_ospf - (deprecated, removed after 2022-06-01) Manages configuration of an ospf instance.
- nxos_ospf_vrf - Manages a VRF for an OSPF router.
- nxos_ospfv2 - OSPFv2 resource module
- nxos_overlay_global - Configures anycast gateway MAC of the switch.
- nxos_pim - Manages configuration of a PIM instance.
- nxos_pim_interface - Manages PIM interface configuration.
- nxos_pim_rp_address - Manages configuration of an PIM static RP address instance.
- nxos_ping - Tests reachability using ping from Nexus switch.
- nxos_reboot - Reboot a network device.
- nxos_rollback - Set a checkpoint or rollback to a checkpoint.
- nxos_rpm - Install patch or feature rpms on Cisco NX-OS devices.
- nxos_smu - Perform SMUs on Cisco NX-OS devices.
- nxos_snapshot - Manage snapshots of the running states of selected features.
- nxos_snmp_community - Manages SNMP community configs.
- nxos_snmp_contact - Manages SNMP contact info.
- nxos_snmp_host - Manages SNMP host configuration.
- nxos_snmp_location - Manages SNMP location information.
- nxos_snmp_traps - Manages SNMP traps.
- nxos_snmp_user - Manages SNMP users for monitoring.
- nxos_static_route - (deprecated, removed after 2022-06-01) Manages static route configuration
- nxos_static_routes - Static routes resource module
- nxos_system - Manage the system attributes on Cisco NXOS devices
- nxos_telemetry - TELEMETRY resource module
- nxos_udld - Manages UDLD global configuration params.
- nxos_udld_interface - Manages UDLD interface configuration params.
- nxos_user - Manage the collection of local users on Nexus devices
- nxos_vlan - (deprecated, removed after 2022-06-01) Manages VLAN resources and attributes.
- nxos_vlans - VLANs resource module
- nxos_vpc - Manages global VPC configuration
- nxos_vpc_interface - Manages interface VPC configuration
- nxos_vrf - Manages global VRF configuration.
- nxos_vrf_af - Manages VRF AF.
- nxos_vrf_interface - Manages interface specific VRF configuration.
- nxos_vrrp - Manages VRRP configuration on NX-OS switches.
- nxos_vtp_domain - Manages VTP domain configuration.
- nxos_vtp_password - Manages VTP password configuration.
- nxos_vtp_version - Manages VTP version configuration.
- nxos_vxlan_vtep - Manages VXLAN Network Virtualization Endpoint (NVE).
- nxos_vxlan_vtep_vni - Creates a Virtual Network Identifier member (VNI)

Storage
~~~~~~~

- nxos_devicealias - Configuration of device alias.
- nxos_vsan - Configuration of vsan.
- nxos_zone_zoneset - Configuration of zone/zoneset.
