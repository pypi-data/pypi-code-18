# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import mock
from munch import munchify as m

from s3manage.index import HTML_BASE
from s3manage.index import Index

test_data = [mock.Mock(**{'key': 'test.txt', 'last_modified': '2011-01-01', 'size': 100000000}),
             mock.Mock(**{'key': 'help.dat', 'last_modified': '2011-01-01', 'size': 100000000}),
             mock.Mock(**{'key': 'firstdir/', 'last_modified': '2011-01-01', 'size': 0}),
             mock.Mock(**{'key': 'firstdir/firstfile.txt', 'last_modified': '2011-01-01', 'size': 100000000}),
             mock.Mock(**{'key': 'firstdir/nope.exe', 'last_modified': '2011-01-01', 'size': 100000000}),
             mock.Mock(**{'key': 'seconddir/', 'last_modified': '2011-01-01', 'size': 0}),
             mock.Mock(**{'key': 'notadir', 'last_modified': '2011-01-01', 'size': 100000000})]


def test_create_index():
    mock_bucket = mock.Mock(**{'get_items.return_value': test_data,
                               'get_index_name.return_value': 'index.html'})
    index = Index(mock_bucket)
    index.construct()
    assert index._root.is_dir
    assert len(index._root._children) == 5
    assert len(index._root._children['firstdir']._children) == 2
    assert len(index._root._children['seconddir']._children) == 0
    assert not index._root._children['notadir'].is_dir
    index.write_indexes()
    c1 = mock.call(ContentType="text/html",
              Body=bytearray(FIRST_LEVEL, 'utf-8'),
              Key="index.html")
    c2 = mock.call(ContentType="text/html",
              Body=bytearray(SECOND_LEVEL, 'utf-8'),
              Key="firstdir/index.html")
    c3 = mock.call(ContentType="text/html",
              Body=bytearray(SECOND_LEVEL_2, 'utf-8'),
              Key="seconddir/index.html")
    mock_bucket.put_object.assert_has_calls([c1, c2, c3])


FIRST_LEVEL=HTML_BASE.format("""<tr><td>📁</td><td><a href="firstdir">firstdir</a></td><td>2011-01-01</td><td> - </td></tr>
<tr><td>📃</td><td><a href="help.dat">help.dat</a></td><td>2011-01-01</td><td>100 MB</td></tr>
<tr><td>📃</td><td><a href="notadir">notadir</a></td><td>2011-01-01</td><td>100 MB</td></tr>
<tr><td>📁</td><td><a href="seconddir">seconddir</a></td><td>2011-01-01</td><td> - </td></tr>
<tr><td>📃</td><td><a href="test.txt">test.txt</a></td><td>2011-01-01</td><td>100 MB</td></tr>""")

SECOND_LEVEL=HTML_BASE.format("""<tr><td></td> <td><a href="..">&lt;Parent&gt;</a></td><td></td><td></td></tr>
<tr><td>📃</td><td><a href="firstfile.txt">firstfile.txt</a></td><td>2011-01-01</td><td>100 MB</td></tr>
<tr><td>📃</td><td><a href="nope.exe">nope.exe</a></td><td>2011-01-01</td><td>100 MB</td></tr>""")

SECOND_LEVEL_2=HTML_BASE.format('<tr><td></td> <td><a href="..">&lt;Parent&gt;</a></td><td></td><td></td></tr>')
