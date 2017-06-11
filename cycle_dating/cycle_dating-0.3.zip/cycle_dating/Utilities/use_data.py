import random
import os

import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as plt_cols
import numpy as np

from cycle_dating.Utilities import series as ser

class BSPointDuplicateError(Exception):
    def __str__(self):
        return "Duplicates found in position vector"


def plot_data(series, show = True, zorder=1):
    """
    Helper function for plot_solution
    """
    idx = []
    val = []
    for i in range(len(series)):
        idx.append(series[i].idx)
        val.append(series[i].val)

    plt.plot(idx, val, zorder=zorder)
    if (show):
        plt.show()


def plot_solution(dat_obj, points=None, label = None, title=None, show = True, scatter=False, highlight=None,
                  saveas=None, clear=False, show_orig=True, join_points=True, orig_points=None,
                  points_are_orig=False, fix_lims = True, scatter_size=30, linewidth=None):
    """
    Plot a given solution defined by 'points', on the series object 'dat_obj'. Various options are available for the
    type of plot demanded

    Args:
        dat_obj          (Series): the series on which the solution is defined
        points           (list<int>): the time series indices (either for the reduced or full time series) that define
                                        the solution
        label            (str): the label that will appear on the plot
        title            (str): the title that will appear on the plot
        show             (bool): if True, show plot immediately after plotting this solution, if False, do not show
                                    solution. This is sometimes useful if many solutions are to be plotted on the same
                                    axis.
        scatter          (bool): show the buy-sell points as dots, as on a scatter plot
        highlight        (list<list<int>>): contains two lists.  The first list indicates between which time series
                                            observations the areas must be highlighted in yellow.
                                            The second list is for indicating which buy-sell points,
                                            at what indices, must be highlighted in bright red (the others will be
                                            in a brownish color). The second list only has an effect if scatter=True.
        saveas           (str): provides a filepath where the plot must be saved. If None, do not save the plot.
        clear            (bool): if True, clear the plot when this function exits
        show_orig        (bool): if True, show the time series on which the solution is defined
        join_points      (bool): if True, join buy-sell points with lines
        orig_points      (list<int>): plots points at these indices from the original time series, as a new series
        points_are_orig: (bool): if True, indices in the 'points' variable define points on the original time series.
                                    if False, indices in the 'points' variable define point on the reduced time series.
        fix_lims         (bool): if True, fixes axes to either the limits of the original series, or if that is not
                                    plotted, fixes it to the limits of the buy-sell points series.
        scatter_size     (int): size of the dots representing buy-sell points. Only has an effect if scatter=True
        linewidth        (float): width of lines joining buy-sell points
        :param fix_lims:
        :param scatter_size:
        :param linewidth:
    :return:
    """
    if points is None:
        points = []
    xlim, ylim = None, None
    if show_orig:
        plot_data(dat_obj.orig, False, zorder=1)
        xlim = plt.xlim()
        ylim = plt.ylim()
    idx = []
    val = []
    x_vals = []
    y_vals = []
    if points_are_orig:
        for i in points:
            x_vals.append(dat_obj.orig[i].idx)
            y_vals.append(dat_obj.orig[i].val)
    else:
        for i in points:
            x_vals.append(dat_obj.reduced[i].idx)
            y_vals.append(dat_obj.reduced[i].val)
    if join_points:
        plt_obj = plt.plot(x_vals, y_vals, zorder=2, label=label)
        if linewidth is not None:
            plt.setp(plt_obj, linewidth=linewidth)
        if xlim is None and ylim is None:
            xlim, ylim = plt.xlim(), plt.ylim()
    if title is not None:
        plt.title(label)
    if label is not None:
        plt.legend(loc="best", prop={"size": 7})
    if scatter:
        if highlight is None or highlight[1] is None:
            plt.scatter(x_vals, y_vals, color='r', s=scatter_size, zorder=3)
        else:
            other_col = highlight[1]
            for count, plt_info in enumerate(zip(x_vals, y_vals)):
                x_v, y_v = plt_info
                if count not in other_col:
                    col = plt_cols.hex2color("#440000")
                else:
                    col = 'r'
                plt.scatter(x_v, y_v, color=col, s=scatter_size, zorder=3)
    if orig_points is not None:
        if join_points:
            for i in orig_points:
                idx.append(dat_obj.orig[i].idx)
                val.append(dat_obj.orig[i].val)
            plt_obj2 = plt.plot(idx, val, zorder=2, label=label)
            if linewidth is not None:
                plt.setp(plt_obj2, linewidth=linewidth)
            if xlim is None and ylim is None:
                xlim, ylim = plt.xlim(), plt.ylim()
        if scatter:
            if highlight is None or highlight[1] is None:
                plt.scatter([dat_obj.orig[p].idx for p in orig_points], [dat_obj.orig[p].val for p in orig_points], color='r', s=30)
            else:
                x_vals = [dat_obj.orig[p].idx for p in orig_points]
                y_vals = [dat_obj.orig[p].val for p in orig_points]
                other_col = highlight[1]
                for count, plt_info in enumerate(zip(x_vals, y_vals)):
                    x_v, y_v = plt_info
                    if count not in other_col:
                        col = plt_cols.hex2color("#440000")
                    else:
                        col = 'r'
                    plt.scatter(x_v, y_v, color=col, s=30, zorder=3)
    if highlight is not None:
        if highlight[0] is not None:
            for h_range in highlight[0]:
                if h_range[1] > h_range[0]:
                    plt.axvspan(h_range[0], h_range[1], color='y', alpha=0.5)
    if fix_lims:
        plt.xlim(xlim)
        plt.ylim(ylim)
    if saveas is not None:
        directory, filename = sep_filename_dir(saveas)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(saveas)
    if (show):
        plt.show()
    if clear:
        plt.clf()


def sep_filename_dir(filepath):
    reversed_filepath = filepath[::-1]
    split_idx = reversed_filepath.index("/")
    filename = (reversed_filepath[:split_idx])[::-1]
    directory = (reversed_filepath[split_idx:])[::-1]
    return directory, filename

def export_result(filepath, df, include_index=False):
    directory, filename = sep_filename_dir(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not (directory[-1] == "/"):
        directory += "/"
    df.to_csv(directory + filename, index=include_index)

def get_series_filename(filecode, folder="data"):
    if folder[-1] == "/":
        folder = folder[:-1]
    return folder + "/test_data" + filecode + ".csv"

def make_filepaths(filespecs):
    filepaths = []
    for spec in filespecs:
        yield ("results/PSO_Refined results " + str(spec)  +  ".csv")

def get_all_series(series_filecode, filespecs):
    all_series = []
    series_filename = get_series_filename(series_filecode)
    for filepath in make_filepaths(filespecs):
        df = pandas.read_csv(filepath)
        a_list = list(df[series_filename])
        all_series.append([eval(el)[0] for el in a_list])
    return all_series


def list_to_pts(series):
    new_ser = []
    for i in range(len(series)):
        new_ser.append(ser.Point(i, series[i]))
    return new_ser

def lists_to_pts(dates, values):
    pts = []
    for i, j in zip(dates, values):
        pts.append(ser.Point(i, j))
    return pts

def list_to_series(lst):
    return ser.Series(list_to_pts(lst))

def generate_series(size, stddev=1.0, mean=0.0, start_val=0, seed=None):
    if seed is not None:
        np.random.seed(seed)
    values = np.cumsum(np.random.normal(size=size, loc=mean, scale=stddev))
    values -= min(values) - start_val
    ser_vals = list_to_pts(values)
    return ser.Series(ser_vals)

def make_series_basic(filepath):
    """
    Generate a new Series object from the data in the file at filepath. No indices or dates are imported from this file,
    only the y-values. Indices ranging from 0 to length - 1 are automatically assigned to each observation.

    Args:
        filepath    (str): string describing the location of the file containing the time series data

    Returns (list<Series>):
        a list of series objects imported from the file
    """
    df = pandas.read_csv(filepath)
    all_series = []
    for series_name in df:
        series_list = list(df[series_name])
        dates = list(range(len(series_list)))
        pts = lists_to_pts(dates, series_list)
        all_series.append(ser.Series(pts, descr=series_name))
    return all_series


class GenerateProper:
    def __init__(self, parent_inst, pre_pos):
        self.parent_inst = parent_inst
        sort_temp = sorted(pre_pos)
        self.orig_pos = pre_pos
        if not (list(pre_pos) == sort_temp):
            print ("WARNING: position given to GenerateProper object not sorted")
        self.pre_pos = sort_temp
        self.long = self.parent_inst.long
        self.data = self.parent_inst.data
        if self.data.reduced[0].val < self.data.reduced[1].val:
            self.long_series = True
        else:
            self.long_series = False
        self.first_even = self.long == self.long_series

        self.eliminate_doubles()
        if self.has_doubles():
            print ("POSITION STILL HAS DOUBLES")
            for idx in range(1, len(self.pre_pos)):
                if self.pre_pos[idx] == self.pre_pos[idx - 1]:
                    print (self.pre_pos[max(0, idx - 5):min(len(self.pre_pos), idx + 5)])
            raise BSPointDuplicateError

    def get_open_positions(self):
        open_positions = []
        for idx in range(len(self.pre_pos)):
            if idx == 0:
                open_positions.append(list(range(self.pre_pos[idx])))
            else:
                open_positions.append(list(range(self.pre_pos[idx-1] + 1, self.pre_pos[idx])))
        open_positions.append(list(range(self.pre_pos[-1] + 1, len(self.data.reduced))))
        return open_positions

    def has_doubles(self):
        if len(set(self.pre_pos)) == len(self.pre_pos):
            return False
        else:
            return True

    def eliminate_doubles(self):
        open_positions = self.get_open_positions()
        for idx in range(1, len(self.pre_pos)):
            if self.pre_pos[idx] == self.pre_pos[idx - 1] + 2:
                if self.modify_valid_extrema(idx, self.pre_pos[idx]):
                    self.pre_pos[idx] -= 1
                else:
                    self.pre_pos[idx - 1] += 1
        for idx in list(range(1, len(self.pre_pos))):
            if self.pre_pos[idx] == self.pre_pos[idx - 1]:
                move_idxes = []
                moved = False
                for pos_list_idx in range(idx - 1, -1, -1):
                    move_idxes.append(pos_list_idx)
                    if len(open_positions[pos_list_idx]) > 1:
                        for mov_idx in move_idxes:
                            self.pre_pos[mov_idx] -= 2
                        del open_positions[pos_list_idx][-1]
                        del open_positions[pos_list_idx][-1]
                        open_positions[idx].append(0)
                        moved = True
                        break
                if not moved:
                    move_idxes = []
                    for pos_list_idx in range(idx + 1, len(open_positions)):
                        move_idxes.append(pos_list_idx - 1)
                        if len(open_positions[pos_list_idx]) > 1:
                            for mov_idx in move_idxes:
                                #print ("moving right", self.pre_pos[mov_idx], "for", self.pre_pos[idx])
                                self.pre_pos[mov_idx] += 2
                            del open_positions[pos_list_idx][0]
                            del open_positions[pos_list_idx][0]
                            #open_positions[idx].append(0)
                            open_positions[idx].append(0)
                            moved = True
                            #print ()
                            break
                if not moved:
                    print ("SERIES PROBABLY INVALID")
                    raise BSPointDuplicateError
        if self.has_doubles():
            print ("DOUBLES MISSED BY ELIMINATE DOUBLES FUNCTION")
            for idx in range(1, len(self.pre_pos)):
                if self.pre_pos[idx] == self.pre_pos[idx - 1]:
                    print (self.pre_pos[max(idx - 5, 0):min(len(self.pre_pos), idx + 5)])
                    print (self.orig_pos[max(idx - 5, 0):min(len(self.pre_pos), idx + 5)])
            raise BSPointDuplicateError
        self.pre_pos.sort()

    def modify_valid_extrema(self, count, position):
            if (count % 2 == 0):
                    return self.first_even == (position % 2 == 1)
            else:
                    return not (self.first_even == (position % 2 == 1))

    def shift_group(self, group):
        if len(group) == 0:
            return
        if self.pre_pos[group[0]] is not 0:
            for g_idx in group:
                self.pre_pos[g_idx] -= 1
        else:
            for g_idx in group:
                self.pre_pos[g_idx] += 1

    def shift_single(self, pos):
        if not (pos == 0) and not (pos == len(self.data.reduced) - 1):
            pos += random.sample([-1, 1], 1)[0]
        elif pos == 0:
            pos += 1
        else:
            pos -= 1
        return pos

    def fix_pre_exist_pos(self):
        mod_vals = []
        for idx, p in enumerate(self.pre_pos):
            if self.modify_valid_extrema(idx, p):
                mod_vals.append(idx)

        idx = 0
        group = []

        single_sort = 0
        group_sort = 0

        while idx < len(mod_vals):
            curr_pos = mod_vals[idx]
            if idx < len(mod_vals) - 1:
                if self.pre_pos[curr_pos] == self.pre_pos[mod_vals[idx + 1]] - 1:
                    group.append(curr_pos)
                elif len(group) > 0:
                    group.append(curr_pos)
                    self.shift_group(group)
                    group_sort += 1
                    group = []
                else:
                    self.pre_pos[curr_pos] = self.shift_single(self.pre_pos[curr_pos])
                    single_sort += 1
            elif idx == len(mod_vals) - 1:
                if len(group) > 0:
                    group.append(curr_pos)
                    self.shift_group(group)
                else:
                    self.pre_pos[curr_pos] = self.shift_single(self.pre_pos[curr_pos])
            idx += 1

        return self.pre_pos




if __name__ == "__main__":
    series_obj = generate_series(1100)
