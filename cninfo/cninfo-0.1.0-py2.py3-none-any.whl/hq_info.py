# -*- coding: utf-8 -*-

import requests
import requests_cache
import pandas as pd
from datetime import timedelta
from tabulate import tabulate
from .hq import load


class HQInfo(object):
    def __init__(self, stock_code):
        with requests_cache.enabled('cache_db', expire_after=timedelta(hours=8), allowable_methods=('GET', 'POST')):
            res = requests.post('http://www.cninfo.com.cn/cninfo-new/data/query', data={
                'keyWord': '0',
                'maxNum': '10000',  # 最大数量
                'hq_or_cw': '2'  # '1' # 默认 hq + index | '2' # 股票 a 股 + b 股
            })
            self.stocks = pd.DataFrame(res.json())

        try:
            stock_info = self.stocks[self.stocks['code'] == stock_code]
            assert stock_info.empty is False, u'-'

            self.s = stock_info.to_dict('records')[0]
        except Exception as e:
            print(e)
            self.s = None

    def display_current(self):
        content = tabulate(
            {u'市场': [self.s['market']], u'分类': [self.s['category']], u'代码': [self.s['code']], u'简称': [self.s['zwjc']],
             u'上市年份': [self.s['startTime']], }, headers='keys', tablefmt='psql', showindex=False)
        print(content)

    __all__ = ['hq']

    def __getattr__(self, type):
        try:
            assert self.s is not None, '1'

            fn = {
                'hq': load,  # 历史日行情
                'lrb': load,  # 利润表
                'fzb': load,  # 资产表
                'llb': load,  # 现金表
            }.get(type, None)

            assert fn is not None, '2'
            return fn(self.s, type)
        except Exception as e:
            print(e)
