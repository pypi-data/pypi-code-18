# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import traceback
import logging

from influxdb import InfluxDBClient

try:
    # noinspection PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

log = logging.getLogger(__name__)


def get_client(config):
    """
    db.host = 127.0.0.1
    db.port = 8086
    db.username = user
    db.password = pass
    db.name = mymetrics
    """
    db = InfluxDBClient(host=config.get('main', 'db.host'),
                        port=config.getint('main', 'db.port'),
                        username=config.get('main', 'db.username'),
                        password=config.get('main', 'db.password'),
                        database=config.get('main', 'db.name'))
    return db


def reset(idbc, config, confirm=True):
    """
    :param idbc: InfluxDBClient instance
    :param config: ConfigParser instance
    :param confirm: prompt to confirm reset?
    :return: True if reset is successful else False
    """
    db_name = config.get('main', 'db.name')

    if confirm:
        doreset = input('Reset db "%s" and DELETE ALL EXISTING DATA? (enter "YES" to continue): ' % db_name)
        if doreset != "YES":
            print('db reset cancelled')
            return False

    try:
        dbs = idbc.get_list_database()
        for db in dbs:
            if db['name'] == db_name:
                idbc.drop_database(db_name)
                break
        idbc.create_database(db_name)
    except:
        print('error resetting db "%s":\n%s' % (db_name, traceback.format_exc()))
        return False
    else:
        print('db reset successful')
        return True


def write_points(idbc, points, kwargs=None):
    """
    :param idbc: InfluxDBClient instance
    :param points: sequence of points (measurement dicts) with values to store in db
    :param kwargs: kwargs for InfluxDBClient.write_points()
    :return: None
    Example:
        points = [
            # measurementd: cpu_load_short,host=server01,region=us-west value=0.64
            {
                "measurement": "cpu_load_short",
                "tags": {"host": "server01", "region": "us-west"},
                "fields": {"value": "0.64"},
            }
        ]
    """
    if kwargs is None:
        kwargs = {}
    if 'time_precision' not in kwargs:
        kwargs['time_precision'] = 's'
    idbc.write_points(points, **kwargs)
