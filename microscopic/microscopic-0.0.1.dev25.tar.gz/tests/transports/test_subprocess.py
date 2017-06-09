import pytest

from microscopic.transports import subprocess


def generate_code(chunk_size):
    test_code = """
import os
stdin, stdout = os.fdopen(0, 'rb', 0), os.fdopen(1, 'wb', 0)
while True:
    ret = stdin.read({chunk_size})
    if not ret:
        break
    stdout.write(ret.upper())
    """.format(chunk_size=chunk_size)
    return test_code


@pytest.fixture
def st(request):
    st = subprocess.SubprocessTransport(
        'python', '-c', generate_code(chunk_size=1),
        chunk_size=1)

    yield st

    assert st._process.returncode is not None


@pytest.mark.skip(reason="microscope#4")
async def test_sanity(st):
    async with st:
        await st.write_chunk(b't')
        result = await st.read_chunk()

    assert result == b'T'


async def test_context_manager_returns_self(st):
    async with st as st:
        assert isinstance(st, subprocess.SubprocessTransport)


async def test_context_terminates_process_on_throw(st):
    with pytest.raises(TypeError):
        async with st:
            raise TypeError('test')
