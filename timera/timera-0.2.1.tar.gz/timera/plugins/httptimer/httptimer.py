# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import traceback
import logging

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import timera

log = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# required by all plugin modules, called by worker thread
def get_metrics(config, timestamp, plugin):
    """
    :param config: ConfigParser instance
    :param timestamp: unix timestamp (seconds since epoch) for current collection interval
    :param plugin: dict with parsed plugin values
    """
    do_work(config, timestamp, plugin)


#
# plugin-required api above
# module's implementation below
#


def do_work(config, timestamp, plugin):
    idbc = timera.db.get_client(config)
    proxy = plugin['config'].get('proxy')
    include_direct = timera.util.asbool(plugin['config'].get('include_direct'))
    if not proxy or include_direct:
        # get metrics using direct connection
        metrics_direct = get_url(config, timestamp, plugin, None)
        write_metrics(idbc, metrics_direct)
    if proxy:
        # get metrics using proxy
        metrics_proxy = get_url(config, timestamp, plugin, proxy)
        write_metrics(idbc, metrics_proxy)
    # make sure socket is closed
    idbc._session.close()


def get_url(config, timestamp, plugin, proxy):
    # return metrics: measurementd
    connect_timeout = float(config.get('main', 'plugins.httptimer.connect_timeout'))
    read_timeout = float(config.get('main', 'plugins.httptimer.read_timeout'))
    name = plugin['config']['name']
    url = plugin['config']['url']
    method = plugin['config'].get('method', 'get').lower()
    if method != 'get':
        raise NotImplemented('get is currently the only supported http method')
    verify = timera.util.asbool(plugin['config'].get('ssl_verify', 'true'))
    proxies = dict(http=proxy, https=proxy) if proxy else None
    measurement = name + '_' + get_proxy_name(proxy) if proxy else name
    try:
        r = requests.get(url, timeout=(connect_timeout, read_timeout), proxies=proxies, verify=verify)
    except:
        log.error('exception for url "%s":\n%s' % (url, traceback.format_exc()))
        response_time = 0.0
    else:
        """
        http://docs.python-requests.org/en/latest/api/#requests.Response
        elapsed:
            The amount of time elapsed between sending the request and the arrival
            of the response (as a timedelta). This property specifically measures
            the time taken between sending the first byte of the request and
            finishing parsing the headers. It is therefore unaffected by consuming
            the response content or the value of the stream keyword argument.
        """
        response_time = r.elapsed.total_seconds()
    response_time = float(response_time)
    log.info('url "%s" response time (%s): value=%f' % (url, measurement, response_time))
    return dict(measurement=measurement, time=timestamp, fields=dict(value=str(response_time)))


def get_proxy_name(proxy_url):
    # return consistent, normalized proxy name from proxy url for use as db column name
    # omit scheme, return hostname/ip and port
    parsed = timera.util.parse_url(proxy_url)
    # index 1 is "netloc"
    return parsed[1]


def write_metrics(idbc, measurementd):
    # write metrics to db
    timera.db.write_points(idbc, [measurementd])
