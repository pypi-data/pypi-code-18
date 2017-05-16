# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from future.utils import python_2_unicode_compatible

import base64
from six import string_types, binary_type
from Crypto.Cipher import AES

from django.conf import settings


_cipher = None


@python_2_unicode_compatible
class AESCipher(object):
    '''
    from http://qiita.com/teitei_tk/items/0b8bae99a8700452b718
    $ python -c "import string, random; print(''.join(
       [random.choice(string.ascii_letters + string.digits) for i in range(50)]))"
    '''
    def __init__(self, key, block_size=32):
        self.bs = block_size
        key = key.encode('UTF-8', errors='escape')
        if len(key) >= block_size:
            self.key = key[:block_size]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        encoded = b'0'
        if isinstance(raw, string_types):
            raw = raw.encode('UTF-8', errors='escape')
            encoded = b'1'
        if not isinstance(raw, binary_type):
            raw = repr(raw).encode('UTF-8', errors='escape')
            encoded = b'2'
        raw = self._pad(raw)
        iv = (b'x' * (AES.block_size - 1)) + encoded
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
        except (UnicodeEncodeError, ValueError):
            raise TypeError()
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        raw = self._unpad(cipher.decrypt(enc[AES.block_size:]))
        try:
            key = iv.decode('UTF-8')[-1]
        except UnicodeDecodeError:
            raise TypeError()
        if key == '1':
            raw = raw.decode('UTF-8', errors='escape')
        elif key == '2':
            raw = eval(raw)
        return raw

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode('UTF-8')

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


def __get_cipher():

    global _cipher
    if _cipher is None:
        _cipher = AESCipher(settings.CRYPTO_KEY)
    return _cipher


def aes_encrypt(value):
    return __get_cipher().encrypt(value)


def aes_decrypt(value):
    return __get_cipher().decrypt(value)
