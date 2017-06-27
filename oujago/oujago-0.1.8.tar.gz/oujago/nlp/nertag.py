# -*- coding: utf-8 -*-

"""
Named Entity Recognition

"""

import os
import pyltp
import oujago


_mode = 'ltp'
_support_modes = ['ltp']

_ltp_instance = None


class BaseNER(object):
    """Abstract NOR class.
    """
    def recognize(self, sentence=None, words=None, postags=None, **kwargs):
        raise NotImplementedError


class LTPNER(BaseNER):
    """HIT-SCIR Language Technology Platform (LTP) NER Tagging.

    命名实体识别标注集
    -------------------

    NE识别模块的标注结果采用O-S-B-I-E标注形式，其含义为

    +------+----------------------+
    | 标记 | 含义                 |
    +======+======================+
    | O    | 这个词不是NE         |
    +------+----------------------+
    | S    | 这个词单独构成一个NE |
    +------+----------------------+
    | B    | 这个词为一个NE的开始 |
    +------+----------------------+
    | I    | 这个词为一个NE的中间 |
    +------+----------------------+
    | E    | 这个词位一个NE的结尾 |
    +------+----------------------+

    LTP中的NE 模块识别三种NE，分别如下：

    +------+--------+
    | 标记 | 含义   |
    +======+========+
    | Nh   | 人名   |
    +------+--------+
    | Ni   | 机构名 |
    +------+--------+
    | Ns   | 地名   |
    +------+--------+

    References
    ----------

    .. [1] http://ltp.readthedocs.io/zh_CN/latest/index.html
    """
    def __init__(self):
        ner_path = os.path.join(oujago.utils.DATA_PATH, 'ltp/ner.model')
        if not os.path.exists(ner_path):
            raise oujago.utils.LTPFileError()
        self.recognizer = pyltp.NamedEntityRecognizer()
        self.recognizer.load(ner_path)

    def __del__(self):
        self.recognizer.release()

    def recognize(self, sentence=None, words=None, postags=None, **kwargs):
        if sentence is None:
            assert words and postags
        else:
            assert sentence is not None
            words = oujago.nlp.seg(sentence)
            postags = oujago.nlp.pos(words)
        return list(self.recognizer.recognize(words, postags))


def ner(sentence=None, words=None, postags=None, mode=_mode, **kwargs):

    # LTP
    if mode == 'ltp':
        # init
        global _ltp_instance
        if _ltp_instance is None:
            _ltp_instance = LTPNER()

        # NER
        return _ltp_instance.pos(sentence, words, postags, **kwargs)

    raise ValueError("Unknown mode: {}".format(mode))

