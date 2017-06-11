__author__ = 'User'

class InvalidArgumentError(Exception):
    def __str__(self):
        return "Invalid argument passed to SGAQueue constructor: argument " + \
               "init_vals must be a list with at least one element"

class Node:
    __slots__ = ["idx", "next"]
    def __init__(self, idx, next=None):
        self.idx = idx
        self.next = next

class SGAQueue:
    def __init__(self, init_vals):
        if (not isinstance(init_vals, list)) or len(init_vals) == 0:
            raise InvalidArgumentError
        self.back = self.root = Node(init_vals[0])
        for val in init_vals[1:]:
            self.append_val(val)

    def append_node(self, node):
        self.back.next = node
        self.back = node

    def append_val(self, idx):
        new_node = Node(idx)
        self.append_node(new_node)

    def remove_front(self):
        self.root = self.root.next

    def is_empty(self):
        if self.root is None:
            return True
        else:
            return False

    def print(self):
        print_str = ""
        curr_node = self.root
        print_str += str(curr_node.idx)
        while curr_node is not self.back:
            curr_node = curr_node.next
            print_str += " -> " + str(curr_node.idx)
        print(print_str)

    def values(self):
        curr_node = self.root
        yield curr_node.idx
        while curr_node is not self.back:
            curr_node = curr_node.next
            yield curr_node.idx

    def make_list(self):
        return [idx for idx in self.values()]

if __name__ == "__main__":
    queue = SGAQueue([4, 5, 6, 3, 2, 1])
    queue.print()
    queue.append_val(10)
    queue.append_val(12)
    queue.print()
    queue.remove_front()
    queue.print()
    queue.append_val(100)
    while not queue.is_empty():
        queue.print()
        queue.remove_front()


