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
import logging
import re
import json
from enum import Enum
from cloudmunch import request

class CommandType(Enum):
	LIST = 1,
	DETAILS = 2,
	POST = 3

# URL constants
url_dict = {
		'application' : 'applications/{{ }}', 
		'pipeline': 'applications/{{ }}/pipelines/{{ }}',
		'run' : 'applications/{{ }}/pipelines/{{ }}/runs/{{ }}',
		'integration': 'applications/{{ }}/integrations/{{ }}',
		'resource': 'applications/{{ }}/resources/{{ }}',
		'insight_report' : 'applications/{{ }}/resources/{{ }}/insight_reports/{{ }}',
		'key_metric' : 'applications/{{ }}/resources/{{ }}/insight_reports/{{ }}/key_metrics/{{ }}',
		'insight_card' : 'applications/{{ }}/resources/{{ }}/insight_reports/{{ }}/insight_cards/{{ }}',
    'integration_def' : 'integrations/{{ }}',
    'datastore': 'applications/{{ }}/resources/{{ }}/datastores/{{ }}',
    'extract': 'applications/{{ }}/resources/{{ }}/datastores/{{ }}/extracts/{{ }}'
		}

def build_url(context, **kwargs):
  rep_list = []
  placehoder = url_dict[context] 
  pattern = r'\{{(.+?)\}}'

  if context is 'application':
  	rep_list = [kwargs['application']]

  if context is 'pipeline':
    rep_list = [kwargs['application'], kwargs['pipeline']]

  if context is 'run':
    rep_list = [kwargs['application'], kwargs['pipeline'], kwargs['run']]  

  if context is 'integration':
    rep_list = [kwargs['application'], kwargs['integration']]      

  if context is 'insight_report':
    rep_list = [kwargs['application'], kwargs['resource'], kwargs['insight_report']]

  if context is 'datastore':
    rep_list = [kwargs['application'], kwargs['resource'], kwargs['datastore']]      

  if context is 'resource':
    rep_list = [kwargs['application'], kwargs['resource']]   

  if context is 'key_metric':
  	rep_list = [kwargs['application'], kwargs['resource'], kwargs['insight_report'], kwargs['key_metric']]

  if context is 'insight_card':
  	rep_list = [kwargs['application'], kwargs['resource'], kwargs['insight_report'], kwargs['insight_card']]	

  if context is 'extract':
    rep_list = [kwargs['application'], kwargs['resource'], kwargs['datastore'], kwargs['extract']]      

  items = iter(str(el) for el in rep_list)
  url = re.sub(pattern, lambda L: next(items), placehoder)

  logging.getLogger(__name__).debug("Generated Url - {0}".format(url))
 
  return url
  
def is_context_id(context, value):
  """
  @brief      Determines if value provided is an id of type context.
  
  @param      context  context
  @param      value    value
  
  @return     True if value is id, False otherwise.
  """
  pattern = r"^" + re.escape(context[0:3].lower()) + r"\d{19}$"
  ret = re.match(pattern, value.lower())
  return True if ret else False 

def get_id_for_name(key, payload=None, **kwargs):
  """
  @brief      Gets the identifier for name.
  
  @param      key      The key
  @param      payload  The payload
  @param      kwargs   The kwargs
  
  @return     The identifier for name.
  """
  name = kwargs[key]
  kwargs[key] = ''  

  if is_context_id(key, name):
    return name
  
  if not payload:
    payload = {'fields':'id, name','filter' : json.dumps({'name' : name})}

  r = request.Request()
  url = build_url(key, **kwargs)
  resp = r.get(payload, url)
  if resp:
    result = resp.json()
    if result['request']['status'] == 'SUCCESS' and result['data']:
      return result['data'][0]['id']
    else:
      print('No {} found with name {}.'.format(key, name))
      return None
  else:
    return None 
  #return utils.check_and_get_data(resp, 'id', [key, name])
  