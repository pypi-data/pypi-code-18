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

import click
import logging
from cloudmunch.cli import cli
from cloudmunch.commands.configuration import service
from cloudmunch import decorators

@cli.group()
def configuration():
    """Configure the endpoint and API Key to access CloudMunch"""

@configuration.command('list')
@decorators.timer
@decorators.output
def configuration_list():
    """List current configuration options"""
    logging.getLogger(__name__).info('List all configuration options')
    return service.list()

@configuration.command('update')
@click.argument('option')
@click.argument('value')
@decorators.timer
@decorators.output
def configuration_describe(option, value):
    """Update specified configuration option value"""
    logging.getLogger(__name__).info('Update value for %s to %s' % (option, value))    
    return service.update(option, value)
