"""
The MIT License (MIT)
Copyright (c) 2017 orisano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from Crypto.Cipher import AES
from Crypto import Random

import base64
import hashlib
import hmac
import json
from typing import Optional


def pad(data: bytes, block_size: int) -> bytes:
    padding_len = block_size - len(data) % block_size
    return data + bytes([padding_len] * padding_len)


def unpad(data: bytes, block_size: int) -> bytes:
    padded_len = len(data)
    assert padded_len % block_size == 0

    padding_len = data[-1]
    assert 0 < padding_len < block_size
    assert data[-padding_len:] == bytes([padding_len] * padding_len)
    return data[:-padding_len]


class InvalidSignature(Exception):
    pass


class MessageVerifier(object):
    def __init__(self, secret: bytes):
        self.secret = secret

    def generate(self, value: bytes) -> bytes:
        data = self._encode(value)
        digest = self._generate_digest(data)
        return b"--".join([data, digest])

    def is_valid_message(self, signed_message: bytes) -> bool:
        data, digest = signed_message.split(b"--")
        return self._generate_digest(data) == digest

    def verified(self, signed_message: bytes) -> Optional[bytes]:
        if not self.is_valid_message(signed_message):
            return None
        data, _ = signed_message.split(b"--")
        return self._decode(data)

    def verify(self, signed_message: bytes) -> bytes:
        verified = self.verified(signed_message)
        if verified is None:
            raise InvalidSignature()
        return verified

    def _generate_digest(self, data: bytes) -> bytes:
        return hmac.new(self.secret, msg=data, digestmod="sha1").hexdigest().encode()

    @staticmethod
    def _encode(data: bytes) -> bytes:
        return base64.b64encode(data)

    @staticmethod
    def _decode(data: bytes) -> bytes:
        return base64.b64decode(data)


class MessageEncryptor(object):
    def __init__(self, secret: bytes, sign_secret: bytes):
        self.secret = secret
        self.sign_secret = sign_secret
        self.verifier = MessageVerifier(sign_secret)

    def encrypt_and_sign(self, value: bytes) -> bytes:
        return self.verifier.generate(self._encrypt(value))

    def decrypt_and_verify(self, value: bytes) -> bytes:
        return unpad(self._decrypt(self.verifier.verify(value)), 16)

    def _encrypt(self, value: bytes) -> bytes:
        cipher = self._new_cipher(self.secret)
        return b"--".join(map(base64.b64encode, [cipher.encrypt(pad(value, 16)), cipher.IV]))

    def _decrypt(self, encrypted_message: bytes) -> bytes:
        encrypted_data, iv = map(base64.b64decode, encrypted_message.split(b"--"))
        cipher = self._new_cipher(self.secret, iv=iv)
        return cipher.decrypt(encrypted_data)

    @staticmethod
    def _new_cipher(key: bytes, iv: Optional[bytes]=None) -> AES.AESCipher:
        if iv is None:
            iv = Random.new().read(16)
        return AES.new(key, mode=AES.MODE_CBC, IV=iv)


class RailsCookie(object):
    def __init__(self, secret_key_base: bytes):
        secret = self._generate_key(secret_key_base, b"encrypted cookie")[:32]
        sign_secret = self._generate_key(secret_key_base, b"signed encrypted cookie")
        self.encryptor = MessageEncryptor(secret, sign_secret)

    @staticmethod
    def _generate_key(secret: bytes, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha1", secret, salt, 1000, dklen=64)

    def loads(self, encoded_cookie: bytes) -> dict:
        return json.loads(self.encryptor.decrypt_and_verify(encoded_cookie).decode())

    def dumps(self, cookie: dict) -> bytes:
        return self.encryptor.encrypt_and_sign(json.dumps(cookie).encode())
