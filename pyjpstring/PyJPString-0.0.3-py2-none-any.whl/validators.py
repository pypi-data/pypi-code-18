# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from jpstring import patterns


def is_hiragana(text):
    '''渡された文字列がすべてひらがなかどうかを返します'''
    return bool(patterns.hiragana.match(text))


def is_katakana(text):
    '''渡された文字列がすべてカタカナかどうかを返します'''
    return bool(patterns.katakana.match(text))


def is_numeric(text):
    '''渡された文字列がすべて数字文字かどうかを返します'''
    return bool(patterns.numeric.match(text))


def is_zipcode(text, split=False):
    '''渡された文字列が郵便番号かどうかを返します'''
    if split:
        return bool(patterns.split_zipcode.match(text))
    else:
        return bool(patterns.zipcode.match(text))


def is_phone_number(text, split=False):
    '''渡された文字列が電話番号かどうかを返します'''
    if split:
        return bool(patterns.split_phone_number.match(text))
    else:
        return bool(patterns.phone_number.match(text))


def is_mobile_number(text, split=False):
    '''渡された文字列が携帯電話番号かどうかを返します'''
    if split:
        return bool(patterns.split_mobile_number.match(text))
    else:
        return bool(patterns.mobile_number.match(text))


def _length(text, combined_chars=False):
    count = len(text)
    if combined_chars:
        count += len(patterns.combined_chars.findall(text))
    return count


def max_length(text, max, **kwargs):
    '''渡された文字列の数が max 以下かどうかを返します。'''
    count = _length(text, **kwargs)
    return count <= max


def min_length(text, min, **kwargs):
    '''渡された文字列の数が min 以上かどうかを返します。'''
    count = _length(text, **kwargs)
    return count >= min


def between(text, min, max, **kwargs):
    '''渡された文字列の数が min 以上かつ、 max 以下かどうかを返します。'''
    count = _length(text, **kwargs)
    return min <= count <= max
