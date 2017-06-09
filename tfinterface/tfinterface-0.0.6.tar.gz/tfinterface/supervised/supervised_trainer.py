#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x41328778

# Compiled with Coconut version 1.2.2 [Colonel]

# Coconut Header: --------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_compose, _coconut_pipe, _coconut_starpipe, _coconut_backpipe, _coconut_backstarpipe, _coconut_bool_and, _coconut_bool_or, _coconut_minus, _coconut_tee, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: ------------------------------------------------------

from abc import abstractmethod
import random
import tensorflow as tf
import cytoolz as cz
import itertools as it
from copy import copy
from tfinterface.decorators import return_self
from tfinterface.decorators import with_graph_as_default

from tfinterface.base import Trainer


class SupervisedTrainer(Trainer):
    """
# Inteface
* `model : SupervisedModel` -
* `loss : Tensor` -
* `update : Tensor` -
    """
    def __init__(self, name, loss="mse", optimizer=tf.train.AdamOptimizer, learning_rate=0.001, **kwargs):
        super(SupervisedTrainer, self).__init__(name, **kwargs)

        self._loss_arg = loss
        self._optimizer = optimizer
        self._learning_rate_arg = learning_rate

    def _build(self, model):
# shallow copy model to remain semi-immutable
        self.model = copy(model)



    @return_self
    @with_graph_as_default
    def fit(self, epochs=2000, data_generator=None, log_summaries=False, writer_kwargs={}):
        if log_summaries and not hasattr(self, "writer"):
            self.writer = tf.summary.FileWriter(self.logs_path, graph=self.graph, **writer_kwargs)

        if not hasattr(self, "summaries"):
            self.summaries = tf.no_op()

        if data_generator is None:
#generator of empty dicts
            data_generator = it.repeat({})

        data_generator = (_coconut.functools.partial(cz.take, epochs))(data_generator)

        for i, batch_feed_data in enumerate(data_generator):

            fit_feed = self.model.inputs.fit_feed(**batch_feed_data)
            _, summaries = self.sess.run([self.model.update, self.summaries], feed_dict=fit_feed)

            if log_summaries and summaries is not None:
                self.writer.add_summary(summaries, global_step=global_step)


## REMOVE NEXT, ONLY FOR TESTING
            loss, score = self.sess.run([self.model.loss, self.model.score_tensor], feed_dict=fit_feed)
            print("loss {}, score {}, at {}".format(loss, score, i))
