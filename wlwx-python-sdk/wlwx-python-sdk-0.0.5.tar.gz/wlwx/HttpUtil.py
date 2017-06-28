#!/usr/bin/python3
#  -*- coding:utf-8 -*-
# filename:HttpUtil
__author__ = 'zhouzhao'

import platform,requests
from wlwx.Config import wlwx_config
from wlwx.Result import Result
_sys_info = '{0}; {1}'.format(platform.system(), platform.machine())
_python_ver = platform.python_version()

_session = None
_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

def _init():
    pass

def request_post(obj, url, data=None, retry=0):
    if not data:
        return Result(data, None, '参数为空')
    if _session is None:
        _init()
    try:
        if type(data) == dict:
            r = requests.post(url, data=data, headers=_headers, timeout=5)
        else:
            r = requests.post(url, data=bytes(data,'utf8'), headers=_headers, timeout=5)
        r.encoding = 'utf-8'

    except Exception as e:
        if retry > 0:
            return request_post(url, data, retry - 1)
        else:
            return Result(data, None, e)
    return Result(data, r)

if __name__ == '__main__':
    pass