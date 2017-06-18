"""
HMAC Auth plugin for HTTPie.

"""
import datetime
import base64
import hashlib
import hmac

from httpie.plugins import AuthPlugin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = '0.0.1'
__author__ = 'Pierre Coueffin'
__licence__ = 'MIT'


class HmacAuth:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, r):
        method = r.method

        content_type = r.headers.get('content-type')
        if (content_type != 'application/json'):
            raise ValueError('Visionect will not work unless you explicitly use application/json')

        httpdate = r.headers.get('date')
        if not httpdate:
            now = datetime.datetime.utcnow()
            httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
            r.headers['Date'] = httpdate

        path = urlparse(r.url).path

        string_to_sign = method + "\n\n" + content_type + "\n" +  httpdate + "\n" + path
        signature = base64.encodestring(hmac.new(self.secret_key, string_to_sign, hashlib.sha256).digest()).strip()


        if self.access_key == '':
            raise ValueError('HMAC User Name cannot be empty.')
        elif self.secret_key == '':
            raise ValueError('HMAC secret key cannot be empty.')
        else:
            r.headers['Authorization'] = '%s:%s' % (self.access_key, signature)

        return r


class HmacAuthPlugin(AuthPlugin):

    name = 'HMAC token auth'
    auth_type = 'visionect'
    description = 'Sign requests using a HMAC authentication method for JoanAssistant Visionect'

    def get_auth(self, username=None, password=None):
        return HmacAuth(username, password)
