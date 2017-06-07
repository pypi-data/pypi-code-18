import sys
import subprocess

# Syncronously runs a shell command and returns STDOUT as a string
def run(command):
    return subprocess.check_output(command.split(' ')).rstrip('\n')