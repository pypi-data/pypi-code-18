# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import re
import unicodedata

import six

from jpstring.converters import (
    zenkaku_to_hankaku,
)


# Python3系には long はないので int に置き換える
if six.PY3:
    long = int


class TextNormalizer(object):
    bad_hyphen_pattern = re.compile('|'.join((
        six.unichr(0x2010),
        six.unichr(0x2011),
        six.unichr(0x2012),
        six.unichr(0x2013),
        six.unichr(0x2014),
        six.unichr(0x2015),
        six.unichr(0x2043),
        six.unichr(0x2212),
    )))

    invalid_hyphen_pattern = re.compile(r'(?:ｰ+ *\d+ *ｰ*)|(?:ｰ* *\d+ *ｰ+)')

    def __call__(self, text):
        '''
        テキスト内の英数字と記号は半角文字、その他は全角文字に正規化します。
        '''
        # 結合文字の濁点を単独文字に変更
        text = text.replace('\u3099', '\u309B')

        # 結合文字の半濁点を単独文字に変更
        text = text.replace('\u309A', '\u309C')

        # 「フ゛」等に対応するため、カタカナを一度半角にする。
        text = zenkaku_to_hankaku(text)

        # ハイフンの代わりに半角の長音記号が使用されている場合の対応。
        text = self.invalid_hyphen_pattern.sub(
            self._replace_invalid_hyphen,
            text
        )

        # ハイフンを置換
        text = self.bad_hyphen_pattern.sub('-', text)

        # 正規化
        text = unicodedata.normalize('NFKC', text)

        # 前頭と末尾のwhitespaceを削除。
        text = text.strip(' \t\r\n')

        return text

    def _replace_invalid_hyphen(self, match):
        text = match.group()
        text = text.replace('ｰ', '-')
        text = text.replace(' ', '')
        return text


normalize_text = TextNormalizer()


class NumericNormalizer(object):
    numeric_pattern = re.compile(
        r'[\d{}{}{}{}{}{}\.．,，]+'.format(
            r'０１２３４５６７８９',
            r'〇一二三四五六七八九',
            r'零壱壹弌弐貳弍参參弎伍陸漆柒捌玖',
            r'十百千',
            r'拾廿卅丗卌佰阡',
            r'万萬億兆',
        ),
    )

    numeric_transmap = {
        ord('零'): '0', ord('〇'): '0', ord('０'): '0',
        ord('一'): '1', ord('壱'): '1', ord('壹'): '1', ord('１'): '1',
        ord('弌'): '2', ord('二'): '2', ord('２'): '2',
        ord('弐'): '3', ord('貳'): '3', ord('弍'): '3', ord('三'): '3',
        ord('参'): '3', ord('參'): '3', ord('弎'): '3', ord('３'): '3', 
        ord('四'): '4', ord('４'): '4',
        ord('五'): '5', ord('伍'): '5', ord('５'): '5',
        ord('六'): '6', ord('陸'): '6', ord('６'): '6',
        ord('七'): '7', ord('漆'): '7', ord('柒'): '7', ord('７'): '7',
        ord('八'): '8', ord('捌'): '8', ord('８'): '8',
        ord('九'): '9', ord('玖'): '9', ord('９'): '9',
        ord(','): '', ord('，'): '',
        ord('．'): '.',
    }

    def __call__(self, text):
        return self.numeric_pattern.sub(self._normalize_numeric, text)

    def _normalize_numeric(self, numeric):
        '''
        テキスト内の数字文字を正規化します。
        '''
        if type(numeric).__name__ == 'SRE_Match':
            numeric = numeric.group()

        numeric = numeric.translate(self.numeric_transmap)

        total = 0

        result = re.findall('([^{0}]*)([{0}])?'.format('万萬億兆'), numeric)
        for value, unit in result:
            if not value and not unit:
                continue
            total += self._convert_large_value(value, unit)

        if total % 1.0 == 0.0:
            total = long(total)

        return str(total)

    def _convert_large_value(self, value, unit):
        power = unicodedata.numeric(unit) if unit else 1

        total = 0

        result = re.findall('([^{0}]*)([{0}])?'.format('十拾廿卅丗卌百佰千阡'), value)
        for value, unit in result:
            if not value and not unit:
                continue
            total += self._convert_small_value(value, unit)

        total = total * power

        return total

    def _convert_small_value(self, value, unit):
        power = unicodedata.numeric(unit) if unit else 1

        value = value if value else '1'
        total = float(value) * power

        return total


normalize_numeric = NumericNormalizer()
