#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author acrazing - joking.young@gmail.com
# @version 1.0.0
# @since 2017-05-22 23:54:42
#
# Client.py
#
from soulapi.Api import Api
from soulapi.Post import Post

version = '0.0.5'


class Client(Api):
    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        self.version = version
        self.post = Post(self)
