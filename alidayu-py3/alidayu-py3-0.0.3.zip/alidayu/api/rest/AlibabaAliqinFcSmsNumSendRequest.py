# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcSmsNumSendRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.extend = None
        self.rec_num = None
        self.sms_free_sign_name = None
        self.sms_param = None
        self.sms_template_code = None
        self.sms_type = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.sms.num.send'
