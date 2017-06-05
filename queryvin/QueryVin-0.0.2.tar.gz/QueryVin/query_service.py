# -*- coding: utf-8 -*-

import logging
from traceback import format_exc
import requests
from lxml import etree


class VinService(object):
    def __init__(self):
        self.session = requests.session()
        self.url = 'http://chinacar.com.cn/vin_index.html'
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'vin_cookie=8782',
            'Host': 'chinacar.com.cn',
            'Origin': 'http://chinacar.com.cn',
            'Referer': 'http://chinacar.com.cn/vin_index.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        }

    def run(self, left_vin, right_vin):
        """
        返回第一页的10条记录，如果有多页，暂时不考虑
        :param left_vin:
        :type left_vin: str
        :param right_vin:
        :type right_vin: str
        :return:
        :rtype: list
        [{
            u"车辆型号": u'朗逸牌SVW7167LSD轿车',
        },
        {
            u'车辆型号': u'别克牌SGM7162DAAA轿车',
        }]
        """
        data = {
            'leftvin': left_vin,
            'rightvin': right_vin,
            'textfield3': ''
        }
        res = []
        try:
            response = self.session.post(self.url, data=data, headers=self.header)
            tree = etree.HTML(response.text)
            t_bodys = tree.xpath(".//table[@class='table-list']//tr[position()>1]")
            head = tree.xpath(".//table[@class='table-list']//tr[1]/th/text()")
            for body in t_bodys:
                _body = body.xpath('.//td//text()')
                res.append(dict(zip(head, _body)))
            return res
        except Exception as e:
            logging.error(e)
            logging.error(format_exc())
            return res


if __name__ == "__main__":
    VinService().run('LSVAL218', 'B2366933')
