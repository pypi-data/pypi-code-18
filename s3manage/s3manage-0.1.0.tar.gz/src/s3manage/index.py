from __future__ import print_function

import posixpath as webpath

from munch import munchify


class Index(object):
    """
    Models and can optionally create a set of static HTML files that link to
    the given S3 bucket's files in the vein of Apache's +Indexes option.
    """
    def __init__(self, bucket):
        self._bucket = bucket

    def construct(self):
        files = self._bucket.get_items()
        # Find the root
        self._root = RootNode()
        # Construct the tree, in memory
        for f in files:
            node = node_factory(f)
            self._root.add_child(node)

    def write_indexes(self):
        self._root.write_index_file(self._bucket, self._bucket.get_index_name())


def node_factory(item):
    if item.key == '':
        return RootNode()
    elif item.key.endswith('/'):
        return DirNode(item)
    else:
        return Node(item)


class Node(object):
    """
    A base node, anywhere in the tree. Behanves mostly as a single, stand-alone
    item and doesn't take too much stock in its cihldren, although it can have
    some. It's more or less like a deadbeat parent who just has kids and then
    ignores them unless it's very convenient to itself.

    Use as the base class for other types of nodes.
    """
    def __init__(self, item):
        self._item = item
        self._children = {}
        self.virtual = False
        self.is_dir = self._item.key.endswith('/')
        self.parts = self._item.key.split('/')

    def add_child(self, node, depth=0):
        """
        Adds a child node into the hierarchy. The child node should already be
        instantiated as part of itself.

        :param node: The node that is going to be inserted into this hierarchy
        :param depth: The depth down the tree that this node should descend.
        Strictly speaking, this parameter might be removed in the future, so do
        not depend on it from outside of this class itself
        """
        part = node.get_part(depth)
        # If new node is at its max depth, end recursion.
        if depth == len(node.parts) - 1:
            if part in self._children:
                self._children[part].set_node(node)
            else:
                self._children[part] = node
            return
        # Create a virtual node, if we don't have an existing node for it
        if part not in self._children:
            s = '/'.join(node.parts[:depth+1]) + '/'
            self._children[part] = VirtualNode(s)
        # Add this incoming child to the trie
        self._children[part].add_child(node, depth+1)

    def get_part(self, part):
        """
        Get a path segment at the specified depth in this node's tree structure

        :param part: Index depth down the path structure to fetch back. 0-index
        :returns: The path segment at the specified depth, None if the request
        is out of bounds
        """
        if part > len(self.parts):
            return None
        else:
            return self.parts[part]

    def set_node(self, other):
        """
        Replace myself with the other node that has been discovered. The main
        purpose for this method is to transform a formerly virtual node into a
        concrete node. Initializes all the variables appropriately.

        :param other: The concrete node with which to replace our own values
        """
        if not self.virtual:
            raise NodeError('wtf: You have the same thing twice?')
        self._item = other._item
        self.parts = other.parts
        self.is_dir = other.is_dir
        self.virtual = False

    def print_tree(self, indent=0):
        if indent > 0:
            print("|   " * indent, end='')
        print("|---", self._item.key)

    def get_index_file_links(self, links):
        pass

    def get_index_file(self):
        return None

    def write_index_file(self, destination, name):
        pass


class DirNode(Node):
    """
    A node that is speficially analgous to a filesystem directory or folder.
    Unlike a generic node, this one pays much closer attention to its children
    and works with them as often as they can appear.
    """
    def __init__(self, item):
        super(DirNode, self).__init__(item)
        self.is_dir = True
        self.parts = self.parts[:-1]

    def get_index_file(self):
        links = ['<a href="..">&lt;Parent&gt;</a>']
        self.get_index_file_links(links)
        return self.add_links_to_body(links)

    def add_links_to_body(self, links):
        # Construct the full file
        link_strs = '<br />\n        '.join(links)
        body = '    <body>\n        {0}\n    </body>'.format(link_strs)
        f = '<!DOCTYPE html>\n<html>\n{0}\n</html>'.format(body)
        return f

    def get_index_file_links(self, links):
        # Create each link for child elements
        for child in sorted(self._children.keys()):
            links.append('<a href="{0}">{0}</a>'.format(child))

    def print_tree(self, indent=0):
        super(DirNode, self).print_tree(indent)
        for child in sorted(self._children.keys()):
            self._children[child].print_tree(indent+1)

    def write_index_file(self, destination, name):
        mine = self.get_index_file()
        key = webpath.join(self._item.key, name)
        destination.put_object(ContentType='text/html',
                               Body=bytearray(mine, 'utf-8'),
                               Key=key)
        for child in sorted(self._children.keys()):
            self._children[child].write_index_file(destination, name)


class VirtualNode(DirNode):
    """
    A node that, strictly speaking, should be present in the tree but, for
    whatever reason, does not yet exist there. This could be because it was
    created after elements that are contained within itself. Or it could be
    because the S3 API might allow the direct creation of elements without
    explicitly creating their folder structure.
    """
    def __init__(self, path):
        o = munchify({'key': path})
        super(VirtualNode, self).__init__(o)
        self.virtual = True


class RootNode(DirNode):
    def __init__(self):
        super(RootNode, self).__init__(munchify({'key': ''}))
        self.virtual = True

    def get_index_file(self):
        links = []
        self.get_index_file_links(links)
        return self.add_links_to_body(links)


class NodeError(Exception):
    pass
