from pylab import *


class Plotter:

    def __init__(self, factors_list=list(), common_name=''):
        '''
        :param factors_list: list of Factor objects
        '''
        self.factors_list = factors_list
        self.common_name = common_name

    def plot_all(self):
        for factor in self.factors_list:
            self._plot_factor_if_notnone(factor)

    def add_factor(self, newfactor):
        self.factors_list.append(newfactor)

    def remove_factor(self, factor):
        self.factors_list.remove(factor)

    def _plot_factor_if_notnone(self, factor):
        '''
        :param factor: Factor object
        '''
        if not factor:
            return
        t11 = list(map(lambda e: e[0], factor.vals))
        t12 = list(map(lambda e: e[1], factor.vals))

        plt.bar(range(len(t12)), t12, align='center')
        plt.xticks(range(len(t12)), t11, size='small')
        plt.suptitle(factor.name + '\n' + self.common_name, fontsize=20)
        plt.show()
        pass


class Factor:

    def __init__(self, vals, name='unnamed'):
        '''
        :param vals: list of tuples (x_val, y_val)
        :param name: name for the factor
        '''
        self.vals = vals
        self.name = name