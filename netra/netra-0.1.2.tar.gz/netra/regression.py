import tensorflow as tf

from netra.base import BaseModel
from netra.utils import get_logger

logger = get_logger(__name__)


class Regression(BaseModel):

    NAME = 'regression'

    def __init__(self, input_nodes=28 * 28, output_nodes=10,
                 learning_rate=0.01, model_path=None):
        self.inputs = tf.placeholder(tf.float32, [None, input_nodes])
        self.weights = tf.Variable(tf.zeros([input_nodes, output_nodes]),
                                   name='weights')
        self.bias = tf.Variable(tf.zeros([output_nodes]), name='bias')
        self.outputs = tf.placeholder(tf.float32, [None, output_nodes])
        self.learning_rate = learning_rate
        self.setup()

    def output(self):
        r_output = tf.matmul(self.inputs, self.weights) + self.bias
        output = tf.nn.softmax(r_output)
        return output

    def train(self, epochs=100000, batch_size=100):
        self.restore()
        logger.info('Starting training')
        logger.info('Epochs {}, Batch size: {}'.format(epochs, batch_size))

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
            logits=self.output(), labels=self.outputs))
        train_step = tf.train.GradientDescentOptimizer(
            self.learning_rate).minimize(cross_entropy)
        self.session.run(tf.global_variables_initializer())
        for epoch in range(epochs):
            inputs, outputs = self.data.train.next_batch(batch_size)
            self.session.run(train_step,
                             feed_dict=self.feed_dict(inputs, outputs))
        prediction = tf.equal(tf.argmax(self.output(), 1),
                              tf.argmax(self.outputs, 1))
        accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))
        data = self.feed_dict(self.data.test.images,
                              self.data.test.labels)
        accuracy_value = self.session.run(accuracy, feed_dict=data)
        logger.info('Accuracy: {}'.format(accuracy_value))
        logger.info('Completed training')
        self.save()

    def query(self, input_):
        restored = self.restore()
        if not restored:
            self.train()
        output = self.session.run(
            self.output(), feed_dict={self.inputs: input_}).flatten().tolist()
        self.print_probs(output)
