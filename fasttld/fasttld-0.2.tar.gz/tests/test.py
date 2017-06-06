#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fasttld import FastTLDExtract


import time
t1 = time.time()
import os

# print t.trie
# for k,v in t.trie.items():
#     print k + ' ' + str(t.trie[k])
# print t.trie['mm']
# print time.time() - t1
# print t.trie['au']['edu']['wa']
t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in xrange(1, 1000000):
    t.extract('1.cn', subdomain=True)
# print time.time() - t1
# print t.extract('111.user-define.com', subdomain=True)
t1 = time.time()
# import tldextract
#
# for i in xrange(1, 1000000):
#     tldextract.extract('1.cn')
# print time.time() - t1
#
# from tld import get_tld
# t1 = time.time()
# for i in xrange(1, 1000000):
#     get_tld('1.cn', fix_protocol=True)
# print time.time() - t1
# print t.trie['uk']
# print t.extract('abc.123.ck', format=False)

# print t.extract('www1.ck', format=False)
# print t.extract('www.ck', format=False)
# print t.extract('w1c.www.ck', format=False)
# print t.extract('w1c.abc.ck', format=False)
# print t.extract('www.google.co.uk')
# print t.extract('big.news.www.ck')
# print t.extract('abc.local')
from fasttld import update
update()
