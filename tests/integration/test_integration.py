import subprocess


def test_integration(ansible_project, environment):
    playbook = str(ansible_project.playbook)
    inventory = str(ansible_project.inventory)
    command = f"ansible-navigator run {playbook} -i {inventory} --ee false --mode stdout"
    subprocess.check_call(
        command,
        shell=True,
        env=environment,
    )
