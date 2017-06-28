#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Applicable to webstarts"""
import json
import os

__author__ = "john"


def get_conf(env):
  """Right now just checks if it is debug mode"""
  conf = json.loads(env.get('WSCONF', '{}'))
  debug = True if env.get('WSDEV') else False
  conf.update(debug=debug)
  return conf


def configure(env=os.environ):
  from . import wlog, backend
  conf = get_conf(env)
  wlog.setup(conf)
  backend.setup_celery(conf)
  return conf


def entry():
  """Run eventlet


  - structlog
    Check out colorama
    Like queries always do log = log.new(y=23)
    logging.getLogger('foo').addHandler(logging.NullHandler()) should be used by libraries
  - GoogleCloud logging - when the shit gets fixed
    I could add the handler to logging.getLogger('socialclime') since it will be the parent of all app loggers.
    Now that i finally understand logging.

  """
  from gevent import monkey
  monkey.patch_all(subprocess=True)

  conf = configure()

  from .gunicorn import WebstartsApp

  app = WebstartsApp('%(prog)s [OPTIONS] [APP_MODULE]', conf['debug'])
  return app.run()
