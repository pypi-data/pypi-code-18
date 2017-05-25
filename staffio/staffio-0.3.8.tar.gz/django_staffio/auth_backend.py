# -*- coding: UTF-8 -*-
"""
Obtain
STAFFIO_CLIENT_ID & STAFFIO_CLIENT_SECRET
and put into sentry.conf.py
"""
from __future__ import absolute_import

from os import getenv
import requests

from social_auth.backends import BaseOAuth2, OAuthBackend
from social_auth.exceptions import AuthCanceled, AuthUnknownError


_prefix = getenv('STAFFIO_PREFIX', 'https://www.lcgc.work')
STAFFIO_TOKEN_EXCHANGE_URL = '%s/token' % _prefix
STAFFIO_AUTHORIZATION_URL = '%s/authorize' % _prefix
STAFFIO_USER_DETAILS_URL = '%s/info/me' % _prefix
del _prefix


class StaffioBackend(OAuthBackend):
    """Staffio OAuth authentication backend"""
    name = 'staffio'
    EXTRA_DATA = [
        ('email', 'email'),
        ('name', 'nickname'),
        ('username', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details from Staffio account"""

        return {'username': response.get('username'),
                'email': response.get('email'),
                'full_name': response.get('cn'),
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}


class StaffioAuth(BaseOAuth2):
    """Staffio OAuth authentication mechanism"""
    AUTHORIZATION_URL = STAFFIO_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = STAFFIO_TOKEN_EXCHANGE_URL
    AUTH_BACKEND = StaffioBackend
    SETTINGS_KEY_NAME = 'STAFFIO_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'STAFFIO_CLIENT_SECRET'
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        headers = {'Authorization': 'Bearer %s' % access_token}
        try:
            resp = requests.get(STAFFIO_USER_DETAILS_URL,
                                headers=headers)
            resp.raise_for_status()
            return resp.json()['data']
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        try:
            response = requests.post(
                self.ACCESS_TOKEN_URL, data=params,
                headers=self.auth_headers())
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        else:
            try:
                response = response.json()
            except (ValueError, KeyError):
                raise AuthUnknownError(self)

        response.pop('data')
        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    @classmethod
    def refresh_token(cls, token):
        params = cls.refresh_token_params(token)
        response = requests.post(cls.ACCESS_TOKEN_URL, data=params,
                                 headers=cls.auth_headers())
        response.raise_for_status()
        return response.json()

# Backend definition
BACKENDS = {
    'staffio': StaffioAuth,
}
