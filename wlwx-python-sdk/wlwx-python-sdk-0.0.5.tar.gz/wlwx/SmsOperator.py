#!/usr/bin/python3
# -*- coding:utf-8 -*-
# filename:SmsOperator

__author__ = 'zhouzhao'
import urllib,hashlib,json
from wlwx.Config import wlwx_config
from wlwx import Result
from wlwx.HttpUtil import request_post


class SmsOperator(object):
    def __init__(self, cust_code=None, cust_pwd=None):
        if cust_code == None:
            raise Exception("please set cust_code")
        else:
            self.cust_code = cust_code
        if cust_pwd == None:
            raise Exception("please set cust_pwd")
        else:
            self.cust_pwd = cust_pwd
        self.sp_code = wlwx_config['SP_CODE']
        self.need_report = wlwx_config['NEED_REPORT']
        self.uid = wlwx_config['UID']

    def send_comSms(self, data=None):
        if not data:
            data = {}
        if 'destMobiles' not in data:
            return Result(None, 'destMobiles 为空')
        if 'content' not in data:
            return Result(None, 'content 为空')
        if 'sp_code' not in data:
            data['sp_code'] = self.sp_code
        if 'need_report' not in data:
            data['need_report'] = self.need_report
        data['cust_code'] = self.cust_code
        sign = data['content'] + self.cust_pwd
        sign = sign.encode('utf-8')
        m = hashlib.md5()
        m.update(sign)
        sign = m.hexdigest()
        data['sign'] = sign
        print(sign)
        return request_post(self,wlwx_config['URI_SEND_COMMON_SMS'], json.dumps(data, ensure_ascii=False))

    def send_varSms(self, data=None):
        if not data:
            data = {}
        if 'content' not in data:
            return Result(None, 'content 为空')
        if 'params' not in data:
            return Result(None, 'params 为空')
        if len(data['params'][0]['vars']) != data['content'].count('${var'):
            return Result(None, '变量参数的个数不匹配')
        if 'sp_code' not in data:
            data['sp_code'] = self.sp_code
        data['cust_code'] = self.cust_code
        sign = data['content'] + self.cust_pwd
        sign = sign.encode('utf-8')
        m = hashlib.md5()
        m.update(sign)
        sign = m.hexdigest()
        data['sign'] = sign
        return request_post(self,wlwx_config['URI_SEND_VARIANT_SMS'], json.dumps(data, ensure_ascii=False))

    def get_token(self):
        return request_post(self, wlwx_config['URI_GET_TOKEN'], json.dumps({'cust_code':self.cust_code}, ensure_ascii=False)).content

    def get_queryInfo(self):
        data ={}
        data['cust_code'] = self.cust_code
        tokens= self.get_token()
        print(type(tokens))
        print(tokens)
        data['token_id'] = tokens['token_id']
        sign = tokens['token'] + self.cust_pwd
        sign = sign.encode('utf-8')
        m = hashlib.md5()
        m.update(sign)
        sign = m.hexdigest()
        data['sign'] = sign
        return  data

    def get_report(self):
        return request_post(self,wlwx_config['URI_GET_REPORT'], json.dumps(self.get_queryInfo(), ensure_ascii=False))

    def get_mo(self):
        return request_post(self,wlwx_config['URI_GET_MO'], json.dumps(self.get_queryInfo(), ensure_ascii=False))

    def get_account(self):
        return request_post(self,wlwx_config['URI_QUERY_ACCOUNT'], json.dumps(self.get_queryInfo(), ensure_ascii=False))