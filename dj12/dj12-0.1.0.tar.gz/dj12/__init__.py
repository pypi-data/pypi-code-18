"""
django12factor: Bringing 12factor configuration to Django.

* https://12factor.net/
* https://12factor.net/config
* https://github.com/doismellburning/django12factor
"""

import django_cache_url
import dj_database_url
import dj_email_url
import os
import logging
import six
import sys

from ._bool import to_bool

logger = logging.getLogger(__name__)


def _get_many(key, default, transform):
    config = {}

    for (k, v) in six.iteritems(os.environ):
        _SUFFIX = '_' + key
        _OFFSET = len(_SUFFIX)

        if k.endswith(_SUFFIX):
            prefix = k[:-_OFFSET]

            if not prefix.isupper():
                # i.e. it was not already all upper-cased
                logger.warning("Ignoring %s because the prefix (%s) is not all upper-case - dj12 will automatically convert prefixes to lower-case", key, prefix)
                continue

            config[prefix.lower()] = transform(v)

    if not 'default' in config:
        config['default'] = transform(os.getenv(key, default))

    return config


def get_config():
    settings = dict(
        USE_I18N = True,
        USE_L10N = True,
        USE_TZ = True,

        SECRET_KEY = os.getenv('SECRET_KEY'),
        ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(','),
        DEBUG = to_bool(os.getenv('DEBUG'), False),

        DATABASES = _get_many('DATABASE_URL', 'sqlite:///db.sqlite3', dj_database_url.parse),
        CACHES = _get_many('CACHE_URL', 'locmem://', django_cache_url.parse),
        DEFAULT_FROM_EMAIL = os.getenv('EMAIL_FROM', "webmaster@localhost"),

        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if to_bool(os.getenv('TRUST_X_FORWARDED_PROTO'), False) else None,

        LANGUAGE_CODE = os.getenv('LANG', 'en-us').replace('_', '-').split('.', 1)[0].lower(),
        TIME_ZONE = os.getenv('TIME_ZONE', 'UTC'),

        RAVEN_CONFIG = dict(
            dsn = os.getenv('RAVEN_URL'),
        ),
    )
    settings.update(dj_email_url.parse(os.getenv('EMAIL_URL', 'dummy://')))

    if settings['LANGUAGE_CODE'] == 'c':
        settings['LANGUAGE_CODE'] = 'en-us'

    settings['LOGGING'] = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'stderr': {
                'level': 'INFO' if not settings['DEBUG'] else 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'root': {
            'handlers': ['stderr'],
        },
    }

    if not settings['SECRET_KEY']:
        if settings['DEBUG']:
            settings['SECRET_KEY'] = 'debugkey'
        else:
            sys.exit("""DEBUG is False but no SECRET_KEY is set in the environment - either it has been hardcoded (bad) or not set at all (bad) - exit()ing for safety reasons""")

    return settings
