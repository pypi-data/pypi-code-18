# -*- coding: utf-8 -*-


import os
import pyltp

import jieba.posseg

import oujago

_mode = 'ltp'
_support_modes = ['jieba', 'ltp', 'moran']

_jieba_instance = None
_ltp_instance = None
_moran_instance = None


class BasePOS(object):
    """Abstract Part-of_speech Tagging class.
    """

    def pos(self, input, **kwargs):
        raise NotImplementedError


class LTPPOS(BasePOS):
    """HIT-SCIR Language Technology Platform (LTP) POS Tagging.

    词性标注集
    ---------

    LTP 使用的是863词性标注集，其各个词性含义如下表。

    +-----+---------------------+------------+-----+-------------------+------------+
    | Tag | Description         | Example    | Tag | Description       | Example    |
    +=====+=====================+============+=====+===================+============+
    | a   | adjective           | 美丽       | ni  | organization name | 保险公司   |
    +-----+---------------------+------------+-----+-------------------+------------+
    | b   | other noun-modifier | 大型, 西式 | nl  | location noun     | 城郊       |
    +-----+---------------------+------------+-----+-------------------+------------+
    | c   | conjunction         | 和, 虽然   | ns  | geographical name | 北京       |
    +-----+---------------------+------------+-----+-------------------+------------+
    | d   | adverb              | 很         | nt  | temporal noun     | 近日, 明代 |
    +-----+---------------------+------------+-----+-------------------+------------+
    | e   | exclamation         | 哎         | nz  | other proper noun | 诺贝尔奖   |
    +-----+---------------------+------------+-----+-------------------+------------+
    | g   | morpheme            | 茨, 甥     | o   | onomatopoeia      | 哗啦       |
    +-----+---------------------+------------+-----+-------------------+------------+
    | h   | prefix              | 阿, 伪     | p   | preposition       | 在, 把     |
    +-----+---------------------+------------+-----+-------------------+------------+
    | i   | idiom               | 百花齐放   | q   | quantity          | 个         |
    +-----+---------------------+------------+-----+-------------------+------------+
    | j   | abbreviation        | 公检法     | r   | pronoun           | 我们       |
    +-----+---------------------+------------+-----+-------------------+------------+
    | k   | suffix              | 界, 率     | u   | auxiliary         | 的, 地     |
    +-----+---------------------+------------+-----+-------------------+------------+
    | m   | number              | 一, 第一   | v   | verb              | 跑, 学习   |
    +-----+---------------------+------------+-----+-------------------+------------+
    | n   | general noun        | 苹果       | wp  | punctuation       | ，。！     |
    +-----+---------------------+------------+-----+-------------------+------------+
    | nd  | direction noun      | 右侧       | ws  | foreign words     | CPU        |
    +-----+---------------------+------------+-----+-------------------+------------+
    | nh  | person name         | 杜甫, 汤姆 | x   | non-lexeme        | 萄, 翱     |
    +-----+---------------------+------------+-----+-------------------+------------+
    |     |                     |            | z   | descriptive words | 瑟瑟，匆匆 |
    +-----+---------------------+------------+-----+-------------------+------------+


    References
    ----------

    .. [1] http://ltp.readthedocs.io/zh_CN/latest/index.html
    """

    def __init__(self):
        pos_model_path = os.path.join(oujago.utils.DATA_PATH, 'ltp/pos.model')
        if not os.path.exists(pos_model_path):
            raise oujago.utils.LTPFileError()
        self.tagger = pyltp.Postagger()
        self.tagger.load(pos_model_path)

    def __del__(self):
        self.tagger.release()

    def pos(self, input, **kwargs):
        """LTP POS Tagging.

        Parameters
        ----------
        input : str, or list
            If ``str``, call LTP seg, then, perform LTP pos tag.

        Returns
        -------
        list
            POS tagged list.
        """
        if oujago.utils.type_(input) == 'str':
            input = oujago.nlp.seg(input, mode='ltp')
        return list(self.tagger.postag(input))


class JiebaPOS(BasePOS):
    def __init__(self):
        pass

    def pos(self, input, **kwargs):
        """Jieba POS Tagging.

        Parameters
        ----------
        input : str, or list
            If ``str``, call LTP seg, then, perform LTP pos tag.
        HMM : bool
            Whether to use the Hidden Markov Model.
        """
        if oujago.utils.is_list(input):
            input = ''.join(input)
        paris = jieba.posseg.lcut(input, **kwargs)
        return [p.flag for p in paris]


class MoranPOS(BasePOS):
    def __init__(self):
        pass

    def pos(self, input, **kwargs):
        pass


def set_pos_mode(mode):
    """Set the Part-of-Speech Tagging method.

    Parameters
    ----------
    mode : str
        The tagging method. Must in ``_support_methods``.

    """
    global _mode

    assert mode.lower() in _support_modes
    _method = mode.lower()


def get_pos_mode():
    """Get Part-of-Speech Tagging method.

    Returns
    -------
    str
        The global tagging method.
    """
    return _mode


def pos(input, mode=_mode, **kwargs):
    """Part-of-Speech Tagging.

    Examples:

        >>> from oujago.nlp.postag import pos
        >>> pos('我不喜欢日本和服', 'jieba')
        ['r', 'd', 'v', 'ns', 'nz']
        >>> pos('我不喜欢日本和服')
        ['r', 'd', 'v', 'ns', 'n']


    Parameters
    ----------
    input : str, or list
        To pos string.
    mode : str
        To specify the segment method, 'jieba', 'ltp', or 'moran'.

    Returns
    -------
    list
        Tagged list.

    """
    # check
    assert mode in _support_modes

    # jieba
    if mode == 'jieba':
        # init
        global _jieba_instance
        if _jieba_instance is None:
            _jieba_instance = JiebaPOS()

        # seg
        return _jieba_instance.pos(input, **kwargs)

    # LTP
    if mode == 'ltp':
        # init
        global _ltp_instance
        if _ltp_instance is None:
            _ltp_instance = LTPPOS()

        # seg
        return _ltp_instance.pos(input, **kwargs)

    # moran
    if mode == 'moran':
        # init
        global _moran_instance
        if _moran_instance is None:
            _moran_instance = MoranPOS()

        # seg
        return _moran_instance.pos(input, **kwargs)

    raise ValueError("Unknown mode: {}".format(mode))
