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
