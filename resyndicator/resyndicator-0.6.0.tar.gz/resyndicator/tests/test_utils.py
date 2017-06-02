import pytest
from datetime import datetime
from ..utils.utils import process_time, decode_response, fixed_text, urn_from_string, typed_text


@pytest.mark.parametrize('input,output', [
    ('2017-04-30', datetime(2017, 4, 30, 0, 0)),
    ('2017-04-30 10:00 UTC', datetime(2017, 4, 30, 10, 0)),
    ('2017-04-30 10:00 UTC+1', datetime(2017, 4, 30, 11, 0)),
])
def test_process_time(input, output):
    assert process_time(input) == output


@pytest.mark.parametrize('input,output', [
    (b'B\xc3\xbcro', 'Büro'),
])
def test_decode_response(input, output):
    assert decode_response(type('response', (), {'content': input, 'headers': {}})) == output


@pytest.mark.parametrize('input,output', [
    ('“Q &amp; A”', '“Q & A”'),  # Replaces entities, maintains quotes
])
def test_fixed_text(input, output):
    assert fixed_text()(lambda self: input)(None) == output


@pytest.mark.parametrize('input,output', [
    ('da Pinci', 'urn:uuid:ed4251a3-5668-354c-aefd-6c08cf539ea8'),
])
def test_urn_from_string(input, output):
    assert urn_from_string(input) == output


@pytest.mark.parametrize('text,type,output', [
    ('<strong>da Pinci</strong>', 'html', {'text': '<strong>da Pinci</strong>', 'type': 'html'}),
    (None, 'html', None),
])
def test_typed_text(text, type, output):
    assert typed_text(text, type) == output
