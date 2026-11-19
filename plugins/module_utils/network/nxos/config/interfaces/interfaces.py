#
# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""


from ansible.module_utils.connection import ConnectionError as DeviceConnectionError
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import (
    Facts,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.interfaces import (
    InterfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
    search_system_default_switchport,
)


class Interfaces(ResourceModule):
    """
    The nxos_interfaces config class
    """

    def __init__(self, module):
        super(Interfaces, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="interfaces",
            tmplt=InterfacesTemplate(),
        )
        self.parsers = [
            "description",
            "speed",
            "mtu",
            "duplex",
            "ip_forward",
            "fabric_forwarding_anycast_gateway",
            "mac_address",
            "logging.link_status",
            "logging.trunk_status",
            "snmp.trap.link_status",
            "service_policy.input",
            "service_policy.output",
            "service_policy.type_options.qos.input",
            "service_policy.type_options.qos.output",
            "service_policy.type_options.queuing.input",
            "service_policy.type_options.queuing.output",
        ]
        self._admin_states = None
        if self.state not in ["parsed", "rendered"]:
            self.defaults = self.get_interface_defaults()
        else:
            # For parsed/rendered state, we assume defaults
            self.defaults = {
                "default_mode": "layer3",
                "L2_enabled": True,
            }

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def get_switchport_defaults(self):
        """Wrapper method for `_connection.get()`
        This method exists solely to allow the unit test framework to mock device connection calls.
        """
        return self._connection.get(
            "show running-config all | incl 'system default switchport'",
        )

    @staticmethod
    def _parse_admin_states(data):
        """Read the 'interface', 'shutdown' and 'no shutdown' lines of the 'all' view.

        :rtype: dict
        :returns: lowercase interface name -> True (up) or False (shut)
        """
        states = {}
        name = None
        for line in data.splitlines() if isinstance(data, str) else []:
            line = line.strip()
            if line.startswith("interface "):
                name = line.split()[1].lower()
            elif name and line in ("shutdown", "no shutdown"):
                states[name] = line == "no shutdown"
        return states

    def get_admin_states(self):
        """The admin state of every interface, read from the 'all' view.

        The plain running config leaves out the admin state of an interface that is in
        its default state, the 'all' view always shows 'shutdown' or 'no shutdown'.
        The command is only run when it is needed and the result is kept for the run.
        If the device does not take the command, the admin state of the interfaces is unknown
        and the module goes on without it, with a warning.
        This method exists solely to allow the unit test framework to mock device connection calls.

        :rtype: dict
        :returns: lowercase interface name -> True (up) or False (shut)
        """
        if self._admin_states is None:
            try:
                data = self._connection.get(
                    'show running-config all | include "^interface |^  shutdown$|^  no shutdown$"',
                )
            except DeviceConnectionError as exc:
                self._module.warn(
                    "Could not read the admin state of the interfaces from 'show running-config all', "
                    "it is unknown for the interfaces that show no shutdown line: %s" % exc,
                )
                data = None
            self._admin_states = self._parse_admin_states(data)
        return self._admin_states

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = {entry["name"]: entry for entry in self.want}
        haved = {entry["name"]: entry for entry in self.have}

        for each in wantd, haved:
            self.normalize_interface_names(each)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {k: v for k, v in haved.items() if k in wantd or not wantd}
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in haved.items():
                if k not in wantd:
                    self._compare(want={}, have=have)

        if self.state == "purged":
            self.purge(wantd, haved)
        else:
            for k, want in wantd.items():
                self._compare(want=want, have=haved.pop(k, {}))

    @staticmethod
    def _is_up_by_default(name):
        """Whether the interface is admin-up unless a 'shutdown' line says otherwise.

        That is the case for loopbacks, mgmt0 and port-channels. Subinterfaces of
        a port-channel are not included, they have their own admin state.
        Only used for an interface of the configuration that the 'all' view does not list.
        """
        lowered = name.lower()
        if "loopback" in lowered:
            return True
        return lowered.startswith(("mgmt", "port-channel")) and "." not in lowered

    def _changes_mode(self, want, have):
        """Whether the interface changes between L2 and L3 in this run."""
        want_mode = want.get("mode")
        return want_mode is not None and want_mode != have.get(
            "mode",
            self.defaults.get("default_mode"),
        )

    def _admin_state(self, want, have):
        """The admin state that an existing interface of the configuration has now.

        This is the one place that defines it. An interface that is not in its default
        admin state has a 'shutdown' or 'no shutdown' line in the plain running config. An
        interface in its default admin state has none, the 'all' view always shows it. That is
        the case for ports, loopbacks, mgmt0 and port-channels alike.

        An interface that does not exist yet has no admin state, and neither has one that
        changes between L2 and L3 in this run, it then gets the default admin state of the
        new mode. The admin state of an interface that the 'all' view does not list is unknown,
        except for a loopback, mgmt0 or port-channel (up by default), that is kept from the
        earlier fixes so that the commands of existing playbooks stay as they were.

        :rtype: bool
        :returns: True (up), False (shut) or None (unknown)
        """
        enabled = have.get("enabled")
        if enabled is None and have and not self._changes_mode(want, have):
            name = have.get("name", "")
            enabled = self.get_admin_states().get(name.lower())
            if enabled is None and self._is_up_by_default(name):
                enabled = True
        return enabled

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
        populates the list of commands to be run by comparing
        the `want` and `have` data with the `parsers` defined
        for the Interfaces network resource.
        """
        begin = len(self.commands)
        self.compare(parsers=self.parsers, want=want, have=have)

        # Handle the 'enabled' state separately
        want_enabled = want.get("enabled")
        if want_enabled is not None:
            if want_enabled != self._admin_state(want, have):
                self.addcmd(want, "enabled", want_enabled)
        elif not want and self.state in ["overridden", "deleted"]:
            # An interface that is not in the configuration (overridden) or that is deleted is
            # only shut when its running config shows 'no shutdown', one that shows 'shutdown'
            # is shut already and must not get the command on every run. Its admin state is not
            # read from the 'all' view here, only the interfaces of the configuration use that.
            if have.get("enabled"):
                self.addcmd(have, "enabled", False)

        # Handle the 'mode' state separately
        want_mode = want.get("mode")
        # Only treat the platform-wide default as the interface's current mode
        # when the interface already exists in gathered facts. A brand-new
        # interface (empty `have`) has never had `switchport` / `no switchport`
        # entered, even if `system default switchport` would eventually apply.
        # Substituting the default in that case makes merged/replaced skip the
        # explicit command, which then breaks nxos_l2_interfaces
        # (`switchport mode ...` is rejected until `switchport` is entered).
        # `rendered` always has empty `have` and documents a layer3 default.
        if have or self.state == "rendered":
            have_mode = have.get("mode", self.defaults.get("default_mode"))
        else:
            have_mode = None
        if want_mode is not None:
            if want_mode != have_mode:
                if want_mode == "layer3":
                    self.addcmd(want, "mode", True)
                else:
                    if want:
                        self.addcmd(want, "mode", False)
                    elif have.get("mode"):  # can oly have layer2 as switchport no show cli
                        # handles deleted as want be blank and only
                        self.addcmd(have, "mode", False)
        elif not want and self.state == "deleted":
            if have.get("mode") and have_mode != self.defaults.get("default_mode"):
                no_cmd = True if self.defaults.get("default_mode") == "layer3" else False
                self.addcmd(have, "mode", no_cmd)

        # Handle 'negotiate_auto' separately because its default (enabled) does not
        # appear in running-config; only 'no negotiate auto' appears when disabled.
        # The base class compare() skips bool False vs None, so we own the full logic.
        want_negotiate = want.get("negotiate_auto")
        have_negotiate = have.get("negotiate_auto")
        if want_negotiate is not None:
            # Treat absent have as True (default is enabled, not shown in running-config)
            effective_have = have_negotiate if have_negotiate is not None else True
            if want_negotiate != effective_have:
                # False → emit "no negotiate auto"; True → emit "negotiate auto"
                self.addcmd(want, "negotiate_auto", not want_negotiate)
        elif self.state in ["replaced", "overridden"] or (not want and self.state == "deleted"):
            if have_negotiate is False:
                # Restore default: remove "no negotiate auto"
                self.addcmd(have, "negotiate_auto", False)

        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render(want or have, "name", False))

    def purge(self, wantd, haved):
        """Handle operation for purged state"""
        if wantd:
            for k, want in wantd.items():
                have = haved.pop(k, {})
                if have:
                    self.commands.append(self._tmplt.render(have, "name", True))

    def normalize_interface_names(self, param):
        if param:
            for _k, val in param.items():
                val["name"] = normalize_interface(val["name"])
        return param

    def get_interface_defaults(self):
        """Collect user-defined-default states for 'system default switchport'
        configurations. These configurations determine default L2/L3 modes
        and enabled/shutdown states. The default values for user-defined-default
        configurations may be different for legacy platforms.
        Notes:
        - L3 enabled default state is False on N9K,N7K,N3K but True for N5K,N6K
        - Changing L2-L3 modes may change the default enabled value.
        - '(no) system default switchport shutdown' only applies to L2 interfaces.
        Run through the gathered interfaces and tag their default enabled state.
        """
        interface_defs = {}
        switchport_data = self.get_switchport_defaults()

        # Layer 2/3 mode defaults
        default_mode = search_system_default_switchport(switchport_data)
        if default_mode:
            interface_defs["default_mode"] = "layer3" if default_mode.group(1) else "layer2"

        # Interface enabled state defaults
        default_enabled = search_system_default_switchport(switchport_data, shutdown=True)
        if default_enabled:
            interface_defs["L2_enabled"] = bool(default_enabled.group(1))

        return interface_defs
