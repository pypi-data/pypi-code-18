"""
__author__ = Hagai Hargil
"""

import attr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List
from numba import jit, float64, uint64, int64
from collections import OrderedDict
import warnings


@attr.s
class Movie(object):
    """
    A holder for Volume objects to be displayed consecutively.
    """
    data     = attr.ib()
    reprate  = attr.ib(validator=attr.validators.instance_of(float))
    x_pixels = attr.ib(validator=attr.validators.instance_of(int))
    y_pixels = attr.ib(validator=attr.validators.instance_of(int))
    z_pixels = attr.ib(validator=attr.validators.instance_of(int))
    name     = attr.ib(validator=attr.validators.instance_of(str))
    binwidth = attr.ib(validator=attr.validators.instance_of(float))
    big_tiff = attr.ib(default=True)
    bidir    = attr.ib(default=True)

    @property
    def list_of_volume_times(self) -> List:
        """ All volumes start-times in the movie. """

        volume_times = np.unique(self.data.index.get_level_values('Frames'))
        if len(volume_times) > 1:
            diff_between_frames = np.mean(np.diff(volume_times))
        else:
            diff_between_frames = self.data['time_rel_frames'].max()

        volume_times = list(volume_times)
        volume_times.append(volume_times[-1] + diff_between_frames)
        return volume_times

    def gen_of_volumes(self):
        """ Populate the deque containing the volumes as a generator. """

        list_of_frames = self.list_of_volume_times
        for idx, current_time in enumerate(list_of_frames[:-1]):  # populate deque with frames
            cur_data = self.data.xs(current_time, level='Frames')
            if not cur_data.empty:
                yield Volume(data=cur_data, x_pixels=self.x_pixels,
                             y_pixels=self.y_pixels, z_pixels=self.z_pixels, number=idx,
                             reprate=self.reprate, binwidth=self.binwidth, empty=False,
                             end_time=(list_of_frames[idx + 1] - list_of_frames[idx]),
                             bidir=self.bidir)
            else:
                yield Volume(data=cur_data, x_pixels=self.x_pixels,
                             y_pixels=self.y_pixels, z_pixels=self.z_pixels, number=idx,
                             reprate=self.reprate, binwidth=self.binwidth, empty=True,
                             end_time=(list_of_frames[idx + 1] - list_of_frames[idx]),
                             bidir=self.bidir)

    def create_tif(self):
        """ Create all volumes, one-by-one, and save them as tiff. """

        from tifffile import TiffWriter
        from collections import namedtuple

        # Create a list containing the frames before showing them
        VolTuple = namedtuple('Volume', ('hist', 'edges'))
        data_of_vol = VolTuple
        volumes_in_movie = self.gen_of_volumes()
        try:
            cur_vol = next(volumes_in_movie)
            data_of_vol.hist, data_of_vol.edges = cur_vol.create_hist()
        except StopIteration:
            raise UserWarning('No frames were generated.')

        try:
            with TiffWriter('{}.tif'.format(self.name[:-4]), bigtiff=self.big_tiff,
                            imagej=True) as tif:
                while True:
                    tif.save(data_of_vol.hist.astype(np.uint16))
                    try:
                        cur_vol = next(volumes_in_movie)
                        data_of_vol.hist, data_of_vol.edges = cur_vol.create_hist()
                    except StopIteration:
                        break
        except:
            warnings.warn("Permission Error: Not allowed to save file to original directory.")

    def create_array(self):
        """ Create all volumes, one-by-one, and return the array of data that holds them. """
        from collections import namedtuple, deque

        # Create a deque and a namedtuple for the frames before showing them
        VolTuple = namedtuple('Volume', ('hist', 'edges'))
        data_of_vol = VolTuple
        deque_of_vols = deque()
        volumes_in_movie = self.gen_of_volumes()

        try:
            cur_vol = next(volumes_in_movie)
        except StopIteration:
            raise ValueError('No volumes generated.')

        while True:
            data_of_vol.hist, data_of_vol.edges = cur_vol.create_hist()
            deque_of_vols.append(data_of_vol)
            try:
                cur_vol = next(volumes_in_movie)
            except StopIteration:
                break

        assert len(deque_of_vols) == len(self.list_of_volume_times) - 1
        return deque_of_vols

    def create_single_volume(self, vols) -> np.array:
        """ Aggregate the frames\volumes that vols mark to a single frame\volume.
        :vols Volumes to aggregate. 'all' is all of them.
        :return np.array of histogram
        """

        deque_of_vols = self.create_array()

        if vols == 'all':
            summed = np.zeros_like(deque_of_vols[0].hist, dtype=np.int32)
            for vol in deque_of_vols:
                summed += vol.hist
            return summed

        if isinstance(vols, int):
            return deque_of_vols[vols]

        try:
            summed = np.array([0], dtype=np.int32)
            for idx in vols:
                summed += deque_of_vols[vols[idx]]
        except TypeError:
            raise TypeError('vols parameter should be "all", integer or list of volumes.')


@attr.s(slots=True)
class Volume(object):
    """
    A Movie() is a sequence of volumes. Each volume contains frames in a plane.
    """

    x_pixels = attr.ib()
    y_pixels = attr.ib()
    z_pixels = attr.ib()
    number   = attr.ib(validator=attr.validators.instance_of(int))  # the volume's ordinal number
    data     = attr.ib()
    reprate  = attr.ib()  # laser repetition rate, relevant for FLIM
    end_time = attr.ib()
    binwidth = attr.ib()
    bidir    = attr.ib()  # Bi-derictional scanning
    empty    = attr.ib(default=False, validator=attr.validators.instance_of(bool))

    @property
    def __metadata(self) -> OrderedDict:
        """
        Creates the metadata of the volume to be created, to be used for creating the actual images
        using histograms. Metadata can include the first photon arrival time, start and end of volume, etc.
        :return: Dictionary of all needed metadata.
        """

        metadata = OrderedDict()
        jitter = 0.02  # 2% of jitter of the signals that creates volumes

        # Volume metadata
        volume_start = 0
        volume_end = self.end_time
        metadata['Volume'] = Struct(start=volume_start, end=volume_end, num=self.x_pixels + 1)

        # y-axis metadata
        y_start, y_end, self.empty = metadata_ydata(data=self.data, jitter=jitter)
        metadata['Y'] = Struct(start=y_start, end=y_end, num=self.y_pixels + 1)

        # z-axis metadata
        if 'Phase' in self.data.columns:
            z_start = -1
            z_end = 1
            metadata['Z'] = Struct(start=z_start, end=z_end, num=self.z_pixels + 1)

        # Laser pulses metadata
        if 'time_rel_pulse' in self.data.columns:
            try:
                laser_start = 0
                laser_end = np.ceil(1 / (self.reprate * self.binwidth)).astype(int)
                metadata['Laser'] = Struct(start=laser_start, end=laser_end, num=laser_end + 1)
            except ZeroDivisionError:
                laser_start = 0
                warnings.warn('No laser reprate provided. Assuming 80 MHz.')
                laser_end = np.ceil(1 / (80e6 * self.binwidth)).astype(int)
                metadata['Laser'] = Struct(start=laser_start, end=laser_end, num=laser_end + 1)

        return metadata

    def __create_hist_edges(self):
        """
        Create three vectors that will create the grid of the frame. Uses Numba internal function for optimization.
        :return: Tuple of np.array
        """
        metadata = self.__metadata
        list_of_edges = []

        if self.empty is not True:
            for num_of_dims, key in enumerate(metadata, 1):
                list_of_edges.append(create_linspace(start=metadata[key].start,
                                                     stop=metadata[key].end,
                                                     num=metadata[key].num))

            return list_of_edges, num_of_dims
        else:
            return list(np.ones(len(metadata)))

    def create_hist(self):
        """
        Create the histogram of data using calculated edges.
        :return: np.ndarray of shape [num_of_cols, num_of_rows] with the histogram data, and edges
        """

        list_of_data_columns = []

        if not self.empty:
            list_of_edges, num_of_dims = self.__create_hist_edges()
            list_of_data_columns.append(self.data['time_rel_frames'].values)
            list_of_data_columns.append(self.data['time_rel_line'].values)
            try:
                list_of_data_columns.append(self.data['Phase'].values)
            except KeyError:
                pass
            try:
                list_of_data_columns.append(self.data['time_rel_pulse'].values)
            except KeyError:
                pass

            data_to_be_hist = np.reshape(list_of_data_columns, (num_of_dims, self.data.shape[0])).T

            assert data_to_be_hist.shape[0] == self.data.shape[0]
            assert len(list_of_data_columns) == data_to_be_hist.shape[1]

            hist, edges = np.histogramdd(sample=data_to_be_hist, bins=list_of_edges)
            return hist.astype(np.int32), edges
        else:
            return np.zeros((self.x_pixels, self.y_pixels, self.z_pixels), dtype=np.int32), 0, 0, 0

    def show(self):
        """ Show the Volume. Mainly for debugging purposes, as the Movie object doesn't use it. """

        hist, edges = self.create_hist()
        plt.figure()
        # plt.imshow(hist, cmap='gray')
        plt.title('Volume number {}'.format(self.number))
        plt.axis('off')


def validate_number_larger_than_zero(instance, attribute, value: int=0):
    """
    Validator for attrs module - makes sure line numbers and row numbers are larger than 0.
    """

    if value >= instance.attribute:
        raise ValueError("{} has to be larger than 0.".format(attribute))


@jit((float64[:](int64, uint64, uint64)), nopython=True, cache=True)
def create_linspace(start, stop, num):
    linspaces = np.linspace(start, stop, num)
    assert np.all(np.diff(linspaces) > 0)
    return linspaces


def metadata_ydata(data: pd.DataFrame, jitter: float=0.02):
    """
    Create the metadata for the y-axis.
    """
    lines_start = 0
    empty = False

    unique_indices = np.unique(data.index.get_level_values('Lines'))
    if unique_indices.shape[0] > 1:  # TODO: Doesn't make sense that there's a single line in a frame
        diffs = np.diff(unique_indices)
        diffs_max = diffs.max()
    else:
        diffs = unique_indices
        diffs_max = unique_indices

    try:
        if diffs_max > ((1 + 4 * jitter) * np.mean(diffs)):  # Noisy data
            lines_end = np.mean(diffs) * (1 + jitter)
        else:
            lines_end = int(diffs_max)
    except ValueError:
        lines_end = 0
        empty = True

    return lines_start, lines_end, empty


@attr.s
class Struct(object):
    """ Basic struct-like object for data keeping. """

    start = attr.ib()
    end = attr.ib()
    num = attr.ib(default=None)
