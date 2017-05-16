#!/usr/bin/env python

import inspect

__all__ = ['Node', 'Tree', 'BinaryNode', 'BinaryTree', 'AVLNode', 'AVLTree']

class Node(object):
    BRANCH_FUNCTION = None
    LABEL_CLASS = None
    VALUE_CLASS = None

    def __init__(self, **kwargs):
        self.branch_function = kwargs.setdefault('branch_function', self.BRANCH_FUNCTION)

        if self.branch_function is None:
            raise ValueError('branch function cannot be None')
        
        if not callable(self.branch_function):
            raise ValueError('branch function must be a callable object')
        
        self.label_class = kwargs.setdefault('label_class', self.LABEL_CLASS)

        if self.label_class is None:
            raise ValueError('label_class cannot be None')

        if not inspect.isclass(self.label_class):
            raise ValueError('label_class must be a class object')

        self.value_class = kwargs.setdefault('value_class', self.VALUE_CLASS)

        if not self.value_class is None and not inspect.isclass(self.value_class):
            raise ValueError('value_class must be a class object')

        self.set_left_child(kwargs.setdefault('left', None))
        self.set_right_child(kwargs.setdefault('right', None))
        self.set_parent(kwargs.setdefault('parent', None))

        label = kwargs.setdefault('label', None)

        self.set_label(label)
        
        value = kwargs.setdefault('value', None)

        self.set_value(value)

    def set_left_child(self, node):
        if not node is None and not isinstance(node, self.__class__):
            raise ValueError('left child must be the same class as this node')

        self.left = node

        if not node is None:
            node.parent = self

    def set_right_child(self, node):
        if not node is None and not isinstance(node, self.__class__):
            raise ValueError('right child must be the same class as this node')

        self.right = node

        if not node is None:
            node.parent = self

    def set_parent(self, node):
        if not node is None and not isinstance(node, self.__class__):
            raise ValueError('parent must be the same class as this node')

        self.parent = node

        if not node is None:
            branch = self.branch_function(self.label, node.label)

            if not isinstance(branch, int):
                raise ValueError('branch function returned invalid value')

            if branch < 0:
                node.left = self
            elif branch > 0:
                node.right = self

    def set_label(self, label):
        if label is None:
            raise ValueError('label cannot be None')

        if not isinstance(label, self.label_class):
            raise ValueError('label must be an instance of the label class')

        self.label = label

    def set_value(self, value):
        if not value is None and self.value_class is None:
            raise RuntimeError('value class cannot be None')
        
        if not value is None and isinstance(value, self.value_class):
            raise ValueError('value must be an instance of the value class')

        self.value = value

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self.label))

class Tree(object):
    NODE_CLASS = Node
    BRANCH_FUNCTION = None
    LABEL_CLASS = None
    VALUE_CLASS = None

    def __init__(self, **kwargs):
        self.node_class = kwargs.setdefault('node_class', self.NODE_CLASS)

        if self.node_class is None:
            raise ValueError('node_class cannot be None')

        if not issubclass(self.node_class, Node):
            raise ValueError('node_class must implement Node')
        
        self.branch_function = kwargs.setdefault('branch_function', self.BRANCH_FUNCTION)

        if self.branch_function is None:
            self.branch_function = self.node_class.BRANCH_FUNCTION
            
        if self.branch_function is None:
            raise ValueError('branch function cannot be None')
        
        if not callable(self.branch_function):
            raise ValueError('branch function must be a callable object')

        self.label_class = kwargs.setdefault('label_class', self.LABEL_CLASS)

        if self.label_class is None:
            self.label_class = self.node_class.LABEL_CLASS

        if self.label_class is None:
            raise ValueError('label_class cannot be None')

        if not inspect.isclass(self.label_class):
            raise ValueError('label_class must be a class object')

        self.value_class = kwargs.setdefault('value_class', self.VALUE_CLASS)

        if self.value_class is None:
            self.value_class = self.node_class.VALUE_CLASS

        if not self.value_class is None and not inspect.isclass(self.value_class):
            raise ValueError('value_class must be a class object')

        self.set_root(kwargs.setdefault('root_node', None))
        self.nodes = dict()

    def set_root(self, root):
        if not root is None and not isinstance(root, self.node_class):
            raise ValueError('root node must be an instance of the node class')
        
        self.root = root

    def is_empty(self):
        return self.root is None

    def new_node(self, label, value=None, parent=None, left=None, right=None):
        node = self.node_class(branch_function=self.branch_function
                               ,label_class=self.label_class
                               ,value_class=self.value_class
                               ,parent=parent
                               ,left=left
                               ,right=right
                               ,label=label
                               ,value=value)
        self.nodes[id(node)] = node

        return node

    def add_node(self, label, value=None):
        raise NotImplementedError

    def find_node(self, label):
        raise NotImplementedError

    def remove_node(self, label):
        raise NotImplementedError

    def in_order_traversal(self):
        if self.root is None:
            return

        visited = dict()
        node_stack = [self.root]
        nodes = len(node_stack)

        while nodes > 0:
            node = node_stack[-1]
            
            if not node.left is None and not node.left.label in visited:
                node_stack.append(node.left)
                nodes += 1
                continue

            yield node
            visited[node.label] = None
            node_stack.pop()
            nodes -= 1

            if not node.right is None and not node.right.label in visited:
                node_stack.append(node.right)
                nodes += 1
                continue

    def post_order_traversal(self):
        if self.root is None:
            return

        visited = dict()
        node_stack = [self.root]
        nodes = len(node_stack)

        while nodes > 0:
            node = node_stack[-1]
            
            if not node.left is None and not node.left.label in visited:
                node_stack.append(node.left)
                nodes += 1
                continue

            if not node.right is None and not node.right.label in visited:
                node_stack.append(node.right)
                nodes += 1
                continue

            yield node
            visited[node.label] = None
            node_stack.pop()
            nodes -= 1

    def pre_order_traversal(self):
        if self.root is None:
            return

        visited = dict()
        node_stack = [self.root]
        nodes = len(node_stack)

        while nodes > 0:
            node = node_stack[-1]

            if not node.label in visited:
                yield node
                visited[node.label] = None
            
            if not node.left is None and not node.left.label in visited:
                node_stack.append(node.left)
                nodes += 1
                continue

            if not node.right is None and not node.right.label in visited:
                node_stack.append(node.right)
                nodes += 1
                continue

            node_stack.pop()
            nodes -= 1

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, ', '.join(map(repr, self.in_order_traversal())))

    def __iter__(self):
        return self.in_order_traversal()

class BinaryNode(Node):
    BRANCH_FUNCTION = cmp
    LABEL_CLASS = int
    
    def search_path(self, label):
        node = self
        nodes = [self]
        branch = self.branch_function(label, node.label)

        if not isinstance(branch, int):
            raise ValueError('branch function returned invalid value')

        while not branch == 0:
            if branch < 0 and node.left is None:
                break
            elif branch < 0:
                node = node.left
            elif branch > 0 and node.right is None:
                break
            elif branch > 0:
                node = node.right

            nodes.append(node)
            branch = self.branch_function(label, node.label)

        return nodes

class BinaryTree(Tree):
    NODE_CLASS = BinaryNode

    def add_node(self, label, value=None):
        if self.root is None:
            self.root = self.new_node(label, value)
            return self.root

        path = self.root.search_path(label)
        parent = path[-1]
        branch = parent.branch_function(label, parent.label)

        if not isinstance(branch, int):
            raise ValueError('branch function returned invalid value')

        if branch == 0:
            raise RuntimeError('label already exists in tree')
        
        new_node = self.new_node(label, value)

        if branch < 0:
            parent.set_left_child(new_node)
        elif branch > 0:
            parent.set_right_child(new_node)

        return new_node

    def find_node(self, label):
        if self.is_empty():
            raise RuntimeError('tree is empty')
        
        path = self.root.search_path(label)
        parent = path[-1]

        if parent.label == label:
            return parent

    def has_node(self, node):
        if not isinstance(node, self.node_class):
            raise ValueError('node object must be the same object as the node class')
        
        return id(node) in self.nodes

    def remove_node(self, label):
        if self.is_empty():
            raise RuntimeError('tree is empty')

        path = self.root.search_path(label)
        parent = path[-1]

        if not parent.label == label:
            raise RuntimeError('node not found')

        node = parent

        if node.left is None and node.right is None:
            if not node.parent is None:
                if node.parent.left == node:
                    node.parent.left = None
                elif node.parent.right == node:
                    node.parent.right = None

            if node == self.root:
                self.root = None
        elif node.left is None or node.right is None:
            if node.left is None:
                replacement_node = node.right
            elif node.right is None:
                replacement_node = node.left

            if node == self.root:
                self.root = replacement_node
            elif node.parent.left == node:
                node.parent.left = replacement_node
                replacement_node.parent = node.parent
            elif node.parent.right == node:
                node.parent.right = replacement_node
                replacement_node.parent = node.parent
        elif not node.left is None and not node.right is None:
            leftmost = node.right

            while not leftmost.left is None:
                path.append(leftmost)
                leftmost = leftmost.left

            path.append(leftmost.right)
            leftmost.parent.left = leftmost.right
            leftmost.right = node.right
            leftmost.left = node.left
            leftmost.parent = node.parent

            if node == self.root:
                self.root = leftmost
            elif not node.parent is None:
                if node.parent.left == node:
                    node.parent.left = leftmost
                elif node.parent.right == node:
                    node.parent.right = leftmost

        node.left = None
        node.right = None
        node.parent = None

        del self.nodes[id(node)]

class AVLNode(BinaryNode):
    HEIGHT = 0
    
    def __init__(self, **kwargs):
        super(AVLNode, self).__init__(**kwargs)
        
        self.height = kwargs.setdefault('height', self.HEIGHT)

        if not isinstance(self.height, int):
            raise ValueError('height must be an int')

    def left_height(self):
        return 0 if self.left is None else self.left.height

    def right_height(self):
        return 0 if self.right is None else self.right.height

    def get_height(self):
        return max(self.left_height(), self.right_height()) + 1

    def balance(self):
        return self.right_height() - self.left_height()

    def __repr__(self):
        return '<%s: %d/%s>' % (self.__class__.__name__, self.balance(), str(self.label))
        
class AVLTree(BinaryTree):
    NODE_CLASS = AVLNode

    def rotate_left(self, rotation_root):
        if not self.has_node(rotation_root):
            raise RuntimeError('no such node in tree')

        pivot_root = rotation_root.right
        left_child = pivot_root.left
        rotation_parent = rotation_root.parent

        if rotation_parent is None:
            self.root = pivot_root
        elif rotation_parent.left == rotation_root:
            rotation_parent.left = pivot_root
        elif rotation_parent.right == rotation_root:
            rotation_parent.right = pivot_root

        pivot_root.parent = rotation_parent

        if not left_child is None:
            left_child.parent = rotation_root
            
        rotation_root.right = left_child
        pivot_root.left = rotation_root
        rotation_root.parent = pivot_root
        
    def rotate_right(self, rotation_root):
        if not self.has_node(rotation_root):
            raise RuntimeError('no such node in tree')

        pivot_root = rotation_root.left
        right_child = pivot_root.right
        rotation_parent = rotation_root.parent

        if rotation_parent is None:
            self.root = pivot_root
        elif rotation_parent.left == rotation_root:
            rotation_parent.left = pivot_root
        elif rotation_parent.right == rotation_root:
            rotation_parent.right = pivot_root

        pivot_root.parent = rotation_parent

        if not right_child is None:
            right_child.parent = rotation_root
            
        rotation_root.left = right_child
        pivot_root.right = rotation_root
        rotation_root.parent = pivot_root
        
    def update_height(self, node):
        if not self.has_node(node):
            raise RuntimeError('no such node in tree')

        while not node is None:
            balance = node.balance()

            if abs(balance) > 1:
                self.rebalance_node(node)

            node.height = node.get_height()
            node = node.parent

    def rebalance_node(self, node):
        if not self.has_node(node):
            raise RuntimeError('no such node in tree')

        if node.balance() > 0:
            if not node.right is None and node.right.balance() < 0:
                self.rotate_right(node.right)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif node.balance() < 0:
            if not node.left is None and node.left.balance() > 0:
                self.rotate_left(node.left)
                self.rotate_right(node)
            else:
                self.rotate_right(node)

    def add_node(self, label, value=None):
        new_node = super(AVLTree, self).add_node(label, value)

        self.update_height(new_node)

        return new_node

    def remove_node(self, label):
        if self.is_empty():
            raise RuntimeError('tree is empty')

        path = self.root.search_path(label)
        parent = path[-1]

        if not parent.label == label:
            raise RuntimeError('node not found')

        node = parent

        if node.left is None and node.right is None:
            if not node.parent is None:
                if node.parent.left == node:
                    node.parent.left = None
                elif node.parent.right == node:
                    node.parent.right = None

            if node == self.root:
                self.root = None
                
            self.update_height(node.parent)
        elif node.left is None or node.right is None:
            if node.left is None:
                replacement_node = node.right
            elif node.right is None:
                replacement_node = node.left

            if node == self.root:
                self.root = replacement_node
            elif node.parent.left == node:
                node.parent.left = replacement_node
                replacement_node.parent = node.parent
            elif node.parent.right == node:
                node.parent.right = replacement_node
                replacement_node.parent = node.parent

            self.update_height(node.parent)
        elif not node.left is None and not node.right is None:
            leftmost = node.right

            while not leftmost.left is None:
                leftmost = leftmost.left
            
            replaced_node = leftmost.right
            leftmost_parent = leftmost.parent
            leftmost.parent.left = replaced_node
        
            leftmost.right = node.right
            leftmost.left = node.left
            leftmost.parent = node.parent
            leftmost.height = node.height

            if not node.left is None:
                node.left.parent = leftmost

            if not node.right is None:
                node.right.parent = leftmost

            if node == self.root:
                self.root = leftmost
            elif not node.parent is None:
                if node.parent.left == node:
                    node.parent.left = leftmost
                elif node.parent.right == node:
                    node.parent.right = leftmost

            if not replaced_node is None:
                self.update_height(replaced_node)
            else:
                self.update_height(leftmost_parent)

        node.left = None
        node.right = None
        node.parent = None

        del self.nodes[id(node)]
