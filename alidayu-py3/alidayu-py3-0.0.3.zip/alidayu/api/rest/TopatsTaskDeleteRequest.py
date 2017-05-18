# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class TopatsTaskDeleteRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.task_id = None

    def get_api_name(self):
        return 'taobao.topats.task.delete'
