"""This utils module will contain the utilities needed for the affiliations."""

from __future__ import absolute_import
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import importlib

from .affiliations_settings import (
    AFFILIATE_QUERY_STRING_KEY,
)


def strip_affiliate_part_from_url(url):
    """
    Take care of stripping away the affiliate part of an URL.

    returns the stripped URL. Remove the ? if AFFILIATE_QUERY_STRING_KEY is the
    only query string parameter.

    An example of what is meant by "strip away":
    The request has the URL:
        https://example.com/some/page?page_id=9&affiliate_id=1234wxyz&other=3.
    The affiliate part of the URL here is affiliate_id=1234wxyz. Thus, the
    stripped URL to redirect to should be:
        https://example.com/some/page?page_id=9&other=3.
     Remember to also remove the ? if affiliate_id is the only query string
     parameter.
    :param url:
    :return:
    """
    parsed_url = urlparse.urlparse(url)
    query = urlparse.parse_qs(parsed_url.query)
    query.pop(AFFILIATE_QUERY_STRING_KEY, None)
    parsed_url = parsed_url._replace(query=urlencode(query, True))

    return urlparse.urlunparse(parsed_url)


def convert_url_query_string_to_dict(url):
    """
    Will convert the url query string into a dict, and return it.

    :param url:
    :return:
    """
    return dict(
        urlparse.parse_qsl(
            urlparse.urlsplit(url).query
        )
    )


def import_from_path(path):
    """
    Will resolve the path, and return the function or class imported.

    :param path: a Python path to a function or class
    :return: the function or class resolved
    """
    module_str, to_import_str = path.rsplit('.', 1)
    module = importlib.import_module(module_str)

    return getattr(module, to_import_str)
