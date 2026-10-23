# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type
from textwrap import dedent
from unittest.mock import patch

from ansible_collections.cisco.nxos.plugins.modules import nxos_vrf_address_family

from .nxos_module import TestNxosModule, set_module_args


class TestNxosVrfAddressFamilyModule(TestNxosModule):
    """Test the nxos_vrf_address_family module."""

    module = nxos_vrf_address_family

    def setUp(self):
        """Set up for nxos_vrf_address_family module tests."""
        super(TestNxosVrfAddressFamilyModule, self).setUp()

        self.mock_get_resource_connection_facts = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base."
            "get_resource_connection",
        )
        self.get_resource_connection_facts = self.mock_get_resource_connection_facts.start()

        self.mock_execute_show_command = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.vrf_address_family.vrf_address_family."
            "Vrf_address_familyFacts.get_config",
        )
        self.execute_show_command = self.mock_execute_show_command.start()

    def tearDown(self):
        super(TestNxosVrfAddressFamilyModule, self).tearDown()
        self.mock_get_resource_connection_facts.stop()
        self.mock_execute_show_command.stop()

    def test_nxos_vrf_address_fam_parsed(self):
        """Test parsed."""
        set_module_args(
            dict(
                running_config=dedent(
                    """\
                    vrf context VRF1
                        address-family ipv4 unicast
                            route-target import 64512:200
                            route-target export 64512:200
                            export map 22
                            export vrf default map 44 allow-vpn
                            export vrf allow-vpn
                            maximum routes 900 22 reinstall 44
                        address-family ipv6 unicast
                            route-target import 554832:500
                    """,
                ),
                state="parsed",
            ),
        )

        parsed_item = [
            {
                "name": "VRF1",
                "address_families": [
                    {
                        "afi": "ipv4",
                        "safi": "unicast",
                        "route_target": [
                            {
                                "import": "64512:200",
                            },
                            {
                                "export": "64512:200",
                            },
                        ],
                        "export": [
                            {
                                "map": "22",
                            },
                            {
                                "vrf": {
                                    "allow_vpn": True,
                                    "map_import": "44",
                                },
                            },
                            {
                                "vrf": {
                                    "allow_vpn": True,
                                },
                            },
                        ],
                        "maximum": {
                            "max_routes": 900,
                            "max_route_options": {
                                "threshold": {
                                    "threshold_value": 22,
                                    "reinstall_threshold": 44,
                                },
                            },
                        },
                    },
                    {
                        "afi": "ipv6",
                        "safi": "unicast",
                        "route_target": [
                            {
                                "import": "554832:500",
                            },
                        ],
                    },
                ],
            },
        ]

        result = self.execute_module(changed=False)
        self.assertEqual(parsed_item, result["parsed"])

    def test_vrf_af_merged(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target import 64512:200
                address-family ipv6 unicast
                    route-target import 554832:500
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                                "import": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        commands = [
            "vrf context VRF1",
            "address-family ipv4 unicast",
            "maximum routes 500 60 reinstall 80",
            "route-target export 65512:200",
            "export map 22",
            "export vrf default map 44 allow-vpn",
            "export vrf allow-vpn",
            "address-family ipv6 unicast",
            "maximum routes 1000",
            "route-target import 65512:200",
            "import map 22",
            "import vrf default map 44 advertise-vpn",
            "import vrf advertise-vpn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_merged_idempotent(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target import 64512:200
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
                address-family ipv6 unicast
                    route-target import 554832:500
                    maximum routes 1000
                    route-target import 65512:200
                    import map 22
                    import vrf default map 44 advertise-vpn
                    import vrf advertise-vpn
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                                "import": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="merged",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_overridden(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target import 64512:200
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
                address-family ipv6 unicast
                    route-target import 554832:500
                    maximum routes 1000
                    route-target import 65512:200
                    import map 22
                    import vrf default map 44 advertise-vpn
                    import vrf advertise-vpn
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "VRF2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                                "import": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        commands = [
            "vrf context VRF1",
            "address-family ipv4 unicast",
            "no maximum routes 500 60 reinstall 80",
            "no route-target import 64512:200",
            "no export vrf default map 44 allow-vpn",
            "no export vrf allow-vpn",
            "address-family ipv6 unicast",
            "no route-target import 554832:500",
            "no import map 22",
            "no import vrf default map 44 advertise-vpn",
            "no import vrf advertise-vpn",
            "vrf context VRF2",
            "address-family ipv4 unicast",
            "maximum routes 500 60 reinstall 80",
            "route-target export 65512:200",
            "export map 22",
            "export vrf default map 44 allow-vpn",
            "export vrf allow-vpn",
            "address-family ipv6 unicast",
            "maximum routes 1000",
            "route-target import 65512:200",
            "import map 22",
            "import vrf default map 44 advertise-vpn",
            "import vrf advertise-vpn",
        ]
        result = self.execute_module(changed=True)
        print(result["commands"])
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_overridden_idemp(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target export 65512:200
                    export map 22
                address-family ipv6 unicast
                    maximum routes 1000
                    route-target import 65512:200
            vrf context VRF2
                address-family ipv4 unicast
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
                address-family ipv6 unicast
                    maximum routes 1000
                    route-target import 65512:200
                    import map 22
                    import vrf default map 44 advertise-vpn
                    import vrf advertise-vpn
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "VRF2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "maximum": {
                                    "max_routes": 1000,
                                },
                                "route_target": [
                                    {
                                        "import": "65512:200",
                                    },
                                ],
                                "import": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "advertise_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="overridden",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_deleted(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target export 65512:200
                    export map 22
                address-family ipv6 unicast
                    maximum routes 1000
                    route-target import 65512:200
            vrf context VRF2
                address-family ipv4 unicast
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
                address-family ipv6 unicast
                    maximum routes 1000
                    route-target import 65512:200
                    import map 22
                    import vrf default map 44 advertise-vpn
                    import vrf advertise-vpn
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="deleted",
            ),
        )
        commands = [
            "vrf context VRF2",
            "address-family ipv4 unicast",
            "no maximum routes 500 60 reinstall 80",
            "no route-target export 65512:200",
            "no export map 22",
            "no export vrf default map 44 allow-vpn",
            "no export vrf allow-vpn",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_replaced(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv4 unicast
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                address-family ipv6 unicast
                    maximum routes 1000
                    route-target import 65512:200
            vrf context VRF2
                address-family ipv4 unicast
                    route-target export 65512:200
                address-family ipv6 unicast
                    maximum routes 1000
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "VRF2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        commands = [
            "vrf context VRF1",
            "address-family ipv4 unicast",
            "no route-target export 65512:200",
            "no export map 22",
            "no export vrf default map 44 allow-vpn",
            "address-family ipv6 unicast",
            "maximum routes 500 60 reinstall 80",
            "no route-target import 65512:200",
            "route-target export 65512:200",
            "export map 22",
            "export vrf default map 44 allow-vpn",
            "export vrf allow-vpn",
            "vrf context VRF2",
            "address-family ipv4 unicast",
            "maximum routes 500 60 reinstall 80",
            "export map 22",
            "export vrf default map 44 allow-vpn",
            "export vrf allow-vpn",
            "address-family ipv6 unicast",
            "no maximum routes 1000",
        ]
        result = self.execute_module(changed=True)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    def test_vrf_af_replaced_idem(self):
        """Test merged."""
        self.execute_show_command.return_value = dedent(
            """\
            vrf context VRF1
                address-family ipv6 unicast
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
            vrf context VRF2
                address-family ipv4 unicast
                    maximum routes 500 60 reinstall 80
                    route-target export 65512:200
                    export map 22
                    export vrf default map 44 allow-vpn
                    export vrf allow-vpn
            """,
        )

        set_module_args(
            dict(
                config=[
                    {
                        "name": "VRF1",
                        "address_families": [
                            {
                                "afi": "ipv6",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "VRF2",
                        "address_families": [
                            {
                                "afi": "ipv4",
                                "safi": "unicast",
                                "route_target": [
                                    {
                                        "export": "65512:200",
                                    },
                                ],
                                "maximum": {
                                    "max_routes": 500,
                                    "max_route_options": {
                                        "threshold": {
                                            "threshold_value": 60,
                                            "reinstall_threshold": 80,
                                        },
                                    },
                                },
                                "export": [
                                    {
                                        "map": "22",
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                            "map_import": "44",
                                        },
                                    },
                                    {
                                        "vrf": {
                                            "allow_vpn": True,
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
                state="replaced",
            ),
        )
        commands = []
        result = self.execute_module(changed=False)
        self.assertEqual(sorted(result["commands"]), sorted(commands))

    # The route-target ``both`` / ``evpn`` tests below use fixtures that are
    # ASSUMED, not hardware-verified: whether NX-OS shows ``route-target both``
    # as one line or as an import + export pair is unconfirmed, so both display
    # forms are exercised.

    @staticmethod
    def _rt_config(route_target, vrf="VRF1", afi="ipv4"):
        return [
            {
                "name": vrf,
                "address_families": [
                    {"afi": afi, "safi": "unicast", "route_target": route_target},
                ],
            },
        ]

    @staticmethod
    def _rt_device(*lines):
        body = "".join(f"        {line}\n" for line in lines)
        return "vrf context VRF1\n    address-family ipv4 unicast\n" + body

    def _run_rt(self, device, route_target, state, changed, commands=None):
        self.execute_show_command.return_value = device
        set_module_args(dict(config=self._rt_config(route_target), state=state))
        result = self.execute_module(changed=changed)
        self.assertEqual(result["commands"], commands or [])

    def test_vrf_af_rt_parsed_evpn(self):
        set_module_args(
            dict(
                running_config=self._rt_device(
                    "route-target import 65000:100",
                    "route-target both auto",
                    "route-target both auto evpn",
                    "route-target import auto evpn",
                    "route-target export 65000:100 evpn",
                ),
                state="parsed",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["parsed"][0]["address_families"][0]["route_target"],
            [
                {"import": "65000:100"},
                {"both": "auto"},
                {"both": "auto", "evpn": True},
                {"import": "auto", "evpn": True},
                {"export": "65000:100", "evpn": True},
            ],
        )

    def test_vrf_af_rt_rendered_evpn(self):
        set_module_args(
            dict(
                config=self._rt_config(
                    [
                        {"import": "65000:100"},
                        {"both": "auto"},
                        {"both": "auto", "evpn": True},
                        {"export": "65000:200", "evpn": True},
                    ],
                ),
                state="rendered",
            ),
        )
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["rendered"],
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "route-target import 65000:100",
                "route-target both auto",
                "route-target both auto evpn",
                "route-target export 65000:200 evpn",
            ],
        )

    def test_vrf_af_rt_gathered_evpn(self):
        self.execute_show_command.return_value = self._rt_device("route-target both auto evpn")
        set_module_args(dict(state="gathered"))
        result = self.execute_module(changed=False)
        self.assertEqual(
            result["gathered"][0]["address_families"][0]["route_target"],
            [{"both": "auto", "evpn": True}],
        )

    def test_vrf_af_rt_merged_both_evpn(self):
        self._run_rt(
            self._rt_device("route-target both auto"),
            [{"both": "auto"}, {"both": "auto", "evpn": True}],
            "merged",
            True,
            ["vrf context VRF1", "address-family ipv4 unicast", "route-target both auto evpn"],
        )

    def test_vrf_af_rt_merged_import_evpn(self):
        self._run_rt(
            self._rt_device("route-target import 65000:100"),
            [{"import": "65000:100", "evpn": True}],
            "merged",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "route-target import 65000:100 evpn",
            ],
        )

    def test_vrf_af_rt_idempotent_both_one_line(self):
        rts = [{"both": "auto"}, {"both": "auto", "evpn": True}]
        device = self._rt_device("route-target both auto", "route-target both auto evpn")
        for state in ("merged", "replaced", "overridden"):
            self._run_rt(device, rts, state, False)

    def test_vrf_af_rt_idempotent_both_expanded(self):
        # device shows ``both`` as an import + export pair
        rts = [{"both": "65000:100"}, {"both": "65000:100", "evpn": True}]
        device = self._rt_device(
            "route-target import 65000:100",
            "route-target import 65000:100 evpn",
            "route-target export 65000:100",
            "route-target export 65000:100 evpn",
        )
        for state in ("merged", "replaced", "overridden"):
            self._run_rt(device, rts, state, False)

    def test_vrf_af_rt_idempotent_pair_wanted_as_both(self):
        # want import + export, device shows a single ``both`` line
        rts = [{"import": "65000:100", "evpn": True}, {"export": "65000:100", "evpn": True}]
        for state in ("merged", "replaced"):
            self._run_rt(self._rt_device("route-target both 65000:100 evpn"), rts, state, False)

    def test_vrf_af_rt_idempotent_import_evpn(self):
        rts = [{"import": "65000:100", "evpn": True}]
        device = self._rt_device("route-target import 65000:100 evpn")
        for state in ("merged", "replaced", "overridden"):
            self._run_rt(device, rts, state, False)

    def test_vrf_af_rt_evpn_distinct_from_plain(self):
        # ``import 65000:100`` on the device does not satisfy ``import 65000:100 evpn``
        self._run_rt(
            self._rt_device("route-target import 65000:100"),
            [{"import": "65000:100", "evpn": True}],
            "replaced",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "route-target import 65000:100 evpn",
                "no route-target import 65000:100",
            ],
        )

    def test_vrf_af_rt_replaced_removes_both(self):
        self._run_rt(
            self._rt_device("route-target both auto", "route-target both auto evpn"),
            [{"both": "auto"}],
            "replaced",
            True,
            ["vrf context VRF1", "address-family ipv4 unicast", "no route-target both auto evpn"],
        )

    def test_vrf_af_rt_replaced_partial_both(self):
        # only the import half is wanted: NX-OS rejects 'no route-target export ...'
        # against a 'both' line, so the whole line is negated and the half re-added
        self._run_rt(
            self._rt_device("route-target both 65000:100 evpn"),
            [{"import": "65000:100", "evpn": True}],
            "replaced",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "no route-target both 65000:100 evpn",
                "route-target import 65000:100 evpn",
            ],
        )

    def test_vrf_af_rt_replaced_partial_both_export(self):
        self._run_rt(
            self._rt_device("route-target both 65000:100 evpn"),
            [{"export": "65000:100", "evpn": True}],
            "replaced",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "no route-target both 65000:100 evpn",
                "route-target export 65000:100 evpn",
            ],
        )

    def test_vrf_af_rt_replaced_partial_plain_both(self):
        self._run_rt(
            self._rt_device("route-target both 65000:100"),
            [{"export": "65000:100"}],
            "replaced",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "no route-target both 65000:100",
                "route-target export 65000:100",
            ],
        )

    def test_vrf_af_rt_replaced_partial_both_idempotent_after_split(self):
        # after the split the device shows two plain lines, which must be stable
        self._run_rt(
            self._rt_device("route-target import 65000:100 evpn"),
            [{"import": "65000:100", "evpn": True}],
            "replaced",
            False,
        )

    def test_vrf_af_rt_overridden_removes_other_vrf(self):
        self.execute_show_command.return_value = (
            self._rt_device("route-target both auto evpn")
            + "vrf context VRF2\n    address-family ipv4 unicast\n"
            + "        route-target both auto evpn\n"
        )
        set_module_args(
            dict(config=self._rt_config([{"both": "auto", "evpn": True}]), state="overridden"),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf context VRF2",
                "address-family ipv4 unicast",
                "no route-target both auto evpn",
            ],
        )

    def test_vrf_af_rt_deleted_both_evpn(self):
        self._run_rt(
            self._rt_device("route-target both auto", "route-target both auto evpn"),
            [{"both": "auto", "evpn": True}],
            "deleted",
            True,
            ["vrf context VRF1", "address-family ipv4 unicast", "no route-target both auto evpn"],
        )

    def test_vrf_af_rt_deleted_import_evpn_keeps_evpn_keyword(self):
        self._run_rt(
            self._rt_device("route-target import auto evpn", "route-target import auto"),
            [{"import": "auto", "evpn": True}],
            "deleted",
            True,
            ["vrf context VRF1", "address-family ipv4 unicast", "no route-target import auto evpn"],
        )

    def test_vrf_af_rt_deleted_one_direction_of_both_fails(self):
        # NX-OS cannot negate one direction of a 'both' line
        self.execute_show_command.return_value = self._rt_device("route-target both auto evpn")
        set_module_args(
            dict(config=self._rt_config([{"import": "auto", "evpn": True}]), state="deleted"),
        )
        result = self.execute_module(failed=True)
        self.assertIn("cannot delete only one direction", result["msg"])

    def test_vrf_af_rt_mixed_legacy_and_new(self):
        self._run_rt(
            self._rt_device("route-target import 65000:100", "route-target export 65000:200"),
            [
                {"import": "65000:100"},
                {"export": "65000:200"},
                {"both": "auto"},
                {"both": "auto", "evpn": True},
            ],
            "merged",
            True,
            [
                "vrf context VRF1",
                "address-family ipv4 unicast",
                "route-target both auto",
                "route-target both auto evpn",
            ],
        )

    def test_vrf_af_rt_evpn_requires_direction(self):
        self.execute_show_command.return_value = ""
        set_module_args(dict(config=self._rt_config([{"evpn": True}]), state="merged"))
        result = self.execute_module(failed=True)
        self.assertIn("requires one of", result["msg"])

    def test_vrf_af_rt_both_mutually_exclusive(self):
        self.execute_show_command.return_value = ""
        set_module_args(
            dict(config=self._rt_config([{"both": "auto", "import": "auto"}]), state="merged"),
        )
        self.execute_module(failed=True)

    def test_vrf_af_rt_auto_only_valid_with_both(self):
        for direction in ("import", "export"):
            self.execute_show_command.return_value = self._rt_device()
            set_module_args(
                dict(config=self._rt_config([{direction: "auto", "evpn": True}]), state="merged"),
            )
            result = self.execute_module(failed=True)
            self.assertIn("only accepts 'auto' with 'both'", result["msg"])

    PURGE_DEVICE = dedent(
        """\
        vrf context VRF1
            address-family ipv4 unicast
                route-target import 64512:200
            address-family ipv6 unicast
                route-target import 554832:500
        vrf context VRF2
            address-family ipv4 unicast
                route-target export 65000:1
        """,
    )

    def test_nxos_vrf_address_fam_purged_name_only(self):
        self.execute_show_command.return_value = self.PURGE_DEVICE
        set_module_args(dict(config=[dict(name="VRF1")], state="purged"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf context VRF1",
                "no address-family ipv4 unicast",
                "no address-family ipv6 unicast",
            ],
        )

    def test_nxos_vrf_address_fam_purged_listed_address_family(self):
        self.execute_show_command.return_value = self.PURGE_DEVICE
        set_module_args(
            dict(
                config=[dict(name="VRF1", address_families=[dict(afi="ipv6", safi="unicast")])],
                state="purged",
            ),
        )
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            ["vrf context VRF1", "no address-family ipv6 unicast"],
        )

    def test_nxos_vrf_address_fam_purged_all_vrfs(self):
        self.execute_show_command.return_value = self.PURGE_DEVICE
        set_module_args(dict(state="purged"))
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["commands"],
            [
                "vrf context VRF1",
                "no address-family ipv4 unicast",
                "no address-family ipv6 unicast",
                "vrf context VRF2",
                "no address-family ipv4 unicast",
            ],
        )

    def test_nxos_vrf_address_fam_purged_nothing_to_remove(self):
        self.execute_show_command.return_value = self.PURGE_DEVICE
        set_module_args(dict(config=[dict(name="VRF9")], state="purged"))
        result = self.execute_module(changed=False)
        self.assertEqual(result["commands"], [])
