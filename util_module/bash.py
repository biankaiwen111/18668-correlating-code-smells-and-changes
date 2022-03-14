import subprocess

"""
    if shell is True, the command will be executed through the shell,
    if check is True, and the process exits with a non-zero exit code, a CalledProcessError exception will be raised
    if capture_output is True, stdout and stderr will be captured
"""


def run_command(command, verbose=True):
    subprocess.run(command, shell=True, check=True, capture_output=not verbose)

