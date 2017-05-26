# -*- coding: utf-8 -*-
import os
import urlparse

from django.conf import settings


DEFAULTS = {
    'API_URL': None,
    'OAUTH2_CLIENT_ID': None,
    'OAUTH2_CLIENT_SECRET': None,
    'SERVICE_ID': None,
    'VERIFY_SSL_CERTIFICATE': True,
    'TOKEN_INFO_TIMEOUT': 60,
    'SYNC_APPS': [],
    'TOKEN_CACHE_KEY': 'account-manager-service-token',
    'TOKEN_INFO_CACHE_KEY': 'account-manager-token-{token}',
    'TOKEN_TYPE': 'Bearer',
}

MANDATORY = (
    'API_URL',
    'OAUTH2_CLIENT_ID',
    'OAUTH2_CLIENT_SECRET',
    'SERVICE_ID',
    'TOKEN_TYPE',
    'SYNC_APPS',
)


class AMAuthSettings(object):
    def __init__(self, defaults=None, mandatory=None):
        self.user_settings = getattr(settings, 'REST_FRAMEWORK_AM_AUTH', None)
        self.defaults = defaults or {}
        self.mandatory = mandatory or ()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid AMAuth setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        if attr == 'API_URL':
            self.handle_api_url(val)
        return val

    def validate_setting(self, attr, val):
        if not val and attr in self.mandatory:
            raise AttributeError("AMAuth setting: '%s' is mandatory" % attr)

    def handle_api_url(self, api_url):
        parsed_url = urlparse.urlparse(api_url)
        if parsed_url.scheme == 'http':
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


am_auth_settings = AMAuthSettings(DEFAULTS, MANDATORY)
