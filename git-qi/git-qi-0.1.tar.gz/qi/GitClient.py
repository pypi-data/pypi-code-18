""" Facade for Git commands. Do not use any of the below commands with user input. """

from collections import OrderedDict
from qi import run
import subprocess
import os


def initialcommit(preferred_orphan=0):
	""" Get SHA-1 hash for initial commit. """
	return run('git rev-list --max-parents=0 HEAD').split('\n')[preferred_orphan]


def checkout(opts):
	""" Run git-checkout using provided options. """
	return run('git checkout --quiet -f {}'.format(opts))


def currentpathspec():
	""" Returns working pathspec (may be branch name or SHA hash if on detached HEAD) """
	out = run('git rev-parse --abbrev-ref HEAD')
	return run('git rev-parse HEAD') if out == 'HEAD' else out


def committime(pathspec=''):
	""" Returns UNIX timestamp for the object's committer time. """
	return int(run(r'git show -s --format=%ct {}'.format(pathspec)))


def commitdate(pathspec=''):
	""" Returns friendly date for pathspec. """
	return run(r'git show -s --format=%cd {}'.format(pathspec))


def firstbefore(datet):
	""" Returns revision found before the given datetime. """
	return subprocess.check_output(['git', 'rev-list', '-n1', '--date=iso', '--before="{}"'.format(datet.replace(microsecond=0).isoformat()), 'HEAD']).rstrip('\n')


def visitroot():
	""" Navigates to the root of the Git repository. Returns True if successful. """
	try:
		os.chdir(run('git rev-parse --show-toplevel'))
	except subprocess.CalledProcessError as err:
		return False

	return True
