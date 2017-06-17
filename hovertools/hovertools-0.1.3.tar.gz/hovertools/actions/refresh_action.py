# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
import logging
import shlex
import subprocess
import time
from hovertools.managers.docker_manager import DockerManager

logger = logging.getLogger(__name__)


def check_running(uptest_doc, containerid):
    ctr = 0
    success = False

    script = uptest_doc['script']

    child_env = os.environ.copy()
    if 'environment' in uptest_doc:
        env = uptest_doc['environment']
        for k,v in env.items():
            child_env[k] = v
    child_env['CONTAINER_ID'] = containerid

    retries = 12
    delay = 5
    if 'delay' in uptest_doc:
        delay = int(uptest_doc['delay'])

    if 'retries' in uptest_doc:
        retries = int(uptest_doc['retries'])

    while ctr < retries:
        logger.info("Checking if container is ready: try {0} of {1}".format(ctr, retries))
        p = subprocess.Popen(script, env=child_env, shell=True)
        p.wait()
        ret = p.returncode
        if ret != 0:
            ctr += 1
            logger.info("Sleeping {0} seconds".format(delay))
            time.sleep(delay)
        else:
            success = True
            break

    if not success:
        raise Exception("Could not bring up the container")


def provision_system(prov_doc):

    script = prov_doc['script']
    child_env = os.environ.copy()
    if 'environment' in prov_doc:
        env = prov_doc['environment']
        for k,v in env.items():
            child_env[k] = v
    p = subprocess.Popen(script, env=child_env, shell=True)
    p.wait()
    if p.returncode != 0:
        raise Exception("The provisioning script returned an error")


def do_refresh(ctx, name):
    """"
    Refreshes a docker instance by name
    """
    yaml_doc = None

    try:
        repo_dir = ctx.obj['repo']
        filename = os.path.join(repo_dir, name+'.yaml')
        with open(filename, 'r') as fin:
            yaml_doc = yaml.safe_load(fin)
    except yaml.YAMLError as e:
        raise Exception("Error in configuration file: {0}".format(e))

    options = None
    env = None
    ports = None
    if 'options' in yaml_doc:
        options = yaml_doc['options']
    if 'environment' in yaml_doc:
        env = yaml_doc['environment']
    if 'ports' in yaml_doc:
        ports = yaml_doc['ports']

    docker_manager = DockerManager(image_name=yaml_doc['image'], 
                                   container_name=yaml_doc['name'],
                                   options=options,
                                   environment=env,
                                   ports=ports)
    logger.info("Refreshing")
    docker_manager.refresh()
    container_id = docker_manager.get_container_id()

    if 'uptest' in yaml_doc:
        check_running(yaml_doc['uptest'], container_id)

    if 'provisioning' in yaml_doc:
        provision_system(yaml_doc['provisioning'])
