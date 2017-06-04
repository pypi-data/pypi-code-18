from pycompressor.priority_queue import MinPQ
from pycompressor.queue import Queue


class Node(object):
    left = None
    right = None
    key = None
    freq = 0

    def __init__(self, key=None, freq=None, left=None, right=None):
        if key is not None:
            self.key = key
        if freq is not None:
            self.freq = freq
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


def char_at(text, i):
    if len(text) - 1 < i:
        return -1
    return ord(text[i])


def write_char(char, bit_stream):
    for i in range(8):
        bit = char % 2
        bit_stream.enqueue(bit)
        char = char // 2


def read_char(bit_stream):
    a = [0] * 8
    for i in range(8):
        if bit_stream.is_empty():
            break
        a[i] = bit_stream.dequeue()

    char = 0
    for i in range(7, -1, -1):
        char = char * 2 + a[i]
    return char


class HuffmanCompressor(object):
    def compress_to_binary(self, text):
        trie = self.build_trie(text)
        bit_stream = Queue()
        code = {}
        self.build_code(trie, '', code)
        self.write_trie(trie, bit_stream)
        self.write_text(code, text, bit_stream)
        return bit_stream

    def decompress_from_binary(self, bit_stream):
        trie = self.read_trie(bit_stream)
        code = {}
        self.build_code(trie, '', code)
        rcode = {}
        for key in code.keys():
            rcode[code[key]] = key
        return self.read_text(rcode, bit_stream)

    def compress_to_string(self, text):
        bit_stream = self.compress_to_binary(text)
        result = ''
        while not bit_stream.is_empty():
            result = result + chr(read_char(bit_stream))
        return result

    def decompress_from_string(self, text):
        bit_stream = Queue()
        for i in range(len(text)):
            write_char(char_at(text, i), bit_stream)
        return self.decompress_from_binary(bit_stream)

    def read_text(self, code, bit_stream):
        text = ''
        cc = ''
        while not bit_stream.is_empty():
            bit = bit_stream.dequeue()
            if bit == 0:
                cc = cc + '0'
            else:
                cc = cc + '1'
            if cc in code:
                text = text + chr(code[cc])
                cc = ''
        return text

    def read_trie(self, bit_stream):
        bit = bit_stream.dequeue()
        if bit == 1:
            return Node(key=read_char(bit_stream))
        left = self.read_trie(bit_stream)
        right = self.read_trie(bit_stream)
        return Node(left=left, right=right)

    def write_text(self, code, text, bit_stream):
        for i in range(len(text)):
            cc = code[char_at(text, i)]
            for j in range(len(cc)):
                if cc[j] == '0':
                    bit_stream.enqueue(0)
                elif cc[j] == '1':
                    bit_stream.enqueue(1)

    def build_code(self, x, prefix, code):
        if x.is_leaf():
            code[x.key] = prefix
            return
        self.build_code(x.left, prefix + '0', code)
        self.build_code(x.right, prefix + '1', code)

    def build_trie(self, text):
        search_trie = dict()
        for i in range(len(text)):
            c = char_at(text, i)
            if c in search_trie:
                search_trie[c].freq += 1
            else:
                node = Node(key=c, freq=1)
                search_trie[c] = node

        pq = MinPQ(lambda x, y: x.freq - y.freq)
        for node in search_trie.values():
            pq.enqueue(node)

        while pq.size() > 1:
            node1 = pq.del_min()
            node2 = pq.del_min()
            freq = node1.freq + node2.freq
            node = Node(freq=freq, left=node1, right=node2)
            pq.enqueue(node)

        return pq.del_min()

    def write_trie(self, x, bit_stream):
        if x is None:
            return
        if x.is_leaf():
            bit_stream.enqueue(1)
            write_char(x.key, bit_stream)
            return

        bit_stream.enqueue(0)
        self.write_trie(x.left, bit_stream)
        self.write_trie(x.right, bit_stream)
