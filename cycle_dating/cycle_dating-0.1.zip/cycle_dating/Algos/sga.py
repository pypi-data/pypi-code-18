import time
import copy

import numpy
import numpy as np

from cycle_dating.Algos import optim_virtual as ov
from cycle_dating.Utilities.use_data import GenerateProper
from cycle_dating.Utilities import use_data as ud, series
from cycle_dating.Algos.Utilities.SGAQueue import SGAQueue

def np_sign(val):
    return numpy.sign(val)

class ParentError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if not isinstance(self.msg, str):
            return "Invalid parent for individual"
        else:
            return self.msg

class SmallSeriesException(Exception):
    """
    Exception defined for if series size is too small relative to number of required buy-
    sell points (K). For example, if K is larger than the number of peaks/troughs
    """
    def __str__(self):
        return "Dimension larger than series"

class SGA(ov.Optim):
    """
    Class implementation of SGA method. Acts as a manager for all SGA individuals. All SGA
    individuals are implemented as objects of type Individual (defined below this
    class)

    Args:
        dim (int): Number of buy-sell points (K)
        pop_size (int): population size
        indiv_iter (int): individual iteration
        running_time (float): maximum running time in seconds.
        init_pos (list): initial position of buy-sell points
        long (bool): If true, do long optimisation (sequence starts with buy point, ends
                        with sell point
        trans_cost (float): transaction cost
        from_hierarch (bool): True if the method is being implemented within hierarchical
                                method as HR-SGA
    """
    def __init__(self, dim = 0, pop_size=15, indiv_iter=1, running_time=float("inf"), init_pos=None, long=True,
                 trans_cost=0.0, from_hierarch=False, **kwargs):
        self.pop_size = max(1, int(np.round(pop_size)))
        self.indiv_iter = max(1, int(np.round(indiv_iter)))
        self.total_pop_size = self.pop_size*self.indiv_iter
        self.initial_pos = init_pos
        self.init_pos = self.initial_pos
        if init_pos is not None:
            dim = len(init_pos)

        self.running_time = running_time

        super().__init__(dim, long, trans_cost, from_hierarch)

    def __str__(self):
        return "SGA"

    def get_name(self):
        return "SGA Pop: " + str(self.pop_size)

    def get_params(self):
        return {"Name": self.get_name()}

    def init_pop(self, var_dist=None, new_dim=None):
        """Initialise the SGA population.

        Also used as a way to reset the algorithm
        without creating a new object
        Args:
            new_dim (int): if given (i.e. if new_dim is not None) reset the required number
                            of buy-sell points to new_dim
        Returns:
            None
        """
        if new_dim is not None:
            self.dim = new_dim
        self.pop = []
        for i in range(self.pop_size):
            for j in range(self.indiv_iter):
                if j >= 1:
                    if var_dist is not None:
                        self.pop.append(Individual(init_pos=self.pop[-1].pos, parent=self))
                    elif self.initial_pos is not None:
                        self.pop.append(Individual(init_pos=self.initial_pos, parent=self))
                    else:
                        self.pop.append(Individual(init_pos=self.pop[-1].pos, parent=self))
                else:
                    if var_dist is not None:
                        self.pop.append(Individual(init_pos=var_dist.sample(self.dim), parent=self))
                    elif self.initial_pos is not None:
                        self.pop.append(Individual(init_pos=self.initial_pos, parent=self))
                    else:
                        self.pop.append(Individual(parent=self))

    def max_indiv(self):
        """Find the individual with the highest fitness in the population

        Returns (sga.Individual):
            Individual object with highest fitness
        """
        max_val = -1000000
        max_indiv = None
        for i in range(self.total_pop_size):
            if (self.pop[i].val > max_val):
                max_indiv = self.pop[i]
                max_val = self.pop[i].val
        return max_indiv

    def _optimise(self):
        """Run algorithm to find optimal buy-sell points

        Args:
            None
        Returns (tuple):
            (position, fitness) of best individual
        """
        begin_time = time.clock()
        for i in range(self.total_pop_size):
            if (time.clock() - begin_time) >= self.running_time:
                break
            self.pop[i].optimise()
        max_indiv = self.max_indiv()
        self.max_val = max_indiv.val
        self.fitness = self.max_val
        self.pos = list(max_indiv.pos)
        return max_indiv.pos, max_indiv.val

    def evaluate(self):
        return self.max_val


class Individual(ov.IndivBase):
    """
    Class implementation of a single individual in SGA method.

    Args:
        parent (SGA): a pointer to the SGA implementation whose population this individual
                        belongs to
        other (Individual): serves as a copy constructor if this parameter is present
        init_pos (list): initial position for this individual
    """
    def __init__(self, parent=None, other=None, init_pos=None):
        if other is not None:
            self.parent = other.parent
            self.pos = other.pos
            self.val = other.val
            self.dim = other.dim
            self.long = other.long
            self.trans_cost = other.trans_cost
            self.data = other.data
        elif init_pos is not None:
            self.parent = parent
            self.data = parent.data
            self.pos = copy.copy(init_pos)
            self.dim = len(init_pos)
            if not (self.dim == self.parent.dim):
                raise ParentError("individual's parent dimensions not equal to assigned position's dimension.")
            self.up = 1
            self.long = parent.long
            self.initial_pos = copy.deepcopy(self.pos)
            if not (sorted(self.pos) == list(self.pos)):
                print ("pos not sorted before generating proper")
            gen_prop = GenerateProper(self, self.pos)
            self.pos = gen_prop.fix_pre_exist_pos()
            if not (sorted(self.pos) == list(self.pos)):
                print ("pos not sorted after generating proper")
                print ("Initial position: ", self.initial_pos)
                print ("unsorted position: ", self.pos)
            self.trans_cost = self.parent.trans_cost
            try:
                self.evaluate()
            except IndexError:
                raise IndexError(self.pos)
        else:
            if not isinstance(parent, SGA):
                raise ParentError("parent argument not a valid type (must be of type 'SGA')")
            super().__init__(parent)
            self.generate_proper()
            self.evaluate()

    def init_pos(self):
        return list(sorted(np.random.randint(size=self.dim, low=0, high=len(self.parent.data.reduced))))

    def adjust_one(self, pos_idx):
        """
        Adjusts a single buy-sell point in current solution.

        Args:
            pos_idx (int): index (in vector of buy-sell points) of the point to adjust
        Returns (int):
            1 if point is moved forward, -1 if backward
        """
        orig_pos = self.pos[pos_idx]
        mod = (pos_idx % 2)*2 - 1
        if not self.long:
            mod *= -1
        try:
            best_idx = self.pos[pos_idx]
            best_pt = self.parent.data.reduced[best_idx]
        except IndexError:
            raise IndexError("self.pos[pos_idx]: ", self.pos[pos_idx], "\nlen(self.parent.data.reduced): ", len(self.parent.data.reduced))
        """
        initially, curr_idx refers to the lower bound of the region to be processed, and
        next_idx refers to the upper bound of the region. after that, curr_idx keeps track of
        the current index we are looking at and comparing
        """
        for count, sub_range in enumerate(self.search_list[pos_idx]):
            curr_idx = sub_range[0]
            next_idx = sub_range[1]

            while curr_idx < next_idx:
                if self.parent.data.reduced[curr_idx].val*mod > best_pt.val*mod:
                    best_idx = curr_idx
                    best_pt = self.parent.data.reduced[best_idx]
                curr_idx += 2
            if count == 0:
                self.search_list[pos_idx][count][1] = self.search_list[pos_idx][count][0] - 1
            else:
                self.search_list[pos_idx][count][0] = self.search_list[pos_idx][count][1] + 1
        self.pos[pos_idx] = best_idx
        return numpy.sign(self.pos[pos_idx] - orig_pos)

    def init_searchable_spaces(self):
        self.search_list = [None for i in range(self.dim)]
        for i in range(self.dim):
            if i == 0:
                self.search_list[i] = [[0, 0],
                                       [0, self.pos[i + 1]],
                                       [self.pos[i + 1] + 1, self.pos[i + 1]]]
            elif i == self.dim - 1:
                self.search_list[i] = [[self.pos[i - 1] + 1, self.pos[i - 1]],
                                       [self.pos[i - 1] + 1, len(self.data.reduced)],
                                       [len(self.data.reduced), len(self.data.reduced)]]
            else:
                self.search_list[i] = [[self.pos[i - 1] + 1, self.pos[i - 1]],
                                       [self.pos[i - 1] + 1, self.pos[i + 1]],
                                       [self.pos[i + 1] + 1, self.pos[i + 1]]]
        return self.search_list

    def generate_proper(self):
        buy_points = np.random.choice(np.arange(0, len(self.data.reduced) - 2, 2), size=self.dim/2, replace=False)
        buy_points.sort()
        sell_points = []
        for bp_idx in range(len(buy_points) - 1):
            sell_points.append(np.random.randint(buy_points[bp_idx], buy_points[bp_idx + 1]))
        sell_points.append(np.random.randint(buy_points[-1], len(self.data.reduced)))
        self.pos = []
        for bp, sp in zip(buy_points, sell_points):
            self.pos.append(bp)
            self.pos.append(sp)

    def modify_search_list(self, idx, right):
        """Update search list for specific individual

        modifies the search list of the buy-sell point at index
        idx (in the list of buy-sell points).
        Args
            idx (int): the index of the buy-sell point (in the vector of buy-sell points)
            right (bool): true if the point to the right of idx moved, false if the left
                            point moved
        Returns:
            None
        """
        if self.search_list[idx][1][0] < self.search_list[idx][1][1]:
            "if point at idx has not been modified yet"
            if right:
                "if the point to the right of point at idx moved either away or towards it"
                self.search_list[idx][1][1] = self.pos[idx + 1]
                self.search_list[idx][2][0] = self.pos[idx + 1] + 1
                self.search_list[idx][2][1] = self.pos[idx + 1]
            else:
                "if the point to the left of point at idx moved either away or towards it"
                self.search_list[idx][1][0] = self.pos[idx - 1] + 1
                self.search_list[idx][0][0] = self.pos[idx - 1] + 1
                self.search_list[idx][0][1] = self.pos[idx - 1]
        elif right:
            "if the point to the right of point at idx moved either away or towards it"
            if self.pos[idx + 1] > self.search_list[idx][2][1]:
                self.search_list[idx][2][1] = self.pos[idx + 1]
        else:
            "if the point to the left of point at idx moved either away or towards it"
            if self.pos[idx - 1] + 1 < self.search_list[idx][0][0]:
                self.search_list[idx][0][0] = self.pos[idx - 1] + 1

    def search_list_is_empty(self, idx):
        """
        Check if searchable area is empty

        Args:
            idx (int): index of buy-sell point for which to check search list
        Returns:
            None
        """
        if self.search_list[idx][0][0] < self.search_list[idx][0][1]:
            return False
        if self.search_list[idx][1][0] < self.search_list[idx][1][1]:
            return False
        if self.search_list[idx][2][0] < self.search_list[idx][2][1]:
            return False
        return True

    def adjust_all(self):
        """Adjust SGA individual solution, until finished

        calling this function causes the SGA individual to adjust points
        until its adjustment queue is empty

        Returns:
            None
        """
        adjust_idxes = set(list(range(self.dim)))
        self.init_searchable_spaces()
        adjustments = 0
        random_range = list(numpy.random.choice(list(adjust_idxes), len(adjust_idxes), replace=False))
        adj_queue = SGAQueue(random_range)
        while not adj_queue.is_empty():
            idx = adj_queue.root.idx
            dir = self.adjust_one(idx)
            adjustments += 1
            if dir == -1:
                if idx < self.dim - 1:
                    if self.search_list_is_empty(idx + 1):
                        adj_queue.append_val(idx + 1)
                    self.modify_search_list(idx + 1, False)
                if idx > 0:
                    self.modify_search_list(idx - 1, True)
            elif dir == 1:
                if idx > 0:
                    if self.search_list_is_empty(idx - 1):
                        adj_queue.append_val(idx - 1)
                    self.modify_search_list(idx - 1, True)
                if idx < self.dim - 1:
                    self.modify_search_list(idx + 1, False)
            adj_queue.remove_front()
        self.evaluate()

    def optimise(self):
        """
        Wrapper function (decorator) for the adjust_all function.

        Returns:
            (tuple): (final set of buy-sell points, final objective function value)
        """
        self.adjust_all()
        return self.pos, self.val


def main():
    my_series = series.Series(series_len=10000, seed=None)
    my_sga = SGA(20, pop_size=100)
    my_sga.set_data(my_series)
    my_sga.init_pop()
    pos, fitness = my_sga.optimise()
    ud.plot_solution(my_series, pos)

if __name__ == "__main__":
    main()
