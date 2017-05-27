# -*- coding: utf-8 -*-
from typing import Union
from flask import request
from functools import wraps


def base_dn_from_url(url: str) -> str:
    """Split a url into a base_dn.

    :param url:  A url string.

    :Example:

        >>> base_dn_from_url('open_directory.local')
        'dc=open_directory,dc=local'
        >>> base_dn_from_url('api.open_directory.com')
        'dc=api,dc=open_directory,dc=com'

    """
    if url:
        parts = map(
            lambda s: 'dc={}'.format(s),
            (s for s in str(url).split('.') if s != '')
        )
        return ','.join(parts)


def username_from_request() -> Union[str, None]:
    """Get the username from the request, or ``None`` if not found

    """
    try:
        return request.authorization.username
    except AttributeError:
        pass
