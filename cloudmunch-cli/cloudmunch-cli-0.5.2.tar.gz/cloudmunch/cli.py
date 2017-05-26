# Copyright 2016 Cloudmunch Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import os.path
import sys
import click
import logging
import cloudmunch.config
import urllib3

@click.group()
@click.version_option()
@click.option('--debug', is_flag=True, default=False, help='Enable debug output. Disabled by default')
#@click.option('-c', '--config-dir', default='~/.cloudmunch', help='Directory with config files. Default is ~/.cloudmunch')
@click.option('-o', '--output', default='json', help='Output format')
@click.option('-q', '--query', default='', help='JSON Path query for output results')
def cli(debug, output, query):
    """CloudMunch CLI.\n
    This is a CLI tool for executing commands against CloudMunch API.
    """
    log = logging.getLogger('cloudmunch')

    stdoutHanlder = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdoutHanlder.setFormatter(formatter)
    log.addHandler(stdoutHanlder)

    if debug:
        log.setLevel(logging.DEBUG)
        import httplib
        httplib.HTTPConnection.debuglevel = 1

        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        if sys.version_info >= (2,7):
            logging.captureWarnings(True)
    else:
        log.setLevel(logging.NOTSET)
        urllib3.disable_warnings()
        if sys.version_info >= (2,7):
            logging.captureWarnings(False)


    #log.info('Setting config dir to %s' % config_dir)
    log.info('Python version is %s - %s' % (sys.version, sys.hexversion))
    #cloudmunch.config.config_dir = config_dir
    #cloudmunch.config.credentials = cloudmunch.config.Credentials(cloudmunch.config.config_dir)
    cloudmunch.config.config = cloudmunch.config.Config(cloudmunch.config.config_dir)


def isPluginDir(filename):
    cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'commands'))
    return os.path.isdir(os.path.join(cmd_folder, filename)) and os.path.isfile(os.path.join(cmd_folder, filename, 'commands.py'))


def loadCommands():
    cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'commands'))
    for filename in os.listdir(cmd_folder):
        if isPluginDir(filename):
            name = "%s.commands" % filename
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            exec("import cloudmunch.commands.%s" % name)                

loadCommands()

if __name__ == '__main__':    
    cli()