from cycle_dating.Algos import optim_virtual as ov


def gen_nums(num_lim, start):
    init = start
    while init < num_lim:
        yield init
        init += 2


class FE2(ov.Optim):
    data = None

    def __init__(self, trans_cost, long, *args, **kwargs):
        super().__init__(dim=2, long=long, trans_cost=trans_cost, from_hierarch=True)

    def __str__(self):
        return "FE2"

    def get_name(self):
        return str(self)

    def evaluate(self, _point1, _point2):
        return (_point2 - _point1)*self.up \
                - self.trans_cost*(_point1 + _point2)

    def _optimise(self):
        if self.long:
            self.up = 1
        else:
            self.up = -1
        self.points = [0, 1]
        self.val = self.evaluate(self.data.reduced[self.points[0]].val, self.data.reduced[self.points[1]].val)

        for i in gen_nums(len(self.data.reduced), 0):
            for j in gen_nums(len(self.data.reduced), i + 1):
                cand_val = self.evaluate(self.data.reduced[i].val, self.data.reduced[j].val)
                if cand_val > self.val:
                    self.points = [i, j]
                    self.val = cand_val

        if (self.points[1] - self.points[0]) % 2 == 0:
            print (self.data.reduced[0].idx, self.data.reduced[1].idx)

        return self.points, self.val

