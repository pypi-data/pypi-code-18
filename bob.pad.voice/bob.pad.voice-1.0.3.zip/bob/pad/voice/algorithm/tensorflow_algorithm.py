#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Pavel Korshunov <pavel.korshunov@idiap.ch>
# @date: Wed 19 Oct 23:43:22 2016

from bob.pad.base.algorithm import Algorithm
import numpy

import bob.io.base

# import tensorflow as tf

import logging

logger = logging.getLogger("bob.pad.voice")


class TensorflowAlgo(Algorithm):
    """This class is used to test all the possible functions of the tool chain, but it does basically nothing."""

    def __init__(self,
                 **kwargs):
        """Generates a test value that is read and written"""

        # call base class constructor registering that this tool performs everything.
        Algorithm.__init__(
            self,
            performs_projection=True,
            requires_projector_training=False,
        )

        self.data_reader = None
        # self.session = tf.Session()
        self.dnn_model = None

#    def __del__(self):
#        self.session.close()

    def _check_feature(self, feature):
        """Checks that the features are appropriate."""
        if not isinstance(feature, numpy.ndarray) or feature.ndim != 1 or feature.dtype != numpy.float32:
            raise ValueError("The given feature is not appropriate", feature)
        return True

    def load_projector(self, projector_file):
        logger.info("Loading pretrained model from {0}".format(projector_file))
        from bob.learn.tensorflow.network.SequenceNetwork import SequenceNetwork
        self.dnn_model = SequenceNetwork()
        # self.dnn_model.load_hdf5(bob.io.base.HDF5File(projector_file), shape=[1, 6560, 1])
        self.dnn_model.load(projector_file, True)

    def project_feature(self, feature):

        logger.debug(" .... Projecting %d features vector" % feature.shape[0])
        from bob.learn.tensorflow.datashuffler import DiskAudio
        if not self.data_reader:
            self.data_reader = DiskAudio([0], [0])
        frames, labels = self.data_reader.extract_frames_from_wav(feature, 0)
        frames = numpy.asarray(frames)
        logger.debug(" .... And %d frames are extracted to pass into DNN model" % frames.shape[0])
        frames = numpy.reshape(frames, (frames.shape[0], -1, 1))
        forward_output = self.dnn_model(frames)
        # return tf.nn.log_softmax(tf.nn.log_softmax(forward_output)).eval(session=self.session)
        return forward_output

    def project(self, feature):
        """project(feature) -> projected

        This function will project the given feature.
        It is assured that the :py:meth:`load_projector` was called once before the ``project`` function is executed.

        **Parameters:**

        feature : object
          The feature to be projected.

        **Returns:**

        projected : object
          The projected features.
          Must be writable with the :py:meth:`write_feature` function and readable with the :py:meth:`read_feature` function.

        """
        if len(feature) > 0:
            feature = numpy.cast['float32'](feature)
            self._check_feature(feature)
            return self.project_feature(feature)
        else:
            return numpy.zeros(1, dtype=numpy.float64)

    def score_for_multiple_projections(self, toscore):
        """scorescore_for_multiple_projections(toscore) -> score

        **Returns:**

        score : float
          A score value for the object ``toscore``.
        """
        scores = numpy.asarray(toscore, dtype=numpy.float32)
        real_scores = scores[:, 0]
        logger.debug("Mean score %f", numpy.mean(real_scores))
        return [numpy.mean(real_scores)]

    def score(self, toscore):
        """Returns the evarage value of the probe"""
        logger.debug("score() score %f", toscore)
        # return only real score
        return [toscore[0]]


algorithm = TensorflowAlgo()
