"""
git-pythonpath

Include remote git repository (temporarily) in python path.
"""
import sys
import logging
import datetime
import time
import os
import shutil
import subprocess
import shlex
from contextlib import contextmanager

__version__ = '0.1.0'

logging.basicConfig(level=logging.DEBUG)
module_logger = logging.getLogger(__name__)

home_dir = os.path.expanduser("~")
INCLUDE_PATH = os.path.join(home_dir, ".git-pythonpath")
CACHING_TIME = 5*60


def cleanup(repo_name, caching_time):
    """
    Clean up repos in the INCLUDE_PATH,
    if the folders were created more than an hour ago.
    remove INCLUDE_PATH from system path
    Args:
        repo_name (str): The name of the local repository to remove
        caching_time (int/float): The length of time to cache the respository
    """
    full_path = os.path.join(INCLUDE_PATH, repo_name)
    mtime = os.path.getmtime(full_path)
    d = datetime.datetime.fromtimestamp(mtime)
    delta_d = datetime.datetime.now() - d
    if delta_d.seconds > caching_time:
        module_logger.debug("Removing {}".format(full_path))
        shutil.rmtree(full_path)

    if INCLUDE_PATH in sys.path:
        sys.path.remove(INCLUDE_PATH)

@contextmanager
def append_git_repo(git_repo, caching_time=CACHING_TIME):
    """
    Append a git repo to the system path
    Args:
        git_repo (str): The name of the remote git_repo
        caching_time (int/float): The length of time to cache the respository
    """
    if not os.path.exists(INCLUDE_PATH):
        os.mkdir(INCLUDE_PATH)
    sys.path.append(INCLUDE_PATH)
    repo_name = git_repo.split("/")[-1].replace(".git","")
    if os.path.exists(os.path.join(INCLUDE_PATH, repo_name)):
        pass
    else:
        cmd = "git clone {} {}".format(git_repo, os.path.join(INCLUDE_PATH, repo_name))
        cmd_list = shlex.split(cmd)
        clone_proc = subprocess.Popen(cmd_list, shell=False,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
        clone_proc.wait()
        return_code = clone_proc.returncode
        module_logger.debug("Return code from git clone operation: {}".format(return_code))
        if int(return_code) != 0:
            raise RuntimeError("Can't clone repository!")
    yield
    cleanup(repo_name, caching_time)

if __name__ == '__main__':
    url1 = "https://github.com/dean-shaff/pyro4tunneling.git"
    # url1 = "foofaa"
    url2 = "git@github.com:dean-shaff/pyro4tunneling.git"
    with append_git_repo(url1):
        import pyro4tunneling
    print(pyro4tunneling.TUNNELING_LOGGER)
