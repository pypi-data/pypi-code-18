import random
import copy
import time

import numpy as np

import cycle_dating.Algos.optim_virtual as ov
from cycle_dating.Utilities import use_data as ud, series
from cycle_dating.Algos import sga as nlg
from cycle_dating.Algos.Utilities.gen_types import LinearScale

class DomainError(Exception):
    def __str__(self):
        return "Domain size zero"

class individual:
    """
    Class implementation of a single individual in PSO population
    Args:
        domain (list): indicates which indices of the time series this individual has access
                        to
        master (PSO): PSO object whose population this individual is a part of
        this_idx (int): unique integer assigned to this individual in the population
        pos (list): If given, initial position (or solution) for this individual
    """
    __slots__ = ["vel", "pos", "pers_best", "val", "dim", "this_idx", "pers_best_pos",
                 "pers_best_val", "best_nbr_idx", "left_border", "right_border"]

    def __init__(self, domain, dim, master, this_idx, pos=None):
        self.left_border, self.right_border = master.get_nbr_bounds(this_idx)
        self.dim = dim
        self.pos = [0, 0]
        if domain[1] - domain[0] == 0:
            raise DomainError
        gen_size = (domain[1] - domain[0] + 1)/dim
        if gen_size < 1:
            self.pos = list(range(domain[1] - domain[0] + 1))
            return
        if pos==None:
            while (self.pos[0] == self.pos[1]):
                try:
                    self.pos = np.asarray([random.randrange(int(gen_size*i), int(gen_size*(i + 1))) for i in range(dim)])
                except ValueError:
                    raise ValueError("gen_size: ", gen_size, ", domain: ", domain)
        else:
            self.pos = pos
        self.pos.sort()
        self.pos = np.asarray(self.pos).astype(np.float64)
        self.vel = np.random.random(size=self.dim)*domain[1]/self.dim/2 - domain[1]/self.dim/4

    def init_pers_best(self):
        self.pers_best_pos = copy.deepcopy(self.pos)
        self.pers_best_val = -float("inf")

class PSOMeta:
    def __str__(self):
        return "PSO"


class PSO(ov.Optim):
    """
    Class implementation of the PSO algorithm, adapted for the cycle dating optimisation problem.

    Args:
        dim                  (int): number of dimensions of objective function (number of buy-sell points, in our case)
        pop_size             (int): number of particles in swarm
        nbr_rad              (int): neighbourhood radius. Neighbourhood size is then 2 * nbr_rad + 1. The ring
                                    topology was used for the algorithm
        cog_scale_info       (any derived type of gen_types.Scale): scaling data structure for the cognitive scale
                                                                        parameter
        soc_scale_info       (any derived type of gen_types.Scale): scaling data structure for the social scale
                                                                        parameter
        inertia              (float): inertia weight parameter
        max_time             (float): maximum time in seconds that algorithm may run
        mutate               (bool): if True, then mutate particles' position at each iteration (see PSO.mutate method)
        trans_cost           (float): transaction cost to take into account in objective function (zero for my thesis)
        no_change_stop_ratio (float): ratio of maximum number of iterations (max_iter), that algorithm must stop after
                                        if no improvement in best position is found
        max_iter             (int): maximum number of iterations that algorithm may run for
        long                 (bool): if True, then objective function has the long form, if False, it has the short form
        from_hierarch        (bool): if True, this instance is used within the hierarchical method, if False, it is not
        return_top           (int or NoneType): if None, then only return best particle after optimisation, if a number
                                                    n, then return top n best particles in swarm after iteration
        nbr_rad_rate         (float or NoneType): if not None, then make neighbourhood radius (nbr_rad) this ratio of
                                                    the total swarm size. If None, keep nbr_rad as is

    """
    def __init__(self, dim, pop_size,  nbr_rad, cog_scale_info, soc_scale_info, inertia,
                 max_time, mutate, trans_cost, no_change_stop_ratio, max_iter, long=True, from_hierarch=False,
                 return_top=None, nbr_rad_rate=None, **kwargs):
        self.cog_scale_info = copy.deepcopy(cog_scale_info)
        self.cog_scale = copy.deepcopy(cog_scale_info)
        self.soc_scale_info = copy.deepcopy(soc_scale_info)
        self.soc_scale = copy.deepcopy(soc_scale_info)
        self.inertia = max(0.05, abs(inertia))
        self.max_time = max_time
        self.do_mutate = mutate
        self.pop_size = max(1, int(np.round(pop_size)))
        if nbr_rad_rate is not None:
            nbr_rad = nbr_rad_rate*self.pop_size
        self.nbr_rad = min(max(0, int(np.ceil(nbr_rad))), self.pop_size)
        self.nbr_rad_rate = nbr_rad_rate
        self.return_top = int(np.round(return_top))

        self.no_change = 0
        self.iter_count = 0

        self.max_iter = max(0, int(np.round(max_iter)))
        self.no_change_stop_ratio = max(0.005, no_change_stop_ratio)
        self.no_change_stop = max(0, int(np.round(no_change_stop_ratio*self.max_iter)))

        super().__init__(dim, long, trans_cost, from_hierarch)

        if self.long:
            self.search_up = 1
        else:
            self.search_up = -1


    def __str__(self):
        return "PSO"

    def init_pop(self, new_dim=None, new_max_time=None):
        """
        Initializes the PSO population.

        The two arguments are for resetting the number of dimensions and the maximum
        computation time allowed. This proved useful in the case where S-Race was run, so that new instances of PSO
        did not have to be created each time.

        Args:
            new_dim      (int): Sets a new number of dimensions for the PSO instance
            new_max_time (float): Sets a new maximum time for the PSO instance
        Returns:
            None
        """
        self.soc_scale = copy.deepcopy(self.soc_scale_info)
        self.cog_scale = copy.deepcopy(self.cog_scale_info)
        self.begin_time = time.perf_counter()
        if new_dim is not None:
            self.dim = new_dim
        self.pop = []
        if not self.data_set:
            print("No data available - population vector empty")
            return
        for i in range(self.pop_size):
            pos = None
            self.pop.append(individual((0, len(self.data.reduced) - 1), self.dim, pos=pos, master=self, this_idx=i))
            self.pop[-1].init_pers_best()
        for i in range(self.pop_size):
            self.evaluate(i)

    def update_velocity(self, cog_sc=None, soc_sc=None, indiv_idx=None):
        """
        Updates velocity of all particles, or of one particle

        If indiv_idx is None, then all particles' positions are updated from this invocation of the function. This
        function is called recursively in that case, but only one level 'down' (see for loop just before return
        statement). If indiv_idx is a number (int), then the velocity is updated for the particle with that index.
        Velocity is updated via the formula given in the thesis, and may also be found in any text dealing with
        Particle Swarm Optimization.

        Args:
            cog_sc (float): cognitive scale factor for the current iteration
            soc_sc (float): social scale factor for the current iteration
        """
        if (not (indiv_idx == None)):
            if (self.nbr_rad > 0) and (self.nbr_rad < self.pop_size):
                social_pos, social_val, best_nbr_idx = self.get_best_nbr(indiv_idx)
                self.pop[indiv_idx].best_nbr_idx = best_nbr_idx
            else:
                social_pos = self.glob_best_pos
            self.pop[indiv_idx].vel = self.pop[indiv_idx].vel*self.inertia\
            + np.multiply(np.asarray([random.random() for i in range(self.dim)])*cog_sc, (self.pop[indiv_idx].pers_best_pos - self.pop[indiv_idx].pos))\
            + np.multiply(np.asarray([random.random() for i in range(self.dim)])*soc_sc, (social_pos - self.pop[indiv_idx].pos))
            for idx, v in enumerate(self.pop[indiv_idx].vel):
                if idx == 0 and self.pop[indiv_idx].pos[idx] + v < 0:
                    self.pop[indiv_idx].vel[idx] = -self.pop[indiv_idx].pos[idx]
                elif idx == self.dim - 1 and self.pop[indiv_idx].pos[idx] + v > len(self.data.reduced) - 1:
                    self.pop[indiv_idx].vel[idx] = len(self.data.reduced) - 1 - self.pop[indiv_idx].pos[idx]
                elif idx > 0 and idx < self.dim - 1 and self.pop[indiv_idx].pos[idx] + v >= self.pop[indiv_idx].pos[idx + 1]:
                    self.pop[indiv_idx].vel[idx] = self.pop[indiv_idx].pos[idx + 1] - self.pop[indiv_idx].pos[idx]
                elif (idx > 0 and idx < self.dim - 1) and self.pop[indiv_idx].pos[idx] + v <= self.pop[indiv_idx].pos[idx - 1]:
                    self.pop[indiv_idx].vel[idx] = self.pop[indiv_idx].pos[idx - 1] - self.pop[indiv_idx].pos[idx]
            return
        else:
            cog_sc = self.cog_scale.new_scale()
            soc_sc = self.soc_scale.new_scale()
            for idx, obj in enumerate(self.pop):
                self.update_velocity(cog_sc, soc_sc, idx)
            return

    def update_pos(self, indiv_idx = None):
        """
        Update the position by adding the velocity vector to the position vector for each particle

        Works the same way, recursive-wise, as update_vel: if indiv_idx is None, all particles' positions are updated
        via an update_pos call from this function. If indiv_idx is an index, then the particle with that index has its
        position updated from within this function.

        Args:
            indiv_idx (int): index of particle which will have its position updated

        Returns:
            None
        """
        if not (indiv_idx is None):
            self.pop[indiv_idx].pos += self.pop[indiv_idx].vel
        else:
            for idx in range(len(self.pop)):
                self.update_pos(idx)
                if self.do_mutate:
                    self.mutate(idx)
                self.pop[idx].pos = np.asarray(list(map(self.fix_bounds, self.pop[idx].pos))).astype(np.float64)
                self.pop[idx].pos.sort()
                self.evaluate(idx)
                if self.pop[idx].val > self.glob_best_val:
                    self.glob_best_pos = copy.deepcopy(self.pop[idx].pos)
                    self.glob_best_val = self.pop[idx].val

    def mutate(self, indiv_idx):
        """
        Provides functionality to mutate a particle's position in the same fashion that a genetic algorithm might
        mutate it. This was not used in the thesis.

        Parameters could be added to the function to control the exact behaviour of the mutation.

        Args:
            indiv_idx (int): index of the particle which must have its position mutated

        Returns:
            None
        """
        indiv = self.pop[indiv_idx]
        for p_idx in range(len(indiv.pos)):
            if random.random() < min(0.5, 0.1 + 0.05*self.no_change):
                if random.random() < 0.5:
                    indiv.pos[p_idx] += 2*random.randrange(3)
                else:
                    indiv.pos[p_idx] -= 2*random.randrange(3)

    def fix_bounds(self, pos_val):
        """
        If a particle's position in any dimension falls outside the ends of the time series, this function will put the
        values for those dimensions back within the time series.

        Args:
            pos_val (numeric): value of the given dimension. May be either of type float or int.
        """
        if pos_val >= len(self.data.reduced):
            if len(self.data.reduced) >= 4:
                return len(self.data.reduced) - 1 - random.randrange(int(len(self.data.reduced))//4)
            else:
                return len(self.data.reduced) - 1
        elif pos_val < 0:
            if len(self.data.reduced) >= 4:
                return random.randrange(int(len(self.data.reduced))//4)
            else:
                return 0
        elif pos_val >= len(self.data.reduced) - 1:
            return len(self.data.reduced) - 1
        else:
            return pos_val

    def update_all(self):
        self.update_velocity()
        self.update_pos()

    def pop_info(self):
        for indiv in self.pop:
            print ("position: ", indiv.pos)
            print ("velocity: ", indiv.vel)
            print ("value: ", indiv.val)
            print ("")

    def _optimise(self, **kwargs):
        self.no_change = 0
        self.iter_count = 0
        self.glob_best_pos, self.glob_best_val = self.get_glob_best()
        prev_glob_best_val = self.glob_best_val
        self.glob_best_pos = np.asarray([p for p in self.glob_best_pos])
        if (self.no_change_stop <= 0) or (self.max_iter <= 0):
            if self.return_top is None or (self.return_top == 1):
                return self.glob_best_pos.astype(np.int64), self.glob_best_val
            else:
                return [(indiv.pers_best_pos.astype(np.int64), indiv.pers_best_val) for indiv in self.get_top_k()]
        condition_true = True
        while condition_true:
            self.update_all()
            self.iter_count += 1
            if isinstance(self.max_time, float) or isinstance(self.max_time, int):
                condition_true = time.perf_counter() - self.begin_time < self.max_time
            if condition_true:
                condition_true = self.no_change < self.no_change_stop and self.iter_count < self.max_iter
            if prev_glob_best_val == self.glob_best_val:
                self.no_change += 1
        if (self.return_top is None) or (self.return_top == 1):
            return self.glob_best_pos.astype(np.int64), self.glob_best_val
        else:
            return [(indiv.pers_best_pos.astype(np.int64), indiv.pers_best_val) for indiv in self.get_top_k()]

    def get_glob_best(self):
        """
        Find the best position ever visited by any particle in the entire swarm

        Returns (tuple) := (numpy.ndarray, float):
            (position, fitness)
        """
        glob_best_pos = self.pop[0].pers_best_pos
        glob_best_val = self.pop[0].pers_best_val
        for idx, particle in enumerate(self.pop[1:]):
            if particle.pers_best_val > glob_best_val:
                glob_best_val = particle.pers_best_val
                glob_best_pos = particle.pers_best_pos
        return copy.deepcopy(glob_best_pos), glob_best_val

    def get_top_k(self):
        """
        Get best self.return_top particles with highest personal best values

         Returns (list<individual>):
            list of self.return_top best particles
        """
        sorted_pop = sorted(self.pop,key=lambda x: x.pers_best_val, reverse=True)
        return sorted_pop[:self.return_top]

    def get_nbr_bounds(self, idx):
        """
        Get indexed bounds of neighbourhood for particle at index idx. This is not entirely trivial since
        the population wraps around in a ring-like fashion, i.e., particle at last index is next to particle at first
        index

        Args:
            idx (int): index of particle for which we must find neighbourhood bounds
        Returns (tuple) := (int, int):
            (begin index, end index)
        """
        if idx < self.nbr_rad:
            begin = idx - self.nbr_rad + self.pop_size
        else:
            begin = idx - self.nbr_rad

        if idx > len(self.pop) - 1 - self.nbr_rad:
            end = idx - len(self.pop) + self.nbr_rad
        else:
            end = idx + self.nbr_rad

        return begin, end

    def get_best_nbr(self, indiv_idx):
        """
        Get the best neighbour out of the particle at indiv_idx's neighbourhood. This is done in an optimised fashion,
        i.e. the fact that neighbourhoods have considerable overlap is exploited here. Note that the best "neighbour"
        might actually be this particle itself.

        Args:
            indiv_idx (int): index of individual for which we must find its best neighbour

        Returns:
            None
        """
        begin, end = self.get_nbr_bounds(indiv_idx)

        if indiv_idx == 0:
            whole_search = True
        else:
            if self.pop[indiv_idx - 1].best_nbr_idx == self.pop[indiv_idx - 1].left_border:
                whole_search = True
            else:
                whole_search = False
        if whole_search:
            best_nbr_pos = self.pop[end].pers_best_pos
            best_nbr_val = self.pop[end].pers_best_val
            best_nbr_idx = end

            if begin > end:
                for idx in range(begin, self.pop_size):
                    if self.pop[idx].pers_best_val > best_nbr_val:
                        best_nbr_pos = self.pop[idx].pers_best_pos
                        best_nbr_val = self.pop[idx].pers_best_val
                        best_nbr_idx = idx
                for idx in range(end + 1):
                    if self.pop[idx].pers_best_val > best_nbr_val:
                        best_nbr_pos = self.pop[idx].pers_best_pos
                        best_nbr_val = self.pop[idx].pers_best_val
                        best_nbr_idx = idx
            else:
                for idx in range(begin, end):
                    if self.pop[idx].pers_best_val > best_nbr_val:
                        best_nbr_pos = self.pop[idx].pers_best_pos
                        best_nbr_val = self.pop[idx].pers_best_val
                        best_nbr_idx = idx
            return best_nbr_pos, best_nbr_val, best_nbr_idx
        else:
            if self.pop[self.pop[indiv_idx - 1].best_nbr_idx].pers_best_val >\
               self.pop[self.pop[indiv_idx].right_border].pers_best_val:
                return self.pop[self.pop[indiv_idx - 1].best_nbr_idx].pers_best_pos,\
                       self.pop[self.pop[indiv_idx - 1].best_nbr_idx].pers_best_val,\
                       self.pop[indiv_idx - 1].best_nbr_idx
            else:
                return self.pop[self.pop[indiv_idx].right_border].pers_best_pos,\
                       self.pop[self.pop[indiv_idx].right_border].pers_best_val,\
                       self.pop[indiv_idx].right_border


    def evaluate(self, indiv_idx):
        indiv = self.pop[indiv_idx]
        total = 0.0
        ineq_count = 0
        for pos_idx in range(1, len(indiv.pos), 2):
            total += self.data.reduced[int(np.round(indiv.pos[pos_idx]))].val - self.data.reduced[int(np.round(indiv.pos[pos_idx - 1]))].val
        trans_cost = 0.0
        if self.trans_cost is not None:
            for pos_idx in range(1, len(indiv.pos), 2):
                trans_cost += self.trans_cost*(self.data.reduced[int(np.round(indiv.pos[pos_idx]))].val
                                               + self.data.reduced[int(np.round(indiv.pos[pos_idx - 1]))].val)
        indiv.val = self.search_up*total
        indiv.val -= trans_cost
        if (indiv.val > indiv.pers_best_val):
            indiv.pers_best_val = indiv.val
            indiv.pers_best_pos = copy.deepcopy(indiv.pos)

    def set_pop_size(self, pop_size):
        self.pop_size = pop_size

    def get_pop_size(self):
        return self.pop_size


class PSORefined(PSO):
    """
    Class structure for PSO-SGA, as described in the thesis. This algorithm first does a preliminary optimisation via
    PSO, then these "optimised" points are used as input to the SGA method, from which we get the final solution.

    For the following parameters, please refer to the PSO class: dim, pop_size, nbr_rad, cog_scale_info,
        soc_scale_info, inertia, max_time, mutate, trans_cost, return_top, no_change_stop, max_iter, long, from_hierarch,
        nbr_rad_rate

    Args:
        nlg_pop_size (int): population size for the SGA method, when the second optimisation step is done
    """
    def __init__(self, nlg_pop_size, dim, pop_size, nbr_rad, cog_scale_info, soc_scale_info,
                inertia, max_time, mutate, trans_cost, return_top, no_change_stop, max_iter, long=False,
                from_hierarch=False, nbr_rad_rate=None, *args):
        self.ident = "PSO Refined"
        self.nlg_pop_size = max(0, int(np.round(nlg_pop_size)))
        self.pso_obj = PSO(dim=dim, pop_size=pop_size, nbr_rad=nbr_rad, cog_scale_info=cog_scale_info,
                           soc_scale_info=soc_scale_info, inertia=inertia, max_time=max_time, mutate=mutate,
                           trans_cost=trans_cost, no_change_stop_ratio=no_change_stop, max_iter=max_iter, return_top=return_top,
                           from_hierarch=from_hierarch, nbr_rad_rate=nbr_rad_rate, long=long, no_change_stop=10, *args)
        ov.Optim.__init__(self, dim, long, trans_cost, from_hierarch)
        self.pop_size = self.pso_obj.pop_size
        self.nbr_rad = self.pso_obj.nbr_rad
        self.cog_scale_info = self.pso_obj.cog_scale_info
        self.soc_scale_info = self.pso_obj.soc_scale_info
        self.inertia = self.pso_obj.inertia
        self.max_time = self.pso_obj.max_time
        self.mutate = self.pso_obj.mutate
        self.no_change_stop = self.pso_obj.no_change_stop
        self.max_iter = self.pso_obj.max_iter
        self.nbr_rad_rate = self.pso_obj.nbr_rad_rate
        self.return_top = self.pso_obj.return_top
        self.no_change_stop = max(1, self.no_change_stop)
        self.max_iter = max(1, self.max_iter)

    def __str__(self):
        return "PSO Refined"

    def get_params(self):
        return {"pop_size": self.pop_size, "nbr_rad": self.nbr_rad, "inertia": self.inertia, "max_iter": self.max_iter,
                "no_change_stop": self.no_change_stop, "nlg_pop_size": self.nlg_pop_size, "return_top": self.return_top}

    def init_pop(self, new_dim=None):
        if new_dim is not None:
            self.dim = new_dim
        self.pso_obj.init_pop(new_dim=new_dim)

    def set_data(self, data):
        super().set_data(data)
        self.pso_obj.set_data(data)

    def _optimise(self, **kwargs):
        best_list = self.pso_obj.optimise()
        self.iter_count = self.pso_obj.iter_count
        if not isinstance(best_list, list):
            best_list = [best_list]
        if self.nlg_pop_size <= 0:
            return best_list[0]
        highest_val = -float("inf")
        highest_pos = None
        self.raw_pso_fitness = best_list[0][1]
        for pos, val in best_list:
            if not (sorted(pos) == list(pos)):
                print ("Position vector unsorted before going to refinement")
            nlg_inst = nlg.SGA(init_pos=pos, pop_size=self.nlg_pop_size, long=self.long, trans_cost=self.trans_cost)
            nlg_inst.set_data(self.data)
            nlg_inst.init_pop()
            new_pos, new_val = nlg_inst.optimise()
            if not (sorted(new_pos) == list(new_pos)):
                print ("Position vector unsorted after refinement")
                print (new_pos)
            if new_val > highest_val:
                highest_val = new_val
                highest_pos = new_pos
        return highest_pos, highest_val


def main():
    cog_scale_info = LinearScale(min_val=0.1, max_val=0.9, begin_scale=0.9, incr=-0.001)
    soc_scale_info = LinearScale(min_val=0.1, max_val=0.9, begin_scale=0.1, incr=0.001)
    series_obj = series.Series(series_len=5000, seed=300)
    begin_time = time.perf_counter()
    pso_ref_obj = PSORefined(nlg_pop_size=1, dim=20, pop_size=50, nbr_rad=10, cog_scale_info=cog_scale_info,
                              soc_scale_info=soc_scale_info, inertia=0.9, max_time=2, mutate=False, trans_cost=0.0,
                              no_change_stop=100000000000.0, max_iter=1000000000, long=True, from_hierarch=False, return_top=10)
    pso_ref_obj.set_data(series_obj)
    pso_ref_obj.init_pop()
    pos, fitness = pso_ref_obj.optimise()
    print ("Time: ", time.perf_counter() - begin_time)
    ud.plot_solution(series_obj, pos)

if __name__ == "__main__":
    main()