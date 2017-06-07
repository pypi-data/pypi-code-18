#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- notifyAll.config.local
~~~~~~~~~~~~~~

- Local dev environment settings
"""

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydb',
    }
}
#
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER='akki.inforian@gmail.com'
# EMAIL_HOST_PASSWORD='odeskakki'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#
# EMAIL_PORT = 587

