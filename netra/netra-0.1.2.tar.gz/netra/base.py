from os.path import expanduser, join

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.framework import errors_impl

from netra import OKGREEN, ENDC, BOLD
from netra.utils import get_logger


logger = get_logger(__name__)


class BaseModel:
    NAME = None

    def setup(self, model_path=None):
        if not model_path:
            model_path = join(self.cache_dir, 'model.{}'.format(self.NAME))
        self.model_path = model_path
        self.data = input_data.read_data_sets(self.cache_dir, one_hot=True)
        self.session = tf.Session()
        self.saver = tf.train.Saver([self.weights, self.bias])

    @property
    def cache_dir(self):
        return expanduser('~/.cache/tensorflow/{}/'.format(self.NAME))

    def feed_dict(self, inputs, outputs):
        return {self.inputs: inputs, self.outputs: outputs}

    def output():
        pass

    def train(self):
        pass

    def query(self):
        pass

    def restore(self):
        try:
            self.saver.restore(self.session, '{}'.format(self.model_path))
            logger.info('Restored model from {}'.format(self.model_path))
            return True
        except errors_impl.NotFoundError:
            logger.info('No model to restore')

    def save(self):
        logger.info('Saving model')
        return self.saver.save(self.session, self.model_path)

    def color_print(self, text):
        print(BOLD + OKGREEN + text + ENDC)

    def print_probs(self, output):
        max_index = output.index(max(output))
        text = '\nPredicted digit: {}\n'.format(max_index)
        self.color_print(text)

        print('Propabilites:')
        for index, value in enumerate(output):
            if index == max_index:
                text = '{} {}'.format(index, value)
                self.color_print(text)
            else:
                print(index, value)
