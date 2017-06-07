from html_to_etree import (_decode_bytes, parse_html_bytes,
                           clean_html, _detect_encoding)

import logging

import pickle

from lxml import etree
from html_text import extract_text

TEST_DATA = None

BLACKLIST = [
    'http://ppomppu.co.kr/',  # cchardet detects 'utf-8' instead of 'euc-kr'
]


def get_data():
    if TEST_DATA:
        return TEST_DATA

    with open('tests/test_data.pkl', 'rb') as fhandle:
        data = pickle.load(fhandle)
        return [x for x in data
                if len(clean_html(x['webdata']['byte_body'])) > 1000
                and x['meta']['url'] not in BLACKLIST]


def test_contains():
    for rec in get_data():
        meta = rec['meta']
        url = meta['url']
        webdata = rec['webdata']

        encoding, uni = _decode_bytes(body=webdata['byte_body'],
                                      content_type=webdata['content-type'])
        contains = meta['contains']
        logging.warning('%s %s', url, encoding)
        assert contains in uni, (url, contains, uni)


def test_tree():
    for rec in get_data():
        meta = rec['meta']
        url = meta['url']
        contains = meta['contains']

        webdata = rec['webdata']
        body = webdata['byte_body']
        content_type = webdata['content-type']

        if len(clean_html(body)) < 100:
            logging.warning('skipping %s', url)
            continue

        tree = parse_html_bytes(body=body,
                                content_type=content_type)

        assert contains in extract_text(tree), (
            url, contains, etree.tostring(tree, encoding='utf-8'))
