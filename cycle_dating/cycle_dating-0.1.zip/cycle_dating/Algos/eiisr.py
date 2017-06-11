__author__ = 'User'

import copy
import time

from cycle_dating.Algos import optim_virtual
from cycle_dating.Utilities import use_data as ud, series
from cycle_dating.Algos.Utilities.LinkedListEIISR import LinkedListEIISR

def combo_loop_help(lst, curr_idx, curr_num, total_num, all_els, all_perms):
    """
    Helper function for the combinations function defined below
    """
    if all_els is None:
        all_els = []
    for i in range(curr_idx, len(lst)):
        all_els.append(lst[i])
        if curr_num == total_num:
            all_perms.append(copy.deepcopy(all_els))
            del all_els[-1]
        else:
            combo_loop_help(lst, i + 1, curr_num + 1, total_num, all_els, all_perms)
            del all_els[-1]

def combinations(lst, num):
    """
    Find all combinations of size num out of list lst

    Args:
        lst (list<object>): list of any kind of object out of which we must find combinations
        num (int): size of each combination
    Returns (list<list<object>>):
        list of lists of object types contained in lst
    """
    all_perms = []
    combo_loop_help(lst, 0, 1, int(num), None, all_perms)
    return all_perms


class EIISR(optim_virtual.Optim):
    """
    Class implementation for EIISR algorithm.

    Args:
        dim          (int): Number of buy-sell points, K
        long         (bool): True if long sequence if buy-sell points is required
        trans_cost   (float): transaction cost
        with_troughs (bool): True if we must find troughs in the first phase of EIISR, False if peaks
    """
    def __init__(self, dim, long=True, trans_cost=0.0, from_hierarch=False, with_troughs=True, **kwargs):
        self.with_troughs = with_troughs
        super().__init__(dim, long, trans_cost, from_hierarch)
        if with_troughs:
            self.troughs_mod = 1
        else:
            self.troughs_mod = -1

    def get_name(self):
        return "EIISR"

    def get_params(self):
        return {"Name": self.get_name()}

    def set_data(self, series_obj):
        super().set_data(series_obj)

    def advance_next_round(self, idx, window_size):
        """
        Determines whether the time series observation at time index idx is to be included in the next clearance set

        Args:
            idx         (int): index of time series observation where we wish to test whether it should be in
                                next clearance set
            window_size (int): Size of window where we test whether observation at idx should be in next clearance set
        Returns (bool):
            True if included in next clearance set, False otherwise
        """
        left_boundary = max(idx - window_size, 0)
        right_boundary = min(idx + window_size, self.data.orig_len - 1)
        if (self.data.orig[idx].val < self.data.orig[left_boundary].val)\
        and (self.data.orig[idx].val < self.data.orig[right_boundary].val):
            return True
        if (self.data.orig[idx].val < self.data.orig[left_boundary].val)\
        and (self.data.orig[idx].val == self.data.orig[right_boundary].val):
            return True
        if (idx == left_boundary) and (self.data.orig[idx].val < self.data.orig[right_boundary].val)\
        or (idx == right_boundary) and (self.data.orig[idx].val < self.data.orig[left_boundary].val):
            return True
        return False

    def find_best(self, begin_idx, end_idx):
        """
        Find highest (if self.troughs_mod = 1) or lowest (if self.troughs_mod = -1) time series observation between
        begin_idx and end_idx

        Args:
            begin_idx (int): starting index of place to find best
            end_idx   (int): the last index of place to find best
        Returns:
            None
        """
        best_idx = begin_idx
        curr_idx = best_idx + 1
        while curr_idx < end_idx:
            if self.data.orig[curr_idx].val*self.troughs_mod > self.data.orig[best_idx].val*self.troughs_mod:
                best_idx = curr_idx
            curr_idx += 1
        return best_idx

    def in_between(self, idxes):
        """
        Given a set of troughs (peaks), this function finds all optimal peaks (troughs)

        Args
            idxes (int): time indices of all optimal troughs (peaks)
        Returns:
            None
        """
        insert_list = []
        for curr_idx in range(len(idxes)):
            if not self.forward:
                if curr_idx == 0:
                    begin_idx = 0
                else:
                    begin_idx = idxes[curr_idx - 1]
                end_idx = idxes[curr_idx]
            else:
                if curr_idx == len(idxes) - 1:
                    end_idx = len(self.data.orig)
                else:
                    end_idx = idxes[curr_idx + 1]
                begin_idx = idxes[curr_idx]
            insert_idx = self.find_best(begin_idx, end_idx)
            if self.forward:
                insert_list.append([curr_idx + 1, insert_idx])
            else:
                insert_list.append([curr_idx, insert_idx])
        insert_list.reverse()
        for insert_info in insert_list:
            idxes.insert(insert_info[0], insert_info[1])

    def all_combos(self, prev_del_idxes, curr_idxes):
        """
        Finds all combinations of the set theoretic difference between the last two
        clearance sets, and the last clearance set, as described in the thesis

        Args:
            prev_del_idxes (list<int>): set-theoretic difference between the last and second to last clearance sets
            curr_idxes:    (list<int>): last clearance set
        Returns (list<list<int>>):
            list of lists of all combinations between the two clearance sets (of size required_num, defined below)
        """
        num_idxes = self.dim/2
        required_num = num_idxes - len(curr_idxes)
        if required_num > 0:
            return combinations(prev_del_idxes, required_num)
        else:
            return [curr_idxes]

    def _optimise(self, **kwargs):
        """
        The main function called to obtain an optimal set of buy-sell points via the EIISR method

        Args
            kwargs (dict): extra arguments - for compatibility in the inheritance structure
        Returns (tuple) := (list<int>, float):
            (time indices of buy-sell points, fitness value)
        """
        if self.long:
            self.forward = self.with_troughs
        else:
            self.forward = not self.with_troughs
        if self.forward:
            leave_out_start = 0
            leave_out_end = 1
        else:
            leave_out_start = 1
            leave_out_end = 0
        in_idxes = LinkedListEIISR()
        in_idxes.add_idx_range(leave_out_start, len(self.data.orig) - leave_out_end)
        window_size = 1
        remove_elements = []
        if self.dim == 2:
            condition_not_met = in_idxes.size > 5
        else:
            condition_not_met = in_idxes.size > self.dim/2
        while condition_not_met:
            remove_elements = []
            for in_idx in in_idxes:
                if not self.advance_next_round(in_idx.idx, window_size):
                    remove_elements.append(in_idx)
            for el in remove_elements:
                in_idxes.remove_node(el)
            window_size += 1
            if self.dim == 2:
                condition_not_met = in_idxes.size > 1
            else:
                condition_not_met = in_idxes.size > self.dim/2
        in_idxes = list(in_idxes)
        in_idxes = [node.idx for node in in_idxes]
        prev_del_idxes = [node.idx for node in remove_elements]
        top_fitness, top_pos = -float("inf"), None
        if self.dim == 2:
            perm_func = combinations
            perm_args = prev_del_idxes + in_idxes, 1
        else:
            perm_func = self.all_combos
            perm_args = prev_del_idxes, in_idxes
        for perm in perm_func(*perm_args):
            if len(perm) < self.dim/2:
                test_idxes = sorted(perm + in_idxes)
            else:
                test_idxes = sorted(perm)
            self.in_between(test_idxes)
            self.pos = test_idxes
            fitness = self.evaluate("orig")
            if fitness > top_fitness:
                top_fitness = fitness
                top_pos = copy.deepcopy(self.pos)
        self.pos = top_pos
        self.fitness = top_fitness
        reduced_pos = find_reduced_idxes(self.data, self.pos)
        return reduced_pos, self.fitness


def find_reduced_idxes(series_obj, idxes):
    """
    Helper function for the EIISR class above. Finds reduced indices from optimal set of buy-sell points. May be
    removed in future
    Args:
        series_obj (series):  time series object for which we find reduced indices
        idxes      (list<int>):  list of buy-sell points for which we find the reduced indices
    Returns (list<int>):
        reduced set of indices of idxes
    """
    reduced_idxes = []
    curr_reduced_idx = 0
    try:
        for count, pos_idx in enumerate(sorted(idxes)):
            while True:
                if series_obj.reduced[curr_reduced_idx].idx == series_obj.orig[pos_idx].idx:
                    reduced_idxes.append(curr_reduced_idx)
                    curr_reduced_idx += 1
                    break
                curr_reduced_idx += 1
    except IndexError:
        print("curr_reduced_idx = ", curr_reduced_idx)
        print("idxes: ", idxes)
        print(("reduced_idxes: [".join([" %i " for i in range(len(reduced_idxes))]) + "], series_obj.reduced[reduced_idxes[0]].idx: %i")
            % (tuple(reduced_idxes) + (series_obj.reduced[reduced_idxes[0]].idx,)))
        print("series_obj.reduced[0].idx = %i, series_obj.reduced[-1].idx = %i"
               % (series_obj.reduced[0].idx, series_obj.reduced[-1].idx))
        print("series_obj.orig[idxes[0]].idx = %i, series_obj.orig[idxes[1]].idx = %i"
               % (series_obj.orig[idxes[0]].idx, series_obj.orig[idxes[1]].idx))
        print ("idxes: ", [idxes[count - 1], idxes[count]])
        ud.plot_solution(series_obj, [idxes[count - 1], idxes[count]], points_are_orig=True, scatter=True)
        print ("idxes: ", idxes, "series lengths: ", len(series_obj.reduced), len(series_obj.orig))
        ud.plot_solution(series_obj, [])
        raise IndexError("find_reduced_idxes received invalid data. buy-sell point index: %i. Total series reduced size: %i"
                         ". Total series original size: %i"
                         % (count, len(series_obj.reduced), len(series_obj.orig)))
    return reduced_idxes

if __name__ == "__main__":
    """
    Example of the usage of EIISR
    """
    length = 16000
    dim = 50
    series_obj = series.Series(series_len=length)
    begin_time = time.time()
    eiisr_obj = EIISR(dim, True)
    eiisr_obj.set_data(series_obj)
    pos, fitness = eiisr_obj.optimise()
    print ("EIISR time: %f" % (time.time() - begin_time))
    ud.plot_solution(series_obj, pos, show_orig=True)
    print ("EIISR fitness: %f" % fitness)
