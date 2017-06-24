__all__ = ['Node', 'hash_algo']
__version__ = (0, 0, 1)

from Crypto.Hash import SHA512


def get_hash(bit_string):
    assert isinstance(bit_string, bytes)
    return SHA512.new(bit_string).hexdigest()


class Node:
    def __init__(self, *data_or_children):
        self.children = data_or_children

    def hash(self):
        string = ''
        for child in self.children:
            if isinstance(child, Node):
                string += child.hash()
            else:
                string += get_hash(str(child).encode())
        return get_hash(string.encode())
