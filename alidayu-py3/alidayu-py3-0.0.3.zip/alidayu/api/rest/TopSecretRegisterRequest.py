# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class TopSecretRegisterRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.user_id = None

    def get_api_name(self):
        return 'taobao.alidayu.secret.register'
