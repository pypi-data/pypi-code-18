# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcIotRechargeCardRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.bill_real = None
        self.bill_source = None
        self.eff_code = None
        self.iccid = None
        self.offer_id = None
        self.out_recharge_id = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.iot.rechargeCard'
