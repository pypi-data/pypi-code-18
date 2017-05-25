#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author acrazing - joking.young@gmail.com
# @version 1.0.0
# @since 2017-05-22 23:55:15
#
# Api.py
#
from __future__ import unicode_literals

import hashlib
import json
import os
import time
from sys import stderr
from threading import Thread

import requests

DEFAULT_CACHE_FILE = os.path.join(os.path.expanduser('~'), '.soul.json')


class Api:
    HOST = 'http://api.soulapp.cn'

    def __init__(self, persist_file=DEFAULT_CACHE_FILE, flush=False, log_file=None, sleep=0, timeout=5, platform='IOS',
                 **config):
        self.log_file = stderr if log_file is None else open(log_file, 'a+', buffering=1)
        self.persist_file = persist_file
        self.platform = platform
        self.user_id = 0
        self.secret = ''
        self.profile = {}
        self.config = config
        self.sleep = sleep
        self.timeout = timeout
        self.load()
        flush is True and self.flush()

    def load(self):
        if self.persist_file is None:
            return
        if os.path.isfile(self.persist_file) is False:
            return
        self.log('load session from %s' % self.persist_file)
        with open(self.persist_file, 'r') as f:
            data = json.load(f)
            self.user_id = data.get('user_id', 0)
            self.profile = data.get('profile', {})
            self.secret = data.get('secret', '')
            config = data.get('config', {})
            config.update(self.config)
            self.config = config
        return self

    def _persist(self):
        with open(self.persist_file, 'w+') as f:
            json.dump({
                'user_id': self.user_id,
                'profile': self.profile,
                'secret': self.secret,
                'config': self.config,
            }, f, indent=2)

    def persist(self):
        self.log('persist session to %s' % self.persist_file)
        thread = Thread(target=self._persist)
        thread.start()
        thread.join()
        return self

    def req(self, method='get', url='/', params=None, data=None, headers=None, auth=True, **kwargs):
        """
        :param method: 
        :param url: 
        :param params: 
        :param data: 
        :param headers:
        :param auth:
        :param kwargs: 
        :rtype: requests.Response
        :return: 
        """
        self.log('request [%s] %s' % (method, url), 'info')
        headers = {} if headers is None else headers
        if self.secret:
            headers.update({
                'app-version': '3.1.11',
                'device-id': '84C372C1-2EA6-47F1-9E32-404B82CEBDEA',
                'app-time': str(int(time.time() * 1000)),
                'User-Agent': '[WIFI;iPhone 6s;iOS;10.3.1;375*667;100001;zh_CN]',
                'app-id': '10000001',
                'X-Auth-UserId': str(self.user_id),
                'X-Auth-Token': self.secret,
            })
        url = self.HOST + url if url.startswith('/') else url
        s = requests.session()
        r = s.request(method, url, params=params, data=data, headers=headers, timeout=self.timeout, **kwargs)
        s.close()
        self.log('request [%s] %s response: %s' % (method, r.url, r.text[:50]))
        data = r.json()
        if data is None:
            data = {}
        r.json = lambda: data
        if data.get('code') == 20001:
            if self.user_id != 0:
                self.expire()
            if auth is True:
                raise PermissionError(data.get('message', r.text))
        elif data.get('success') is not True:
            raise RuntimeError(data.get('message', r.text))
        if self.sleep != 0:
            time.sleep(self.sleep)
        return r

    def json(self, **kwargs):
        """
        :param kwargs: 
        :rtype: dict
        :return: 
        """
        return self.req(**kwargs).json()

    def login(self, phone, password, area='86'):
        """
        :type phone: str
        :type password: str
        :type area: str
        :rtype: dict
        """
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        data = self.json(method='post', url='/login', data={
            'area': area,
            'phone': phone,
            'password': password,
            'platform': self.platform,
        })
        profile = data.get('data', {})
        user_id = profile.get('userId', 0)
        secret = profile.get('token')
        self.user_id = user_id
        self.secret = secret
        self.profile = profile
        self.persist()
        return profile

    def expire(self):
        if self.user_id is 0:
            return
        self.log('session expired for user %s' % self.user_id)
        self.user_id = 0
        self.secret = ''
        self.profile = {}
        self.persist()
        return

    def flush(self):
        if self.user_id is not 0:
            return
        user = self.json(url='/login', auth=False).get('data')
        if user is None:
            return
        self.user_id = user.get('userId', 0)
        self.profile = user
        self.persist()
        return

    def use(self, secret):
        self.secret = secret
        self.flush()
        return self

    def log(self, data, level='debug'):
        self.log_file.write('%s [%s] - %s\n' % (time.strftime('%y-%m-%d %H:%M:%S'), level.upper(), data))
        return self

    def __repr__(self):
        return 'soul api client for <%s>' % self.profile.get('signature', self.user_id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.log_file.closed is False:
            self.log_file.close()

    @staticmethod
    def to_json(obj):
        return json.dumps(obj, separators=(',', ':'), default=lambda x: x.__repr__())


class Module:
    def __init__(self, api):
        """
        :type api: Api
        :param api: 
        """
        self.api = api
