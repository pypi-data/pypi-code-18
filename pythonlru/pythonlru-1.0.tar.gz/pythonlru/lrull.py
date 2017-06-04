# LRU cache working:
# Least Recently Used Cache, we keep adding elements to the cache
# and when the cache is full we remove the least used node is removed
# and the new value is added to the top

# Used Doubly Liked List for managing most recently used element.
# if the list is full the last element is removed from the end
# and the new node is appended to the top, the DLL has a good
# performance of removing and adding node to the end and front

# we have also used the a dict for getting O(1) access of cache
# elements

# If we accessed the element from the cache then that element
# is the recently accessed element so we need to move that
# element to the front as most accessed element

# Mutable Dict is a interface is used for inheritance
# to add common methods of a dict object
from collections import MutableMapping


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.previous = None
        self.next = None


class LRUCache(MutableMapping):
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.rear = None
        self.size = 0

    def __len__(self):
        return self.size

    def set(self, key, value):
        if key in self.cache:
            old_node = self.cache.get(key)
            old_node.value = value
            self.remove_node(old_node)
            self.push_front(old_node)
        else:
            new_node = Node(key, value)
            if len(self.cache) >= self.capacity:
                self.cache.pop(self.rear.key)
                self.remove_node(self.rear)
                self.push_front(new_node)
            else:
                self.push_front(new_node)

            self.cache[key] = new_node
            self.size += 1

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key, default=None):
        if key in self.cache:
            temp_node = self.cache.get(key)
            self.remove_node(temp_node)
            self.push_front(temp_node)
            return temp_node.value
        elif default is not None:
            return default
        return -1

    def __getitem__(self, key):
        self.get(key, default=None)

    def push_front(self, node):
        if isinstance(node, Node):
            node.next = self.head
            node.previous = None

            if self.head is not None:
                self.head.previous = node

            self.head = node

            if self.rear is None:
                self.rear = self.head

    def remove_node(self, node):
        # if the removal node in head
        if node.previous is None:
            self.head = node.next
            node.next.previous = None
            node.next = None

        # if the removal node in rear
        elif node.next is None:
            self.rear = node.previous
            node.previous.next = None
            node.previous = None

        else:
            node.previous.next = node.next
            node.next.previous = node.previous
        self.size -= 1

    def __iter__(self):
        pass

    def __delitem__(self, key):
        pass