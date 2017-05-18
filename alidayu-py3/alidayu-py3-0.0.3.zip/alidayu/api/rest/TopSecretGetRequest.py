# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class TopSecretGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.customer_user_id = None
        self.random_num = None
        self.secret_version = None

    def get_api_name(self):
        return 'taobao.alidayu.secret.get'
