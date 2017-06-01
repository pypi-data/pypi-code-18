# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

import re

import six
import zenhan


hiragana_pattern = re.compile(r'[ぁ-ゖ]')


def hiragana_to_katakana(text):
    '''ひらがなをカタカナに変換します。'''
    return hiragana_pattern.sub(
        lambda x: six.unichr(ord(x.group(0)) + 0x60),
        text,
    )


katakana_pattern = re.compile(r'[ァ-ヶ]')


def katakana_to_hiragana(text):
    '''カタカナをひらがなに変換します。'''
    return katakana_pattern.sub(
        lambda x: six.unichr(ord(x.group(0)) - 0x60),
        text,
    )


def zenkaku_to_hankaku(text):
    '''全角文字を半角文字に変換します。'''
    return zenhan.z2h(text, mode=7)


def hankaku_to_zenkaku(text):
    '''半角文字を全角文字に変換します。'''
    return zenhan.h2z(text, mode=7)


def numeric_to_kanji(number):
    '''
    数字を漢数字に変換します。
    '''
    return re.sub(r'\d+', _numeric_to_kanji, number)


def _numeric_to_kanji(numeric):
    if type(numeric).__name__ == 'SRE_Match':
        numeric = numeric.group()

    if numeric == '0':
        return '〇'

    nums = ('', '一', '二', '三', '四', '五', '六', '七', '八', '九')
    units1 = ('', '十', '百', '千')
    units2 = ('', '万', '億', '兆', '京')
    text = ''
    numeric = numeric[::-1]

    for i in range(0, len(numeric), 4):
        buf = ''
        for j, char in enumerate(numeric[i:i+4]):
            v = int(char)
            if j == 0:
                buf += nums[v]
            elif v > 0:
                buf += units1[j]
                if v > 1:
                    buf += nums[v]
        if buf:
            text += units2[int(i / 4)] + buf
        buf = ''
    return text[::-1]
