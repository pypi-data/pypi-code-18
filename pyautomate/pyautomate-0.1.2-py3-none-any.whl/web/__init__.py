# coding: utf-8
import os
import sys
import stat
import platform
import subprocess
import time
import urllib
from urllib.parse import urlparse
import re
import importlib
import warnings
from collections import namedtuple

import requests
import pip
import pandas as pd
from selenium.webdriver.common.keys import Keys

from .html import Html
from ..__init__ import FileExistsWarning


def parse_html(src, encoding='utf-8'):
    """Returns BeautifulSoup from URL or file

    src: url or html string or file-like object
    """
    if not isinstance(src, str):
        raise ValueError('{} must be str, url, or html file')
    # check if url or filepath
    if src.startswith('http'):
        res = requests.get(src)
        res.raise_for_status()
        doc = res.text
    elif os.path.isfile(src):
        doc = open(src, encoding=encoding)
    else:
        doc = src

    return Html(doc)


def get_attribute(elem, attr):
    """ Get HTML Tag element attribute
    """
    if hasattr(elem, 'get'):
        return elem.get(attr)
    elif hasattr(elem, 'get_attribute'):
        return elem.get_attribute(attr)


def get_urls(elements):
    # control characters
    trans_map = dict.fromkeys(range(32))
    # add special characters
    trans_map.update(dict.fromkeys(list(range(166, 256)), ' '))

    Url = namedtuple('URL', ['text', 'url'])
    urls = []
    for elem in elements:
        url = get_attribute(elem, 'href')
        text = elem.text.translate(trans_map).strip()
        if text and url:
            urls.append(Url(text, url))

    return urls


def download(url, filepath, chunksize=100000, overwrite=False):
    if os.path.exists(filepath) and not overwrite:
        return warnings.warn(
            FileExistsWarning(filepath, 'overwrite=True to overwrite'))

    res = requests.get(url)
    res.raise_for_status()

    with open(filepath, 'wb') as target_file:
        for chunk in res.iter_content(chunksize):
            if chunk:
                target_file.write(chunk)


def unquote_url(url):
    if '+' in url:
        return urllib.parse.unquote_plus(url)
    return urllib.parse.unquote(url)


def get_browser(driverpath, browser='Chrome'):
    from selenium import webdriver
    driver = getattr(webdriver, browser)(driverpath)
    return driver


def setup_webdriver(driver_version, download_dir='.', test=False):
    print('chromedriver 다운로드')
    url = get_chromedriver_url(driver_version)
    # 다운로드 파일 경로 구성
    filename = url.split('/')[-1]
    filepath = os.path.join(download_dir, filename)
    download(url, filepath)

    # 압축 해제
    print('다운로드 받은 파일 압축 해제', end=' ... ')
    command_to_extract_zip = 'python -m zipfile -e {} .'
    command_to_extract_zip = command_to_extract_zip.format(filepath).split()
    subprocess.run(command_to_extract_zip, check=True)
    print('완료')

    # 실행권한 설정
    driverfile = 'chromedriver'
    if platform.system() == 'Windows':
        driverfile += '.exe'
    file_stat = os.stat(driverfile)
    os.chmod(driverfile, file_stat.st_mode | stat.S_IEXEC)

    if test:
        print('설정 테스트', end=' ... ')
        test_webdriver(driverfile)
        print('완료')


def get_chromedriver_url(version):
    driverfile_map = {
        'Windows': 'chromedriver_win32.zip',
        'Darwin': 'chromedriver_mac64.zip'}
    download_target = driverfile_map.get(platform.system(), None)

    if download_target is None:
        sys.exit('No chromedriver for {0}'.format(platform.system()))

    chromedriver_url = 'http://chromedriver.storage.googleapis.com/'
    chromedriver_url += '{}/{}'.format(version, download_target)
    return chromedriver_url


def test_webdriver(driverfile):
    from selenium import webdriver
    chrome = webdriver.Chrome(os.path.join('.', driverfile))
    chrome.get('http://www.gogle.com')
    time.sleep(1)
    search_box = chrome.find_element_by_name('q')
    search_box.send_keys('파이썬')
    time.sleep(1)
    search_box.submit()
    time.sleep(1)
    chrome.quit()
