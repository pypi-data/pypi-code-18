# -*- coding: utf-8 -*-
"""
@date: 2017/5/18
@author: SongTao
@contact: songtao@kicen.com
"""
from alidayu.api.base import RestApi


class AlibabaAliqinFcVoiceNumDoublecallRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.called_num = None
        self.called_show_num = None
        self.caller_num = None
        self.caller_show_num = None
        self.extend = None
        self.session_time_out = None

    def get_api_name(self):
        return 'alibaba.aliqin.fc.voice.num.doublecall'
