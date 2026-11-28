# -*- coding: utf-8 -*-
# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

"""
The nxos_netflow_interfaces config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)

from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts import Facts
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.rm_templates.netflow_interfaces import (
    Netflow_interfacesTemplate,
)
from ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.utils.utils import (
    normalize_interface,
)


# the keyword of the command for each protocol, in the order the commands are generated
CLI = {"ipv4": "ip", "ipv6": "ipv6", "layer2_switched": "layer2-switched"}
DIRECTIONS = ("input", "output")
SLOTS = [(protocol, direction) for protocol in CLI for direction in DIRECTIONS]


class Netflow_interfaces(ResourceModule):
    """
    The nxos_netflow_interfaces config class
    """

    def __init__(self, module):
        super(Netflow_interfaces, self).__init__(
            empty_fact_val=[],
            facts_module=Facts(module),
            module=module,
            resource="netflow_interfaces",
            tmplt=Netflow_interfacesTemplate(),
        )

    def execute_module(self):
        """Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self._apply()
        result = self.result
        if (
            self.state in ["merged", "replaced", "overridden"]
            and "after" in result
            and not self._module.check_mode
        ):
            self._check_applied(result)
        return result

    def _apply(self):
        """Send the commands, a rejected command is reported with the commands that were sent.

        The commands are sent in one session, the ones before the rejected one stay applied.
        """
        try:
            self.run_commands()
        except Exception as exc:  # pylint: disable=broad-except
            self._module.fail_json(
                msg="The device rejected a command, the commands before it can have been applied: {0}".format(
                    self._error(exc),
                ),
                commands=self.commands,
            )

    @staticmethod
    def _error(exc):
        """The text of the device without the escapes of the terminal."""
        text = str(exc)
        if text[:2] in ("b'", 'b"') and text[-1] == text[1]:
            text = text[2:-1]
        text = text.replace("\\r", "").replace("\\n", " ")
        return " ".join(text.split())

    def _check_applied(self, result):
        """The device can accept a command and not apply it, for example the egress NetFlow
        TCAM that is not carved only gives a message. The flow monitors that are missing are reported.
        """
        applied = self._slots(result["after"], strict=False)
        missing = []
        for entry in self.want:
            name = normalize_interface(entry["name"])
            for item in entry.get("flow_monitors") or []:
                slot = (item.get("protocol") or "ipv4", item["direction"])
                if applied.get(name, {}).get(slot) != item["monitor"]:
                    missing.append(
                        "{0}: {1} flow monitor {2} {3}".format(
                            name,
                            CLI[slot[0]],
                            item["monitor"],
                            slot[1],
                        ),
                    )
        if missing:
            self._module.fail_json(
                msg="The device accepted the commands but did not apply: {0}. "
                "A flow monitor in the direction output needs the egr-netflow TCAM region to be carved.".format(
                    "; ".join(missing),
                ),
                commands=self.commands,
                after=result["after"],
            )

    def generate_commands(self):
        """Generate configuration commands to send based on
        want, have and desired state.
        """
        wantd = self._slots(self.want, strict=True)
        haved = self._slots(self.have, strict=False)

        if self.state == "deleted":
            unknown = [name for name in wantd if name not in haved]
            if unknown:
                self._module.warn(
                    "No flow monitors are configured on {0}, nothing is removed there.".format(
                        ", ".join(unknown),
                    ),
                )
            for name in list(wantd) if wantd else list(haved):
                self._interface(name, {}, haved.get(name, {}), prune=True)
            return

        prune = self.state in ["replaced", "overridden"]
        for name, want in wantd.items():
            self._interface(name, want, haved.get(name, {}), prune)

        if self.state == "overridden":
            for name, have in haved.items():
                if name not in wantd:
                    self._interface(name, {}, have, prune=True)

    def _slots(self, entries, strict):
        """Return {interface: {(protocol, direction): monitor}}.

        An interface can have one monitor for each protocol and direction, the
        user is told when more than one is given for the same.
        """
        result = {}
        for entry in entries:
            name = normalize_interface(entry["name"])
            slots = result.setdefault(name, {})
            for item in entry.get("flow_monitors") or []:
                slot = (item.get("protocol") or "ipv4", item["direction"])
                if strict and slots.get(slot, item["monitor"]) != item["monitor"]:
                    self._module.fail_json(
                        msg="{0}: only one flow monitor is possible for the protocol {1} and the direction {2}, got '{3}' and '{4}'".format(
                            name,
                            slot[0],
                            slot[1],
                            slots[slot],
                            item["monitor"],
                        ),
                    )
                slots[slot] = item["monitor"]
        return result

    def _interface(self, name, want, have, prune):
        """The commands of one interface.

        The device rejects a second monitor for the same protocol and direction, the
        old one is removed first.
        """
        begin = len(self.commands)
        for slot in SLOTS:
            wanted = want.get(slot)
            current = have.get(slot)
            if wanted == current or (wanted is None and not prune):
                continue
            if current:
                self.addcmd(self._data(slot, current), "flow_monitors", True)
            if wanted:
                self.addcmd(self._data(slot, wanted), "flow_monitors")
        if len(self.commands) != begin:
            self.commands.insert(begin, self._tmplt.render({"name": name}, "name", False))

    @staticmethod
    def _data(slot, monitor):
        return {"cli": CLI[slot[0]], "monitor": monitor, "direction": slot[1]}
