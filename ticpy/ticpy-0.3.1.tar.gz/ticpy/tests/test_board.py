from ticpy.src.board import Board
from ticpy.src.constants import SEED, SEED_REPR


def test_clear(board):
    board.cells[2][2].content = SEED.CROSS
    flat_board = sum(board.cells, [])
    assert not all(cell.content == SEED.EMPTY for cell in flat_board)
    board.clear()
    assert all(cell.content == SEED.EMPTY for cell in flat_board)


def test_is_draw(filled_board):
    filled_board.cells[2][2].content = SEED.EMPTY
    assert not filled_board.is_draw()


def test_has_won(cross_board):
    assert cross_board.has_won(SEED.CROSS)


def test_str(cross_board):
    cross = SEED_REPR[SEED.CROSS]
    assert str(cross_board).find(cross)

