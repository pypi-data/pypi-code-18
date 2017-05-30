from .decoder import Decoder
from .exceptions import TokenError  # noqa


def init(public_key=None, allowed_audiences=None):
    decoder = Decoder(
        public_key=public_key,
        allowed_audiences=allowed_audiences,
    )

    global decode, decode_header
    decode = decoder.decode
    decode_header = decoder.decode_header
