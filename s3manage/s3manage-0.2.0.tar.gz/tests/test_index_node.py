# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import mock
import pytest
import six
from munch import munchify

from s3manage.index import DirNode
from s3manage.index import Node
from s3manage.index import NodeError
from s3manage.index import RootNode
from s3manage.index import VirtualNode
from s3manage.index import node_factory
from s3manage.index import HTML_BASE


def test_root_node_only():
    node = node_factory(munchify({'key': ''}))
    assert node.is_dir
    assert node._item.key == ''
    assert node.get_index_file() == ROOT_NODE_ONLY_INDEX
    assert node.get_part(7) is None

def test_dir_node_only():
    node = DirNode(munchify({'key': 'asdf/'}))
    assert node.is_dir
    assert len(node.parts) == 1
    assert node.get_index_file() == DIR_NODE_ONLY_INDEX
    str(node)

def test_first_level_children(capsys):
    node = RootNode()
    node.add_child(Node(munchify({'key': 'derp.txt'})))
    node.add_child(Node(munchify({'key': 'asdf/herp.dat'})))
    node.add_child(DirNode(munchify({'key': 'asdf/'})))
    assert node.is_dir
    assert len(node._children) == 2
    assert not node._children['derp.txt'].is_dir
    assert node._children['asdf'].is_dir
    assert len(node._children['asdf']._children) == 1
    assert node.get_index_file() == FIRST_LEVEL_CHILDREN_INDEX
    assert node._children['asdf'].get_index_file() == FIRST_LEVEL_CHILDREN_L2_INDEX
    node.print_tree()
    out, err = capsys.readouterr()
    assert out == FIRST_LEVEL_CHILDREN_TREE
    dest = mock.Mock()
    node.write_index_file(dest, 'index.html')
    first = mock.call(ContentType='text/html',
                 Body=bytearray(FIRST_LEVEL_CHILDREN_INDEX, 'utf-8'),
                 Key='index.html')
    second = mock.call(ContentType='text/html',
                  Body=bytearray(FIRST_LEVEL_CHILDREN_L2_INDEX, 'utf-8'),
                  Key='asdf/index.html')
    dest.put_object.assert_has_calls([first, second])
    str(node._children['derp.txt'])

def test_basic_node():
    node = Node(munchify({'key': 'asdf/derp.txt'}))
    assert node.get_index_file() is None
    links = []
    node.get_index_file_links(links)
    assert len(links) == 0
    assert not node.is_dir
    # On a standard node, this method should not operate on the destination at
    # all
    destination = mock.Mock()
    node.write_index_file(destination, 'index.html')
    assert len(destination.method_calls) == 0

def test_virtual_node():
    node = VirtualNode('testdir/')
    assert node.is_dir
    assert node.virtual
    assert len(node.parts) == 1

def test_non_virtual_node_complains():
    node = Node(munchify({'key': 'repeat'}))
    with pytest.raises(NodeError) as e_info:
        node.set_node(node)

ROOT_NODE_ONLY_INDEX=HTML_BASE.format("")

DIR_NODE_ONLY_INDEX=HTML_BASE.format('<a href="..">&lt;Parent&gt;</a>')

FIRST_LEVEL_CHILDREN_INDEX=HTML_BASE.format("""📁 <a href="asdf">asdf</a><br />
        📃 <a href="derp.txt">derp.txt</a>""")

FIRST_LEVEL_CHILDREN_L2_INDEX=HTML_BASE.format("""<a href="..">&lt;Parent&gt;</a><br />
        📃 <a href="herp.dat">herp.dat</a>""")

FIRST_LEVEL_CHILDREN_TREE="""|--- 
|   |--- asdf/
|   |   |--- asdf/herp.dat
|   |--- derp.txt
"""
