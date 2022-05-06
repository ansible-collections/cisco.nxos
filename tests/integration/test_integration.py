import os
import subprocess

def log(message):
    if os.environ.get('GITHUB_ACTIONS'):
        print(f"\n{message}", flush=True)

def test_integration(ansible_project, environment):
    log(f"::group::{ansible_project.role}")
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
        "local,nxapi"
    ]
    log(" ".join(args))
    try:
        subprocess.check_call(
            args,
            env=environment,
        )
    except subprocess.CalledProcessError as exc:
        log("::endgroup::")
        log(f"::error title=Integration test failure::{ansible_project.role}", flush=True)
        raise exc
    log("::endgroup::")

