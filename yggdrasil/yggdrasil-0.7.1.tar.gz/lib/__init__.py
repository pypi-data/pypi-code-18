#!/usr/bin/env python

import inspect

__all__ = ['Node', 'Tree', 'BinaryNode', 'BinaryTree', 'AVLNode', 'AVLTree']

class Node(object):
    BRANCH_FUNCTION = None

    def __init__(self, **kwargs):
        self.branch_function = kwargs.setdefault('branch_function', self.BRANCH_FUNCTION)

        if self.branch_function is None:
            raise ValueError('branch function cannot be None')
        
        if not callable(self.branch_function):
            raise ValueError('branch function must be a callable object')

        self.tree = kwargs.get('tree', None)

        if self.tree is None:
            raise ValueError('tree cannot be None')

        if not isinstance(self.tree, Tree):
            raise ValueError('tree must be a Tree object')
        
        self.left = kwargs.get('left')

        if not self.left is None:
            self.left.parent = self

        self.right = kwargs.get('right')

        if not self.right is None:
            self.right.parent = self

        self.parent = kwargs.get('parent')
        self.label = kwargs.get('label')

        if self.label is None:
            raise ValueError('label cannot be None')
        
        self.value = kwargs.get('value')

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

        old_label = self.label
        self.label = label
        del self.tree.labels[old_label]
        self.tree.labels[label] = self

    def set_value(self, value):
        self.value = value

    def is_leaf(self):
        return self.left is None and self.right is None

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self.label))

class Tree(object):
    NODE_CLASS = Node
    BRANCH_FUNCTION = None

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

        self.root = kwargs.setdefault('root', None)
        self.nodes = dict()
        self.labels = dict()

    def set_root(self, root):
        if not root is None and not isinstance(root, self.node_class):
            raise ValueError('root node must be an instance of the node class')
        
        self.root = root

    def is_empty(self):
        return self.root is None

    def new_node(self, label, value=None, parent=None, left=None, right=None):
        node = self.node_class(branch_function=self.branch_function
                               ,tree=self
                               ,parent=parent
                               ,left=left
                               ,right=right
                               ,label=label
                               ,value=value)
        self.nodes[id(node)] = node
        self.labels[label] = node

        return node

    def add_node(self, label, value=None):
        raise NotImplementedError

    def find_node(self, label):
        raise NotImplementedError

    def remove_node(self, label):
        raise NotImplementedError

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, ', '.join(map(repr, self.in_order_traversal())))

    def __len__(self):
        return len(self.nodes)

    def __iter__(self):
        return self.in_order_traversal()

class BinaryNode(Node):
    BRANCH_FUNCTION = cmp
    
    def search_path(self, label):
        node = self
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

            branch = self.branch_function(label, node.label)

        return node

class BinaryTree(Tree):
    NODE_CLASS = BinaryNode

    def add_node(self, label, value=None):
        if self.root is None:
            self.root = self.new_node(label, value)
            return self.root

        if self.has_label(label):
            raise RuntimeError('label already exists in tree')

        parent = self.root.search_path(label)
        branch = parent.branch_function(label, parent.label)

        if not isinstance(branch, int):
            raise ValueError('branch function returned invalid value')
        
        new_node = self.new_node(label, value)

        if branch < 0:
            parent.left = new_node
        elif branch > 0:
            parent.right = new_node

        new_node.parent = parent
        
        return new_node

    def find_node(self, label):
        if self.is_empty():
            raise RuntimeError('tree is empty')
        
        return self.labels.get(label)

    def has_label(self, label):
        return label in self.labels
        
    def has_node(self, node):
        return id(node) in self.nodes

    def remove_node(self, label):
        if self.is_empty():
            raise RuntimeError('tree is empty')

        if not self.has_label(label):
            raise RuntimeError('node not found')

        node = self.labels[label]

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
                leftmost = leftmost.left

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
        del self.labels[node.label]

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

class AVLNode(BinaryNode):
    HEIGHT = 0
    
    def __init__(self, **kwargs):
        super(AVLNode, self).__init__(**kwargs)
        
        self.height = kwargs.setdefault('height', self.HEIGHT)

        if not isinstance(self.height, int):
            raise ValueError('height must be an int')

    def __repr__(self):
        return '<%s: %d/%s>' % (self.__class__.__name__, self.height, str(self.label))
        
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

        # only the pivot and the rotation node need to have their heights recalculated
        if rotation_root.left is None:
            left_height = 0
        else:
            left_height = rotation_root.left.height

        if rotation_root.right is None:
            right_height = 0
        else:
            right_height = rotation_root.right.height

        rotation_root.height = max(left_height, right_height)+1

        if pivot_root.left is None:
            left_height = 0
        else:
            left_height = pivot_root.left.height

        if pivot_root.right is None:
            right_height = 0
        else:
            right_height = pivot_root.right.height

        pivot_root.height = max(left_height, right_height)+1
        
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

        # only the pivot and the rotation node need to have their heights recalculated
        if rotation_root.left is None:
            left_height = 0
        else:
            left_height = rotation_root.left.height

        if rotation_root.right is None:
            right_height = 0
        else:
            right_height = rotation_root.right.height

        rotation_root.height = max(left_height, right_height)+1

        if pivot_root.left is None:
            left_height = 0
        else:
            left_height = pivot_root.left.height

        if pivot_root.right is None:
            right_height = 0
        else:
            right_height = pivot_root.right.height

        pivot_root.height = max(left_height, right_height)+1
        
    def update_height(self, node):
        if node is None:
            return
        
        if not self.has_node(node):
            raise RuntimeError('no such node in tree')

        while not node is None:
            if node.left is None:
                left_height = 0
            else:
                left_height = node.left.height

            if node.right is None:
                right_height = 0
            else:
                right_height = node.right.height

            old_height = node.height
            node.height = max(left_height,right_height)+1
            balance = right_height - left_height

            if balance > 1 or balance < -1:
                self.rebalance_node(node)
                break

            if old_height == node.height:
                break
            
            node = node.parent

    def rebalance_node(self, node):
        if not self.has_node(node):
            raise RuntimeError('no such node in tree')

        if node.left is None:
            left_height = 0
        else:
            left_height = node.left.height

        if node.right is None:
            right_height = 0
        else:
            right_height = node.right.height

        parent_balance = right_height - left_height

        if parent_balance > 0:
            child_node = node.right

            if not child_node is None:
                if child_node.left is None:
                    left_height = 0
                else:
                    left_height = child_node.left.height

                if child_node.right is None:
                    right_height = 0
                else:
                    right_height = child_node.right.height

                child_balance = right_height - left_height
            else:
                child_balance = 0
                
            if child_balance < 0:
                self.rotate_right(child_node)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif parent_balance < 0:
            child_node = node.left

            if not child_node is None:
                if child_node.left is None:
                    left_height = 0
                else:
                    left_height = child_node.left.height
                     
                if child_node.right is None:
                    right_height = 0
                else:
                    right_height = child_node.right.height

                child_balance = right_height - left_height
            else:
                child_balance = 0

            if child_balance > 0:
                self.rotate_left(child_node)
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

        if not self.has_label(label):
            raise RuntimeError('node not found')

        node = self.labels[label]

        if node.left is None and node.right is None:
            if not node.parent is None:
                if node.parent.left == node:
                    node.parent.left = None
                elif node.parent.right == node:
                    node.parent.right = None

            if node == self.root:
                self.root = None

            parent = node.parent
            node.parent = None
                
            self.update_height(parent)
        elif node.left is None or node.right is None:
            if node.left is None:
                replacement_node = node.right
            elif node.right is None:
                replacement_node = node.left

            replacement_node.parent = node.parent
            
            if node == self.root:
                self.root = replacement_node
            elif node.parent.left == node:
                node.parent.left = replacement_node
            elif node.parent.right == node:
                node.parent.right = replacement_node

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
        del self.labels[node.label]
