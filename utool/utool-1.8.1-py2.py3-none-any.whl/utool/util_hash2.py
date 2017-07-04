import warnings
import uuid
import six
import numpy as np


def b(x):
    return six.binary_type(six.b(x))

if six.PY3:
    def _int_to_bytes(int_):
        return int_.to_bytes(8, byteorder='big')
else:
    import struct
    def _int_to_bytes(int_):
        return struct.pack('>i', int_)


def _update_hasher(hasher, data):
    """
    This is the clear winner over the generate version.
    Used by hash_data

    Ignore:
        import utool
        rng = np.random.RandomState(0)
        # str1 = rng.rand(0).dumps()
        str1 = b'SEP'
        str2 = rng.rand(10000).dumps()
        for timer in utool.Timerit(100, label='twocall'):
            hasher = hashlib.sha256()
            with timer:
                hasher.update(str1)
                hasher.update(str2)
        a = hasher.hexdigest()
        for timer in utool.Timerit(100, label='concat'):
            hasher = hashlib.sha256()
            with timer:
                hasher.update(str1 + str2)
        b = hasher.hexdigest()
        assert a == b
        # CONCLUSION: Faster to concat in case of prefixes and seps

        nested_data = {'1': [rng.rand(100), '2', '3'],
                       '2': ['1', '2', '3', '4', '5'],
                       '3': [('1', '2'), ('3', '4'), ('5', '6')]}
        data = list(nested_data.values())


        for timer in utool.Timerit(1000, label='cat-generate'):
            hasher = hashlib.sha256()
            with timer:
                hasher.update(b''.join(_serialize(data)))

        for timer in utool.Timerit(1000, label='inc-generate'):
            hasher = hashlib.sha256()
            with timer:
                for b in _serialize(data):
                    hasher.update(b)

        for timer in utool.Timerit(1000, label='inc-generate'):
            hasher = hashlib.sha256()
            with timer:
                for b in _serialize(data):
                    hasher.update(b)

        for timer in utool.Timerit(1000, label='chunk-inc-generate'):
            hasher = hashlib.sha256()
            import ubelt as ub
            with timer:
                for chunk in ub.chunks(_serialize(data), 5):
                    hasher.update(b''.join(chunk))

        for timer in utool.Timerit(1000, label='inc-update'):
            hasher = hashlib.sha256()
            with timer:
                _update_hasher(hasher, data)

        data = ut.lorium_ipsum()
        hash_data(data)
        ut.hashstr27(data)
        %timeit hash_data(data)
        %timeit ut.hashstr27(repr(data))

        for timer in utool.Timerit(100, label='twocall'):
            hasher = hashlib.sha256()
            with timer:
                hash_data(data)

        hasher = hashlib.sha256()
        hasher.update(memoryview(np.array([1])))
        print(hasher.hexdigest())

        hasher = hashlib.sha256()
        hasher.update(np.array(['1'], dtype=object))
        print(hasher.hexdigest())

    """
    for bytes_ in _serialize(data):
        hasher.update(bytes_)


def _serialize_item(data):
    r"""
    Args:
        data (?):

    Returns:
        ?:

    CommandLine:
        python -m utool.util_hash _serialize_item

    Example:
        >>> # DISABLE_DOCTEST
        >>> from utool.util_hash import *  # NOQA
        >>> from utool.util_hash import _serialize_item  # NOQA
        >>> import utool as ut
        >>> data = np.array([1], dtype=np.int64)
        >>> result = _serialize_item(data)
        >>> print(result)
    """
    if isinstance(data, six.binary_type):
        hashable = data
        prefix = b'TXT%d<' % (len(data))
    elif isinstance(data, six.text_type):
        # convert unicode into bytes
        hashable = data.encode('utf-8')
        prefix = b'TXT%d<' % (len(data))
    elif isinstance(data, np.ndarray):
        if data.dtype.kind == 'O':
            msg = '[ut] hashing ndarrays with dtype=object is unstable'
            warnings.warn(msg, RuntimeWarning)
            hashable = data.dumps()
        else:
            hashable = data.tobytes()
        prefix = b'NP<'
    elif isinstance(data, int):
        # warnings.warn('[util_hash] Hashing ints is slow, numpy is prefered')
        hashable = _int_to_bytes(data)
        prefix = b'INT<'
    elif isinstance(data, float):
        a, b = data.as_integer_ratio()
        hashable = (_int_to_bytes(a) + _int_to_bytes(b))
        prefix = b'FLT<'
    elif isinstance(data, uuid.UUID):
        hashable = data.bytes
        prefix = b'UUID<'
    elif isinstance(data, np.int64):
        return _serialize_item(int(data))
    elif isinstance(data, np.float64):
        return _serialize_item(float(data))
    else:
        raise TypeError('unknown hashable type=%r' % (type(data)))
    suffix = b'>'
    return prefix, hashable, suffix


def _serialize(data):
    """
        import utool
        rng = np.random.RandomState(0)
        nested_data = {'1': [rng.rand(100), '2', '3'],
                       '2': ['1', '2', '3', '4', '5'],
                       '3': [('1', '2'), ('3', '4'), ('5', '6')]}
        data = list(nested_data.values())
        bytes_ = b''.join(list(_serialize(data)))

        import bencode
        benbytes = bencode.Bencoder.encode(data)
        bencode.Bencoder.decode(benbytes)
    """
    # SLOWER METHOD
    if isinstance(data, (tuple, list)):
        # Ensure there is a iterable prefix with a spacer item
        SEP = b','
        yield b'ITER['
        iter_ = iter(data)
        try:
            # try to nest quickly without recursive calls
            for item in iter_:
                for bytes_ in _serialize_item(data):
                    yield bytes_
                yield SEP
        except TypeError:
            # recover from failed item and then continue iterating using slow
            # recursive calls
            for bytes_ in _serialize(item):
                yield bytes_
            yield SEP
            for item in iter_:
                for bytes_ in _serialize(item):
                    yield bytes_
                yield SEP
        yield b']'
    else:
        for bytes_ in _serialize_item(data):
            yield bytes_
