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

def encode_string(strval):
    """对一个str变量进行简单变换后,经过base64编码返回str类型
        Base64编码，64指A-Z、a-z、0-9、+和/这64个字符，还有“=”号不属于编码字符，而是填充字符。
    返回值是base64格式
    """
    strval = strval + "@"
    bytval = strval.encode(encoding="utf-8")
    bytval = base64.b64encode(bytval)
    return bytval.decode()

def decode_string(strval):
    """对一个str变量base64解码后做一个简单变换

    返回值是str类型
    """
    bytval = strval.encode(encoding="utf-8")
    bytval = base64.b64decode(bytval)
    strval = bytval.decode()
    strval = strval[:-1]
    return strval
