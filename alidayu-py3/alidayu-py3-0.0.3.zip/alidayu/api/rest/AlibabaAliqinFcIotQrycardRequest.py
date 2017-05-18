# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcIotQrycardRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.bill_real = None
        self.bill_source = None
        self.iccid = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.iot.qrycard'
