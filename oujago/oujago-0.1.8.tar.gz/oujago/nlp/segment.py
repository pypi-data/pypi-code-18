# -*- coding: utf-8 -*-


import os

import oujago

try:
    import jieba
except ImportError:
    jieba = None

try:
    import pyltp
except ImportError:
    pyltp = None

try:
    import thulac
except ImportError:
    thulac = None

try:
    from thrift.protocol import TBinaryProtocol
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from .moran import Client
    from .moran import LARequest
except ImportError:
    TBinaryProtocol = None
    TSocket = None
    TTransport = None
    Client = None
    LARequest = None


_mode = 'jieba'
_support_modes = ['jieba', 'ltp', 'moran', 'thulac']

_jieba_instance = None
_ltp_instance = None
_moran_instance = None
_thulac_instance = None


class BaseSegment(object):
    """Abstract Segmentation class.
    """
    def seg(self, sentence, **kwargs):
        raise NotImplementedError


class LTPSeg(BaseSegment):
    """HIT-SCIR Language Technology Platform (LTP) Segmentation.

    分词标注集
    -----------

    +------+----------+------------+
    | 标记 | 含义     | 举例       |
    +======+==========+============+
    | B    | 词首     | __中__国   |
    +------+----------+------------+
    | I    | 词中     | 哈__工__大 |
    +------+----------+------------+
    | E    | 词尾     | 科__学__   |
    +------+----------+------------+
    | S    | 单字成词 | 的         |
    +------+----------+------------+

    References
    ----------

    .. [1] http://ltp.readthedocs.io/zh_CN/latest/index.html
    """

    def __init__(self):
        assert pyltp, 'Please install "pyltp" first, "pip install pyltp".'

        ltp_seg_path = os.path.join(oujago.utils.DATA_PATH, 'ltp/cws.model')
        if not os.path.exists(ltp_seg_path):
            raise oujago.utils.LTPFileError()

        self.segment = pyltp.Segmentor()
        self.segment.load(ltp_seg_path)

    def __del__(self):
        self.segment.release()

    def seg(self, sentence, **kwargs):
        return list(self.segment.segment(sentence))


class JiebaSeg(BaseSegment):
    """Jieba Chinese text segmentation.
    """

    def __init__(self):
        assert jieba, 'Please install "jieba" first, "pip install jieba".'

    def seg(self, sentence, **kwargs):
        """Segment method.

        Parameters
        ----------
        sentence : str
            The str(unicode) to be segmented.
        cut_all : bool
            Model type. True for full pattern, False for accurate pattern.
        HMM : bool
            Whether to use the Hidden Markov Model.

        Returns
        -------
        list
            Segmented words.
        """
        return jieba.lcut(sentence, **kwargs)


class MoranSeg(BaseSegment):
    """Moran Segmentation method. For internal use only.
    """

    def __init__(self):
        assert TBinaryProtocol and TSocket and TTransport, \
            'Please install "thrift" first, "pip install thrift".'

        # Make socket
        socket = TSocket.TSocket(host='101.201.28.224', port=8200)

        # Buffering is critical. Raw sockets are very slow
        self.transport = TTransport.TBufferedTransport(socket)
        self.transport.open()

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Create a client to use the protocol encoder
        self.client = Client(protocol)

    def seg(self, sentence, **kwargs):
        # prepare data
        req = LARequest()
        req.query = sentence

        # get results
        result = self.client.process(req)

        # format
        return [token.term for token in result.tokens]

    def __del__(self):
        self.transport.close()


def set_seg_mode(mode):
    """Set the segmentation method.

    Parameters
    ----------
    mode : str
        The segmentation method. Must in ``_support_methods``.

    """
    global _mode

    assert mode.lower() in _support_modes, 'Only support {}'.format(_support_modes)
    _mode = mode.lower()


def get_seg_mode():
    """Get segmentation method.

    Returns
    -------
    str
        The global segmentation method.
    """
    return _mode


def seg(sentence, mode=_mode, **kwargs):
    """Cut, segmentation.

    Examples:

        >>> from oujago.nlp.segment import seg
        >>> sentence = "这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。"
        >>> seg(sentence)
        ['这是', '一个', '伸手不见五指', '的', '黑夜', '。', '我', '叫', '孙悟空', '，', '我', '爱',
        '北京', '，', '我', '爱', 'Python', '和', 'C++', '。']
        >>> seg(sentence, mode='ltp')
        ['这', '是', '一个', '伸手', '不', '见', '五', '指', '的', '黑夜', '。', '我', '叫', '孙悟空',
        '，', '我', '爱', '北京', '，', '我', '爱', 'Python', '和', 'C', '+', '+', '。']
        >>> seg(sentence, mode='jieba')
        ['这是', '一个', '伸手不见五指', '的', '黑夜', '。', '我', '叫', '孙悟空', '，', '我', '爱',
        '北京', '，', '我', '爱', 'Python', '和', 'C++', '。']
        >>> seg(sentence, mode='moran')
        ['这', '是', '一', '个', '伸手', '不', '见', '五指', '的', '黑夜', '。', '我叫', '孙',
        '悟空', '，', '我', '爱', '北京', '，', '我', '爱', 'Python', '和', 'C++', '。']


    Parameters
    ----------
    sentence : str
        To seg string.
    mode : str
        To specify the segment method, 'jieba', 'ltp', or 'moran'.

    Returns
    -------
    list
        Segmented list.

    """
    # check
    assert mode in _support_modes

    # jieba
    if mode == 'jieba':
        # init
        global _jieba_instance
        if _jieba_instance is None:
            _jieba_instance = JiebaSeg()

        # seg
        return _jieba_instance.seg(sentence, **kwargs)

    # LTP
    if mode == 'ltp':
        # init
        global _ltp_instance
        if _ltp_instance is None:
            _ltp_instance = LTPSeg()

        # seg
        return _ltp_instance.seg(sentence, **kwargs)

    if mode == 'thulac':
        assert thulac, 'Please install "thulac" first.'

        raise NotImplementedError

    # moran
    if mode == 'moran':
        # init
        global _moran_instance
        if _moran_instance is None:
            _moran_instance = MoranSeg()

        # seg
        return _moran_instance.seg(sentence, **kwargs)

    raise ValueError("Unknown mode: {}".format(mode))
