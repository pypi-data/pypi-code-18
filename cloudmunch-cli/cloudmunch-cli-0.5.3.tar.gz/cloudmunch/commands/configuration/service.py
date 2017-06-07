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

import requests
import cloudmunch.config

def list():
  result = {
    'apikey': cloudmunch.config.config.apikey(),
    'endpoint': cloudmunch.config.config.endpoint()
  }
  return result

def describe(option):
  result = None
  if option == 'apikey':
    result = cloudmunch.config.config.apikey()
  elif option == 'endpoint':
    result = cloudmunch.config.config.endpoint()
  else:
    raise Exception("Unsupported configuration key %s" % option)

  return {option: result}

def update(option, value):
  if option == 'apikey':
    cloudmunch.config.config.apikey(value)
  elif option == 'endpoint':
        cloudmunch.config.config.endpoint(value)
  else:
    raise Exception("Unsupported configuration key %s" % option)
    
  return {option: value}
