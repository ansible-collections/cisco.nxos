# (c) 2026 Red Hat Inc.
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

from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_evpn_vnis

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

# NOTE: the `section ^evpn` display format below is assumed, it has not been
# verified on hardware.
BASE = dedent(
    """\
    evpn
      vni 10100 l2
        rd auto
        route-target import auto
        route-target export auto
      vni 10200 l2
        rd 65000:10200
        route-target import 65000:10200
        route-target import 65000:10201
        route-target export 65000:10200
    """,
)

# assumed alternative display: the combined form kept as typed
BASE_BOTH = dedent(
    """\
    evpn
      vni 10100 l2
        rd auto
        route-target both auto
    """,
)


class TestNxosEvpnVnisModule(TestNxosModule):
    module = nxos_evpn_vnis

    def setUp(self):
        super(TestNxosEvpnVnisModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.evpn_vnis.evpn_vnis.Evpn_vnisFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()

    def tearDown(self):
        super(TestNxosEvpnVnisModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    # merged

    def test_nxos_evpn_vnis_merged_empty(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=[
                dict(
                    vni=10300,
                    route_distinguisher="auto",
                    route_target_import=["auto"],
                    route_target_export=["auto"],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "evpn",
                "vni 10300 l2",
                "rd auto",
                "route-target import auto",
                "route-target export auto",
            ],
        )

    def test_nxos_evpn_vnis_merged_vni_only(self):
        self.get_config.return_value = ""
        result = self._run(True, config=[dict(vni=10300)], state="merged")
        self.assertEqual(result["commands"], ["evpn", "vni 10300 l2"])

    def test_nxos_evpn_vnis_merged_adds_only(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    vni=10100,
                    route_distinguisher="65000:10100",
                    route_target_import=["65000:10100"],
                ),
            ],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["evpn", "vni 10100 l2", "rd 65000:10100", "route-target import 65000:10100"],
        )

    def test_nxos_evpn_vnis_merged_idempotent(self):
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=[
                dict(vni=10100, route_distinguisher="auto", route_target_import=["auto"]),
                dict(vni=10200, route_target_import=["65000:10201", "65000:10200"]),
            ],
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_evpn_vnis_merged_both_expansion(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=[dict(vni=10100, route_target_both=["auto", "65000:1"])],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "evpn",
                "vni 10100 l2",
                "route-target import auto",
                "route-target import 65000:1",
                "route-target export auto",
                "route-target export 65000:1",
            ],
        )

    def test_nxos_evpn_vnis_merged_both_idempotent(self):
        # `both` input against separate import/export lines on the device
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=[dict(vni=10100, route_target_both=["auto"])],
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_evpn_vnis_merged_both_display_idempotent(self):
        # the device displaying the combined form is read as import + export
        self.get_config.return_value = BASE_BOTH
        result = self._run(
            False,
            config=[
                dict(
                    vni=10100,
                    route_target_import=["auto"],
                    route_target_export=["auto"],
                ),
            ],
            state="merged",
        )
        self.assertEqual(result["commands"], [])

        result = self._run(
            False,
            config=[dict(vni=10100, route_target_both=["auto"])],
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_evpn_vnis_merged_one_evpn_line(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=[dict(vni=10300, route_distinguisher="auto"), dict(vni=10400)],
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            ["evpn", "vni 10300 l2", "rd auto", "vni 10400 l2"],
        )

    # replaced

    def test_nxos_evpn_vnis_replaced(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(
                    vni=10200,
                    route_distinguisher="auto",
                    route_target_import=["65000:10201"],
                    route_target_export=["65000:10200"],
                ),
            ],
            state="replaced",
        )
        self.assertEqual(
            result["commands"],
            [
                "evpn",
                "vni 10200 l2",
                "rd auto",
                "no route-target import 65000:10200",
            ],
        )

    def test_nxos_evpn_vnis_replaced_removes_rd_and_targets(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(vni=10100)], state="replaced")
        self.assertEqual(
            result["commands"],
            [
                "evpn",
                "vni 10100 l2",
                "no rd auto",
                "no route-target import auto",
                "no route-target export auto",
            ],
        )

    def test_nxos_evpn_vnis_replaced_leaves_other_vnis(self):
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=[
                dict(
                    vni=10100,
                    route_distinguisher="auto",
                    route_target_both=["auto"],
                ),
            ],
            state="replaced",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_evpn_vnis_replaced_new_vni(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[dict(vni=10300, route_distinguisher="auto")],
            state="replaced",
        )
        self.assertEqual(result["commands"], ["evpn", "vni 10300 l2", "rd auto"])

    # overridden

    def test_nxos_evpn_vnis_overridden(self):
        self.get_config.return_value = BASE
        result = self._run(
            True,
            config=[
                dict(vni=10100, route_distinguisher="auto", route_target_both=["auto"]),
                dict(vni=10300, route_distinguisher="auto"),
            ],
            state="overridden",
        )
        self.assertEqual(
            result["commands"],
            ["evpn", "no vni 10200 l2", "vni 10300 l2", "rd auto"],
        )

    def test_nxos_evpn_vnis_overridden_idempotent(self):
        self.get_config.return_value = BASE
        result = self._run(
            False,
            config=[
                dict(
                    vni=10100,
                    route_distinguisher="auto",
                    route_target_import=["auto"],
                    route_target_export=["auto"],
                ),
                dict(
                    vni=10200,
                    route_distinguisher="65000:10200",
                    route_target_import=["65000:10200", "65000:10201"],
                    route_target_export=["65000:10200"],
                ),
            ],
            state="overridden",
        )
        self.assertEqual(result["commands"], [])

    # deleted

    def test_nxos_evpn_vnis_deleted(self):
        self.get_config.return_value = BASE
        result = self._run(True, config=[dict(vni=10100), dict(vni=10999)], state="deleted")
        self.assertEqual(result["commands"], ["evpn", "no vni 10100 l2"])

    def test_nxos_evpn_vnis_deleted_all(self):
        self.get_config.return_value = BASE
        result = self._run(True, state="deleted")
        self.assertEqual(result["commands"], ["evpn", "no vni 10100 l2", "no vni 10200 l2"])

    def test_nxos_evpn_vnis_deleted_idempotent(self):
        self.get_config.return_value = ""
        result = self._run(False, state="deleted")
        self.assertEqual(result["commands"], [])

    # rendered / parsed / gathered

    def test_nxos_evpn_vnis_rendered(self):
        result = self._run(
            False,
            config=[
                dict(
                    vni=10100,
                    route_distinguisher="auto",
                    route_target_both=["auto"],
                ),
                dict(vni=10200, route_target_import=["65000:10200"]),
            ],
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            [
                "evpn",
                "vni 10100 l2",
                "rd auto",
                "route-target import auto",
                "route-target export auto",
                "vni 10200 l2",
                "route-target import 65000:10200",
            ],
        )

    def test_nxos_evpn_vnis_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(
            result["parsed"],
            [
                dict(
                    vni=10100,
                    route_distinguisher="auto",
                    route_target_import=["auto"],
                    route_target_export=["auto"],
                ),
                dict(
                    vni=10200,
                    route_distinguisher="65000:10200",
                    route_target_import=["65000:10200", "65000:10201"],
                    route_target_export=["65000:10200"],
                ),
            ],
        )

    def test_nxos_evpn_vnis_parsed_both_display(self):
        result = self._run(False, running_config=BASE_BOTH, state="parsed")
        self.assertEqual(
            result["parsed"],
            [
                dict(
                    vni=10100,
                    route_distinguisher="auto",
                    route_target_import=["auto"],
                    route_target_export=["auto"],
                ),
            ],
        )

    def test_nxos_evpn_vnis_parsed_ignores_other_evpn_config(self):
        cfg = dedent(
            """\
            evpn esi multihoming
              ethernet-segment
            evpn
              vni 10100 l2
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(result["parsed"], [dict(vni=10100)])

    def test_nxos_evpn_vnis_gathered(self):
        self.get_config.return_value = BASE
        result = self._run(False, state="gathered")
        self.assertEqual([e["vni"] for e in result["gathered"]], [10100, 10200])
        self.assertEqual(
            result["gathered"][1]["route_target_import"],
            ["65000:10200", "65000:10201"],
        )
        self.assertNotIn("route_target_both", result["gathered"][0])
