import asyncio
import collections
import json
import logging
import os
import shutil
import uuid

import maxillo.git

APPLICATIONS = '/etc/maxillo/applications'
METAFILE = 'application.json'

LOGGER = logging.getLogger(__name__)

class Application():
    def __init__(self, path, name, git_url, uuid):
        self.git_url    = git_url
        self.name       = name
        self.uuid       = uuid

    def branches(self):
        return maxillo.git.list_branches(self._repo())

    async def checkout_branch(self, branch):
        await maxillo.git.checkout(self._repo(), branch)

    def has_configuration(self):
        configuration = path(self.uuid, 'configuration.yaml')
        return os.path.exists(configuration)

    def path(self, *args):
        return path(self.uuid, *args)

    async def update_code(self):
        await maxillo.git.pull(self._repo())
        LOGGER.info("Updated source code for %s", self.name)

    def _repo(self):
        return self.path('repo')


def path(uuid, *args):
    return os.path.join(APPLICATIONS, uuid, *args)

def list():
    if not os.path.exists(APPLICATIONS):
        return []
    return [get(uuid_) for uuid_ in os.listdir(APPLICATIONS)]

def create(data):
    uuid_ = uuid.uuid4()
    data['uuid'] = str(uuid_)
    update(uuid_, data)
    LOGGER.info("Created new application %s in %s", data['name'], uuid_)
    return uuid_

def get(uuid_):
    metafile = os.path.join(APPLICATIONS, str(uuid_), METAFILE)
    if not os.path.exists(metafile):
        return None
    with open(metafile, 'r') as f:
        data = json.load(f)
    return Application(metafile, **data)

async def update(uuid_, data):
    old_application = get(uuid_)
    has_git_changed = (not old_application) or old_application.git_url != data.get('git_url')

    path = os.path.join(APPLICATIONS, str(uuid_))
    if not os.path.exists(path):
        os.makedirs(path)
    metafile = os.path.join(path, METAFILE)
    with open(metafile, 'w') as f:
        f.write(json.dumps(data))
    LOGGER.info("Wrote new application metadata file for %s in %s", uuid_, metafile)
    git_path = os.path.join(path, 'repo')
    if not has_git_changed:
        return
    LOGGER.info("Detected git change, refreshing git repo")
    if os.path.exists(git_path):
        shutil.rmtree(git_path)
        LOGGER.info("Deleted %s", git_path)
    await maxillo.git.clone(data['git_url'], git_path)
