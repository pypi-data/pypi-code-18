""" Facade for Git commands. Do not use any of the below commands with user input. """

from collections import OrderedDict
from qi import run
import subprocess
import os

def history():
    p = subprocess.Popen(['git', 'log', '--first-parent' ,'--pretty=%H:%cd', '--date=unix'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        sha, timestamp = line.rstrip().split(':')
        yield [sha, int(timestamp)]
		
def inittime():
    """ Get UNIX timestamp for initial commit """
    p = subprocess.Popen(['git', 'log', '--first-parent', '--reverse', '--pretty=%cd', '--date=unix'], stdout=subprocess.PIPE)
    return int(subprocess.check_output(['head', '-n', '1'], stdin=p.stdout).rstrip())

def checkout(opts):
    """ Run git-checkout using provided options. """
    return run(r'git checkout --quiet -f {}'.format(opts))

def currentpathspec():
    """ Returns working pathspec (may be branch name or SHA hash if on detached HEAD) """
    out = run(r'git rev-parse --abbrev-ref HEAD')
    return run(r'git rev-parse HEAD') if out == 'HEAD' else out

def committime(pathspec=''):
    """ Returns UNIX timestamp for the object's committer time. """
    return int(run(r'git show -s --format=%cd --date=unix {}'.format(pathspec)))

def headtime():
    return committime('HEAD')

def commitdate(pathspec=''):
    """ Returns friendly date for pathspec. """
    return run(r'git show -s --date=local --format=%cd {}'.format(pathspec))

def visitroot():
    """ Navigates to the root of the Git repository. Returns True if successful. """
    try:
        os.chdir(run(r'git rev-parse --show-toplevel'))
    except subprocess.CalledProcessError as err:
        return False

    return True
