
class Line(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_clockwise_to_point(self, x, y):
        '''
        Compute the cross product of (AB) X (AP), where P is (x, y)
        '''
        ab = (self.end[0] - self.start[0], self.end[1] - self.start[1])
        ap = (x - self.start[0], y - self.start[1])
        cp = ab[0] * ap[1] - ap[0] * ab[1]

        return cp > 0
