class zip_coordinates:
    '''
    Merge two object that have coordinate chromosome/position.
    The format of the objects must be a tuple with (coordinates, data)
    where coordinate is a tuple with chromosome,position_start, position_end
    and data is a tuple with the data. The data of the two object will be
    merged for matching lines.
    For the first object only the start coordinate is taken into account.
    '''

    def __init__(self, item1, item2):
        self.c2 = item2
        try:
            coordinates, self._last_data = next(self.c2)
        except StopIteration:
            coordinates, self._last_data = ((None, 0, 0), (None, ))
        self._chromosome, self._last_window_s, self._last_window_e = \
            coordinates
        self.c1 = item1
        self._last_chromosome = None
    _sentinel = object()

    def __next__(self):
        return self.next()

    def next(self):
        self.c1_line = next(self.c1)
        going_on = True
        while going_on:
            if self._chromosome == self.c1_line[0][0]:
                self._last_chromosome = self._chromosome
                if self.c1_line[0][1] >= self._last_window_s and \
                        self.c1_line[0][1] < self._last_window_e:
                    data = self.c1_line[1] + self._last_data
                    return (self.c1_line[0], data)
                    going_on = False
                elif self.c1_line[0][1] < self._last_window_s:
                    self.c1_line = next(self.c1)
                elif self.c1_line[0][1] >= self._last_window_e:
                    coordinates, self._last_data = next(self.c2)
                    self._chromosome, self._last_window_s, \
                        self._last_window_e = coordinates
            else:
                if self._last_chromosome != self._chromosome and \
                        self._last_chromosome is not None:
                    self.c1_line = next(self.c1)
                else:
                    coordinates, self._last_data = next(self.c2)
                    self._chromosome, self._last_window_s, \
                        self._last_window_e = coordinates

    def close(self):
        self.c1.close()
        self.c2.close()

    def __iter__(self):
        return (iter(self.next, self._sentinel))
