# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import re

from jpstring.string import (
    hiragana as _hiragana,
    hiragana_dakuon,
    hiragana_handakuon,
    katakana as _katakana,
    katakana_dakuon,
    katakana_handakuon,
)


def include(template, *patterns):
    return re.compile(template.format(*[p.pattern for p in patterns]))


hiragana = re.compile(r'^[{}　]+$'.format(_hiragana))


katakana = re.compile(r'^[{}　]+$'.format(_katakana))


numeric = re.compile(
    r'^[\d０-９零〇一壱壹弌二弐貳弍三参參弎四五伍六陸七漆柒八捌九玖十拾廿卅丗卌百千万萬億兆]+$',
)


zipcode = re.compile(r'^\d{7}$')
split_zipcode = re.compile(r'^\d{3}-\d{4}$')


# http://www.soumu.go.jp/main_sosiki/joho_tsusin/top/tel_number/number_shitei.html
phone_number = re.compile('|'.join((
    r'(?:^0\d{9}$)',
    r'(?:^0[5789]0[1-9]\d{7}$)',
    r'(?:^0800\d{3}\d{4}$)',
    r'(?:^0204\d{7}$)',
)))
split_phone_number = re.compile('|'.join((
    r'(?:^0\d{1}-\d{4}-\d{4}$)',
    r'(?:^0\d{2}-\d{3}-\d{4}$)',
    r'(?:^0\d{3}-\d{2}-\d{4}$)',
    r'(?:^0\d{4}-\d{1}-\d{4}$)',
    r'(?:^0[5789]0-[1-9]\d{3}-\d{4}$)',
    r'(?:^0120-\d{3}-\d{3}$)',
    r'(?:^0800-\d{3}-\d{4}$)',
    r'(?:^0570-\d{3}-\d{3}$)',
    r'(?:^0990-\d{3}-\d{3}$)',
    r'(?:^020-4\d{2}-\d{5}$)',
)))


mobile_number = re.compile(r'^0[789]0[1-9]\d{7}$')
split_mobile_number = re.compile(r'^0[789]0-[1-9]\d{3}-\d{4}$')


combined_chars = re.compile('[{}{}{}{}]'.format(
    hiragana_dakuon,
    hiragana_handakuon,
    katakana_dakuon,
    katakana_handakuon,
))
