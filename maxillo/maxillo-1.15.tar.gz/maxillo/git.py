import asyncio
import logging
import os
import shutil
import subprocess

LOGGER = logging.getLogger(__name__)
def configure():
    "Set up the basic git config so git works"
    ROOT_SSH = '/root/.ssh'
    if os.path.exists(ROOT_SSH) and not os.path.islink(ROOT_SSH):
        shutil.rmtree(ROOT_SSH)
        os.symlink('/etc/maxillo/master/.ssh', ROOT_SSH)
        LOGGER.info("Linked '/etc/maxillo/master/.ssh' to '%s'", ROOT_SSH)
    if os.path.exists('/root/.ssh/id_rsa'):
        os.chmod('/root/.ssh/id_rsa', 0o400)
        LOGGER.info("Locked down '/root/.ssh'")
    if not os.path.exists('/root/.gitconfig'):
        with open('/root/.gitconfig', 'w') as f:
            f.write(''
                '[user]\n'
                '    email = maxillo@authentise.com\n'
                '    name = Maxillo Automation\n'
            )
            LOGGER.info("Wrote new .gitconfig at /root/.gitconfig")

def _sync_git(*args):
    command = ['git'] + list(args)
    LOGGER.debug("Executing '%s'", command)
    result = subprocess.check_output(command)
    return result.decode('utf-8')

async def _async_git(*args):
    command = ['git'] + list(args)
    LOGGER.debug("Executing '%s'", command)
    proc = await asyncio.create_subprocess_exec(*command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate(input=None)
    if proc.returncode != 0:
        LOGGER.info("%s stderr: %s", command, stderr)
        raise Exception("Git command {} failed with status {}".format(command, proc.returncode))
    return stdout.decode('utf-8')

async def clone(git_url, git_path):
    await _async_git('clone', git_url, git_path)
    LOGGER.info("Cloned %s to %s", git_url, git_path)

def list_branches(path):
    result = _sync_git('-C', path, 'branch', '--list')
    lines = result.split('\n')
    branches = [line.strip() for line in lines if line]
    branches = [branch.strip('* ') for branch in branches]
    return branches

async def checkout(path, branch):
    await _async_git('-C', path, 'checkout', branch)
    await _async_git('-C', path, 'branch', '--set-upstream-to=origin/' + branch, branch)
    LOGGER.info("Checked out '%s' at %s", branch, path)

async def pull(path):
    await _async_git('-C', path, 'pull')
