from dots_editor import utf8_braille
import pytest

def test_empty_cell_false(empty_cell):
    assert not empty_cell

def test_a_cell_true(a_cell):
    assert a_cell

def test_empty_cell_unicode(empty_cell):
    assert unicode(empty_cell) == u'\u2800'

def test_a_cell_unicode(a_cell):
    assert unicode(a_cell) == u'\u2801'

def test_eq(a_cell):
    assert a_cell == utf8_braille.Cell(dots_array=[1,0,0,0,0,0,0,0])

def test_add_dots(empty_cell):
    empty_cell.add_dots(1,2,3,4,5,6)
    assert empty_cell.cell == [1,1,1,1,1,1,0,0]

def test_add_dots_2(a_cell):
    a_cell.add_dots(4)
    assert a_cell == utf8_braille.Cell(u'\u2809')

@pytest.fixture
def empty_cell():
    return utf8_braille.Cell()

@pytest.fixture
def a_cell():
    return utf8_braille.Cell(u'\u2801')
