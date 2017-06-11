import abc

class NoDataError(Exception):
    def __str__(self):
        return "Data not set. First call set_data(series_obj) before calling optimise()"


class Optim(metaclass=abc.ABCMeta):
    def long_get(self):
        return self.__long

    def long_set(self, state):
        if not isinstance(state, bool) and not isinstance(state, type(None)):
            raise TypeError("long variable can only be boolean True or False")
        if self.data_set:
            self.data.fix_long_short(long=state)
        self.__long = state

    def long_del(self):
        raise PermissionError("long variable may not be deleted")

    long = property(fget=long_get, fset=long_set, fdel=long_del, doc=None)

    def __init__(self, dim, long=None, trans_cost=0.0, from_hierarch=False):
        self.data_set = False
        self.from_hierarch = from_hierarch
        self.long = long
        self.trans_cost = trans_cost
        if dim % 2 == 0:
            self.dim = dim
        else:
            self.dim = dim + 1
        #self.pos = [0 for i in range(self.dim)]

    def init_pop(self, new_dim=None):
        if new_dim is not None:
            self.dim = new_dim
        pass

    @abc.abstractmethod
    def _optimise(self, **kwargs):
        """
        Abstract method. Derived classes' optimisation functions will
        implement this.
        """
        return

    def optimise(self, **kwargs):
        if not self.data_set:
            raise NoDataError
        return self._optimise(**kwargs)

    def set_data(self, series_obj):
        self.data = series_obj
        self.data_set = True
        """below maybe a bit hackish?"""
        if self.from_hierarch:
            if self.long is None:
                self.long = self.data.begin_is_long()
            self.data.fix_long_short(self.long)
        else:
            self.long = self.long
            self.data.fix_long_short(self.long)
        self.series = [el.val for el in self.data.reduced]

    def evaluate(self, attr="reduced"):
        value = 0.0
        for i in range(1, len(self.pos), 2):
            value += getattr(self.data, attr)[self.pos[int(i)]].val - getattr(self.data, attr)[self.pos[int(i-1)]].val
        if self.long:
            self.fitness = value
            return value
        else:
            self.fitness = -value
            return -value





class IndivBase(metaclass=abc.ABCMeta):

    def __init__(self, parent):
        self.parent = parent
        self.data = parent.data
        self.trans_cost = parent.trans_cost
        self.dim = parent.dim
        self.long = parent.long
        self.pos = self.init_pos()
        self.val = self.evaluate()

    @abc.abstractmethod
    def init_pos(self):
        return

    def evaluate(self):
        total_trans_cost = 0.0
        val = 0.0
        if self.trans_cost > 0.0:
            for i in range(1, self.dim):
                total_trans_cost += self.data.reduced[self.pos[i]].val
            total_trans_cost *= self.trans_cost

        try:
            for i in range(1, self.dim, 2):
                val += self.data.reduced[self.pos[i]].val - self.data.reduced[self.pos[i-1]].val
        except IndexError:
            print ("self.pos: ", self.pos)
            print ("len(self.data.reduced) = ", len(self.data.reduced))

        if not self.long:
            val *= -1

        self.val = val

        return val

