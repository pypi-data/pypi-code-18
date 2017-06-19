from ticpy.cell import Cell
from ticpy.constants import SEED


class Board(object):

    def __init__(self, rows, cols):
        self.ROWS = rows
        self.COLS = cols
        self.cells = [[Cell(i, j)
                       for j in range(cols)]
                      for i in range(rows)]
        self.current_row = None
        self.current_col = None

    def clear(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.cells[i][j].clear()

    def is_draw(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.cells[i][j].content == SEED.EMPTY:
                    return False
        return True

    def has_won(self, seed):
        three_in_row = self.cells[self.current_row][0].content == seed \
                       and self.cells[self.current_row][1].content == seed \
                       and self.cells[self.current_row][2].content == seed

        three_in_column = self.cells[0][self.current_col].content == seed \
                          and self.cells[1][self.current_col].content == seed \
                          and self.cells[2][self.current_col].content == seed

        three_in_diagonal = self.current_row == self.current_col \
                            and self.cells[0][0].content == seed \
                            and self.cells[1][1].content == seed \
                            and self.cells[2][2].content == seed

        three_in_opposite_diagonal = (self.current_row + self.current_col == 2) \
                                     and self.cells[0][2].content == seed \
                                     and self.cells[1][1].content == seed \
                                     and self.cells[2][0].content == seed

        return three_in_row or three_in_column or three_in_diagonal or three_in_opposite_diagonal

    def __str__(self):
        row_repr = '|{}|'
        list_of_letters = map(str, map(chr, range(97, 97+self.COLS, 1)))
        final_str = ' ' + row_repr.format('|'.join(list_of_letters)) + '\n'

        for row in range(self.ROWS):
            final_str += str(row + 1 ) + row_repr.format('|'.join(map(str, self.cells[row]))) + '\n'

        return final_str
