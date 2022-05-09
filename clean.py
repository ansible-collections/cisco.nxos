# cspell:ignore nxapi, nxos, rglob
from typing import OrderedDict
from ansiblelint.yaml_utils import (
    FormattedYAML,
    CommentedSeq,
    CommentToken,
)
from pathlib import Path
from copy import deepcopy

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


file_name = "tests/integration/targets/nxos_bgp_address_family/tasks/main.yaml"
yaml = FormattedYAML()
yaml.preserve_quotes = True


builtins = [
    "add_host",
    "apt",
    "apt_key",
    "apt_repository",
    "assemble",
    "assert",
    "async_status",
    "blockinfile",
    "command",
    "copy",
    "cron",
    "debconf",
    "debug",
    "dnf",
    "dpkg_selections",
    "expect",
    "fail",
    "fetch",
    "file",
    "find",
    "gather_facts",
    "get_url",
    "getent",
    "git",
    "group",
    "group_by",
    "hostname",
    "import_playbook",
    "import_role",
    "import_tasks",
    "include",
    "include_role",
    "include_tasks",
    "include_vars",
    "iptables",
    "known_hosts",
    "lineinfile",
    "meta",
    "package",
    "package_facts",
    "pause",
    "ping",
    "pip",
    "raw",
    "reboot",
    "replace",
    "rpm_key",
    "script",
    "service",
    "service_facts",
    "set_fact",
    "set_stats",
    "setup",
    "shell",
    "slurp",
    "stat",
    "subversion",
    "systemd",
    "sysvinit",
    "tempfile",
    "template",
    "unarchive",
    "uri",
    "user",
    "validate_argument_spec",
    "wait_for",
    "wait_for_connection",
    "yum",
    "yum_repository",
]


def change_key(task, old, new):
    if old in task.ca.items:
        task.ca.items[new] = task.ca.items.pop(old)
    for _ in range(len(task)):
        k, v = task.popitem(False)
        task[new if old == k else k] = v


def update_include_cli(data):
    match = [
        idx
        for idx, item in enumerate(data)
        if item.get("include") == "cli.yaml"
    ]
    if not match:
        return

    name = "Include the CLI tasks"
    for entry in match:
        data[entry]["name"] = name
        data[entry].move_to_end("name", last=False)
        change_key(data[entry], "include", "ansible.builtin.include_tasks")
    return


def update_include_nxapi(data):
    match = [
        idx
        for idx, item in enumerate(data)
        if item.get("include") == "nxapi.yaml"
    ]
    if not match:
        return

    name = "Include the NX-API tasks"
    for entry in match:
        data[entry]["name"] = name
        data[entry].move_to_end("name", last=False)
        change_key(data[entry], "include", "ansible.builtin.include_tasks")
    return


def update_builtins(data):
    for task in data:
        for plugin in builtins:
            if task.get(plugin):
                new_name = f"ansible.builtin.{plugin}"
                change_key(task, plugin, new_name)


def capitalize_names(data):
    for task in data:
        if task.get("name"):
            task["name"] = task["name"].capitalize()
            task.move_to_end("name", last=False)


def set_style(d, flow):
    if isinstance(d, dict):
        if flow:
            d.fa.set_flow_style()
        else:
            d.fa.set_block_style()
        for k in d:
            set_style(d[k], flow)
    elif isinstance(d, list):
        if flow:
            d.fa.set_flow_style()
        else:
            d.fa.set_block_style()
        for item in d:
            set_style(item, flow)


def update_list_of_tasks(list_of_tasks):
    update_include_cli(list_of_tasks)
    update_include_nxapi(list_of_tasks)
    update_builtins(list_of_tasks)
    capitalize_names(list_of_tasks)


def update(file_path):
    data = yaml.load(file_path)
    if not isinstance(data, CommentedSeq):
        logger.info("Skipping: %s", file_path)
        return

    logger.info("Updating: %s", file_path)
    update_list_of_tasks(data)

    for block_part in ["block", "rescue", "always"]:
        ids = [idx for idx, entry in enumerate(data) if entry.get(block_part)]
        for block_id in ids:
            # Remove blank line comments from the block
            update_list_of_tasks(data[block_id][block_part])

    # set_style(data, flow=False)

    logger.info("Writing: %s", file_path)

    with file_path.open(mode="w") as fh:
        yaml.dump(data, fh)


def main():
    path = Path("tests")
    for file_path in sorted(path.rglob("*")):
        if file_path.suffix in [".yaml", ".yml"]:
            update(file_path)


if __name__ == "__main__":
    main()
