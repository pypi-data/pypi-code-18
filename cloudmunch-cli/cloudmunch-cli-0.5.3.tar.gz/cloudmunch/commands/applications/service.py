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

import logging
import json
import time
from cloudmunch import utils, request, decorators

@decorators.get_context_id
def get_data(**kwargs):
  """
  @brief      Constructs the API url and gets data for the 
              provided inputs
  
  @param      kwargs  Dictionary of inputs
  
  @return     returns the response from the API request
  """  
  if (filter(lambda v: v is None, kwargs.values())):
    return None
  
  payload = None
  command = kwargs['command']
  ctype = kwargs['type']  

  # If getting Key Metrics or Insight Cards, get Insight Report Id   
  if command in ('insight_card', 'key_metric'):
    if (kwargs['insight_report'] == '_latest'):
      payload = {'count' : 1, 'fields' : 'id, name'}

    kwargs['insight_report'] = utils.get_id_for_name('insight_report', payload, **kwargs)

    if not kwargs['insight_report']:
      print 'here'
      return None

  if command in ('datastore', 'extract'):
    if kwargs['datastore']:
      kwargs['datastore'] = utils.get_id_for_name('datastore', payload, **kwargs)

      if not kwargs['datastore']:
        return None

  # Build the payload - get required fields based on details or list
  # for resource list, filter by integration_id
  if ctype == utils.CommandType.DETAILS:
    payload = {'fields': get_context_fields(command)} # build the fields list based on the context
  else:
    payload =  {'fields': 'id,name'}
    
    if command == 'resource' and kwargs['integration']:
      payload.update({'filter': json.dumps({'integration_id': kwargs['integration']})})

  # Get the data   
  url = utils.build_url(kwargs['command'], **kwargs)
  req = request.Request()
  response = req.get(payload, url)
  return response

def get_context_fields(context):
  """
  @brief      Gets the fields to get for context.
  
  @param      context  The context
  
  @return     The fields for context.
  """
  fields = '*'

  if context == 'extract':
    fields = 'data as attributes, id, name'

  if context == 'run':
    fields = 'duration, message, status, run, started_by, end_time'

  if context == 'application':
    fields = 'id,name,count(integrations) as integrations_count, count(resources) as resources_count, updated_date, created_by, created_date, tags' 

  if context == 'resource':
    fields = 'id, name, key_fields as configuration, type, created_by, created_date, type'  
  
  if context == 'insight_card':
    fields = 'resource_name as resource, updated_date, data as details, visualization_map, name, id'

  return fields

@decorators.get_context_id
def post_data(**kwargs):
  payload = {}
  url = utils.build_url(kwargs['command'], **kwargs)
  if kwargs['action']:
    payload.update({"action": kwargs['action']})

  req = request.Request()
  response = req.post(payload, url, json.dumps({"data": kwargs['data']}))
  
  if kwargs['command'] == 'pipeline' and kwargs['action'] == 'trigger':
    if response.json()['request']['status'] == 'SUCCESS' and response.json()['data']:
      run_id = response.json()['data']['run_id']
      response = track_run_to_completion(run_id, **kwargs)

  return response

def track_run_to_completion(run_id, **kwargs):
  """
  @brief      Track a task to completion
  
  @param      response  The response
  @param      kwargs    The kwargs
  
  @return     response object. If successful return the details of the completed run
  """
  status = 'queued'
  resp_status = 'SUCCESS'
  kwargs.update({"run": run_id, "command": "run", "type": utils.CommandType.DETAILS})
  
  payload = {'fields': get_context_fields(kwargs['command'])}
  url = utils.build_url(kwargs['command'], **kwargs)
  req = request.Request()

  while (status in ('in-progress', 'queued') and resp_status == 'SUCCESS'):
    if status == 'in-progress':
      print("Task has been running for {} seconds. Will check again in a few seconds ...".format(result['data']['duration']))
    elif status == 'queued':
      print("Task has not started running. Will check in a few seconds")    
    time.sleep(15)

    response = req.get(payload, url)    
    result = response.json()
    resp_status = result['request']['status']  
    if resp_status == 'SUCCESS' and result['data']:
      status = result['data']['status']
      
  return response
