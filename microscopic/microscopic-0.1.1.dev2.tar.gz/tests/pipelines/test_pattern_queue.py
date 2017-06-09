from functools import partial

from asynctest import mock

from microscopic import pattern
from microscopic.pipelines import pattern_queue


async def match_processor(match):
    return bytes(match) + b'processed'


async def test_pattern_queue():
    read_transport = mock.CoroutineMock()
    read_transport.read_chunk.side_effect = [b'test2', b'test1', b'test2', b'']

    result = []

    def append_result(chunk):
        result.append(bytes(chunk))

    write_transport = mock.CoroutineMock()
    write_transport.write_chunk.side_effect = append_result

    processor = match_processor
    pattern_factory = partial(pattern.PatternContext,
                              pattern=b'test1', chunk_size=10)

    await pattern_queue.pipeline(
        read_transport, write_transport, processor, pattern_factory)

    assert result == [b'test2', b'test1processed', b'test2']
