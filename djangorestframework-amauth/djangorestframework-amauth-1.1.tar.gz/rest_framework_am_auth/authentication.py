# -*- coding: utf-8 -*-
import logging
from requests.exceptions import HTTPError

from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .token_info import get_token_info
from .settings import am_auth_settings


logger = logging.getLogger(__name__)


class AMOAuth2TokenAuthentication(TokenAuthentication):
    @property
    def keyword(self):
        return am_auth_settings.TOKEN_TYPE

    def authenticate_credentials(self, key):
        try:
            logger.debug('Trying to get token info for %s', key)
            token_info = get_token_info(key)
        except HTTPError as e:
            logger.debug(e)
            if e.response.status_code == 400:
                raise AuthenticationFailed(_('Invalid token.'))
            if e.response.status_code in (401, 403):
                raise AuthenticationFailed(_(
                    'Cannot authorize the service on AccountManager.'
                ))
            if 500 <= e.response.status_code <= 599:
                raise AuthenticationFailed(_(
                    'Authorization server responded with HTTP 5xx.'
                ))
            else:
                raise e
        return (token_info.user, token_info)
