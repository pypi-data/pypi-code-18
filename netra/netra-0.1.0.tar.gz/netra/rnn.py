import tensorflow as tf

from netra import MNIST_IMAGE_DIMENSIONS
from netra.base import BaseModel
from netra.utils import get_logger


logger = get_logger(__name__)

chunk_size, num_chunks = MNIST_IMAGE_DIMENSIONS


class LSTM(BaseModel):

    NAME = 'lstm'

    def __init__(self, rnn_size=256, output_nodes=10):
        self.rnn_size = rnn_size
        self.inputs = tf.placeholder('float', [None, num_chunks, chunk_size])
        self.outputs = tf.placeholder('float')
        self.weights = tf.Variable(tf.random_normal([rnn_size, output_nodes]))
        self.bias = tf.Variable(tf.random_normal([output_nodes]))
        self.setup()

    def output(self):
        inputs = tf.transpose(self.inputs, [1, 0, 2])
        inputs = tf.reshape(inputs, [-1, chunk_size])
        inputs = tf.split(axis=0, num_or_size_splits=num_chunks, value=inputs)

        lstm_cell = tf.contrib.rnn.BasicLSTMCell(
            self.rnn_size, state_is_tuple=True)
        outputs, states = tf.contrib.rnn.static_rnn(
            lstm_cell, inputs, dtype=tf.float32)

        output = tf.matmul(outputs[-1], self.weights) + self.bias
        return output

    def train(self, epochs=100, batch_size=100):
        logger.info('Starting training')
        prediction = self.output()
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
            logits=prediction, labels=self.outputs))
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        self.session.run(tf.global_variables_initializer())

        for epoch in range(epochs):
            for i in range(int(self.data.train.num_examples / batch_size)):
                inputs, outputs = self.data.train.next_batch(batch_size)
                inputs = inputs.reshape((batch_size, num_chunks, chunk_size))

                self.session.run([optimizer, cost],
                                 feed_dict=self.feed_dict(inputs, outputs))
        correct = tf.equal(tf.argmax(prediction, 1),
                           tf.argmax(self.outputs, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        feed_dict = self.feed_dict(
            self.data.test.images.reshape((-1, num_chunks, chunk_size)),
            self.data.test.labels
        )
        accuracy = self.session.run(accuracy, feed_dict=feed_dict)
        logger.info('Accuracy: {}'.format(accuracy))
        logger.info('Completed training')
        self.save()
