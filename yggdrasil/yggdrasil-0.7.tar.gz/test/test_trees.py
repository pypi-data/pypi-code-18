#!/usr/bin/env python

import random
import unittest

from yggdrasil import *

class BinaryTreeTest(unittest.TestCase):
    def test_add(self):
        tree_obj = BinaryTree()
        unshuffled = [i for i in xrange(20)]
        shuffled = unshuffled[:]
        random.shuffle(shuffled)

        for item in shuffled:
            tree_obj.add_node(item)

        self.assertEqual(map(lambda x: x.label, tree_obj), unshuffled)

    def test_find(self):
        tree_obj = BinaryTree()
        items = [9, 0, 2, 1]

        for item in items:
            tree_obj.add_node(item)

        node = tree_obj.find_node(9)
        self.assertNotEqual(node, None)
        self.assertEqual(node.label, 9)

        node = tree_obj.find_node(10)
        self.assertEqual(node, None)

    def test_delete(self):
        tree_obj = BinaryTree()
        items = map(ord, 'DAHCBGEF')

        for item in items:
            tree_obj.add_node(item)

        tree_obj.remove_node(ord('B'))
        self.assertEqual(map(lambda x: x.label, tree_obj)
                         ,map(ord, 'ACDEFGH'))

        tree_obj.remove_node(ord('A'))
        self.assertEqual(ord('C'), tree_obj.root.left.label)
        self.assertEqual(map(lambda x: x.label, tree_obj)
                         ,map(ord, 'CDEFGH'))

        tree_obj.remove_node(ord('D'))
        self.assertEqual(ord('E'), tree_obj.root.label)
        self.assertEqual(ord('H'), tree_obj.root.right.label)
        self.assertEqual(map(lambda x: x.label, tree_obj)
                         ,map(ord, 'CEFGH'))

class AVLTreeTest(unittest.TestCase):
    def test_avl(self):
        forward_tree = AVLTree()
        forward_values = [
            [0],
            [0, 1],
            [1, 0, 2],
            [1, 0, 2, 3],
            [1, 0, 3, 2, 4],
            [3, 1, 0, 2, 4, 5],
            [3, 1, 0, 2, 5, 4, 6],
            [3, 1, 0, 2, 5, 4, 6, 7],
            [3, 1, 0, 2, 5, 4, 7, 6, 8],
            [3, 1, 0, 2, 7, 5, 4, 6, 8, 9]]

        for i in xrange(10):
            forward_tree.add_node(i)

            self.assertEqual(forward_values[i], map(lambda x: x.label, forward_tree.pre_order_traversal()))

        forward_tree.remove_node(4)
        self.assertEqual([3, 1, 0, 2, 7, 5, 6, 8, 9], map(lambda x: x.label, forward_tree.pre_order_traversal()))

        forward_tree.remove_node(5)
        self.assertEqual([3, 1, 0, 2, 7, 6, 8, 9], map(lambda x: x.label, forward_tree.pre_order_traversal()))

        forward_tree.remove_node(3)
        self.assertEqual([6, 1, 0, 2, 8, 7, 9], map(lambda x: x.label, forward_tree.pre_order_traversal()))
        
        reverse_tree = AVLTree()
        reverse_values = [
            [9],
            [9, 8],
            [8, 7, 9],
            [8, 7, 6, 9],
            [8, 6, 5, 7, 9],
            [6, 5, 4, 8, 7, 9],
            [6, 4, 3, 5, 8, 7, 9],
            [6, 4, 3, 2, 5, 8, 7, 9],
            [6, 4, 2, 1, 3, 5, 8, 7, 9],
            [6, 2, 1, 0, 4, 3, 5, 8, 7, 9]]

        for i in reversed(list(xrange(10))):
            reverse_tree.add_node(i)

            self.assertEqual(reverse_values[9-i], map(lambda x: x.label, reverse_tree.pre_order_traversal()))
