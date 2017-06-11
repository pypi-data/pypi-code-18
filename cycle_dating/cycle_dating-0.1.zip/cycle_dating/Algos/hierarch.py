import copy

import cycle_dating.Algos.optim_virtual as optim_virtual
from cycle_dating.Utilities import use_data as ud


class Hierarch(optim_virtual.Optim):
    """
        Class implementation of hierarchical method

        class structure allows hierarchical method to take any optimisation method class as parameter
        and use it to do two dimensional optimisation in each 'region'.

        Args:
            optim_method_cls (class type object derived from optim_virtual): a reference to the class that contains
                                                                                the optimisation method
            dim              (int): Number of buy-sell points, K
            trans_cost       (float): desired transaction cost in optimisation procedure
            with_troughs     (bool): True if we must find troughs in the first phase of EIISR, False if peaks
    """
    def __init__(self, optim_method_cls, dim, trans_cost=0, long=True, **kwargs):
        self.optim_method_cls = optim_method_cls
        self.add_kwargs = kwargs
        super().__init__(dim, long, trans_cost, False)

    def __str__(self):
        return "Hierarchical with " + self.optim_method_cls(dim=2, trans_cost=self.trans_cost, **self.add_kwargs).__str__()

    def get_params(self):
        return {"Name": "HR-" + self.optim_method_cls(dim=2, trans_cost=self.trans_cost, from_hierarch=True,
                                            long=self.long, **self.add_kwargs).get_name()}

    def get_name(self):
        return self.get_params()["Name"]

    def fix_end_regions(self):
        """
        Optimises the final two regions when the rest of the regions are finished optimising

        Returns:
            None
        """
        lowest_val = float("inf")
        lowest_idx = -1
        for pos in range(0, self.pos[1], 2):
            if self.data.reduced[pos].val < lowest_val:
                lowest_idx = pos
                lowest_val = self.data.reduced[pos].val
        highest_val = -float("inf")
        highest_idx = -1
        for pos in range(self.pos[-2] + 1, len(self.data.reduced), 2):
            if self.data.reduced[pos].val > highest_val:
                highest_idx = pos
                highest_val = self.data.reduced[pos].val
        self.pos[0], self.pos[-1] = lowest_idx, highest_idx


    def _optimise(self):
        self.pos = [0, len(self.data.reduced) - 1]
        self.region_valid = [[None, True]]
        self.num_reg = 1
        self.dat_attr = copy.deepcopy(self.data)
        pre_exit = False
        count = 0
        while len(self.pos) < self.dim:
            count += 1
            if not self.step():
                pre_exit = True
                break
        if pre_exit:
            print ("Optimization exited prematurely")
        self.fix_end_regions()
        return self.pos, self.evaluate()

    def make_points(self):
        pts = []
        for i in self.pos:
            pts.append(self.data.reduced[i])
        return pts

    def get_variation(self, region_idx):
        """
        Get the excess variation of the region_idx with the specified index

        Args:

            region_idx (int): index of region in the region_valid structure

        Returns (float):
            excess variation
        """
        if region_idx >= self.num_reg:
            region_idx = self.num_reg - 1
        if self.region_valid[region_idx][0] is not None:
            return self.region_valid[region_idx][0]
        the_sum = 0
        end_idx = self.pos[region_idx + 1]
        try:
            for i in range(self.pos[region_idx], end_idx):
                the_sum += abs(self.data.reduced[i+1].val - self.data.reduced[i].val)
        except IndexError:
            print ("begin idx, end idx: %i, %i" % (self.pos[region_idx], end_idx))
            print ("Class: ", self.optim_method_cls)
            raise IndexError

        self.region_valid[region_idx][0] = the_sum - abs(self.data.reduced[self.pos[region_idx]].val
                                                    - self.data.reduced[self.pos[region_idx + 1]].val)
        return self.region_valid[region_idx][0]

    def best_region(self):
        """
        Finds the region with the highest excess variation

        Returns (tuple) := (int, float):
            (index of best region, excess variation of best region)
        """
        best_idx = None
        best_val = -1000000
        for i in range(0, self.num_reg):
            if (self.region_valid[i][1]):
                temp_val = self.get_variation(i)
                if (temp_val > best_val):
                    best_idx = i
                    best_val = temp_val
        return best_idx, best_val

    def step(self):
        """
        A single optimisation step in the hierarchical method. This function divides a selected region into three,
        optimally and calculates excess variation for each new region and stores it

        Returns (bool):
            True if step was successful, False if no best region could be found (in which case the caller will end
                the optimisation procedure
        """
        best_reg, best_val = self.best_region()
        if best_val <= 0 or best_reg is None:
            print ("NO BEST REGION")
            print (self.region_valid)
            return False
        else:
            self.region_valid[best_reg] = [None, True]
        if self.pos[best_reg + 1] - self.pos[best_reg] <= 1:
            print ("BEST REGION TOO SMALL")
            return False
        if self.optim_method_cls.__name__ == "EIISR":
            self.dat_attr = self.data.copy_subset(idx_start=self.pos[best_reg] + 1, idx_end=self.pos[best_reg + 1] + 1)
        else:
            self.dat_attr = self.data.copy_subset(idx_start=self.pos[best_reg] + 1, idx_end=self.pos[best_reg + 1])
        try:
            if best_reg == 0 or best_reg == len(self.region_valid) - 1:
                long = not self.long
                self.dat_attr.fix_long_short(self.long)
            else:
                long = not (self.dat_attr.orig[0].val < self.dat_attr.orig[-1].val)
            if self.optim_method_cls.__name__ == "PSORefined" or self.optim_method_cls.__name__ == "DERefined":
                self.add_kwargs["pop_size"] = max(int(len(self.dat_attr.reduced)/50), 4)
            optim2d = self.optim_method_cls(dim=2, trans_cost=self.trans_cost, from_hierarch=True,
                                            long=long, **self.add_kwargs)
            optim2d.set_data(self.dat_attr)
            optim2d.init_pop()
        except IndexError:
            print ("Position: ", self.pos)
            ud.plot_solution(self.dat_attr, self.pos)
            print("Quit because of indexerror")
            exit()
        optim_pos, optim_val = optim2d.optimise()
        if optim_val <= 0.0:
            print ("Optim val: %f. Making region false" % optim_val)
            self.region_valid[best_reg][1] = False
            return True
        if self.dat_attr.begin_fixed:
            add_idx = 0
        else:
            add_idx = 0
        for pos, count in zip(optim_pos, range(len(optim_pos))):
            self.pos.insert(count + 1 + best_reg, self.pos[best_reg] + 1 + pos + add_idx)
            self.region_valid.insert(count + 1 + best_reg, [None, True])
        self.num_reg += 2
        return True


