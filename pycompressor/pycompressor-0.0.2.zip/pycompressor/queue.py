class QueueNode(object):
    value = None
    next_node = None

    def __init__(self, value, next_node=None):
        self.value = value
        if next_node is not None:
            self.next_node = next_node


class Queue(object):

    root = None
    first = None
    last = None
    N = 0

    def enqueue(self, item):
        old_last = self.last
        self.last = QueueNode(value=item)
        if old_last is not None:
            old_last.next_node = self.last
        if self.first is None:
            self.first = self.last
        self.N += 1

    def dequeue(self):
        old_first = self.first
        if old_first is None:
            return None

        self.N -= 1

        item = old_first.value
        self.first = old_first.next_node
        if self.first is None:
            self.last = None
        return item

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0
