# -*- coding: utf-8 -*-

import os
import codecs
import shutil
import requests
import pandas as pd

from datetime import datetime
from zipfile import ZipFile


def load(s, type):
    cache_files = download(s, type)

    df_from_each_file = (pd.read_csv(f) for f in cache_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

    return concatenated_df


def download(s, type):
    code = s.get('code', '')
    market = s.get('market', '')

    res = requests.post('http://www.cninfo.com.cn/cninfo-new/data/download', data={
        'code': code,
        'type': type,
        'market': market,
        'orgid': s.get('orgId', ''),
        'minYear': s.get('startTime', ''),
        'maxYear': datetime.now().year,
        'K_code': ''
    }, stream=True)
    res.raise_for_status()

    if not os.path.isdir('zips'):
        os.mkdir('zips')

    cache_db_file = 'zips/%s.%s-%s.zip' % (code, market, type)

    with open(cache_db_file, 'wb') as out_file:
        shutil.copyfileobj(res.raw, out_file)
        print('saved as zip')

    with ZipFile(cache_db_file) as zf:
        # zf.extractall('cache/%s.%s' % (code, market))
        zf.extractall('cache')
        print('extract all csv')

    if not os.path.isdir('cache/%s/%s/%s' % (market, type, code)):
        os.makedirs('cache/%s/%s/%s' % (market, type, code))

    cache_files = []
    for i in os.listdir('cache'):

        src_path = 'cache/%s' % i
        if not os.path.isfile(src_path):
            continue

        tar_path = 'cache/%s' % i.replace('_', '/')

        content = codecs.open(src_path, 'rb+', 'GB2312').read()
        codecs.open(src_path, 'w', encoding='utf-8').write(content)

        shutil.move(src_path, tar_path)
        cache_files.append(tar_path)
    return cache_files

    # load csv to pandas and return
