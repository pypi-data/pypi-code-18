#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Applicable to webstarts"""
import threading

import requests
from decorator import decorator

from . import defaults, log_id

__author__ = "john"

local = threading.local()
local.cache = {}
_key = requests.Session


def wrap_session(app):
  """wsgi middleware to semi persist requests sessions"""
  if _key not in local.cache:
    _key.prepare_request = pre_hook(_key.prepare_request)
  session = local.cache.get(_key, _key())
  local.cache[_key] = session

  def wrap_session_(environ, start_response):
    environ.update(requests=session)
    return app(environ, start_response)

  return wrap_session_


@decorator
def pre_hook(f, *args):
  prepared = f(*args)
  if defaults.LOG_KEY not in prepared.headers:
    prepared.headers[defaults.LOG_KEY] = log_id.find()
  return prepared
