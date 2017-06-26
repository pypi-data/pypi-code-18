"Models supporting tools"
import hashlib
import random


def random_salt(size=128):
    byte_order = 'big'
    integer = random.getrandbits(size)
    returns = integer.to_bytes(length=size // 8, byteorder=byte_order)
    return returns


def make_hash(salt, text):
    hasher = hashlib.sha256()
    hasher.update(salt)
    hasher.update(text.encode('ASCII'))
    return hasher.hexdigest()
