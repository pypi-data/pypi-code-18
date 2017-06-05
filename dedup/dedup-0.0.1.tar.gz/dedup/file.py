import os
import hashlib

SMALL_HASH_SIZE = 4000


def get_full_hash(path):
    hasher = hashlib.sha512()
    with open(path, 'rb') as file:
        hasher.update(file.read())
    return hasher.hexdigest()


def get_mini_hash(size, path):
    if size > SMALL_HASH_SIZE * 3:
        hasher = hashlib.sha512()
        with open(path, 'rb') as file:
            num_bytes_between_samples = (size - SMALL_HASH_SIZE * 3) / 2

            for offset_multiplier in range(3):
                start_of_sample = int(offset_multiplier * (SMALL_HASH_SIZE + num_bytes_between_samples))
                file.seek(start_of_sample)
                sample = file.read(SMALL_HASH_SIZE)
                hasher.update(sample)
        return hasher.hexdigest()
    else:
        return get_full_hash(path)


class File:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = os.path.realpath(path)
        self.size = os.path.getsize(self.path)
        self.__mini_hash = None
        self.__full_hash = None

    def __cmp__(self, other):
        if self.mini_hash == other.mini_hash:
            return self.full_hash == other.full_hash

    def __gt__(self, other):
        return self.size > other.size

    def __repr__(self):
        return self.name

    def ppsize(self):
        if self.size > 1e9:
            return "{} gb".format(round(self.size / 1e9, 2))
        elif self.size > 1000000:
            return "{} mb".format(round(self.size / 1000000, 2))
        elif self.size > 1000:
            return "{} kb".format(round(self.size / 1000, 2))
        else:
            return "{} bytes".format(round(self.size))

    def info(self):
        return {
            'name': self.name,
            'path': self.path,
            'size': self.ppsize(),
            'hash': self.full_hash
        }

    @property
    def full_hash(self):
        if self.__full_hash is None:
            self.__full_hash = get_full_hash(self.path)
        return self.__full_hash

    @property
    def mini_hash(self):
        if self.__mini_hash is None:
            self.__mini_hash = get_mini_hash(self.size, self.path)
        return self.__mini_hash
