# -*- coding: utf-8 -*-

"""
wcc.utils
----------

工具函数模块。
"""
import os.path
import base64
import calendar
import datetime
import time


def b64encode_as_string(data):
    return to_string(base64.b64encode(data))


def content_md5(data):
    """计算data的MD5值，经过Base64编码并返回str类型。

    返回值可以直接作为HTTP Content-Type头部的值
    """
    m = hashlib.md5(to_bytes(data))
    return b64encode_as_string(m.digest())


def md5_string(data):
    """返回 `data` 的MD5值，以十六进制可读字符串（32个小写字符）的方式。"""
    return hashlib.md5(to_bytes(data)).hexdigest()

