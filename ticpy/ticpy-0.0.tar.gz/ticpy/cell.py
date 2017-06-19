from ticpy.constants import SEED, SEED_REPR


class Cell(object):

    content = SEED.EMPTY

    def __init__(self, row, col):
        self.content = SEED.EMPTY
        self.row = row
        self.col = col

    def clear(self):
        self.content = SEED.EMPTY

    def __str__(self):
        return SEED_REPR[self.content]
