import pytest

from microscopic import pattern


@pytest.fixture
def ctx():
    ctx = pattern.PatternContext(b'fo+', chunk_size=4)
    with ctx:
        yield ctx
        drained = ctx.drain()
        drained = tuple(None if i is None else bytes(i) for i in drained)
        assert drained == (None, None)


def aslist(func):
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))
    return wrapper


@aslist
def unroll(ctx, buf_iter):
    for buf in buf_iter:
        for split, match in ctx.feed(buf):
            yield bytes(split), bytes(match) if \
                isinstance(match, memoryview) else None


def test_match_sanity(ctx):
    calls = [b' fo ']
    expected = [(b' ', b'fo'), (b' ', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_match_multiple(ctx):
    calls = [b'fo fo fo ']
    expected = [(b'', b'fo'), (b' ', b'fo'), (b' ', b'fo'), (b' ', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_nonmatch_sanity(ctx):
    calls = [b'    ']
    expected = [(b'    ', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_nonmatch_nocombine(ctx):
    calls = [b'test', b'test']
    expected = [(b'test', None), (b'test', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_match_drain(ctx):
    calls = [b'fo']

    result = unroll(ctx, calls)
    assert result == []
    assert ctx.drain() == (None, b'fo')


def test_nonmatch_drain(ctx):
    calls = [b'f']

    result = unroll(ctx, calls)
    assert result == []
    assert ctx.drain() == (b'f', None)


def test_match_overflow(ctx):
    calls = [b'foooo']
    expected = [(b'foooo', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_match_overflow_at_boundary(ctx):
    calls = [b'fooo', b'o']
    expected = [(b'foooo', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_match_at_boundary(ctx):
    calls = [b' f', b'o ']
    expected = [(b' ', None), (b'', b'fo'), (b' ', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_match_expands_at_boundary(ctx):
    calls = [b'fo', b'oo ']
    expected = [(b'', b'fooo'), (b' ', None)]

    result = unroll(ctx, calls)
    assert result == expected


def test_repr_dirty(ctx):
    assert 'dirty' not in repr(ctx)

    list(ctx.feed(b'a'))
    assert 'dirty' in repr(ctx)

    ctx.drain()
    assert 'dirty' not in repr(ctx)


def test_context_manager_dirty():
    with pytest.raises(RuntimeError):
        with pattern.PatternContext(b'', chunk_size=0) as ctx:
            list(ctx.feed(b''))


def test_context_manager_exception():
    with pytest.raises(TypeError):
        with pattern.PatternContext(b'', chunk_size=0):
            raise TypeError('test')


def test_string_pattern_encoded():
    ctx = pattern.PatternContext('test', chunk_size=4)

    assert ctx._sre.pattern == b'test'
