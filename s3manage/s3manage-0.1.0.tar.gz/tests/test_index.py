import mock
from munch import munchify as m

from s3manage.index import Index

test_data = [mock.Mock(**{'key': 'test.txt'}),
             mock.Mock(**{'key': 'help.dat'}),
             mock.Mock(**{'key': 'firstdir/'}),
             mock.Mock(**{'key': 'firstdir/firstfile.txt'}),
             mock.Mock(**{'key': 'firstdir/nope.exe'}),
             mock.Mock(**{'key': 'seconddir/'}),
             mock.Mock(**{'key': 'notadir'})]


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


FIRST_LEVEL="""<!DOCTYPE html>
<html>
    <body>
        <a href="firstdir">firstdir</a><br />
        <a href="help.dat">help.dat</a><br />
        <a href="notadir">notadir</a><br />
        <a href="seconddir">seconddir</a><br />
        <a href="test.txt">test.txt</a>
    </body>
</html>"""

SECOND_LEVEL="""<!DOCTYPE html>
<html>
    <body>
        <a href="..">&lt;Parent&gt;</a><br />
        <a href="firstfile.txt">firstfile.txt</a><br />
        <a href="nope.exe">nope.exe</a>
    </body>
</html>"""

SECOND_LEVEL_2="""<!DOCTYPE html>
<html>
    <body>
        <a href="..">&lt;Parent&gt;</a>
    </body>
</html>"""
