import calendar
import datetime as dt
from unittest import TestCase

import jwt

from mbq import tokens
from tests.compat import mock


# keys generated just for these tests
PUBLIC_KEY = """\
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmEYt/zXyPGjhivR56rfO
BcM35PrFlfhbOxYE7rtxltQ/Cj9Cd6WSvaKGCMyPn8AYtfGISEdeQGi0wsbbI3Wi
KkzZcdylO0MqMAX7MgwL8joPXItP0H463X9nR7wWUQ2AsqH7VKC0woSs4ZRI7TM9
O0v/gw0YP1csuPbM/NT4RTTN25LgaQrnOQqg3ECG09avy40BEoN+wZVh8kNdxEKo
zi9tEzEI3+DhXwV2e2zbmjhmE90nGn39EZZeoKdzoJl0JSvcreb44j73aXsaNm/A
c9HPkmw0LtE4JnHyxSHP66RXU+bKl2nDbdtj3hO13IcYDDlG0EImfBP3mtiI1T5/
CQIDAQAB
-----END PUBLIC KEY-----
"""

PRIVATE_KEY = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAmEYt/zXyPGjhivR56rfOBcM35PrFlfhbOxYE7rtxltQ/Cj9C
d6WSvaKGCMyPn8AYtfGISEdeQGi0wsbbI3WiKkzZcdylO0MqMAX7MgwL8joPXItP
0H463X9nR7wWUQ2AsqH7VKC0woSs4ZRI7TM9O0v/gw0YP1csuPbM/NT4RTTN25Lg
aQrnOQqg3ECG09avy40BEoN+wZVh8kNdxEKozi9tEzEI3+DhXwV2e2zbmjhmE90n
Gn39EZZeoKdzoJl0JSvcreb44j73aXsaNm/Ac9HPkmw0LtE4JnHyxSHP66RXU+bK
l2nDbdtj3hO13IcYDDlG0EImfBP3mtiI1T5/CQIDAQABAoIBAGzH5eAlx7EEM+uy
js3xFMrlFS8NPs3OKE5jgo6RdaoMYiSN4IvcyqGSUzJCAHBdKMoBjBwmb9yPcGKc
8Lu6M2kIkWZX++oEJ0U7YKH2HSqj84lnNFN7ec32T+/dHAw3GzOBqCxiyf8UDPTx
m89oBVwxBI24cxP80MQp+3K7Kck1v6mi4EHBQoOWu+csuAb6Zfbg/57wyfyf4BlG
UxoENc++CO40nMMY1QnTwY/haEO3YBgqOb/bx/IzXcLvRKpmI8Py5URAghItPWac
w58qnfzjyZndKNeO8EAVQW01OKMnEcXEuWYdhK0ZqjgJzBSbG06Z8lYrDJHtHmRg
7PZFOgkCgYEAxaEI45XR7vZjmlIhfPiBVsIqvElA8Rwux//o/xjxwlAjfZHdvdPZ
EQZK3rwCWnX3BVLPtRCy5MTdSsYy6NVjMYJWgRjgTYkgH185pETjT2GZbN8L+mIZ
KHbEgfF9mB9VZEiAARnRAzcVb8johF+VJO8txE0u147qLPZIfT7G+WsCgYEAxT/O
pOhMfS6v/u24/QqeQLJ4cbCIEXMVzXAXqIovDfMYWB4HgGqE/HVrpj1na3MP2Zla
bJd4qSK+WVEjPEZ/5vWaqGPb86GQZ8AZGEQ2ViZHLeHDGA7tMHHewPDp2+l8thrR
iZ63egBuOpamhH1l3xHGKOQiriP524UPVSLzAlsCgYAP1BsDJ1++FOvbU1KtULYD
Pd/wXqmd5hT1HdEKhXPvjT2adBFff9U14NwkRMineCVFvuE17lV1rzLOJ1uyfEzK
jVbiVhy4+Q+ik5zpRD80f2urZZ3u+uZq8EBC7BWUFoZfVtMxw2CTMlk8L8o3t/QZ
FjMDMu9agm7NFRivN1T2awKBgQCBgYxWn6KgykeJdGFx2kffKI6F7qbX9hzJfqA5
60hLu2Evcb/xI37fFuUwB77gQHKWpuZEyArT2djqYahlyc/uPzFk//OI+XoLdIfF
c/vNAmLXkBP8tsgqd4kOWt7goWNdWSxcVBYZBzFYTFNWR9Lb7BqT/H18omhJJgrU
FhdBYwKBgQCntS1HVvC+GNxWJyIQiAlbpteoL8UYC3WsS0NimazjgFtAvkBM+/rg
CErdg9ZC7HTre1NGeCbptUCT04kWh526Pe6DY+j6lJJMKSuCNfwxY2J2iAi0rook
4+G/NY6FBTLWWUQbX1p9d+KNNiOJy5unZFy27w55TLpmHJ4yKrCkDw==
-----END RSA PRIVATE KEY-----
"""


def since_epoch():
    return calendar.timegm(dt.datetime.utcnow().utctimetuple())


def make_jwt(audience=None):
    now = dt.datetime.utcnow()
    claims = {
        'aud': audience or 'test_audience',
        'iat': now,
        'exp': now + dt.timedelta(minutes=1),
        'iss': 'https://example.auth0.com/',
        'sub': 'abc123|test@example.com',
    }
    return jwt.encode(claims, PRIVATE_KEY, algorithm='RS256')


class DecoderTest(TestCase):

    def test_init_public_key_required(self):
        with self.assertRaises(tokens.TokenError):
            tokens.Decoder(allowed_audiences=[])

    def test_init_allowed_audiences(self):
        with self.assertRaises(tokens.TokenError):
            tokens.Decoder(public_key='test', allowed_audiences='test')

        with self.assertRaises(tokens.TokenError):
            tokens.Decoder(public_key='test', allowed_audiences=[1, 2, 3])

        audiences = ['test1', 'test2', 'test3']
        tokens.Decoder(public_key='test', allowed_audiences=set(audiences))
        tokens.Decoder(public_key='test', allowed_audiences=list(audiences))
        tokens.Decoder(public_key='test', allowed_audiences=tuple(audiences))

    def test_decode_garbage_does_not_decode(self):
        decoder = tokens.Decoder(public_key=PUBLIC_KEY, allowed_audiences={'test_audience'})
        with self.assertRaises(tokens.TokenError):
            decoder.decode('garbage data')

    def test_decode_bad_audience(self):
        decoder = tokens.Decoder(public_key=PUBLIC_KEY, allowed_audiences={'test_audience'})
        with self.assertRaises(tokens.TokenError):
            decoder.decode(make_jwt(audience='different_audience'))

    def test_decode(self):
        decoder = tokens.Decoder(public_key=PUBLIC_KEY, allowed_audiences={'test_audience'})
        decoded_token = decoder.decode(make_jwt())
        self.assertEqual(decoded_token['aud'], 'test_audience')
        self.assertEqual(decoded_token['iss'], 'https://example.auth0.com/')
        self.assertEqual(decoded_token['sub'], 'abc123|test@example.com')

        now = since_epoch()
        self.assertGreaterEqual(now, decoded_token['iat'])
        self.assertGreater(decoded_token['exp'], now)

    def test_decode_header_bad_header(self):
        decoder = tokens.Decoder(public_key='test', allowed_audiences={'test'})
        decoder.decode = mock.MagicMock()

        with self.assertRaises(tokens.TokenError):
            decoder.decode_header(None)
        self.assertEqual(decoder.decode.call_count, 0)

        with self.assertRaises(tokens.TokenError):
            decoder.decode_header('test')
        self.assertEqual(decoder.decode.call_count, 0)

        with self.assertRaises(tokens.TokenError):
            decoder.decode_header('test test test')
        self.assertEqual(decoder.decode.call_count, 0)

        with self.assertRaises(tokens.TokenError):
            # doesn't start with Bearer
            decoder.decode_header('test test')
        self.assertEqual(decoder.decode.call_count, 0)

    def test_decode_header_extra_whitespace(self):
        decoder = tokens.Decoder(public_key='test', allowed_audiences={'test'})
        decoder.decode = mock.MagicMock()

        decoder.decode_header('   Bearer     test  ')
        args, kwargs = decoder.decode.call_args
        self.assertEqual(args[0], 'test')

    def test_decode_header_case_insensitive_bearer(self):
        decoder = tokens.Decoder(public_key='test', allowed_audiences={'test'})
        decoder.decode = mock.MagicMock()

        decoder.decode_header('bearer test')
        args, kwargs = decoder.decode.call_args
        self.assertEqual(args[0], 'test')
