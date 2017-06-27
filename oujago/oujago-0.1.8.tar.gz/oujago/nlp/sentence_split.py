# -*- coding: utf-8 -*-

"""
Named Entity Recognition

"""

from pyltp import SentenceSplitter


_mode = 'raw'
_support_modes = ['ltp', 'raw']


def sen_split(text, mode=_mode, **kwargs):
    """Sentence Split.

    Parameters
    ----------
    text : str
        To split text.
    mode : str
        Sentence split mode. Must in ``_support_modes``.

    Returns
    -------
    list
        A list of sentences.
    """

    if mode == 'raw':
        raise NotImplementedError


    # LTP
    if mode == 'ltp':
        return list(SentenceSplitter.split(text))

    raise ValueError("Unknown mode: {}".format(mode))


