import pytest

from pathmap.tree import Tree


class TestTree(object):
    @classmethod 
    def setup_class(cls):
        cls.tree  = Tree()

    def setup_method(self, method):
        self.tree.instance = {}
