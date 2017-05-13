import subprocess


def run(command, *args):
    command = command.split() + list(args)
    command = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if command == 0:
        return command.stdout
    else:
        return command.stderr
