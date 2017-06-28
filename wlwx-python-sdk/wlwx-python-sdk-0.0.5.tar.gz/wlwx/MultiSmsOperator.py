#!/usr/bin/python3
# -*- coding:utf-8 -*-
# filename:MultiSmsOperator

__author__ = 'zhouzhao'
import hashlib,json
from wlwx.Config import wlwx_config
from wlwx import Result
from wlwx.HttpUtil import request_post
from urllib.parse import quote


class MultiSmsOperator(object):
    def __init__(self, cust_code=None, cust_pwd=None):
        if cust_code == None:
            raise Exception("please set cust_code")
        else:
            self.uid = cust_code
        if cust_pwd == None:
            raise Exception("please set cust_pwd")
        else:
            self.cust_pwd = cust_pwd
        self.srcphone = wlwx_config['SP_CODE']

    def send_multiSms(self, data=None):
        if not data:
            data = {}
        if 'item' not in data:
            return Result(None, 'item 为空')
        if len(data['item']) == 0:
            return Result(None, '短信包 为空')
        if 'srcphone' not in data:
            data['srcphone'] = self.srcphone
        msg = json.dumps(data['item'], ensure_ascii=False).replace(' ','')
        sign = quote(msg) + self.cust_pwd
        sign = sign.encode('utf-8')
        m = hashlib.md5()
        m.update(sign)
        sign = m.hexdigest()
        data['uid'] = self.uid
        data['msg'] = msg
        data['sign'] = sign
        del data['item']
        return request_post(self,wlwx_config['URI_SEND_MULTI_SMS'], data)