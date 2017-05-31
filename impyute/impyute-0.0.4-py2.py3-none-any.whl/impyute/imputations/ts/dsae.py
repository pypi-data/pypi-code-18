""" Imputation using Denoising Stacked Autoencoders """
from impyute.imputations.ts import locf
import numpy as np
import os
from impyute.utils import checks
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Quiet TensorFlow warnings
import tensorflow as tf


def dsae(data, config):
    """
    PARAMETERS
    ----------
    data: np.ndarray
        2D Tensor
    RETURNS
    ------
    np.ndarray
        Imputed 'data'
    """
    if not checks(data):
        raise Exception("Checks failed")
    # h_layers = config.layers
    h_layers = [300, 150, 40]
    data = locf(data)
    if not (min(data.flatten()) == 0.0 and max(data.flatten()) == 1.0):
        data = data/max(data.flatten())
    n_dim, x_dim = np.shape(data)
    X = tf.placeholder(tf.float32, [n_dim, ])
    e_layer1 = ae_layer(X, x_dim, h_layers[0])
    e_layer2 = ae_layer(e_layer1, h_layers[0], h_layers[1])
    e_layer3 = ae_layer(e_layer2, h_layers[1], h_layers[2])
    d_layer3 = ae_layer(e_layer3, h_layers[2], h_layers[1])
    d_layer2 = ae_layer(d_layer3, h_layers[1], h_layers[0])
    X_ = ae_layer(d_layer2, h_layers[0], x_dim)

    squared_error = tf.reduce_sum(tf.square(X_ - X))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train_step = optimizer.minimize(squared_error)
    init = tf.global_variables_initializer()
    # Train
    with tf.Session() as sess:
        sess.run(init)
        _ = sess.run(train_step, {X: data})
    output = data
    return output


def ae_layer(X_in, channel_in, channel_out, name="autoencoder_layer"):
    with tf.name_scope(name):
        W = tf.Variable(tf.truncated_normal([channel_in, channel_out]),
                        name="weights")
        tf.summary.histogram("weights", W)
        B = tf.Variable(tf.truncated_normal([channel_out]), name="biases")
        tf.summary.histogram("biases", B)
        return tf.nn.sigmoid(tf.matmul(X_in, W) + B)
