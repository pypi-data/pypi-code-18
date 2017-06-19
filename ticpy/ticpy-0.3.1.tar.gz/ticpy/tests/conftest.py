from random import randint
from pytest import fixture
from ticpy.src.constants import SEED
from ticpy.src.cell import Cell
from ticpy.src.board import Board
from ticpy.src.game import Game


@fixture(name='cell')
def get_cell():
    cell = Cell(0, 0)
    yield cell


@fixture(name='board')
def get_board():
    board = Board(3, 3)
    yield board


@fixture(name='filled_board')
def get_filled_board():
    board = Board(3, 3)
    for i in range(3):
        for j in range(3):
            board.cells[i][j].content = randint(SEED.CROSS, SEED.NOUGHT)

    yield board


@fixture(name='cross_board')
def get_cross_board():
    board = Board(3, 3)
    board.current_row = 1
    board.current_col = 1
    for i in range(3):
        for j in range(3):
            board.cells[i][j].content = SEED.CROSS

    yield board


@fixture(name='game')
def get_game():
    game = Game(3, 3)
    yield game
