def exchange(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


class MinPQ(object):
    s = None
    N = 0
    compare = None

    def __init__(self, compare=None):
        self.s = [0] * 10
        self.N = 0
        if compare is None:
            compare = lambda x, y: x - y
        self.compare = compare

    def less(self, a1, a2):
        return self.compare(a1, a2) < 0

    def enqueue(self, item):
        if self.N + 1 >= len(self.s):
            self.resize(len(self.s) * 2)

        self.N += 1
        self.s[self.N] = item
        self.swim(self.N)

    def resize(self, new_length):
        temp = [0] * new_length
        length = min(new_length, len(self.s))
        for i in range(length):
            temp[i] = self.s[i]
        self.s = temp

    def swim(self, k):
        while k > 1:
            parent = k // 2
            if self.less(self.s[k], self.s[parent]):
                exchange(self.s, k, parent)
                k = parent
            else:
                break

    def del_min(self):
        if self.N == 0:
            return None
        item = self.s[1]
        exchange(self.s, 1, self.N)
        self.N -= 1
        self.sink(1)
        return item

    def sink(self, k):
        while 2 * k <= self.N:
            child = k * 2
            if child < self.N and self.less(self.s[child + 1], self.s[child]):
                child += 1
            if self.less(self.s[child], self.s[k]):
                exchange(self.s, k, child)
                k = child
            else:
                break

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0
