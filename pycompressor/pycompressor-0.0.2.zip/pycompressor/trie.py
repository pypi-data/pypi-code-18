

class TsNode(object):
    key = None
    value = None
    left = None
    mid = None
    right = None

    def __init__(self, key, value=None, left=None, right=None, mid=None):
        self.key = key
        if value is not None:
            self.value = value
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right
        if mid is not None:
            self.mid = mid


def char_at(text, i):
    if len(text) - 1 < i:
        return -1
    return ord(text[i])


class TernarySearchTrie(object):
    root = None
    N = 0

    def put(self, key, value):
        self.root = self._put(self.root, key, value, 0)

    def _put(self, x, key, value, d):
        c = char_at(key, d)
        if x is None:
            x = TsNode(key=c)
        compared = c - x.key
        if compared < 0:
            x.left = self._put(x.left, key, value, d)
        elif compared > 0:
            x.right = self._put(x.right, key, value, d)
        else:
            if len(key)-1 == d:
                if x.value is None:
                    self.N += 1
                x.value = value
            else:
                x.mid = self._put(x.mid, key, value, d + 1)
        return x

    def get(self, key):
        x = self._get(self.root, key, 0)
        if x is not None:
            return x.value
        return None

    def _get(self, x, key, d):
        c = char_at(key, d)
        if x is None:
            return None

        compared = c - x.key
        if compared < 0:
            return self._get(x.left, key, d)
        elif compared > 0:
            return self._get(x.right, key, d)
        else:
            if len(key) - 1 == d:
                return x
            else:
                return self._get(x.mid, key, d + 1)

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0

    def contains_key(self, key):
        x = self._get(self.root, key, 0)
        if x is None:
            return False
        return x.value is not None

    def delete(self, key):
        x = self._get(self.root, key, 0)
        if x is not None:
            self.N -= 1
            x.value = None

    def values(self):
        queue = []
        self._collect_values(self.root, "", queue)
        return queue

    def keys(self):
        queue = []
        self._collect(self.root, "", queue)
        return queue

    def _collect(self, x, prefix, queue):
        if x is None:
            return
        if x.value is not None:
            queue.append(prefix + chr(x.key))

        self._collect(x.left, prefix, queue)
        self._collect(x.mid, prefix + chr(x.key), queue)
        self._collect(x.right, prefix, queue)

    def _collect_values(self, x, prefix, queue):
        if x is None:
            return
        if x.value is not None:
            queue.append(x.value)

        self._collect(x.left, prefix, queue)
        self._collect(x.mid, prefix + chr(x.key), queue)
        self._collect(x.right, prefix, queue)