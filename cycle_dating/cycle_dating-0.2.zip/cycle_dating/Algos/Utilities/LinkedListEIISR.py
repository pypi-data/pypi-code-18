__author__ = 'User'

class Node:
    __slots__ = ["idx", "next_node", "prev_node"]

    def __init__(self, idx, prev_node, next_node):
        self.idx = idx
        self.next_node = next_node
        self.prev_node = prev_node

class LinkedListEIISR:

    def __init__(self):
        self.root = None
        self.back = self.root
        self.size = 0

    def add_idx_range(self, first_idx, last_idx):
        curr_idx = first_idx
        while curr_idx != last_idx:
            self.add_node(Node(curr_idx, None, None))
            curr_idx += 1

    def add_node(self, node):
        if self.root is None:
            self.root = node
            self.root.prev_node = None
            self.root.next_node = None
            self.back = self.root
        else:
            self.back.next_node = node
            self.back.next_node.prev_node = self.back
            self.back = self.back.next_node
            self.back.next_node = None
        self.size += 1

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def make_pylist(self):
        return [node.idx for node in self]

    def add_node_content_idx(self, idx):
        self.add_node(Node(idx, None, None))

    def remove_node(self, ref):
        if ref is self.back:
            if self.back is self.root:
                self.back = None
                self.root = None
            else:
                self.back = self.back.prev_node
                self.back.next_node = None
        elif ref is self.root:
            self.root = ref.next_node
            self.root.prev_node = None
        else:
            ref.prev_node.next_node = ref.next_node
            ref.next_node.prev_node = ref.prev_node
        del ref
        self.size -= 1

    def remove_node_idx(self, idx):
        if self.root is None:
            print ("Warning: index out of bounds for linked list remove operator. No removals made")
            return
        valid_break = False
        curr_node = self.root
        curr_node_idx = 0
        while curr_node.next_node is not None:
            curr_node = curr_node.next_node
            curr_node_idx += 1
            if curr_node_idx == idx:
                valid_break = True
                break
        if not valid_break:
            print ("Warning: index out of bounds for linked list remove operator. No removals made")
            return
        self.remove_node(curr_node)

    def __iter__(self):
        curr_node = self.root
        while curr_node is not None:
            yield curr_node
            curr_node = curr_node.next_node


