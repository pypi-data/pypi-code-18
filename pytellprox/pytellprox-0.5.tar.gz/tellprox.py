#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module implements a simple Python interface to the Tellprox API """

__author__ = "Christian Bryn"
__copyright__ = "Copyright 2016, Christian Bryn"
__credits__ = ["Christian Bryn"]
__license__ = "GPLv2"
__version__ = "0.5"
__maintainer__ = "Christian Bryn"
__email__ = "chr.bryn@gmail.com"
__status__ = "Production"


import requests
import json
import logging

DEBUG=False

class TellProx():
  def __init__(self, host, protocol='http', port='8080', loglevel='warning'):
    self.host = host
    self.port = port
    self.protocol = protocol
    self.valid_actions = ['turnon', 'turnoff', 'toggle']

    loglevel_numeric = getattr(logging, loglevel.upper(), None)
    if not isinstance(loglevel_numeric, int):
      raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=loglevel_numeric)

  def _isnum(self, id):
    isnum = id
    try:
      isnum += 1
    except TypeError:
      return False
    return True

  def _api_get(self, action, id=1, type='device'):
    if not self._isnum(id):
      logging.debug("Device id %s is not an integer" % id)
      return False
    # id does not make sense when listing things, but is ignored...so works with id=1
    r = requests.get('%s://%s:%s/json/%s/%s?key=&id=%s' % (self.protocol, self.host, self.port, type, action, id))
    logging.debug("Request URL: %s" % r.url)
    # I think the response needs parsing...but let's assume this works:
    if r.status_code == requests.codes.ok:
      #return True
      return r.text
    return False


  def toggle_device(self, id):
      if not self._api_get('toggle', id):
          logging.warning("Could not toggle device %s" % id)
          return False
      return True

  def enable_device(self, id):
    if not self._api_get('turnon', id):
        logging.warning("Could not turnon device %s" % id)
        return False
    return True

  def disable_device(self, id):
    if not self._api_get('turnoff', id):
        logging.warning("Could not turnoff device %s" % id)
        return False
    return True

  def list_sensors(self):
    try:
      data=self._api_get('list', type='sensors')
      sensors=json.loads(data)
    except Exception as e:
      logging.error("Error listing sensors: %s" % (e))
      return False
    return sensors

  def get_sensor(self, id):
    try:
      data=self._api_get('info', id, type='sensor')
      sensor=json.loads(data)
    except Exception as e:
      logging.error("Error listing sensor %d: %s" % (id, e))
      return False
    return sensor





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
