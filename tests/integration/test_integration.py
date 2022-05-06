import subprocess


def test_integration(ansible_project, environment):
    print(f"::group::{ansible_project.role}")
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
        ansible_project.playbook_artifact,
        "--ll",
        "debug",
        "--lf",
        ansible_project.log_file,
    ]
    try:
        subprocess.check_call(
            args,
            env=environment,
        )
    except subprocess.CalledProcessError as exc:
        print("::endgroup::")
        print(f"::error title=Integration test failure::{ansible_project.role}")
        raise exc
    print("::endgroup::")

