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

from copy import deepcopy
from textwrap import dedent
from unittest.mock import patch

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.cisco.nxos.plugins.modules import nxos_netflow_global
from ansible_collections.cisco.nxos.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
)

from .nxos_module import TestNxosModule, set_module_args


ignore_provider_arg = True

# `show running-config | section ^flow`: the lines that the device does not display are the defaults
BASE = dedent(
    """\
    flow timeout 30
    flow exporter EXP1
      description Collector 1
      destination 192.0.2.10 use-vrf management
      transport udp 9996
      source Ethernet1/1
      dscp 10
      version 9
        template data timeout 600
        option exporter-stats timeout 300
        option interface-table timeout 400
    flow exporter EXP2
      destination 2001:db8::1
      source loopback1
      version 9
    flow record REC4
      description IPv4 flows
      match ipv4 source address
      match ipv4 destination address
      match ip protocol
      match transport destination-port
      collect transport tcp flags
      collect counter bytes
      collect counter packets
      collect timestamp sys-uptime first
      collect timestamp sys-uptime last
      collect ip version
    flow record REC2
      match datalink mac source-address
      match datalink vlan
      collect counter bytes
    flow record REC6
      match ipv6 source address
      match ipv6 destination address
      match ipv6 flow-label
      match ipv6 options
      collect counter packets
    flow monitor MON1
      description Monitor 1
      record REC4
      exporter EXP1
      exporter EXP2
    flow monitor MON2
      record netflow ipv4 original-input
      exporter EXP2
    """,
)

BASE_FACTS = dict(
    timeout=30,
    exporters=[
        dict(
            name="EXP1",
            description="Collector 1",
            destination=dict(address="192.0.2.10", vrf="management"),
            transport_udp=9996,
            source="Ethernet1/1",
            dscp=10,
            template_data_timeout=600,
            option_exporter_stats_timeout=300,
            option_interface_table_timeout=400,
        ),
        dict(name="EXP2", destination=dict(address="2001:db8::1"), source="loopback1"),
    ],
    records=[
        dict(
            name="REC4",
            description="IPv4 flows",
            match=dict(
                ipv4=dict(source_address=True, destination_address=True),
                ip=dict(protocol=True),
                transport=dict(destination_port=True),
            ),
            collect=dict(
                transport_tcp_flags=True,
                counter=dict(bytes=True, packets=True),
                timestamp_sys_uptime=dict(first=True, last=True),
                ip_version=True,
            ),
        ),
        dict(
            name="REC2",
            match=dict(datalink=dict(mac_source_address=True, vlan=True)),
            collect=dict(counter=dict(bytes=True)),
        ),
        dict(
            name="REC6",
            match=dict(
                ipv6=dict(
                    source_address=True,
                    destination_address=True,
                    flow_label=True,
                    options=True,
                ),
            ),
            collect=dict(counter=dict(packets=True)),
        ),
    ],
    monitors=[
        dict(name="MON1", description="Monitor 1", record="REC4", exporters=["EXP1", "EXP2"]),
        dict(name="MON2", record="netflow ipv4 original-input", exporters=["EXP2"]),
    ],
)


class TestNxosNetflowGlobalModule(TestNxosModule):
    maxDiff = None
    module = nxos_netflow_global

    def setUp(self):
        super(TestNxosNetflowGlobalModule, self).setUp()

        self.mock_get_resource_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module_base.get_resource_connection",
        )
        self.get_resource_connection = self.mock_get_resource_connection.start()

        self.mock_get_config = patch(
            "ansible_collections.cisco.nxos.plugins.module_utils.network.nxos.facts.netflow_global.netflow_global.Netflow_globalFacts.get_config",
        )
        self.get_config = self.mock_get_config.start()
        self.get_config.return_value = BASE

    def tearDown(self):
        super(TestNxosNetflowGlobalModule, self).tearDown()
        self.mock_get_resource_connection.stop()
        self.mock_get_config.stop()

    def _run(self, changed, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(changed=changed)

    def _warned(self, changed, **args):
        """Run the module and return the result and the warnings."""
        set_module_args(args, ignore_provider_arg)
        with patch.object(AnsibleModule, "warn") as warn:
            result = self.execute_module(changed=changed)
        return result, [str(call.args[0]) for call in warn.call_args_list]

    def _fail(self, **args):
        set_module_args(args, ignore_provider_arg)
        return self.execute_module(failed=True)

    def _commands(self, state, config, changed=True):
        return self._run(changed, config=config, state=state)["commands"]

    # facts

    def test_nxos_netflow_global_parsed(self):
        result = self._run(False, running_config=BASE, state="parsed")
        self.assertEqual(result["parsed"], BASE_FACTS)

    def test_nxos_netflow_global_gathered(self):
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], BASE_FACTS)

    def test_nxos_netflow_global_gathered_nothing(self):
        self.get_config.return_value = ""
        result = self._run(False, state="gathered")
        self.assertEqual(result["gathered"], {})

    def test_nxos_netflow_global_parsed_texts_that_look_like_numbers(self):
        cfg = dedent(
            """\
            flow exporter 10
              description 123
              destination 192.0.2.1
              version 9
            flow record 1,2
              description 1.50
              match ip tos
            flow monitor 0x10
              record 7
              exporter 10
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                exporters=[
                    dict(name="10", description="123", destination=dict(address="192.0.2.1")),
                ],
                records=[dict(name="1,2", description="1.50", match=dict(ip=dict(tos=True)))],
                monitors=[dict(name="0x10", record="7", exporters=["10"])],
            ),
        )

    def test_nxos_netflow_global_parsed_lines_with_trailing_spaces(self):
        cfg = "flow exporter EXP1 \n  destination 192.0.2.1  \n  version 9 \n"
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(exporters=[dict(name="EXP1", destination=dict(address="192.0.2.1"))]),
        )

    def test_nxos_netflow_global_parsed_a_description_in_every_section(self):
        cfg = dedent(
            """\
            flow exporter E
              description exporter text
            flow record R
              description record text
            flow monitor M
              description monitor text
            """,
        )
        result = self._run(False, running_config=cfg, state="parsed")
        self.assertEqual(
            result["parsed"],
            dict(
                exporters=[dict(name="E", description="exporter text")],
                records=[dict(name="R", description="record text")],
                monitors=[dict(name="M", description="monitor text")],
            ),
        )

    # rendered

    def test_nxos_netflow_global_rendered(self):
        result = self._run(
            False,
            config=dict(
                timeout=20,
                exporters=[
                    dict(
                        name="E1",
                        description="text",
                        destination=dict(address="198.51.100.1", vrf="management"),
                        source="Eth1/2",
                        transport_udp=9000,
                        dscp=4,
                        template_data_timeout=100,
                        option_exporter_stats_timeout=200,
                        option_interface_table_timeout=300,
                    ),
                ],
                records=[
                    dict(
                        name="R1",
                        match=dict(ipv4=dict(source_address=True), ip=dict(tos=True)),
                        collect=dict(counter=dict(bytes=True)),
                    ),
                ],
                monitors=[dict(name="M1", record="R1", exporters=["E1"])],
            ),
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            [
                "flow timeout 20",
                "flow exporter E1",
                "description text",
                "destination 198.51.100.1 use-vrf management",
                "transport udp 9000",
                "source Ethernet1/2",
                "dscp 4",
                "version 9",
                "template data timeout 100",
                "option exporter-stats timeout 200",
                "option interface-table timeout 300",
                "flow record R1",
                "match ip tos",
                "match ipv4 source address",
                "collect counter bytes",
                "flow monitor M1",
                "record R1",
                "exporter E1",
            ],
        )

    def test_nxos_netflow_global_rendered_defaults_and_false_send_nothing(self):
        result = self._run(
            False,
            config=dict(
                timeout=10,
                exporters=[
                    dict(
                        name="E1",
                        destination=dict(address="192.0.2.1", vrf="default"),
                        transport_udp=9995,
                        dscp=0,
                        template_data_timeout=15,
                        option_exporter_stats_timeout=0,
                        option_interface_table_timeout=0,
                    ),
                ],
                records=[dict(name="R1", match=dict(ip=dict(tos=False)))],
            ),
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            ["flow exporter E1", "destination 192.0.2.1", "flow record R1"],
        )

    # merged

    def test_nxos_netflow_global_merged_from_empty(self):
        self.get_config.return_value = ""
        result = self._run(
            True,
            config=dict(
                exporters=[dict(name="E1", destination=dict(address="192.0.2.1"), dscp=3)],
                monitors=[dict(name="M1", record="netflow-original", exporters=["E1"])],
            ),
            state="merged",
        )
        self.assertEqual(
            result["commands"],
            [
                "flow exporter E1",
                "destination 192.0.2.1",
                "dscp 3",
                "flow monitor M1",
                "record netflow-original",
                "exporter E1",
            ],
        )

    def test_nxos_netflow_global_merged_idempotent(self):
        self._run(False, config=deepcopy(BASE_FACTS), state="merged")

    def test_nxos_netflow_global_merged_idempotent_a_subset(self):
        config = dict(
            exporters=[dict(name="EXP1", dscp=10)],
            monitors=[dict(name="MON1", exporters=["EXP2"])],
        )
        self._run(False, config=config, state="merged")

    def test_nxos_netflow_global_merged_keeps_what_is_not_given(self):
        commands = self._commands(
            "merged",
            dict(
                exporters=[dict(name="EXP1", dscp=11)],
                records=[dict(name="REC2", match=dict(datalink=dict(ethertype=True)))],
            ),
        )
        self.assertEqual(
            commands,
            ["flow exporter EXP1", "dscp 11", "flow record REC2", "match datalink ethertype"],
        )

    def test_nxos_netflow_global_merged_defaults_and_false_remove_the_setting(self):
        commands = self._commands(
            "merged",
            dict(
                timeout=10,
                exporters=[
                    dict(
                        name="EXP1",
                        dscp=0,
                        transport_udp=9995,
                        template_data_timeout=15,
                        option_exporter_stats_timeout=0,
                        destination=dict(address="192.0.2.10", vrf="management"),
                    ),
                ],
                records=[
                    dict(
                        name="REC4",
                        match=dict(ip=dict(protocol=False)),
                        collect=dict(counter=dict(bytes=False)),
                    ),
                ],
            ),
        )
        self.assertEqual(
            commands,
            [
                "no flow timeout",
                "flow exporter EXP1",
                "no transport udp",
                "no dscp",
                "version 9",
                "template data timeout 15",
                "option exporter-stats timeout 0",
                "flow record REC4",
                "no match ip protocol",
                "no collect counter bytes",
            ],
        )

    def test_nxos_netflow_global_merged_defaults_and_false_on_a_clean_switch_send_nothing(self):
        self.get_config.return_value = ""
        result = self._run(
            False,
            config=dict(timeout=10),
            state="merged",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_netflow_global_merged_monitor_exporters_are_added(self):
        commands = self._commands(
            "merged",
            dict(monitors=[dict(name="MON2", exporters=["EXP1"])]),
        )
        self.assertEqual(commands, ["flow monitor MON2", "exporter EXP1"])

    def test_nxos_netflow_global_merged_destination_without_vrf_resets_the_vrf(self):
        commands = self._commands(
            "merged",
            dict(exporters=[dict(name="EXP1", destination=dict(address="192.0.2.77"))]),
        )
        self.assertEqual(
            commands,
            ["flow exporter EXP1", "destination 192.0.2.77 use-vrf default"],
        )

    def test_nxos_netflow_global_merged_interface_names_are_normalised(self):
        self._run(
            False,
            config=dict(
                exporters=[dict(name="EXP1", source="Eth1/1"), dict(name="EXP2", source="Lo1")],
            ),
            state="merged",
        )

    def test_nxos_netflow_global_merged_new_entity_without_settings(self):
        commands = self._commands("merged", dict(records=[dict(name="NEW")]))
        self.assertEqual(commands, ["flow record NEW"])

    # replaced

    def test_nxos_netflow_global_replaced(self):
        commands = self._commands(
            "replaced",
            dict(
                exporters=[
                    dict(name="EXP1", destination=dict(address="192.0.2.99"), dscp=5),
                ],
                records=[
                    dict(
                        name="REC6",
                        match=dict(ipv4=dict(source_address=True)),
                        collect=dict(counter=dict(packets=True)),
                    ),
                ],
                monitors=[dict(name="MON1", exporters=["EXP2"], record="REC4")],
            ),
        )
        self.assertEqual(
            commands,
            [
                # the monitor loses an exporter first
                "flow monitor MON1",
                "no description",
                "no exporter EXP1",
                "no flow timeout",
                "flow exporter EXP1",
                "no description",
                "no transport udp",
                "no source",
                "destination 192.0.2.99 use-vrf default",
                "dscp 5",
                "version 9",
                "template data timeout 15",
                "option exporter-stats timeout 0",
                "option interface-table timeout 0",
                # the record is of another type, what is of the old type is removed first
                "flow record REC6",
                "no match ipv6 source address",
                "no match ipv6 destination address",
                "no match ipv6 flow-label",
                "no match ipv6 options",
                "match ipv4 source address",
            ],
        )

    def test_nxos_netflow_global_replaced_idempotent(self):
        self._run(False, config=deepcopy(BASE_FACTS), state="replaced")

    def test_nxos_netflow_global_replaced_does_not_touch_the_other_entities(self):
        config = dict(timeout=30, exporters=[deepcopy(BASE_FACTS["exporters"][1])])
        self._run(False, config=config, state="replaced")

    def test_nxos_netflow_global_replaced_resets_the_timeout_that_is_not_given(self):
        config = dict(exporters=deepcopy(BASE_FACTS["exporters"][1:]))
        commands = self._commands("replaced", config)
        self.assertEqual(commands, ["no flow timeout"])

    def test_nxos_netflow_global_replaced_the_record_of_a_monitor_cannot_be_removed(self):
        config = dict(timeout=30, monitors=[dict(name="MON2", exporters=["EXP2"])])
        self._run(False, config=config, state="replaced")

    def test_nxos_netflow_global_replaced_the_record_of_a_monitor_is_replaced(self):
        config = dict(
            timeout=30,
            monitors=[dict(name="MON2", record="netflow-original", exporters=["EXP2"])],
        )
        commands = self._commands("replaced", config)
        self.assertEqual(commands, ["flow monitor MON2", "record netflow-original"])

    def test_nxos_netflow_global_replaced_new_entities_and_the_order(self):
        config = dict(
            timeout=30,
            monitors=[dict(name="NEWMON", record="NEWREC", exporters=["NEWEXP"])],
            records=[dict(name="NEWREC", match=dict(ip=dict(protocol=True)))],
            exporters=[dict(name="NEWEXP", destination=dict(address="192.0.2.5"))],
        )
        commands = self._commands("replaced", config)
        self.assertEqual(
            commands,
            [
                "flow exporter NEWEXP",
                "destination 192.0.2.5",
                "flow record NEWREC",
                "match ip protocol",
                "flow monitor NEWMON",
                "record NEWREC",
                "exporter NEWEXP",
            ],
        )

    # overridden

    def test_nxos_netflow_global_overridden(self):
        config = dict(
            timeout=30,
            exporters=[deepcopy(BASE_FACTS["exporters"][1])],
            records=[deepcopy(BASE_FACTS["records"][2])],
            monitors=[dict(name="MON2", record="netflow ipv4 original-input", exporters=["EXP2"])],
        )
        commands = self._commands("overridden", config)
        self.assertEqual(
            commands,
            [
                "no flow monitor MON1",
                "no flow record REC4",
                "no flow record REC2",
                "no flow exporter EXP1",
            ],
        )

    def test_nxos_netflow_global_overridden_idempotent(self):
        self._run(False, config=deepcopy(BASE_FACTS), state="overridden")

    # deleted

    def test_nxos_netflow_global_deleted(self):
        commands = self._run(True, state="deleted")["commands"]
        self.assertEqual(
            commands,
            [
                "no flow monitor MON1",
                "no flow monitor MON2",
                "no flow record REC4",
                "no flow record REC2",
                "no flow record REC6",
                "no flow exporter EXP1",
                "no flow exporter EXP2",
                "no flow timeout",
            ],
        )

    def test_nxos_netflow_global_deleted_the_listed_entities(self):
        commands = self._commands(
            "deleted",
            dict(
                exporters=[dict(name="EXP2"), dict(name="UNKNOWN")],
                monitors=[dict(name="MON2")],
            ),
        )
        self.assertEqual(commands, ["no flow monitor MON2", "no flow exporter EXP2"])

    def test_nxos_netflow_global_deleted_the_timeout(self):
        commands = self._commands("deleted", dict(timeout=30))
        self.assertEqual(commands, ["no flow timeout"])

    def test_nxos_netflow_global_deleted_nothing_to_delete(self):
        self.get_config.return_value = ""
        self._run(False, state="deleted")

    def test_nxos_netflow_global_deleted_unknown_entities(self):
        self._run(False, config=dict(records=[dict(name="UNKNOWN")]), state="deleted")

    # validation

    def test_nxos_netflow_global_validation(self):
        for config in (
            dict(timeout=4),
            dict(timeout=61),
            dict(exporters=[dict(name="E", transport_udp=0)]),
            dict(exporters=[dict(name="E", transport_udp=65536)]),
            dict(exporters=[dict(name="E", dscp=64)]),
            dict(exporters=[dict(name="E", template_data_timeout=0)]),
            dict(exporters=[dict(name="E", option_exporter_stats_timeout=86401)]),
            dict(exporters=[dict(name="E", option_interface_table_timeout=-1)]),
            dict(exporters=[dict(name="E"), dict(name="E")]),
            dict(monitors=[dict(name="M", exporters=["A", "B", "C"])]),
        ):
            for state in ("merged", "replaced", "overridden", "rendered"):
                self._fail(config=config, state=state)

    def test_nxos_netflow_global_monitor_exporters_of_the_device_are_not_validated(self):
        self._run(False, state="gathered")

    def test_nxos_netflow_global_merged_too_many_exporters_with_the_ones_of_the_device(self):
        result = self._fail(
            config=dict(
                exporters=[dict(name="EXP3", destination=dict(address="192.0.2.3"))],
                monitors=[dict(name="MON1", exporters=["EXP3"])],
            ),
            state="merged",
        )
        self.assertIn("2 exporters at most", result["msg"])

    def test_nxos_netflow_global_empty_config(self):
        for state in ("merged", "replaced", "overridden", "rendered"):
            self._fail(config={}, state=state)

    def test_nxos_netflow_global_check_mode_sends_nothing(self):
        set_module_args(
            dict(config=dict(timeout=40), state="merged", _ansible_check_mode=True),
            ignore_provider_arg,
        )
        result = self.execute_module(changed=True)
        self.assertEqual(result["commands"], ["flow timeout 40"])
        self.get_resource_connection.return_value.edit_config.assert_not_called()

    # negative cases: the argument specification

    def test_nxos_netflow_global_negative_argspec(self):
        cases = [
            (dict(config=dict(timeout="abc"), state="merged"), "is of type"),
            (dict(config=dict(bogus=1), state="merged"), "Unsupported parameters"),
            (
                dict(config=dict(exporters=[dict(description="x")]), state="merged"),
                "missing required arguments: name",
            ),
            (
                dict(
                    config=dict(exporters=[dict(name="E", destination=dict(vrf="management"))]),
                    state="merged",
                ),
                "missing required arguments: address",
            ),
            (
                dict(config=dict(exporters=[dict(name="E", dscp="high")]), state="merged"),
                "is of type",
            ),
            (
                dict(
                    config=dict(
                        records=[dict(name="R", match=dict(ipv4=dict(source_address="maybe")))],
                    ),
                    state="merged",
                ),
                "boolean",
            ),
            (dict(config=dict(timeout=20), state="bogus"), "value of state must be one of"),
            (
                dict(config=dict(timeout=20), running_config="x", state="merged"),
                "mutually exclusive",
            ),
            (
                dict(config=dict(timeout=20), running_config="x", state="rendered"),
                "mutually exclusive",
            ),
            (dict(state="parsed"), "state is parsed but all of the following are missing"),
            (dict(state="merged"), "state is merged but all of the following are missing"),
            (dict(state="rendered"), "state is rendered but all of the following are missing"),
        ]
        for args, text in cases:
            result = self._fail(**args)
            self.assertIn(text, result["msg"], args)

    def test_nxos_netflow_global_negative_empty_running_config_for_parsed(self):
        result = self._fail(running_config="", state="parsed")
        self.assertIn("must not be empty", result["msg"])

    def test_nxos_netflow_global_negative_parsed_garbage(self):
        result = self._run(
            False,
            running_config="garbage\nflow exporter\n  foo bar\n!!\n",
            state="parsed",
        )
        self.assertEqual(result["parsed"], {})

    def test_nxos_netflow_global_negative_values_out_of_range(self):
        for key, value in (
            ("timeout", 0),
            ("timeout", 100),
        ):
            result = self._fail(config={key: value}, state="merged")
            self.assertIn("must be in the range 5-60", result["msg"])
        result = self._fail(
            config=dict(exporters=[dict(name="E", dscp=-1)]),
            state="replaced",
        )
        self.assertIn("dscp must be in the range 0-63", result["msg"])

    def test_nxos_netflow_global_negative_destination_is_not_an_address(self):
        for address in ("999.1.1.1", "collector", "2001:db8::g", "192.0.2"):
            result = self._fail(
                config=dict(exporters=[dict(name="E", destination=dict(address=address))]),
                state="merged",
            )
            self.assertIn("IPv4 or IPv6 address", result["msg"])

    # negative cases: references and dependencies

    def test_nxos_netflow_global_negative_monitor_uses_unknown_objects(self):
        for state in ("merged", "replaced", "overridden"):
            result = self._fail(
                config=dict(monitors=[dict(name="NEW", record="NOREC")]),
                state=state,
            )
            self.assertIn("record 'NOREC' that does not exist", result["msg"])
            result = self._fail(
                config=dict(monitors=[dict(name="NEW", exporters=["NOEXP"])]),
                state=state,
            )
            self.assertIn("exporter 'NOEXP' that does not exist", result["msg"])

    def test_nxos_netflow_global_negative_rendered_does_not_check_references(self):
        result = self._run(
            False,
            config=dict(monitors=[dict(name="NEW", record="NOREC", exporters=["NOEXP"])]),
            state="rendered",
        )
        self.assertEqual(
            result["rendered"],
            ["flow monitor NEW", "record NOREC", "exporter NOEXP"],
        )

    def test_nxos_netflow_global_negative_predefined_records_and_new_objects_are_accepted(self):
        commands = self._commands(
            "merged",
            dict(
                exporters=[dict(name="NEWEXP", destination=dict(address="192.0.2.5"))],
                records=[dict(name="NEWREC", match=dict(ip=dict(tos=True)))],
                monitors=[
                    dict(
                        name="A",
                        record="netflow ipv6 original-input",
                        exporters=["NEWEXP", "EXP1"],
                    ),
                    dict(name="B", record="NEWREC"),
                ],
            ),
        )
        self.assertIn("record netflow ipv6 original-input", commands)
        self.assertIn("record NEWREC", commands)

    def test_nxos_netflow_global_negative_overridden_cannot_keep_a_reference_to_what_it_removes(
        self,
    ):
        result = self._fail(
            config=dict(
                exporters=[dict(name="EXP1", destination=dict(address="192.0.2.10"))],
                monitors=[dict(name="MON1", exporters=["EXP1", "EXP2"])],
            ),
            state="overridden",
        )
        self.assertIn("exporter 'EXP2' that does not exist", result["msg"])

    def test_nxos_netflow_global_negative_third_exporter_of_a_monitor(self):
        for state in ("merged", "replaced", "overridden", "rendered"):
            result = self._fail(
                config=dict(
                    exporters=[
                        dict(name="EXP1", destination=dict(address="192.0.2.10")),
                        dict(name="EXP2", destination=dict(address="192.0.2.11")),
                        dict(name="EXP3", destination=dict(address="192.0.2.12")),
                    ],
                    monitors=[dict(name="NEW", exporters=["EXP1", "EXP2", "EXP3"])],
                ),
                state=state,
            )
            self.assertIn("2 exporters at most", result["msg"])

    def test_nxos_netflow_global_negative_duplicate_exporters_of_a_monitor_count_once(self):
        commands = self._commands(
            "merged",
            dict(monitors=[dict(name="NEW", exporters=["EXP1", "EXP1"])]),
        )
        self.assertEqual(commands, ["flow monitor NEW", "exporter EXP1"])

    def test_nxos_netflow_global_negative_record_types_cannot_be_mixed(self):
        cases = [
            # merged adds to what the device has: REC4 is IPv4, REC2 is Layer 2, REC6 is IPv6
            ("REC4", dict(match=dict(ipv6=dict(source_address=True))), "ipv4 and ipv6"),
            ("REC4", dict(match=dict(datalink=dict(vlan=True))), "datalink"),
            ("REC6", dict(match=dict(ipv4=dict(source_address=True))), "ipv4 and ipv6"),
            ("REC2", dict(match=dict(ipv4=dict(source_address=True))), "datalink"),
            ("REC2", dict(match=dict(ip=dict(tos=True))), "datalink"),
            ("REC2", dict(match=dict(transport=dict(source_port=True))), "datalink"),
            ("REC2", dict(collect=dict(ip_version=True)), "datalink"),
            ("REC2", dict(collect=dict(transport_tcp_flags=True)), "datalink"),
        ]
        for name, settings, text in cases:
            result = self._fail(config=dict(records=[dict(name=name, **settings)]), state="merged")
            self.assertIn(text, result["msg"], (name, settings))

    def test_nxos_netflow_global_negative_record_types_in_one_new_record(self):
        for state in ("merged", "replaced", "overridden", "rendered"):
            self._fail(
                config=dict(
                    records=[
                        dict(
                            name="NEW",
                            match=dict(datalink=dict(vlan=True), ipv4=dict(source_address=True)),
                        ),
                    ],
                ),
                state=state,
            )

    def test_nxos_netflow_global_negative_record_type_can_change_with_replaced_and_merged_false(
        self,
    ):
        commands = self._commands(
            "merged",
            dict(
                records=[
                    dict(
                        name="REC6",
                        match=dict(
                            ipv6=dict(
                                source_address=False,
                                destination_address=False,
                                flow_label=False,
                                options=False,
                            ),
                            ipv4=dict(source_address=True),
                        ),
                    ),
                ],
            ),
        )
        self.assertEqual(
            commands,
            [
                "flow record REC6",
                "no match ipv6 source address",
                "no match ipv6 destination address",
                "no match ipv6 flow-label",
                "no match ipv6 options",
                "match ipv4 source address",
            ],
        )

    def test_nxos_netflow_global_negative_deleting_what_is_used_removes_it_from_the_monitors(self):
        # the device removes the exporter and the record from the monitors, the module only deletes them
        commands = self._commands(
            "deleted",
            dict(exporters=[dict(name="EXP1")], records=[dict(name="REC4")]),
        )
        self.assertEqual(commands, ["no flow record REC4", "no flow exporter EXP1"])

    # negative cases: empty or missing configuration, the modes

    def test_nxos_netflow_global_negative_no_feature_gives_nothing(self):
        self.get_config.return_value = ""
        self._run(False, state="gathered")
        self._run(False, state="deleted")
        self._run(False, config=dict(timeout=10), state="replaced")
        self._run(False, config=dict(timeout=10), state="overridden")
        result = self._run(False, config=dict(timeout=20), state="rendered")
        self.assertEqual(result["rendered"], ["flow timeout 20"])

    def test_nxos_netflow_global_negative_overridden_with_a_default_removes_everything(self):
        commands = self._commands("overridden", dict(timeout=10))
        self.assertEqual(
            commands,
            [
                "no flow monitor MON1",
                "no flow monitor MON2",
                "no flow record REC4",
                "no flow record REC2",
                "no flow record REC6",
                "no flow exporter EXP1",
                "no flow exporter EXP2",
                "no flow timeout",
            ],
        )

    def test_nxos_netflow_global_negative_empty_lists_are_empty_config(self):
        for state in ("merged", "replaced", "overridden"):
            self._fail(config=dict(exporters=[], records=[], monitors=[]), state=state)

    def test_nxos_netflow_global_negative_deleted_with_empty_config_deletes_everything(self):
        commands = self._run(True, config={}, state="deleted")["commands"]
        self.assertEqual(len(commands), 8)

    def test_nxos_netflow_global_negative_check_mode_and_diff_mode_change_nothing(self):
        for extra in (
            dict(_ansible_check_mode=True),
            dict(_ansible_diff=True, _ansible_check_mode=True),
        ):
            self.get_resource_connection.return_value.edit_config.reset_mock()
            set_module_args(
                dict(
                    config=dict(
                        exporters=[dict(name="NEW", destination=dict(address="192.0.2.9"))],
                    ),
                    state="merged",
                    **extra,
                ),
                ignore_provider_arg,
            )
            result = self.execute_module(changed=True)
            self.assertEqual(result["commands"], ["flow exporter NEW", "destination 192.0.2.9"])
            self.get_resource_connection.return_value.edit_config.assert_not_called()

    # negative cases: names

    def test_nxos_netflow_global_negative_interface_name_variants_are_idempotent(self):
        for ethernet in ("Eth1/1", "eth1/1", "ethernet1/1", "Ethernet1/1", "ETHERNET1/1"):
            for loopback in ("lo1", "Lo1", "loopback1", "Loopback1", "LOOPBACK1"):
                self._run(
                    False,
                    config=dict(
                        exporters=[
                            dict(name="EXP1", source=ethernet),
                            dict(name="EXP2", source=loopback),
                        ],
                    ),
                    state="merged",
                )

    def test_nxos_netflow_global_negative_other_interface_names(self):
        commands = self._commands(
            "merged",
            dict(
                exporters=[
                    dict(name="A", source="Po10"),
                    dict(name="B", source="vlan 10"),
                    dict(name="C", source="MGMT0"),
                    dict(name="D", source="port-channel 11"),
                ],
            ),
        )
        self.assertIn("source port-channel10", commands)
        self.assertIn("source Vlan10", commands)
        self.assertIn("source mgmt0", commands)
        self.assertIn("source port-channel11", commands)

    def test_nxos_netflow_global_negative_names_are_case_sensitive(self):
        # the device keeps the case of the names, exp1 is another exporter than EXP1
        commands = self._commands(
            "merged",
            dict(exporters=[dict(name="exp1", destination=dict(address="192.0.2.1"))]),
        )
        self.assertEqual(commands, ["flow exporter exp1", "destination 192.0.2.1"])

    def test_nxos_netflow_global_negative_vrf_default_in_any_case_is_the_default(self):
        self._run(
            False,
            config=dict(
                exporters=[
                    dict(name="EXP2", destination=dict(address="2001:db8::1", vrf="default")),
                ],
            ),
            state="merged",
        )

    # reviewer lessons: CRLF, values only the device has, warnings, garbage

    def test_nxos_netflow_global_crlf_and_trailing_spaces_gathered_and_parsed(self):
        crlf = BASE.replace("\n", "\r\n")
        spaces = "".join(line + "  \n" for line in BASE.splitlines())
        for text in (crlf, spaces, crlf.replace("\r\n", " \r\n")):
            result = self._run(False, running_config=text, state="parsed")
            self.assertEqual(result["parsed"], BASE_FACTS)
            self.get_config.return_value = text
            result = self._run(False, state="gathered")
            self.assertEqual(result["gathered"], BASE_FACTS)
            self._run(False, config=deepcopy(BASE_FACTS), state="replaced")
        self.get_config.return_value = BASE

    def test_nxos_netflow_global_parsed_garbage_never_gives_a_traceback(self):
        huge = "9" * 400
        samples = [
            "",
            "\n\n  \n",
            "flow",
            "flow exporter",
            "flow exporter  \n  destination",
            "flow timeout\nflow timeout x\nflow timeout " + huge,
            "flow exporter E\n  transport udp " + huge + "\n  dscp -5\n  template data timeout 1e5",
            "flow exporter E\n  destination " + "x" * 5000 + " use-vrf",
            "flow exporter E\n  source\n  description\n  version\n  option exporter-stats timeout",
            "flow record R\n  match\n  collect counter\n  match ipv4 source address extra",
            "flow monitor M\n  exporter\n  record\n  exporter " + huge,
            "\x00\x01\x02 flow exporter E\r\r\n\xff\xfe",
            "flow exporter E\n\tdestination 192.0.2.1\n",
            "interface Ethernet1/1\n  ip flow monitor M input\n",
        ]
        for text in samples:
            set_module_args(dict(running_config=text, state="parsed"), ignore_provider_arg)
            try:
                self.module.main()
            except (AnsibleExitJson, AnsibleFailJson):
                continue
            self.fail("the module did not exit for {0!r}".format(text))

    def test_nxos_netflow_global_unparsed_lines_are_reported_and_not_removed(self):
        cfg = dedent(
            """\
            flow exporter EXP1
              destination 192.0.2.10
              something new 5
              version 9
            flow record REC1
              match input interface
              match flow direction
              match ipv4 source address
            """,
        )
        result, warnings = self._warned(False, running_config=cfg, state="parsed")
        self.assertEqual(len(warnings), 1)
        self.assertIn("something new 5", warnings[0])
        self.assertNotIn("match input interface", warnings[0])
        self.get_config.return_value = cfg
        # an unknown line is not turned into something to remove or to add
        result, _warnings = self._warned(
            False,
            config=dict(
                exporters=[dict(name="EXP1", destination=dict(address="192.0.2.10"))],
                records=[dict(name="REC1", match=dict(ipv4=dict(source_address=True)))],
            ),
            state="overridden",
        )
        self.assertEqual(result["commands"], [])

    def test_nxos_netflow_global_values_only_the_device_has_are_not_validated(self):
        odd = dedent(
            """\
            flow timeout 9999
            flow exporter ODD
              destination not-an-address use-vrf management
              transport udp 99999
              dscp 99
              source nosuchtype7
              version 9
                template data timeout 0
            flow record ODDREC
              match ipv4 source address
              match ipv6 source address
              match datalink vlan
            flow monitor ODDMON
              record missing-record
              exporter A
              exporter B
              exporter C
            """,
        )
        self.get_config.return_value = odd
        for state, config in (
            ("merged", dict(exporters=[dict(name="NEW", destination=dict(address="192.0.2.1"))])),
            ("merged", dict(timeout=20)),
            ("replaced", dict(records=[dict(name="NEWREC", match=dict(ip=dict(tos=True)))])),
            ("deleted", dict(exporters=[dict(name="NEW")])),
            ("deleted", None),
            ("replaced", dict(monitors=[dict(name="NEWMON", record="netflow-original")])),
        ):
            args = dict(state=state)
            if config:
                args["config"] = config
            self._run(state != "deleted" or config is None, **args)
        # what the device has can also be replaced and deleted
        result = self._run(True, config=dict(exporters=[dict(name="ODD")]), state="overridden")
        self.assertIn("no flow monitor ODDMON", result["commands"])

    def test_nxos_netflow_global_deleted_warns_about_the_names_that_are_not_configured(self):
        result, warnings = self._warned(
            False,
            config=dict(
                exporters=[dict(name="NOEXP")],
                records=[dict(name="NOREC1"), dict(name="NOREC2")],
            ),
            state="deleted",
        )
        self.assertEqual(result["commands"], [])
        self.assertEqual(len(warnings), 2)
        self.assertIn("exporters NOEXP", warnings[0])
        self.assertIn("records NOREC1, NOREC2", warnings[1])

    def test_nxos_netflow_global_deleted_warns_only_for_the_missing_names(self):
        result, warnings = self._warned(
            True,
            config=dict(exporters=[dict(name="EXP2"), dict(name="NOEXP")]),
            state="deleted",
        )
        self.assertEqual(result["commands"], ["no flow exporter EXP2"])
        self.assertEqual(len(warnings), 1)

    def test_nxos_netflow_global_commands_order_for_the_device(self):
        # the monitors lose their references first, then what is not wanted is deleted, then the
        # exporters, the records and last the monitors that use them are written
        commands = self._commands(
            "overridden",
            dict(
                exporters=[
                    dict(name="EXP2", destination=dict(address="2001:db8::1"), source="lo1"),
                    dict(name="NEWEXP"),
                ],
                records=[dict(name="NEWREC", match=dict(ip=dict(tos=True)))],
                monitors=[dict(name="MON2", record="NEWREC", exporters=["NEWEXP"])],
            ),
        )
        self.assertEqual(
            commands,
            [
                "flow monitor MON2",
                "no exporter EXP2",
                "no flow monitor MON1",
                "no flow record REC4",
                "no flow record REC2",
                "no flow record REC6",
                "no flow exporter EXP1",
                "no flow timeout",
                "flow exporter NEWEXP",
                "flow record NEWREC",
                "match ip tos",
                "flow monitor MON2",
                "record NEWREC",
                "exporter NEWEXP",
            ],
        )
