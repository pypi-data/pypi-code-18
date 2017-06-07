#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pickle

import requests
from tqdm import tqdm

import metadata

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def fetch_data(url):
    try:
        res = requests.get(url,
                           headers=HEADERS,
                           timeout=10)
        content_type = res.headers.get('content-type')
        raw = res.content
        return {'content-type': content_type,
                'byte_body': raw}
    except Exception as e:
        logging.exception(e)
        return None

def main():
    data = [{'meta': rec,
             'webdata': fetch_data(rec['url'])}
            for rec in tqdm(metadata.SAMPLES)
            if rec
           ]

    with open('test_data.pkl', 'wb') as fhandle:
        pickle.dump(data, fhandle, protocol=2)

main()
