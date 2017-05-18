# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcSmsNumQueryRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.biz_id = None
        self.current_page = None
        self.page_size = None
        self.query_date = None
        self.rec_num = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.sms.num.query'
