import logging
import multiprocessing as mp
import numpy as np
import Queue
import atexit
import random
from multiprocessing import Pool
from PIL import Image

import mxnet as mx


class ImageFolder(mx.io.DataIter):
    '''
    To read  

    Example:
        root/dog/xx01.jpg
        root/dog/xx02.jpg

        root/cat/xx01.jpg
        root/cat/xx02.jpg
    '''

    def __init__(self):
        pass


class SampleLoader(mx.io.DataIter):
    """
        In mxnet, 5 functions below is necessary for implementing a DataLoader
    """

    def __init__(self):
        """
            set all required variables ready, see implementation below for more details 
        """
        raise NotImplementedError('you must override __init__() yourself')

    def next(self):
        """
        :return:
            mx.io.DataBatch(data = [data], label = [label]) 
                detailed explaination later        
        :raises:
            StopIteration: 
                if data loader reachs epoch end
        """
        raise NotImplementedError('you must override next() you self')

    @property
    def provide_data(self):
        """
        :return:
            [mx.io.DataDesc(), ... ]
                A list of mx.io.DataDesc, which describes all data input blocks in network  
        """
        raise NotImplementedError('you must override provide_data() yourself')

    @property
    def provide_label(self):
        """
        :return:
            [mx.io.DataDesc(), ... ]
                A list of mx.io.DataDesc, which describes all label input blocks in network  
        """
        raise NotImplementedError('you must override provide_label() yourself')

    def reset(self):
        """
        reset variables related to iterations, such as current_index, shuffle, etc
        """
        raise NotImplementedError('you must override reset() yourself')


class DataLoader(mx.io.DataIter):
    """
        In mxnet, 5 functions below is necessary for implementing a DataLoader
    """

    def __init__(self, dataset, feedin_shape, read_threads=1, ):
        """
            set all required variables ready, see implementation below for more details 
        """
        super(DataLoader, self).__init__()

        self.dataset = dataset

        # shape related variables
        self.data_shapes = self.dataset.data_shapes
        self.label_shapes = self.dataset.label_shapes
        self.batch_size = self.dataset.batch_size

        # self.batch_size = 32
        # self.data_shapes = [mx.io.DataDesc(name='data', shape=(32, 13, 128, 128), layout='NCHW')]
        # self.label_shapes = [mx.io.DataDesc(name='softmax_label', shape=(32,), layout='N')]

        # self.loader_list = []  # TODO: add a function interface
        self.current = 0
        self.total = len(self.dataset)
        self.random_shuffle = False

        # multi thread acceleration
        self.read_threads = read_threads
        if self.read_threads > 1:
            self.pool = Pool(self.read_threads)  # TODO: add pin memory to optimize speed
        # raise NotImplementedError('you must override __init__() you self')

    def next(self):
        """
        :return:
            mx.io.DataBatch(data = [data], label = [label]) 
                detailed explanation later        
        :raises:
            StopIteration: 
                if data loader reaches epoch end
        """
        if self.current + self.batch_size > self.total:
            raise StopIteration  # reach epoch end
        else:
            return self.get_batch()

    def load_batch(self):
        # make it static, unreachable from outside
        index_list = range(self.current, self.current + self.batch_size)

        if self.read_threads > 1:
            batch = self.pool.map(self.__getitem__, index_list)
        else:
            batch = []
            for ind in index_list:
                batch.append(self.__getitem__(ind))
        return batch

    def get_batch(self):
        batch = self.load_batch()
        # TODO: make batch here

        return

    def get_single_pair(self, index):
        # TODO: will be removed. Replace it by __getitem__
        return self.__getitem__(index)

    def __getitem__(self, index):
        """
        :param index(int): Index
        :return: 
            tuple: (data, label) where data and label are collections 
        """
        return self.dataset[index]

    @staticmethod
    def pil_loader(path):
        # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                return img.convert('RGB')

    @property
    def provide_data(self):
        """
        :return:
            [mx.io.DataDesc(), ... ]
                A list of mx.io.DataDesc, which describes all data input blocks in network  
        """
        return self.data_shapes
        # raise NotImplementedError('you must override provide_data() ')

    @property
    def provide_label(self):
        """
        :return:
            [mx.io.DataDesc(), ... ]
                A list of mx.io.DataDesc, which describes all label input blocks in network  
        """
        return self.label_shapes
        # raise NotImplementedError('you must override provide_label() ')

    def reset(self):
        """
        reset variables related to iterations, such as current_index, shuffle, etc
        """
        self.current = 0
        # TODO: implement shuffle later
        # if self.random_shuffle:
        #     random.shuffle(self.loader_list)

    def __len__(self):
        return len(self.loader_list)
