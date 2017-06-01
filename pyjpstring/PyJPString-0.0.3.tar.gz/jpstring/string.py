# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import six


hiragana = ''.join([six.unichr(x) for x in range(ord('ぁ'), ord('ゖ') + 1)] + ['ー'])
hiragana_dakuon = "がぎぐげござじずぜぞだぢづでどばびぶべぼゔ"
hiragana_handakuon = "ぱぴぷぺぽ"


katakana = ''.join([six.unichr(x) for x in range(ord('ァ'), ord('ヶ') + 1)] + ['ー'])
katakana_dakuon = "ガギグゲゴザジズゼゾダジヅデドバビブベボヴ"
katakana_handakuon = "パピプペポ"
