

# Cisco NX-OS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.nxos) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/cisco.nxos)-->

The Ansible Cisco NX-OS collection includes a variety of Ansible content to help automate the management of Cisco NX-OS network appliances.

The Cisco NX-OS connection plugins combined with Cisco NX-OS resource modules aligns the Cisco NX-OS experience with the other core networking platforms supported by Ansible.

This collection has been tested against Cisco NX-OS 7.0(3)I5(1).

### Supported connections
The Cisco NX-OS collection supports ``network_cli``  and ``httpapi`` connections.

## Included content
<!--start collection content-->
## Cliconf plugins
Name | Description
--- | ---
[cisco.nxos.nxos](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos.rst)|Use nxos cliconf to run command on Cisco NX-OS platform
## Httpapi plugins
Name | Description
--- | ---
[cisco.nxos.nxos](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos.rst)|Use NX-API to run command on nxos platform
## Terminal plugins
Name | Description
--- | ---
## Modules
Name | Description
--- | ---
[cisco.nxos.nxos_aaa_server](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_aaa_server.rst)|Manages AAA server global configuration.
[cisco.nxos.nxos_aaa_server_host](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_aaa_server_host.rst)|Manages AAA server host-specific configuration.
[cisco.nxos.nxos_acl](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_acl.rst)|(deprecated, removed after 2022-06-01) Manages access list entries for ACLs.
[cisco.nxos.nxos_acl_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_acl_interface.rst)|(deprecated, removed after 2022-06-01) Manages applying ACLs to interfaces.
[cisco.nxos.nxos_acl_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_acl_interfaces.rst)|ACL interfaces resource module
[cisco.nxos.nxos_acls](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_acls.rst)|ACLs resource module
[cisco.nxos.nxos_banner](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_banner.rst)|Manage multiline banners on Cisco NXOS devices
[cisco.nxos.nxos_bfd_global](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bfd_global.rst)|Bidirectional Forwarding Detection (BFD) global-level configuration
[cisco.nxos.nxos_bfd_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bfd_interfaces.rst)|BFD interfaces resource module
[cisco.nxos.nxos_bgp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bgp.rst)|Manages BGP configuration.
[cisco.nxos.nxos_bgp_af](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bgp_af.rst)|Manages BGP Address-family configuration.
[cisco.nxos.nxos_bgp_neighbor](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bgp_neighbor.rst)|Manages BGP neighbors configurations.
[cisco.nxos.nxos_bgp_neighbor_af](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_bgp_neighbor_af.rst)|Manages BGP address-family's neighbors configuration.
[cisco.nxos.nxos_command](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_command.rst)|Run arbitrary command on Cisco NXOS devices
[cisco.nxos.nxos_config](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_config.rst)|Manage Cisco NXOS configuration sections
[cisco.nxos.nxos_devicealias](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_devicealias.rst)|Configuration of device alias.
[cisco.nxos.nxos_evpn_global](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_evpn_global.rst)|Handles the EVPN control plane for VXLAN.
[cisco.nxos.nxos_evpn_vni](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_evpn_vni.rst)|Manages Cisco EVPN VXLAN Network Identifier (VNI).
[cisco.nxos.nxos_facts](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_facts.rst)|Gets facts about NX-OS switches
[cisco.nxos.nxos_feature](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_feature.rst)|Manage features in NX-OS switches.
[cisco.nxos.nxos_file_copy](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_file_copy.rst)|Copy a file to a remote NXOS device.
[cisco.nxos.nxos_gir](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_gir.rst)|Trigger a graceful removal or insertion (GIR) of the switch.
[cisco.nxos.nxos_gir_profile_management](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_gir_profile_management.rst)|Create a maintenance-mode or normal-mode profile for GIR.
[cisco.nxos.nxos_hsrp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_hsrp.rst)|Manages HSRP configuration on NX-OS switches.
[cisco.nxos.nxos_hsrp_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_hsrp_interfaces.rst)|HSRP interfaces resource module
[cisco.nxos.nxos_igmp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_igmp.rst)|Manages IGMP global configuration.
[cisco.nxos.nxos_igmp_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_igmp_interface.rst)|Manages IGMP interface configuration.
[cisco.nxos.nxos_igmp_snooping](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_igmp_snooping.rst)|Manages IGMP snooping global configuration.
[cisco.nxos.nxos_install_os](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_install_os.rst)|Set boot options like boot, kickstart image and issu.
[cisco.nxos.nxos_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_interface.rst)|(deprecated, removed after 2022-06-01) Manages physical attributes of interfaces.
[cisco.nxos.nxos_interface_ospf](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_interface_ospf.rst)|Manages configuration of an OSPF interface instance.
[cisco.nxos.nxos_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_interfaces.rst)|Interfaces resource module
[cisco.nxos.nxos_l2_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_l2_interface.rst)|(deprecated, removed after 2022-06-01) Manage Layer-2 interface on Cisco NXOS devices.
[cisco.nxos.nxos_l2_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_l2_interfaces.rst)|L2 interfaces resource module
[cisco.nxos.nxos_l3_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_l3_interface.rst)|(deprecated, removed after 2022-06-01) Manage L3 interfaces on Cisco NXOS network devices
[cisco.nxos.nxos_l3_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_l3_interfaces.rst)|L3 interfaces resource module
[cisco.nxos.nxos_lacp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lacp.rst)|LACP resource module
[cisco.nxos.nxos_lacp_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lacp_interfaces.rst)|LACP interfaces resource module
[cisco.nxos.nxos_lag_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lag_interfaces.rst)|LAG interfaces resource module
[cisco.nxos.nxos_linkagg](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_linkagg.rst)|(deprecated, removed after 2022-06-01) Manage link aggregation groups on Cisco NXOS devices.
[cisco.nxos.nxos_lldp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lldp.rst)|(deprecated, removed after 2022-06-01) Manage LLDP configuration on Cisco NXOS network devices.
[cisco.nxos.nxos_lldp_global](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lldp_global.rst)|LLDP resource module
[cisco.nxos.nxos_lldp_interfaces](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_lldp_interfaces.rst)|LLDP interfaces resource module
[cisco.nxos.nxos_logging](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_logging.rst)|Manage logging on network devices
[cisco.nxos.nxos_ntp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ntp.rst)|Manages core NTP configuration.
[cisco.nxos.nxos_ntp_auth](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ntp_auth.rst)|Manages NTP authentication.
[cisco.nxos.nxos_ntp_options](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ntp_options.rst)|Manages NTP options.
[cisco.nxos.nxos_nxapi](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_nxapi.rst)|Manage NXAPI configuration on an NXOS device.
[cisco.nxos.nxos_ospf](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ospf.rst)|(deprecated, removed after 2022-06-01) Manages configuration of an ospf instance.
[cisco.nxos.nxos_ospf_vrf](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ospf_vrf.rst)|Manages a VRF for an OSPF router.
[cisco.nxos.nxos_ospfv2](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ospfv2.rst)|OSPFv2 resource module
[cisco.nxos.nxos_overlay_global](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_overlay_global.rst)|Configures anycast gateway MAC of the switch.
[cisco.nxos.nxos_pim](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_pim.rst)|Manages configuration of a PIM instance.
[cisco.nxos.nxos_pim_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_pim_interface.rst)|Manages PIM interface configuration.
[cisco.nxos.nxos_pim_rp_address](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_pim_rp_address.rst)|Manages configuration of an PIM static RP address instance.
[cisco.nxos.nxos_ping](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_ping.rst)|Tests reachability using ping from Nexus switch.
[cisco.nxos.nxos_reboot](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_reboot.rst)|Reboot a network device.
[cisco.nxos.nxos_rollback](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_rollback.rst)|Set a checkpoint or rollback to a checkpoint.
[cisco.nxos.nxos_rpm](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_rpm.rst)|Install patch or feature rpms on Cisco NX-OS devices.
[cisco.nxos.nxos_smu](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_smu.rst)|Perform SMUs on Cisco NX-OS devices.
[cisco.nxos.nxos_snapshot](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snapshot.rst)|Manage snapshots of the running states of selected features.
[cisco.nxos.nxos_snmp_community](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_community.rst)|Manages SNMP community configs.
[cisco.nxos.nxos_snmp_contact](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_contact.rst)|Manages SNMP contact info.
[cisco.nxos.nxos_snmp_host](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_host.rst)|Manages SNMP host configuration.
[cisco.nxos.nxos_snmp_location](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_location.rst)|Manages SNMP location information.
[cisco.nxos.nxos_snmp_traps](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_traps.rst)|Manages SNMP traps.
[cisco.nxos.nxos_snmp_user](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_snmp_user.rst)|Manages SNMP users for monitoring.
[cisco.nxos.nxos_static_route](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_static_route.rst)|(deprecated, removed after 2022-06-01) Manages static route configuration
[cisco.nxos.nxos_static_routes](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_static_routes.rst)|Static routes resource module
[cisco.nxos.nxos_system](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_system.rst)|Manage the system attributes on Cisco NXOS devices
[cisco.nxos.nxos_telemetry](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_telemetry.rst)|TELEMETRY resource module
[cisco.nxos.nxos_udld](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_udld.rst)|Manages UDLD global configuration params.
[cisco.nxos.nxos_udld_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_udld_interface.rst)|Manages UDLD interface configuration params.
[cisco.nxos.nxos_user](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_user.rst)|Manage the collection of local users on Nexus devices
[cisco.nxos.nxos_vlan](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vlan.rst)|(deprecated, removed after 2022-06-01) Manages VLAN resources and attributes.
[cisco.nxos.nxos_vlans](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vlans.rst)|VLANs resource module
[cisco.nxos.nxos_vpc](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vpc.rst)|Manages global VPC configuration
[cisco.nxos.nxos_vpc_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vpc_interface.rst)|Manages interface VPC configuration
[cisco.nxos.nxos_vrf](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vrf.rst)|Manages global VRF configuration.
[cisco.nxos.nxos_vrf_af](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vrf_af.rst)|Manages VRF AF.
[cisco.nxos.nxos_vrf_interface](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vrf_interface.rst)|Manages interface specific VRF configuration.
[cisco.nxos.nxos_vrrp](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vrrp.rst)|Manages VRRP configuration on NX-OS switches.
[cisco.nxos.nxos_vsan](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vsan.rst)|Configuration of vsan.
[cisco.nxos.nxos_vtp_domain](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vtp_domain.rst)|Manages VTP domain configuration.
[cisco.nxos.nxos_vtp_password](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vtp_password.rst)|Manages VTP password configuration.
[cisco.nxos.nxos_vtp_version](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vtp_version.rst)|Manages VTP version configuration.
[cisco.nxos.nxos_vxlan_vtep](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vxlan_vtep.rst)|Manages VXLAN Network Virtualization Endpoint (NVE).
[cisco.nxos.nxos_vxlan_vtep_vni](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_vxlan_vtep_vni.rst)|Creates a Virtual Network Identifier member (VNI)
[cisco.nxos.nxos_zone_zoneset](https://github.com/ansible-collections/nxos/blob/master/docs/cisco.nxos.nxos_zone_zoneset.rst)|Configuration of zone/zoneset.
<!--end collection content-->

Click the ``Content`` button to see the list of content included in this collection.

## Installing this collection

You can install the Cisco NX-OS collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install cisco.nxos

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: cisco.nxos
    version: 1.0.0
```
## Using this collection


This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Cisco NX-OS collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `cisco.nxos.nxos_l2_interfaces`.
The following example task replaces configuration changes in the existing configuration on a Cisco NX-OS network device, using the FQCN:

```yaml
---
  - name: Replace device configuration of specified L2 interfaces with provided configuration.
    cisco.nxos.nxos_l2_interfaces:
      config:
        - name: Ethernet1/1
          trunk:
            native_vlan: 20
            trunk_vlans: 5-10, 15
      state: replaced

```

Alternately, you can call modules by their short name if you list the `cisco.nxos` collection in the playbook's `collections`, as follows:

```yaml
---
- hosts: nxos01
  gather_facts: false
  connection: network_cli

  collections:
    - cisco.nxos

  tasks:
    - name: Merge provided configuration with device configuration.
      nxos_lacp_interfaces:
        config:
          - name: Ethernet1/3
            port_priority: 5
            rate: fast
        state: merged
```


### See Also:

* [Cisco NX-OS Platform Options](https://docs.ansible.com/ansible/latest/network/user_guide/platform_nxos.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

Ongoing development efforts and contributions to this collection are solely focused on enhancements to current resource modules, additional resource modules and enhancements to connection plugins.

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Cisco NX-OS collection repository](https://github.com/ansible-collections/cisco.nxos).

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Changelogs
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.