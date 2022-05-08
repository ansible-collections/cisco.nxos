import os
import subprocess

import logging
import pytest


def test_integration(ansible_project, environment):
    args = [
        "ansible-navigator",
        "run",
        str(ansible_project.playbook),
        "-i",
        str(ansible_project.inventory),
        "--ee",
        "false",
        "--mode",
        "stdout",
        "--pas",
        str(ansible_project.playbook_artifact),
        "--ll",
        "debug",
        "--lf",
        str(ansible_project.log_file),
        "--skip-tags",
        "local,nxapi",
    ]
    logging.info(" ".join(args))
    try:
        subprocess.check_call(
            args,
            env=environment,
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(msg=f"Integration test failed: {ansible_project.role}")
