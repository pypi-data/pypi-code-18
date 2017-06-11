__author__ = 'User'

import matplotlib.pyplot as plt
from numpy import mean, std, asarray
import time
import numpy as np
import copy

def same_sign(x, y):
    if (x*y > 0):
        return True
    if (x*y == 0):
        # this is so that the leftmost point in a flat area will be the only remaining point
        if not(x == 0):
            return True
        else:
            return False
    return False

def same_sign_check_wrongs(x, y):
    if (x*y > 0):
        return False
    else:
        return True

class Point:
    """
    Defines a single point in a time series on which all optimisation algorithms are applied.

    Attributes:
        idx (int): the index in the time series where the point occurs (the x-axis value)
        val (float): the actual value of the observation (the y-axis value)
    """
    __slots__ = ['idx', 'val']
    def __init__(self, idx, val):
        self.idx = idx
        self.val = val

    def __str__(self):
        return "(", self.idx, ", ", self.val, ")"

    def print_point(self):
        print(self.__str__(), end=" ")

    def __le__(self, other):
        return self.val <= other

    def __lt__(self, other):
        return self.val < other

    def __ge__(self, other):
        return self.val >= other

    def __gt__(self, other):
        return self.val > other


def _random_series(length, seed=None, **kwargs):
    if seed is not None:
        np.random.seed(seed)
    noise = np.random.normal(size=length)
    np.random.seed()
    return np.cumsum(noise)

def _make_points_help(rand_series):
    pts = []
    for idx, val in enumerate(rand_series):
        pts.append(Point(idx, val))
    return pts

def _make_points(process=_random_series, **kwargs):
    return _make_points_help(process(**kwargs))


class Series:
    """
    Class implementation for a series object, used with all implementations of optimisation algorithms in the thesis.

    The Series object consists of a series of Point objects. The point object contains an original index and a y-value
     for the point. This is helpful when reducing the series to only peaks/troughs.
    Various other utility methods are also included in this class, such as methods to scale and shift the time series,
     trainsform it to an exponential time series, find all peaks and troughs, etc.

    Args:
        series      (list<Point>): A list of Point objects from which we may construct a full Series object.
        other_ser   (Series): Another Series object from which we construct a copy. This is not really such a necessary
                            parameter, since one may as well just do copy.deepcopy on the other series object.
        series_len  (int): if this parameter is given, but the above two are not given, then a new series of length
                            series_len is randomly generated via the argument given in 'process'.
        long        (bool): if True, indicates a "long" series, i.e. a series that starts with a buy point and ends
                                with a sell point.
        seed        (int): numpy.random seed value for generating a new series
        process     (function): a function that generates a random series with a specified length. Other variables
                                    may also be given to the process function.
        descr       (str): A string describing the series
    """
    def __init__(self, series=None, other_ser=None, series_len=None, long=None, seed=None, process=_random_series,
                 descr=None):
        if series is not None:
            self.long = long
            self._delled_reduced = [None, None]
            self.orig = copy.deepcopy(series)
            self.orig_len = len(series)
            begin_time = time.time()
            self.get_extremes()
            self.begin_fixed = False
            if long is not None:
                self.fix_long_short(self.long)
            self.red_len = len(self.reduced)
        elif other_ser is not None:
            self.__dict__ = copy.deepcopy(other_ser.__dict__)
        elif series_len is not None:
            self.orig = _make_points(process=process, length=series_len, seed=seed)
            self.orig_len = series_len
            self._delled_reduced = [None, None]
            self.get_extremes()
            if long is not None:
                self.fix_long_short(self.long)
            self.red_len = len(self.reduced)
        else:
            raise TypeError("Series constructor call must have either: a list of points ('series'); "
                            "a different series ('other_ser'); or a desired length of a randomly generated "
                            "series ('series_len')")
        if descr is None:
            self.descr = "Series"
        else:
            self.descr = descr

    @staticmethod
    def find_pt_with_idx(pt_series, idx):
        for pt_idx, pt in enumerate(pt_series):
            if pt.idx == idx:
                return pt_idx
        return -1


    def make_exp(self):
        """
        Transform all y-axis values, so that new y-axis values are equal to e^(y). This is the inverse of make_log

        Returns:
            None
        """
        for idx in range(len(self.orig)):
            self.orig[idx].val = np.exp(self.orig[idx].val)

    def make_log(self):
        """
        Transform all y-axis values, so that new y-axis values are equal to log(y). This is the inverse of make_exp.

        Returns:
            None
        """
        for idx in range(len(self.orig)):
            self.orig[idx].val = np.log(self.orig[idx].val)

    def copy_subset(self, idx_start, idx_end, reduced=True):
        """
        Returns a copy of the current series from idx_start to idx_end. These may be the reduced indexes or the indexes
        of the full-length time series

        Args:
            idx_start (int): starting_index
            idx_end   (int): ending_index
            reduced   (bool): if True, idx_start and idx_end are based on indexes in reduced series, if False, indexes
                                are based on full time series
        Returns (Series):
            reduced time series
        """
        if reduced:
            return self._reduced_copy_subset(idx_start, idx_end - 1)
        else:
            pts_list = self.orig[idx_start:idx_end]
            return Series(pts_list)

    def _reduced_copy_subset(self, idx_start, idx_end):
        orig_start_idx = self.find_pt_with_idx(self.orig, self.reduced[idx_start].idx)
        orig_end_idx = self.find_pt_with_idx(self.orig, self.reduced[idx_end].idx)
        pts_list = self.orig[orig_start_idx:orig_end_idx]
        return Series(pts_list)

    def begin_is_long(self):
        """
        Check if first peak/trough is a trough or not

        Returns (bool):
            Return True if first peak/trough is a trough, False otherwise
        """
        return bool(self.reduced[0].val < self.reduced[1].val)

    def end_is_long(self):
        """
        Check if last peak/trough is a peak or not

        Returns (bool):
            Return True if last peak/trough is a peak, False otherwise
        """
        return bool(self.reduced[-1].val > self.reduced[-2].val)

    def fix_long_short(self, long):
        """
        'Fixes' the time series into either a 'long' or 'short' time series

        Args:
            long (bool): if True, time series will have as its first peak/trough, a trough, and its last peak/trough
                            as a peak. Vice versa for False.

        Returns:
            None
        """
        self.long = long
        if self.long is None:
            """
            when self.long = None, it means we want the reduced series in its original form,
            thus we restore any points from self._delled_reduced back into the self.reduced list
            """
            if self._delled_reduced[0] is not None:
                self.begin_fixed = False
                self.reduced.insert(0, self._delled_reduced[0])
                self._delled_reduced[0] = None
            if self._delled_reduced[1] is not None:
                self.begin_fixed = False
                self.reduced.append(self._delled_reduced[1])
                self._delled_reduced[1] = None
            return
        elif self.long:
            change_criteria_bgn = lambda: not self.begin_is_long()
            change_criteria_end = lambda: not self.end_is_long()
            self.begin_long, self.end_long = True, True
        elif not self.long:
            change_criteria_bgn = self.begin_is_long
            change_criteria_end = self.end_is_long
            self.begin_long, self.end_long = False, False
        else:
            return
        if change_criteria_bgn():
            if self._delled_reduced[0] is None:
                self.begin_fixed = True
                self._delled_reduced[0] = self.reduced[0]
                del self.reduced[0]
            else:
                self.begin_fixed = False
                self.reduced.insert(0, self._delled_reduced[0])
                self._delled_reduced[0] = None
        if change_criteria_end():
            if self._delled_reduced[1] is None:
                self._delled_reduced[1] = self.reduced[-1]
                del self.reduced[-1]
            else:
                self.reduced.append(self._delled_reduced[1])
                self._delled_reduced[1] = None

    def calc_volatility(self, abs, lag, reduced):
        """
        Calculate volatility for the time series. This is equivalent to either the standard deviation of the differences
        between observations that are a specified lag apart, or the standard deviation of returns between observations
        a specified lag apart

        Args:
            abs     (bool): if True, take differences between observations, if False, take returns between observations
            lag     (int): the amount of observations that successive points are apart in the calculation
            reduced (bool): if True, calculate for the reduced series, if False, for the full series
        Returns (float):
            the calculated volatility
        """
        if reduced:
            series_obj = self.reduced
        else:
            series_obj = self.orig

        if abs:
            self.abs_diff = [series_obj[idx + lag].val - series_obj[idx].val for idx in range(len(series_obj) - lag)]
            self.abs_vol = std(self.abs_diff)
            return self.abs_vol
        else:
            self.return_diff = [series_obj[idx + lag].val/series_obj[idx].val - 1 for idx in range(len(series_obj) - lag)]
            self.return_vol = std(self.return_diff)
            return self.return_vol

    def get_proportion(self, proportion):
        """
        Get a proportion of the current time series, starting from the beginning of the current time series

        Args:
            proportion (float): the proportion of the time series that we wish to get

        Returns (Series):
            new time series which has its size based on the specified proportion of the current time series
        """
        if proportion > 1:
            proportion = 1
        if proportion < 0:
            proportion = 0
        new_series = Series(self.orig[:int(self.orig_len * proportion)])
        return new_series

    def get_extremes_sub(self, ser):
        """
        Helper function for the get_extremes function
        """
        new_list = [ser[0]]
        for i in range(1, len(ser) - 1):
            if (same_sign(ser[i].val - ser[i-1].val, ser[i].val - ser[i+1].val)):
                new_list.append(ser[i])
        new_list.append(ser[-1])
        return new_list

    def get_extremes(self):
        """
        Finds all peaks and troughs in current time series. Due to certain 'flat' areas on the series, this function
        may have to be run more than once to find all true peaks and troughs

        Returns:
            None
        """
        self.reduced = self.get_extremes_sub(self.orig)

    def print_orig_series(self):
        for pt in self.orig:
            print (pt)

    def get_min(self):
        min_idx = 0
        min_pt = self.reduced[min_idx]
        for i in range(len(self.reduced)):
            if self.reduced[i].val < min_pt.val:
                min_idx = i
                min_pt = self.reduced[min_idx]
        return min_idx

    def get_max(self):
        max_idx = 0
        max_pt = self.reduced[max_idx]
        for i in range(len(self.reduced)):
            if self.reduced[i].val > max_pt.val:
                max_idx = i
                max_pt = self.reduced[max_idx]
        return max_idx

    def plot_reduced(self, show=True):
        x_vals = []
        y_vals = []
        for i in range(len(self.reduced)):
            x_vals.append(self.reduced[i].idx)
            y_vals.append(self.reduced[i].val)

        plt.plot(x_vals, y_vals)
        if show:
            plt.show()

    def plot_orig(self):
        x_vals = []
        y_vals = []
        for i in range(len(self.orig)):
            x_vals.append(self.orig[i].idx)
            y_vals.append(self.orig[i].val)

        plt.plot(x_vals, y_vals)
        plt.show()

    def shift(self, val):
        new_pts = [Point(pt.idx, pt.val + val) for pt in self.orig]
        return Series(new_pts)

    def scale(self, val):
        new_pts = [Point(pt.idx, pt.val*val) for pt in self.orig]
        return Series(new_pts)

if __name__ == "__main__":
    def is_equal(series1, series2):
        for pt1, pt2 in zip(series1.reduced, series2.reduced):
            if not ((pt1.val == pt2.val) and (pt1.idx == pt2.idx)):
                return False
        return True

    my_series = Series(series_len=5000)
    my_series.plot_orig()

