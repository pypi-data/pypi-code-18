# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import os
from werkzeug.utils import cached_property
from flask import session, url_for
from flask_oauthlib.contrib.client import OAuth

from future.moves.urllib.parse import urljoin

from .user import User, Token, Anonymity

import logging


log = logging.getLogger(__name__)


class Client(object):

    def __init__(self, app=None, prefix=None):
        if app is not None:
            self.init_app(app)
        self._prefix = prefix or os.getenv(
            'STAFFIO_PREFIX', 'https://www.lcgc.work')
        self._save_user = None

    def init_app(self, app):
        self.app = app
        app.staffio_client = self

    def save_user(self, callback):
        self._save_user = callback
        return callback

    def _oauth_url(self, name):
        if self._prefix.startswith('http://') \
                or self._prefix.startswith('https://'):
            return urljoin(self._prefix, name)
        return urljoin('http://%s' % self._prefix, name)

    @cached_property
    def oauth(self):
        return OAuth(self.app)

    @cached_property
    def remote_app(self):
        staffio = self.oauth.remote_app(
            name='staffio',
            version='2',
            endpoint_url=self._oauth_url('info/'),
            access_token_url=self._oauth_url('token'),
            refresh_token_url=self._oauth_url('token'),
            authorization_url=self._oauth_url('authorize'),
            scope=['basic'])

        staffio.tokengetter(load_token)

        staffio.tokensaver(save_token)

        return staffio

    def authorized(self):
        log.debug('start authorized_response')
        response = self.remote_app.authorized_response()
        log.debug('got authorized resp: %r', response)
        if response:
            log.debug('authorized OK')
            save_token(response)
            log.debug('call save: %r', self._save_user)
            saved_user = None
            if self._save_user:
                username, userdata = self.get_info()
                saved_user = self._save_user(username, userdata)
                log.info('saved %r %r', username, saved_user)
            return response, saved_user

        log.warning('ERR: call remote_app.authorized_response error')

    def login(self, uri):
        callback_uri = uri if uri else url_for('login_authorized',
                                               _external=True)
        log.debug('login with callback %s' % callback_uri)
        return self.remote_app.authorize(callback_uri)

    def logout(self):
        remove_token()

    def get_staff(self):
        # deprecated
        return self.get_info()

    def get_info(self, topic='me'):
        resp = self.remote_app.get(topic)
        log.debug('resp.content: %r' % resp.content)
        if not resp.ok:
            log.warning(
                'ERR: Invalid Response, url %s status: %r content %s' %
                (resp.url, resp.status_code, resp.content))
            # flash('Unknown error: call get(me) failed')
            # redirect(url_for('login'))
            return
        res = resp.json()
        log.debug('me: %r' % res['me'])
        s = res['me']
        if 'uid' not in s or 'sn' not in s or 'email' not in s:
            log.warning(
                'ERR: Invalid staff, uid/sn/email not found')
            return
        username = s.pop('uid')
        return username, s
        # return username, dict(first_name=s.get('gn', ''),
        #                       last_name=s.get('sn'),
        #                       email=s.get('email'),
        #                       mobile=s.get('mobile', ''),
        #                       display_name=s.get('nickname', ''),
        #                       employee_id=s.get('eid', 0),
        #                       description=s.get('description', ''),
        #                       )

    @property
    def current_user(self):
        token = load_token()
        if token and 'user' in token:
            return User(token['user'])
        log.info('load user failed')

    @property
    def current_token(self):
        token = load_token()
        if token and 'user' in token:
            return Token(
                token['access_token'], User(token['user']))
        log.info('load_token failed')
        return Anonymity


def load_token():
    return session.get('staffio_token')


def save_token(token):
    session['staffio_token'] = token


def remove_token():
    session.pop('staffio_token', None)
