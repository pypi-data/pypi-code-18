# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from operator import itemgetter
from collections import namedtuple


class User(dict):
    uid = property(itemgetter('uid'))
    name = property(itemgetter('name'))
    email = property(itemgetter('email'))


Token = namedtuple('Token', ['access_token', 'user'])

Anonymity = Token(None, None)
