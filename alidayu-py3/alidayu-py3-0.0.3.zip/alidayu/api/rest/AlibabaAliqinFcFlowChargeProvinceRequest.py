# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcFlowChargeProvinceRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.grade = None
        self.out_recharge_id = None
        self.phone_num = None
        self.reason = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.flow.charge.province'
