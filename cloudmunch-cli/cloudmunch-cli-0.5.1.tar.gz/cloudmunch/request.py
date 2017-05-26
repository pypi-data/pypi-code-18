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
import cloudmunch.config
import requests

cfg = cloudmunch.config

class Request(object):
  def __init__(self, url=None, payload=None):
    self.log = logging.getLogger(__name__)
    self.apikey = cfg.config.apikey() if cfg.config else ''
    self.endpoint = cfg.config.endpoint() if cfg.config else 'http://api.cloudmunch.com'

  # Builds the REST API query with the right URL structure and 
  # query parameters  
  def get(self, payload, url, apikey=None, endpoint=None):
    """
    @brief      Executes GET method 
    
    @param      payload  query parameters
    @param      url      endpoint
    
    @return     response object
    """    
    payload['apikey'] = self.apikey
    api_url = '{}/{}'.format(self.endpoint, url)
    self.log.debug('Invoking URL {} with payload {}'.format(api_url, payload))
    response = requests.get(api_url, params=payload)
    return response 

  def post(self, payload, url, data, apikey=None, endpoint=None):
    """
    @brief      Executes POST method
    
    @param      url      endpoint
    @param      payload  query parameters
    @param      data     POST data 
    
    @return     response object
    """
    payload['apikey'] = self.apikey
    api_url = '{}/{}'.format(self.endpoint, url)
    self.log.debug('Invoking POST on URL {} with payload'.format(api_url, payload))
    response = requests.post(api_url, params=payload, data=data)
    return response

  def put(self, url, data, apikey=None, endpoint=None):
    """
    @brief      Executes PUT method
    
    @param      url      endpoint
    @param      payload  query parameters
    @param      data     PUT data 
    
    @return     response object
    """
    payload['apikey'] = self.apikey
    api_url = '{}/{}'.format(self.endpoint, url)
    self.log.debug('Invoking PUT on URL '.format(api_url))
    response = requests.put(api_url, data=data)
    return response    