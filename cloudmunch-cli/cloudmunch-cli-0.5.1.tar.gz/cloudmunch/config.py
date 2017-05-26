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
import logging
from configobj import ConfigObj

class Config:
  def __init__(self, config_dir):
    self.log = logging.getLogger(__name__)

    config_dir = os.path.expanduser(config_dir)

    if os.path.isabs(config_dir):
      configFileName = os.path.join(config_dir, 'config')
    else:
      configFileName = os.path.join(os.getcwd(), config_dir, 'config')
    
    configFileName = os.path.abspath(configFileName)
    self.log.debug('Loading config from %s' % configFileName)

    if not os.path.isfile(configFileName):
      if not os.path.exists(os.path.dirname(configFileName)):
        os.makedirs(os.path.dirname(configFileName))
      with open(configFileName, 'a'):
        os.utime(configFileName, None)

    self.config = ConfigObj(configFileName)
    self.config.raise_errors = True
    #TODO: configCfg.configspec = ...

  def endpoint(self, value=None):
    if value:
      self.config['endpoint'] = value
      self.config.write()
      return value
    else:
      return self.config['endpoint']

  def apikey(self, value=None):
    if value:
      self.config['apikey'] = value
      self.config.write()
      return value
    else:
      return self.config['apikey']      

config_dir = '~/.cloudmunch'

config = None
