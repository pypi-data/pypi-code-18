# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib
import os

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'bml(#c5n-&)j03uf!7)#-(d95z(nz^xx6zw=_cxe+l&-=5al)p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'requests_tracker',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'testapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'testapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


#
# PyMySQL
#

try:
    import pymysql
except ImportError:
    pass
else:
    pymysql.install_as_MySQLdb()


#
# Django-celery
#

try:
    import djcelery
except ImportError:
    pass
else:
    djcelery.setup_loader()


#
# Django-nose
#

django_nose_installed = False

try:
    importlib.import_module('django_nose')
    django_nose_installed = True
except ImproperlyConfigured:
    django_nose_installed = True
except ImportError:
    pass

if django_nose_installed:
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#
# Coverage.py
#

try:
    importlib.import_module('coverage')
except ImportError:
    pass
else:
    cover_packages = []
    for app in INSTALLED_APPS:
        module_name = app.split('.')[0]
        if os.path.isfile(os.path.join(BASE_DIR, module_name, '__init__.py')):
            cover_packages.append(module_name)

    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=%s' % ','.join(cover_packages),
        '--cover-inclusive',
    ]
