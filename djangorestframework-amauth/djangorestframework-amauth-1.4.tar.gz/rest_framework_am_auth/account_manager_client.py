# -*- coding: utf-8 -*-
import json
import logging
from urlparse import urljoin

from django.core.cache import cache
from django.contrib.auth.models import Permission
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

from .settings import am_auth_settings


__all__ = (
    'AccountManagerClient',
    'AccountManagerServices',
)


logger = logging.getLogger(__name__)


class AccountManagerClient(OAuth2Session):
    def __init__(self, client_id=None, client_secret=None):
        self._client_id = client_id
        self._client_secret = client_secret
        token = cache.get(am_auth_settings.TOKEN_CACHE_KEY)
        client = BackendApplicationClient(
            client_id=self.client_id,
        )
        super(AccountManagerClient, self).__init__(
            client=client,
            token=token,
        )
        if not token:
            logger.debug(
                "Token has not found in the cache (key='%s'). "
                "Requesting it from AccountManager.",
                am_auth_settings.TOKEN_CACHE_KEY
            )
            self._fetch_token()

    def _fetch_token(self):
        token = self.fetch_token(
            token_url=self._token_url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            verify=am_auth_settings.VERIFY_SSL_CERTIFICATE,
        )
        cache.set(am_auth_settings.TOKEN_CACHE_KEY, token, token['expires_in'])

    @property
    def client_id(self):
        return self._client_id or am_auth_settings.OAUTH2_CLIENT_ID

    @property
    def client_secret(self):
        return self._client_secret or am_auth_settings.OAUTH2_CLIENT_SECRET

    @property
    def account_manager_api_url(self):
        return am_auth_settings.API_URL

    @property
    def _token_url(self):
        return urljoin(self.account_manager_api_url, '/oauth2/v1/token/')

    def request(self, method, url, **kwargs):
        response = super(AccountManagerClient, self).request(method, url, **kwargs)
        if response.status_code in (401, 403):
            logger.info(
                'Response code is %s (%s). '
                'Trying to obtain a new token and make request again.',
                response.status_code,
                response.content,
            )
            self._fetch_token()
            response = super(AccountManagerClient, self).request(method, url, **kwargs)
        return response


class AccountManagerServices(object):
    def __init__(self):
        self.client = AccountManagerClient()

    def __del__(self):
        self.client.close()

    @property
    def api_url(self):
        return self.client.account_manager_api_url

    @property
    def _token_introspection_url(self):
        return urljoin(self.api_url, '/oauth2/v1/introspect-token/')

    def request(self, method, url, **kwargs):
        request_method = getattr(self.client, method)
        response = request_method(url, **kwargs)
        response.raise_for_status()
        return response.json()

    def introspect_token(self, token):
        return self.request(
            'post',
            self._token_introspection_url,
            data=json.dumps({'token': token}),
            verify=am_auth_settings.VERIFY_SSL_CERTIFICATE,
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
        )

    @property
    def _synchronize_permissions_url(self):
        return urljoin(
            self.api_url,
            '/service-api/v1/services/{service_id}'
            '/synchronize-permissions/'.format(
                service_id=am_auth_settings.SERVICE_ID,
            )
        )

    def synchronize_permissions(self):
        permissions = Permission.objects.all()
        request_data = {
            'data': {
                'attributes': {
                    'permissions': [
                        {
                            'codename': '{app_label}.{codename}'.format(
                                app_label=permission.content_type.app_label,
                                codename=permission.codename
                            ),
                            'name': permission.name,
                        } for permission in permissions
                        if (
                            not am_auth_settings.SYNC_APPS or
                            permission.content_type.app_label
                           )
                        in am_auth_settings.SYNC_APPS
                    ],
                },
                'type': 'services',
            }
        }
        return self.request(
            'post',
            self._synchronize_permissions_url,
            data=json.dumps(request_data),
            headers={
                'content-type': 'application/vnd.api+json',
            },
            verify=am_auth_settings.VERIFY_SSL_CERTIFICATE,
        )
