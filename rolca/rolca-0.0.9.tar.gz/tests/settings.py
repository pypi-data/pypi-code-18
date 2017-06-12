"""
Django settings for running tests for rolca-core package.

"""
import os

from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'

DEBUG = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rolca.core',
    'rolca.frontend',
)

ROOT_URLCONF = 'tests.urls'

LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'rolca.frontend.context_processors.ui_configuration',
            ],
        },
    },
]

LANGUAGES = (
    ('en', _('English')),
    ('sl', _('Slovene')),
)

LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('ROLCA_POSTGRESQL_NAME', 'rolca'),
        'USER': os.environ.get('ROLCA_POSTGRESQL_USER', 'rolca'),
        'HOST': os.environ.get('ROLCA_POSTGRESQL_HOST', 'localhost'),
        'PORT': int(os.environ.get('ROLCA_POSTGRESQL_PORT', 5432)),
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ROLCA_MAX_SIZE = 1048576
ROLCA_MAX_LONG_EDGE = 2400
ROLCA_ACCEPTED_FORMATS = ['JPEG']
