# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from django.core.cache import cache

from .account_manager_client import AccountManagerClient
from .settings import am_auth_settings


logger = logging.getLogger(__name__)


def get_token_info(token):
    token_info_cache_key = am_auth_settings.TOKEN_INFO_CACHE_KEY.format(
        token=token,
    )
    if am_auth_settings.TOKEN_INFO_TIMEOUT:
        logger.debug(
            "Trying to get TokenInfo from the cache (key='%s').",
            token_info_cache_key,
        )
        token_info = cache.get(token_info_cache_key)
    else:
        logger.debug('Caching TokenInfo is disabled.')
        token_info = None
    if not token_info:
        logger.debug(
            'TokenInfo has not gotten from the cache. '
            'Requesting it from AccountManager.'
        )
        account_manager_client = AccountManagerClient()
        token_info = account_manager_client.introspect_token(token)
        if am_auth_settings.TOKEN_INFO_TIMEOUT:
            logger.debug(
                'Caching TokenInfo %s with timeout %s.',
                token_info_cache_key,
                am_auth_settings.TOKEN_INFO_TIMEOUT,
            )
            cache.set(
                token_info_cache_key,
                token_info,
                am_auth_settings.TOKEN_INFO_TIMEOUT,
            )
    return AMOAuth2TokenInfo(token, token_info)


class AMOAuth2TokenInfo(object):
    def __init__(self, token, token_info):
        self._token_info = token_info
        self.token = token

    @cached_property
    def user(self):
        UserModel = get_user_model()
        user, _created = UserModel.objects.get_or_create(
            username=self._token_info['username'],
        )
        return user

    def user_has_perms(self, perms):
        return all(
            perm in self._token_info['scope']
            for perm in perms
        )
