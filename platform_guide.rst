.. _nxos_platform_options:

***************************************
NXOS Platform Options
***************************************

The `Cisco NXOS <https://galaxy.ansible.com/ui/repo/published/cisco/nxos>`_ supports multiple connections. This page offers details on how each connection works in Ansible and how to use it.

.. contents::
  :local:

Connections available
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                    CLI                                         NX-API
    ====================  ==========================================  =========================
    Protocol              SSH                                         HTTP(S)

    Credentials           uses SSH keys / SSH-agent if present        uses HTTPS certificates if
                                                                      present
                          accepts ``-u myuser -k`` if using password

    Indirect Access       by a bastion (jump host)                    by a web proxy

    Connection Settings   ``ansible_connection:``                     ``ansible_connection:``
                            ``ansible.netcommon.network_cli``             ``ansible.netcommon.httpapi``

    Enable Mode           supported: use ``ansible_become: true``     not supported by NX-API
                          with ``ansible_become_method: enable``
                          and ``ansible_become_password:``

    Returned Data Format  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================


Using CLI in Ansible
====================

Example CLI ``group_vars/nxos.yml``
-----------------------------------

.. code-block:: yaml

   ansible_connection: ansible.netcommon.network_cli
   ansible_network_os: cisco.nxos.nxos
   ansible_user: myuser
   ansible_password: !vault...
   ansible_become: true
   ansible_become_method: enable
   ansible_become_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- If you are using SSH keys (including an ssh-agent) you can remove the ``ansible_password`` configuration.
- If you are accessing your host directly (not through a bastion/jump host) you can remove the ``ansible_ssh_common_args`` configuration.
- If you are accessing your host through a bastion/jump host, you cannot include your SSH password in the ``ProxyCommand`` directive. To prevent secrets from leaking out (for example in ``ps`` output), SSH does not support providing passwords through environment variables.

Note
-----

When using ``ansible_connection: ansible.netcommon.network_cli``, the ``ansible_user`` must have permissions to execute the ``terminal length 0`` and ``terminal width 511`` commands on the target device.

Example CLI task
----------------

.. code-block:: yaml

   - name: Backup current switch config (nxos)
     cisco.nxos.nxos_config:
       backup: yes
     register: backup_nxos_location
     when: ansible_network_os == 'cisco.nxos.nxos'



Using NX-API in Ansible
=======================

Enabling NX-API
---------------

Before you can use NX-API to connect to a switch, you must enable NX-API. To enable NX-API on a new switch through Ansible, use the ``nxos_nxapi`` module through the CLI connection. Set up group_vars/nxos.yml just like in the CLI example above, then run a playbook task like this:

.. code-block:: yaml

   - name: Enable NX-API
      cisco.nxos.nxos_nxapi:
          enable_http: yes
          enable_https: yes
      when: ansible_network_os == 'cisco.nxos.nxos'

To find out more about the options for enabling HTTP/HTTPS and local http see the :ref:`nxos_nxapi <nxos_nxapi_module>` module documentation.

Once NX-API is enabled, change your ``group_vars/nxos.yml`` to use the NX-API connection.

Example NX-API ``group_vars/nxos.yml``
--------------------------------------

.. code-block:: yaml

   ansible_connection: ansible.netcommon.httpapi
   ansible_network_os: cisco.nxos.nxos
   ansible_user: myuser
   ansible_password: !vault...
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- If you are accessing your host directly (not through a web proxy) you can remove the ``proxy_env`` configuration.
- If you are accessing your host through a web proxy using ``https``, change ``http_proxy`` to ``https_proxy``.


Example NX-API task
-------------------

.. code-block:: yaml

   - name: Backup current switch config (nxos)
     cisco.nxos.nxos_config:
       backup: yes
     register: backup_nxos_location
     environment: "{{ proxy_env }}"
     when: ansible_network_os == 'cisco.nxos.nxos'

In this example the ``proxy_env`` variable defined in ``group_vars`` gets passed to the ``environment`` option of the module used in the task.

Warning
--------
Never store passwords in plain text. We recommend using SSH keys to authenticate SSH connections. Ansible supports ssh-agent to manage your SSH keys. If you must use passwords to authenticate SSH connections, we recommend encrypting them with Ansible Vault.

Cisco Nexus platform support matrix
===================================

The following platforms and software versions have been certified by Cisco to work with this version of Ansible.

.. table:: Platform / Software Minimum Requirements
     :align: center

     ===================  =====================
     Supported Platforms  Minimum NX-OS Version
     ===================  =====================
     Cisco Nexus N3k      7.0(3)I2(5) and later
     Cisco Nexus N9k      7.0(3)I2(5) and later
     Cisco Nexus N5k      7.3(0)N1(1) and later
     Cisco Nexus N6k      7.3(0)N1(1) and later
     Cisco Nexus N7k      7.3(0)D1(1) and later
     Cisco Nexus MDS      8.4(1) and later (Please see individual module documentation for compatibility)
     ===================  =====================

.. table:: Platform Models
     :align: center

     ========  ==============================================
     Platform  Description
     ========  ==============================================
     N3k       Support includes N30xx, N31xx and N35xx models
     N5k       Support includes all N5xxx models
     N6k       Support includes all N6xxx models
     N7k       Support includes all N7xxx models
     N9k       Support includes all N9xxx models
     MDS       Support includes all MDS 9xxx models
     ========  ==============================================

Notes
-----

`Setting Timeout Option <https://docs.ansible.com/ansible/latest/network/getting_started/network_connection_options.html#timeout-options>`_
