import uuid
import hashlib
import time
import ftfy
from collections import OrderedDict
from datetime import datetime
from functools import wraps
from dateutil.parser import parse as parse_date
from dateutil.tz import tzutc
from utilofies.bslib import intelligent_decode
from .. import settings
from .logger import logger


def process_time(raw_date, default=None, default_tz=tzutc):
    if not raw_date:
        return default
    if type(raw_date) != time.struct_time:
        try:
            date = parse_date(raw_date)
        except (ValueError, AttributeError):
            return default
    else:
        date = datetime.fromtimestamp(time.mktime(raw_date))
    if date.tzinfo is None and default_tz is not None:
        date = date.replace(tzinfo=default_tz())
    return date.astimezone(tzutc()).replace(tzinfo=None)


def decode_response(response):
    if 'charset' not in response.headers.get('content-type', '').lower():
        # Reset default encoding
        # http://www.w3.org/International/O-HTTP-charset.en.php
        response.encoding = None
    dammit = intelligent_decode(
        markup=response.content, override_encodings=(response.encoding,))
    return dammit.unicode_markup


def stopwatch(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time.time()
        results = func(self, *args, **kwargs)
        took = time.time() - start
        if took > 1:
            logger.info('%r executed in %.2f', func, took)
        return results
    return wrapper


def fixed_text(**kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            """Wrap ftfy.fix_text to set defaults and ignore None"""
            kwargs.setdefault('uncurl_quotes', False)
            text = func(self)
            if text:
                return ftfy.fix_text(text, **kwargs)
        return wrapper
    return decorator


def ipython(args):
    import IPython  # Install it only if you need it.
    IPython.embed()


def urn_from_string(string):
    # MD5 just because the length fits (16 bytes)
    digest = hashlib.md5(string.encode('utf-8')).digest()
    return str(uuid.UUID(bytes=digest).urn)


def typed_text(text, type):
    if text:
        return {'text': text, 'type': type}


class Insert:

    def __init__(self, major, minor, start=None, stop=None):
        self.major = major
        self.minor = minor
        if start and stop:
            return self[start:stop]

    def __getitem__(self, slice_):
        start = slice_.start
        stop = slice_.stop
        return self.major[:start] + self.minor + self.major[stop:]


class FeedTemplate:

    @staticmethod
    def feed():
        feed = {
            'feed': OrderedDict([
                ('@xmlns', 'http://www.w3.org/2005/Atom'),
                ('id', None),
                ('title', None),
                ('author', {
                    'name': 'Resyndicator'
                }),
                ('updated', None),  # e.g., '2016-05-20T09,57,34Z'
                ('link', [
                    {
                        '@href': None,
                        '@rel': 'self'
                    },
                    {
                        '@href': settings.HUB,
                        '@rel': 'hub'
                    }
                ]),
                ('generator', 'Resyndicator'),
                ('entry', []),
            ])
        }
        if not settings.HUB:
            del feed['feed']['link'][1]
        return feed

    @staticmethod
    def entry():
        return {
            'id': None,
            'updated': None,  # e.g., '2016-05-20T09:57:34Z'
            'published': None,  # e.g., '2016-05-20T09:57:34Z'
            'title': None,
            'author': {
                'name': None,
            },
            'link': {
                '@href': None,
                '@rel': 'alternate'
            },
            'summary': {
                '@type': None,  # html or text
                '#text': None,
            },
            'content': {
                '@type': None,  # html or text
                '#text': None,
            },
            'source': {
                'id': None,
                'link': {
                    '@href': None,
                    '@rel': 'self',
                },
                'title': None,
            },
        }
