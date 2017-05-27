# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

USER_CONF_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'user.ini'
)
LOGIN_SECTION = 'packtpub'
BOOKS_SECTION = 'books'
LOGIN_KEY = 'login'
PASS_KEY = 'password'
PROJECT_URL = 'https://bitbucket.org/kchomski/pypackt'
PROJECT_DESC = (
    'Tool to claim your daily free eBooks at www.packtpub.com with ease.'
)
