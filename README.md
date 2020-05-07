

# Cisco NX-OS Collection
[![CI](https://zuul-ci.org/gated.svg)](https://dashboard.zuul.ansible.com/t/ansible/project/github.com/ansible-collections/cisco.nxos) <!--[![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/vyos)](https://codecov.io/gh/ansible-collections/cisco.nxos)-->

The Ansible Cisco NX-OS collection includes a variety of Ansible content to help automate the management of Cisco NX-OS network appliances.

The Cisco NX-OS connection plugins combined with Cisco NX-OS resource modules aligns the Cisco NX-OS experience with the other core networking platforms supported by Ansible.

This collection has been tested against Cisco NX-OS 7.0(3)I5(1).

### Supported connections
The Cisco NX-OS collection supports ``network_cli``  and ``httpapi`` connections.

## Included content

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
