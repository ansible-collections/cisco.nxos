# (c) 2019 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vlans

from .nxos_module import TestNxosModule, load_fixture, set_module_args


ignore_provider_arg = True


class TestNxosVlansModule(TestNxosModule):
    module = nxos_vlans

    def setUp(self):
        super(TestNxosVlansModule, self).setUp()

        self.mock_FACT_LEGACY_SUBSETS = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.facts.FACT_LEGACY_SUBSETS",
        )
        self.FACT_LEGACY_SUBSETS = self.mock_FACT_LEGACY_SUBSETS.start()

        self.mock_get_resource_connection_config = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.cfg.base.get_resource_connection",
        )
        self.get_resource_connection_config = self.mock_get_resource_connection_config.start()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts.get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_edit_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vlans.vlans.Vlans.edit_config",
        )
        self.edit_config = self.mock_edit_config.start()

        self.mock_get_device_data = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vlans.vlans.VlansFacts.get_device_data",
        )
        self.get_device_data = self.mock_get_device_data.start()

        self.mock_get_platform = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.config.vlans.vlans.Vlans.get_platform",
        )
        self.get_platform = self.mock_get_platform.start()

    def tearDown(self):
        super(TestNxosVlansModule, self).tearDown()
        self.mock_FACT_LEGACY_SUBSETS.stop()
        self.mock_get_resource_connection_config.stop()
        self.mock_get_resource_connection_facts.stop()
        self.mock_edit_config.stop()
        self.mock_get_platform.stop()

    def prepare(self, test="", nve_overlay=""):
        self.nve_overlay_fixture = "show_running-config_nve_overlay" + nve_overlay
        if test == "_no_facts":
            self.get_device_data.side_effect = self.load_from_file_no_facts
        else:
            self.get_device_data.side_effect = self.load_from_file
        self.get_platform.return_value = "N9K-NXOSv"

    def load_from_file(self, *args, **kwargs):
        cmd = args[1]
        if "nve-overlay" in str(cmd):
            return load_fixture("nxos_vlans", self.nve_overlay_fixture)
        filename = str(cmd).split(" | ", 1)[0].replace(" ", "_")
        return load_fixture("nxos_vlans", filename)

    def load_from_file_no_facts(self, *args, **kwargs):
        cmd = args[1]
        if "nve-overlay" in str(cmd):
            return load_fixture("nxos_vlans", self.nve_overlay_fixture + "_no_facts")
        filename = str(cmd).split(" | ", 1)[0].replace(" ", "_")
        filename += "_no_facts"
        return load_fixture("nxos_vlans", filename)

    def test_1(self):
        """
        **NOTE** This config is for reference only! See fixtures files for real data.
        vlan 1,3-5,8
        vlan 3
          name test-vlan3
        !Note:vlan 4 is present with default settings
        vlan 5
          shutdown
          name test-changeme
          mode fabricpath
          state suspend
          vn-segment 942
        !Note:vlan 7 is not present
        vlan 8
          shutdown
          name test-changeme-not
          state suspend
        """
        self.prepare()
        self.get_platform.return_value = "N7K-Cxxx"

        playbook = dict(
            config=[
                dict(vlan_id=4),
                dict(vlan_id=5, mapped_vni=555, mode="ce"),
                dict(vlan_id=7, mapped_vni=777, name="test-vlan7", enabled=False),
                dict(vlan_id="8", state="active", name="test-changeme-not"),
                # vlan 3 is not present in playbook.
            ],
        )

        merged = [
            # Update existing device states with any differences in the playbook.
            "vlan 5",
            "vn-segment 555",
            "mode ce",
            "vlan 7",
            "vn-segment 777",
            "name test-vlan7",
            "shutdown",
            "vlan 8",
            "state active",
        ]
        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=merged)

        self.get_platform.return_value = "N9K-NXOSv"
        deleted = [
            # Reset existing device state to default values. Scope is limited to
            # objects in the play when the 'config' key is specified. For vlans
            # this means deleting each vlan listed in the playbook and ignoring
            # any play attrs other than 'vlan_id'.
            "no vlan 4",
            "no vlan 5",
            "no vlan 8",
        ]
        playbook["state"] = "deleted"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        self.get_platform.return_value = "N5K-Cxxx"
        overridden = [
            # The play is the source of truth. Similar to replaced but the scope
            # includes all objects on the device; i.e. it will also reset state
            # on objects not found in the play.
            "no vlan 1",
            "no vlan 3",
            "vlan 5",
            "mode ce",
            "vn-segment 555",
            "no state",
            "no shutdown",
            "no name",
            "vlan 8",
            "no shutdown",
            "state active",
            "vlan 7",
            "name test-vlan7",
            "shutdown",
            "vn-segment 777",
        ]
        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=overridden)

        self.get_platform.return_value = "N7K-NXOSv"
        replaced = [
            # Scope is limited to objects in the play.
            # replaced should ignore existing vlan 3.
            "vlan 5",
            "mode ce",
            "vn-segment 555",
            "no state",
            "no shutdown",
            "no name",
            "vlan 7",
            "shutdown",
            "name test-vlan7",
            "vn-segment 777",
            "vlan 8",
            "no shutdown",
            "state active",
        ]
        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_2(self):
        # Test when no 'config' key is used in playbook.
        self.prepare()
        deleted = [
            "no vlan 1",
            "no vlan 3",
            "no vlan 4",
            "no vlan 5",
            "no vlan 8",
        ]
        playbook = dict(state="deleted")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=deleted)

        for test_state in ["merged", "replaced", "overridden"]:
            set_module_args(dict(state=test_state), ignore_provider_arg)
            self.execute_module(failed=True)

    def test_3(self):
        # Test no facts returned
        self.prepare(test="_no_facts")
        playbook = dict(state="deleted")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=False)

    def test_4(self):
        self.prepare()
        # Misc tests to hit codepaths highlighted by code coverage tool as missed.
        playbook = dict(config=[dict(vlan_id=8, enabled=True)])
        replaced = [
            # Update existing device states with any differences in the playbook.
            "vlan 8",
            "no shutdown",
            "no state",
            "no name",
        ]
        playbook["state"] = "replaced"
        playbook["_ansible_check_mode"] = True
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=replaced)

    def test_5(self):
        """
        Idempotency test
        """

        self.prepare()
        playbook = dict(
            config=[
                dict(vlan_id=1, name="default", enabled=True),
                dict(vlan_id=3, name="test-vlan3", enabled=True),
                dict(vlan_id=4, enabled=True),
                dict(
                    vlan_id=5,
                    name="test-changeme",
                    mapped_vni=942,
                    state="suspend",
                    enabled=False,
                ),
                dict(
                    vlan_id=8,
                    name="test-changeme-not",
                    state="suspend",
                    enabled=False,
                ),
            ],
        )

        playbook["state"] = "merged"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)

        playbook["state"] = "overridden"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)

        playbook["state"] = "replaced"
        set_module_args(playbook, ignore_provider_arg)
        r = self.execute_module(changed=False)

    def test_nve_overlay_merged(self):
        # No vlan has nve_overlay set on the device.
        self.prepare()
        playbook = dict(
            config=[
                dict(vlan_id=4, nve_overlay=True),
                dict(vlan_id=5, name="test-changeme", nve_overlay=False),
                dict(vlan_id=7, name="test-vlan7", nve_overlay=True),
            ],
            state="merged",
        )
        merged = [
            "vlan 7",
            "name test-vlan7",
            "system vlan nve-overlay id 7",
            "system vlan nve-overlay id 4",
        ]
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(merged))
        # the global command must follow the sub-commands of its vlan
        cmds = result["commands"]
        self.assertLess(cmds.index("name test-vlan7"), cmds.index("system vlan nve-overlay id 7"))

        # nve_overlay on a vlan that is not on the device creates the vlan first
        playbook = dict(config=[dict(vlan_id=9, nve_overlay=True)], state="merged")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=["vlan 9", "system vlan nve-overlay id 9"])

    def test_nve_overlay_range_in_running_config(self):
        # Device shows 'system vlan nve-overlay id 3-4,8'
        self.prepare(nve_overlay="_ranges")
        playbook = dict(
            config=[
                dict(vlan_id=3, nve_overlay=True),
                dict(vlan_id=4, nve_overlay=True),
                dict(vlan_id=5, nve_overlay=False),
                dict(vlan_id=8, nve_overlay=True),
            ],
        )
        # idempotent for all of the states
        for state in ["merged", "replaced"]:
            playbook["state"] = state
            set_module_args(playbook, ignore_provider_arg)
            result = self.execute_module(changed=state == "replaced")
            if state == "merged":
                self.assertEqual(result["commands"], [])
            else:
                # replaced also resets the other attributes that are not in the play
                self.assertNotIn("no system vlan nve-overlay id 5", result["commands"])
                self.assertNotIn("system vlan nve-overlay id 3", result["commands"])

        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        overlay = sorted(v["vlan_id"] for v in result["gathered"] if v.get("nve_overlay"))
        self.assertEqual(overlay, [3, 4, 8])
        for vlan in result["gathered"]:
            if vlan["vlan_id"] not in overlay:
                self.assertNotIn("nve_overlay", vlan)

    def test_nve_overlay_remove(self):
        self.prepare(nve_overlay="_ranges")
        # merged with false removes it, vlan 4 is left alone
        playbook = dict(
            config=[dict(vlan_id=3, nve_overlay=False), dict(vlan_id=4)],
            state="merged",
        )
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=["no system vlan nve-overlay id 3"])

        # replaced resets it when it is not in the play
        playbook = dict(config=[dict(vlan_id=3, name="test-vlan3", enabled=True)], state="replaced")
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(changed=True, commands=["no system vlan nve-overlay id 3"])

        # overridden resets it and removes the marking of vlans that are deleted
        playbook = dict(
            config=[
                dict(vlan_id=1, name="default", enabled=True),
                dict(vlan_id=3, name="test-vlan3", enabled=True),
                dict(vlan_id=4, enabled=True, nve_overlay=True),
                dict(
                    vlan_id=5,
                    name="test-changeme",
                    mapped_vni=942,
                    state="suspend",
                    enabled=False,
                ),
            ],
            state="overridden",
        )
        set_module_args(playbook, ignore_provider_arg)
        self.execute_module(
            changed=True,
            commands=[
                "no system vlan nve-overlay id 8",
                "no vlan 8",
                "no system vlan nve-overlay id 3",
            ],
        )

        # deleted
        set_module_args(
            dict(config=[dict(vlan_id=3), dict(vlan_id=5)], state="deleted"),
            ignore_provider_arg,
        )
        self.execute_module(
            changed=True,
            commands=["no system vlan nve-overlay id 3", "no vlan 3", "no vlan 5"],
        )

    def test_nve_overlay_rendered_and_parsed(self):
        self.prepare()
        playbook = dict(
            config=[dict(vlan_id=3801, name="L3VNI", mapped_vni=50001, nve_overlay=True)],
            state="rendered",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "vlan 3801",
                "name L3VNI",
                "vn-segment 50001",
                "system vlan nve-overlay id 3801",
            ],
        )

        running_config = "\n\n".join(
            [
                json.dumps(load_fixture("nxos_vlans", "show_vlan")),
                load_fixture("nxos_vlans", "show_running-config"),
                "system vlan nve-overlay id 4-5\nsystem vlan nve-overlay id 8",
            ],
        )
        set_module_args(dict(running_config=running_config, state="parsed"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        overlay = sorted(v["vlan_id"] for v in result["parsed"] if v.get("nve_overlay"))
        self.assertEqual(overlay, [4, 5, 8])

        # running_config without the nve-overlay part still parses
        running_config = "\n\n".join(
            [
                json.dumps(load_fixture("nxos_vlans", "show_vlan")),
                load_fixture("nxos_vlans", "show_running-config"),
            ],
        )
        set_module_args(dict(running_config=running_config, state="parsed"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertFalse([v for v in result["parsed"] if v.get("nve_overlay")])

    def test_nve_overlay_empty_facts_output(self):
        # nothing in 'show running-config | include nve-overlay'
        self.prepare()
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertFalse([v for v in result["gathered"] if "nve_overlay" in v])

    def test_nve_overlay_facts_command_error_is_not_hidden(self):
        self.prepare()
        base = self.get_device_data.side_effect

        def fail_on_overlay(*args, **kwargs):
            if "nve-overlay" in str(args[1]):
                raise Exception("overlay command failed")
            return base(*args, **kwargs)

        self.get_device_data.side_effect = fail_on_overlay
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        with self.assertRaises(Exception) as ctx:
            self.execute_module(changed=False)
        self.assertIn("overlay command failed", str(ctx.exception))

    def test_nve_overlay_merged_already_true_is_idempotent(self):
        # Device shows 'system vlan nve-overlay id 3-4,8'
        self.prepare(nve_overlay="_ranges")
        # explicit true on a vlan that already has it, and omitted on another
        playbook = dict(
            config=[dict(vlan_id=8, nve_overlay=True), dict(vlan_id=3)],
            state="merged",
        )
        set_module_args(playbook, ignore_provider_arg)
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])

    def test_nve_overlay_default_have_is_idempotent(self):
        # No vlan has nve_overlay on the device, so false and omitted are both the default
        self.prepare()
        for state in ["merged", "replaced"]:
            for overlay in [dict(), dict(nve_overlay=False)]:
                config = [dict(vlan_id=4, enabled=True, **overlay)]
                set_module_args(dict(config=config, state=state), ignore_provider_arg)
                result = self.execute_module(changed=False)
                self.assertEqual(result["commands"], [])

    def test_nve_overlay_replaced_overridden_omitted_vs_true(self):
        self.prepare(nve_overlay="_ranges")
        for state in ["replaced", "overridden"]:
            # omitted is treated as false and the marking is removed
            config = [dict(vlan_id=3, name="test-vlan3", enabled=True)]
            if state == "overridden":
                config = self._overridden_config(config)
            set_module_args(dict(config=config, state=state), ignore_provider_arg)
            result = self.execute_module(changed=True)
            self.assertIn("no system vlan nve-overlay id 3", result["commands"])

            # true keeps it, no overlay command is generated
            config = [dict(vlan_id=3, name="test-vlan3", enabled=True, nve_overlay=True)]
            if state == "overridden":
                config = self._overridden_config(config)
            set_module_args(dict(config=config, state=state), ignore_provider_arg)
            result = self.execute_module(changed=state == "overridden")
            self.assertFalse([c for c in result["commands"] if "nve-overlay id 3" in c])

    def _overridden_config(self, config):
        # overridden removes every vlan that is not listed
        return config + [
            dict(vlan_id=1, name="default", enabled=True),
            dict(vlan_id=4, enabled=True, nve_overlay=True),
            dict(vlan_id=5, name="test-changeme", mapped_vni=942, state="suspend", enabled=False),
            dict(vlan_id=8, enabled=False, nve_overlay=True),
        ]

    def prepare_vn_segment_only(self):
        # VLAN 3801 has only a 'vn-segment' line (no name/state), VLAN 249 has a name too
        vlans = [("3801", "VLAN3801"), ("249", "VLAN_249")]
        show_vlan = json.dumps(
            {
                "TABLE_vlanbrief": {
                    "ROW_vlanbrief": [
                        {
                            "vlanshowbr-vlanid": vid,
                            "vlanshowbr-vlanid-utf": vid,
                            "vlanshowbr-vlanname": name,
                            "vlanshowbr-vlanstate": "active",
                            "vlanshowbr-shutstate": "noshutdown",
                        }
                        for vid, name in vlans
                    ],
                },
                "TABLE_mtuinfo": {
                    "ROW_mtuinfo": [
                        {
                            "vlanshowinfo-vlanid": vid,
                            "vlanshowinfo-media-type": "enet",
                            "vlanshowinfo-vlanmode": "ce-vlan",
                        }
                        for vid, _name in vlans
                    ],
                },
            },
        )
        run_cfg = "vlan 1,249,3801\nvlan 249\n  name VLAN_249\n  vn-segment 10249\nvlan 3801\n  vn-segment 50001\n"

        def device_data(*args, **kwargs):
            cmd = str(args[1])
            if "json" in cmd:
                return show_vlan
            if "nve-overlay" in cmd:
                return ""
            return run_cfg

        self.get_device_data.side_effect = device_data
        self.get_platform.return_value = "N9K-NXOSv"

    def test_vn_segment_only_vlan_is_gathered(self):
        self.prepare_vn_segment_only()
        set_module_args(dict(state="gathered"), ignore_provider_arg)
        result = self.execute_module(changed=False)
        mapped = {v["vlan_id"]: v.get("mapped_vni") for v in result["gathered"]}
        self.assertEqual(mapped, {249: 10249, 3801: 50001})

    def test_vn_segment_only_vlan_is_idempotent(self):
        self.prepare_vn_segment_only()
        for state in ["merged", "replaced"]:
            playbook = dict(
                config=[
                    dict(vlan_id=3801, mapped_vni=50001),
                    dict(vlan_id=249, name="VLAN_249", mapped_vni=10249),
                ],
                state=state,
            )
            set_module_args(playbook, ignore_provider_arg)
            result = self.execute_module(changed=False)
            self.assertEqual(result["commands"], [])

    def test_duplicate_vlan_id_is_rejected(self):
        self.prepare()
        for state in ["merged", "replaced", "overridden", "rendered"]:
            playbook = dict(
                config=[dict(vlan_id=3, name="a"), dict(vlan_id=3, nve_overlay=True)],
                state=state,
            )
            set_module_args(playbook, ignore_provider_arg)
            result = self.execute_module(failed=True)
            self.assertIn("vlan_id 3 is listed more than once", result["msg"])

    def test_default_vlan_name_is_never_reset(self):
        # show_vlan has VLAN 1 named 'default'; NX-OS rejects 'no name' for it
        self.prepare()
        for state in ["replaced", "overridden"]:
            playbook = dict(
                config=[
                    dict(vlan_id=1),
                    dict(vlan_id=3, name="test-vlan3", enabled=True),
                    dict(vlan_id=4, enabled=True),
                    dict(
                        vlan_id=5,
                        name="test-changeme",
                        mapped_vni=942,
                        state="suspend",
                        enabled=False,
                    ),
                    dict(vlan_id=8, name="test-changeme-not", state="suspend", enabled=False),
                ],
                state=state,
            )
            set_module_args(playbook, ignore_provider_arg)
            result = self.execute_module(changed=False)
            self.assertNotIn("no name", result["commands"])
