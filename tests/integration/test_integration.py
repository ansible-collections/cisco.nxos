import subprocess


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
        ansible_project.playbook_artifact,
        "--ll",
        "debug",
        "--lf",
        ansible_project.log_file,
    ]
    subprocess.check_call(
        args,
        env=environment,
    )
