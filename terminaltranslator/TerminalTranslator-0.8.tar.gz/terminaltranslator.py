#!/usr/bin/env python
# encoding: utf8
# author: veelion


from __future__ import print_function

import traceback
import json
try:
    # For Python 3
    from urllib.request import urlopen
    from urllib.request import quote
except ImportError:
    # For Python 2
    from urllib2 import urlopen
    from urllib import quote

RED = '\x1b[31m'
GRE = '\x1b[32m'
BRO = '\x1b[33m'
BLU = '\x1b[34m'
PUR = '\x1b[35m'
CYA = '\x1b[36m'
WHI = '\x1b[37m'
NOR = '\x1b[0m'

# http://fanyi.youdao.com/openapi?path=data-mode
YOUDAO_KEYFROM = 'translatorT'
YOUDAO_KEY = '1840641670'


def trans(q):
    print('translating...')
    url = ('http://fanyi.youdao.com/openapi.do?'
           'keyfrom=%s&key=%s&type=data&'
           'doctype=json&version=1.1&'
           'q=%s') % (YOUDAO_KEYFROM, YOUDAO_KEY, quote(q))
    try:
        r = urlopen(url)
        html = r.read()
        data = json.loads(html)
        if data['errorCode'] != 0:
            print(html)
            return
        print(BRO)  # 设置终端字体颜色
        print("================================")
        print(u"%s -> %s" % (data['query'], ','.join(data['translation'])))
        if 'basic' in data:
            if 'uk-phonetic' in data['basic']:
                print(u"英式发音: %s" % data['basic']['uk-phonetic'])
                print(u"美式发音: %s" % data['basic']['us-phonetic'])
            for e in data['basic']['explains']:
                print(u"%s" % e)
        if 'web' in data:
            print("")
            for e in data['web']:
                print(u"%s -> %s" % (e['key'], ','.join(e['value'])))
        print("================================")
        print(NOR)  # 恢复终端字体颜色
    except:
        traceback.print_exc()


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        q = argv[1]
        trans(q)

