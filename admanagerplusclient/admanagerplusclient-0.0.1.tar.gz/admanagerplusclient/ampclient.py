#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os
import base64


use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True


class BrightRollClient:
  client_id = None
  client_secret = None
  id_host = None
  dsp_host = None
  request_auth_url = None
  yahoo_auth = None
  raw_token_results = None
  token = None


  def __init__(self):
    self.client_id = os.environ['BR_CLIENT_ID']
    self.client_secret = os.environ['BR_CLIENT_SECRET']
    self.id_host = os.environ['BR_ID_HOST']
    self.dsp_host = os.environ['BR_DSP_HOST']
    self.request_auth_url = self.id_host + "/oauth2/request_auth?client_id=" + self.client_id + "&redirect_uri=oob&response_type=code&language=en-us"

  def get_yahoo_auth_url(self):
    print("Go to this URL:")
    print(self.request_auth_url)

  def set_yahoo_auth(self, s_auth):
    self.yahoo_auth = s_auth
    return self.yahoo_auth

  def base64auth(self):
    return base64.b64encode(self.client_id + ":" + self.client_secret)
    
  def get_access_token_json(self):
    get_token_url = self.id_host + "/oauth2/get_token"
    # payload = {'grant_type':'authorization_code', 'redirect_uri':'oob','code':self.yahoo_auth}
    payload = "grant_type=authorization_code&redirect_uri=oob&code=" + self.yahoo_auth
    # headers = {'Content-Type': 'application/json', 'Authorization': "Basic " + self.base64auth()}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + self.base64auth()}
    print(get_token_url)
    print(payload)
    print(headers)
    # r = requests.post(get_token_url, json=payload, headers=headers)
    r = requests.post(get_token_url, data=payload, headers=headers)
    return r

  def cli_auth_dance(self):
    self.get_yahoo_auth_url()
    self.yahoo_auth = raw_input("Enter Yahoo! auth code: ")
    print("Auth code, {}, entered.".format(self.yahoo_auth))
    self.raw_token_results = self.get_access_token_json()
    print("raw_token_results:")
    print(self.raw_token_results)

  def campaigns(self):
    return True

  def deals(self):
    return True
