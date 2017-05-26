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
import json
import yaml
import logging
import time
import click
import jsonpath_rw
from cloudmunch import request, utils
from functools import wraps
import re

def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        logging.getLogger(__name__).debug("Command execution time: {0}s".format(time.time()-t))
        return res

    return tmp

def response(f):
    def tmp2(*args, **kwargs):
        res = f(*args, **kwargs)
        if res:
          logging.getLogger(__name__).debug("API execution time: {0}".format(res.json()['request']['response_time']))
          logging.getLogger(__name__).debug("Command response: {0} {1}".format(res.status_code, res.text))

          debug = click.get_current_context().find_root().params['debug']

          if res.json()['request']['status'] != 'SUCCESS':
            if debug:
              raise Exception("REST CALL ERROR: %s" % format(res.json()))
            else:
              print("API error: {0}".format(res.json()['request']['message']))
          else:
            query = click.get_current_context().find_root().params['query']
            if query:
              logging.getLogger(__name__).debug("Query: {0}".format(query))
              query_expr = jsonpath_rw.parse(query)
              queryResult = query_expr.find(res.json()['data'])
              logging.getLogger(__name__).debug( "Query result: {0}".format(queryResult))
              for match in queryResult:
                print(formatOutput(match.value))
            else:
              print(formatOutput(res.json()['data']))

    return tmp2

def output(f):
    def tmp2(*args, **kwargs):
        res = f(*args, **kwargs)

        logging.getLogger(__name__).debug("Command response: {0}".format(res))

        print(formatOutput(res))

    return tmp2

def formatOutput(obj):
  output = click.get_current_context().find_root().params['output']
  logging.getLogger(__name__).info("Output format is: {0}".format(output))
  if output == 'yaml':
    return yaml.safe_dump(obj, default_flow_style=False)
  elif output == 'json':
    return json.dumps(obj, indent=2)
  elif output == 'text':
    return obj
  else:
    raise Exception("Unsupported format: {0}".format(output))

def readInput(data):
  logging.getLogger(__name__).debug("Reading input from {0}".format(data))

  if data.startswith("file://"):    
    data = data[7:]

  if os.path.isfile(data):
    with open(data, 'r') as f:
        logging.getLogger(__name__).debug('Input file: {0}'.format(data))
        data = f.read()

  try:
    obj = json.loads(data)
    logging.getLogger(__name__).debug("Json loaded {0}".format(obj))
  except ValueError:
    obj = yaml.load(data)
    logging.getLogger(__name__).debug("Yaml loaded {0}".format(obj))

  return json.dumps(obj)
  
def get_context_id(func):
  @wraps(func)
  def wrapper(**kwargs):
    logging.getLogger(__name__).debug("After converting names to ids {}".format(kwargs.items()))

    # Start with checking the application because the order of the keys in dictionary
    key = 'application'
    if kwargs[key] and not utils.is_context_id(key, kwargs[key]):
      kwargs[key] = utils.get_id_for_name(key, **kwargs)
      logging.getLogger(__name__).debug("Application Id found {0}".format(kwargs[key]))

    if kwargs[key]:  
      # Iterate over the rest of the items in dictionary   
      for key in kwargs:
        name = kwargs[key]
        if key in ['pipeline', 'integration', 'resource'] and name and not utils.is_context_id(key, name):
          logging.getLogger(__name__).debug("Getting id for {0} with name {1}".format(key, name))
          payload = {'fields':'id,name','filter' : json.dumps({'name' : name})}
          kwargs[key] = utils.get_id_for_name(key, **kwargs)
    return func(**kwargs)

  return wrapper