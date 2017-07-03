# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, Tag
from re import match


class StockStructure:
    def __init__(self, name, code, dates, negotiable_shares, restricted_shares, outstanding_shares, general_capitals):
        """
        :type name: str
        :type code: str
        :type dates: list[str]
        :type negotiable_shares: list[str]
        :type restricted_shares: list[str]
        :type outstanding_shares: list[str]
        :type general_capitals: list[str]
        """
        self.name = name
        self.code = code
        self.dates = dates
        self.negotiable_shares = negotiable_shares
        self.restricted_shares = restricted_shares
        self.outstanding_shares = outstanding_shares
        self.general_capitals = general_capitals
        pass

    def __repr__(self):
        return '<StockStructure name=%s, code=%s, \n\t' \
               'dates=%r, \n\t' \
               'negotiable_shares=%r, \n\t' \
               'restricted_shares=%r, \n\t' \
               'outstanding_shares=%r, \n\t' \
               'general_capitals=%r>' % \
               (self.name, self.code,
                self.dates,
                self.negotiable_shares,
                self.restricted_shares,
                self.outstanding_shares,
                self.general_capitals)


def main(code, enable_log=True):
    """
    :type code: str
    :type enable_log: bool
    :rtype: StockStructure | None
    """

    if match(r'\d+\.\w+', code) is None:
        print('code:%s is not valid' % code)
        return None

    code_part, market_part = [x.lower() for x in code.split('.')]

    url = 'http://www.cninfo.com.cn/search/searchzx.jsp'
    resp = requests.post(url, data={
        'sc': 'stock',
        'map': 'stockstructure',
        'stockID_': code_part
    })
    resp.encoding = 'gbk'
    soup = BeautifulSoup(resp.content, 'html.parser')
    tag = soup.find('script')
    content = tag.string.strip() if tag and tag.string else ''
    matched = match(r'location.href ="\.\./information/stockstructure/(\w+\.html)";', content)

    if matched is None:
        print('code:%s is not valid' % code)
        return None

    path_part = matched.group(1)

    url = 'http://www.cninfo.com.cn/information/stockstructure/%s' % path_part
    resp = requests.get(url)
    resp.encoding = 'gbk'
    status_code, content = resp.status_code, resp.text

    if status_code is not 200:
        print('code:%s is not valid' % code)
        return None

    soup = BeautifulSoup(content, 'html.parser')

    def find_td_with_text(text):
        """
        :type text: str
        :rtype: list[Tag]
        """
        tag = soup.find(name='td', text=text)
        """:type: Tag"""
        for td in tag.find_next_siblings('td'):
            yield td

    name = soup.find('strong', text='股票简称：').next_sibling or None
    dates = [td.string for td in find_td_with_text('变动日期')]
    """变动日期"""
    negotiable_shares = [td.string.strip() for td in find_td_with_text('已流通股份')]
    """已流通股份"""
    restricted_shares = [td.string.strip() for td in find_td_with_text('流通受限股份')]
    """流通受限股份"""
    outstanding_shares = [td.string.strip() for td in find_td_with_text('未流通股份')]
    """未流通股份"""
    general_capitals = [td.string.strip() for td in find_td_with_text('总股本')]
    """总股本"""
    child_count = min([len(dates), len(negotiable_shares), len(restricted_shares), len(general_capitals)])

    if child_count <= 0:
        return None

    dates = dates[:child_count]
    negotiable_shares = negotiable_shares[:child_count]
    restricted_shares = restricted_shares[:child_count]
    outstanding_shares = outstanding_shares[:child_count]
    general_capitals = general_capitals[:child_count]

    structure = StockStructure(name=name,
                               code=code,
                               dates=dates,
                               negotiable_shares=negotiable_shares,
                               restricted_shares=restricted_shares,
                               outstanding_shares=outstanding_shares,
                               general_capitals=general_capitals)

    if enable_log:
        print(structure)

    return structure
