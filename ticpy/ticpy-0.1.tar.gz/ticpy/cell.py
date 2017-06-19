from ticpy.constants import SEED, SEED_REPR


class Cell(object):

    content = SEED.EMPTY

    def __init__(self, row, col):
        """
        :param row: (int) 
        :param col: (int)
        """
        self.content = SEED.EMPTY
        self.row = row
        self.col = col

    def clear(self):
        """
        Resets the cell to empty value
        :return: 
        """
        self.content = SEED.EMPTY

    def __str__(self):
        """
        String representation for 
        :return: 
        """
        return SEED_REPR[self.content]
