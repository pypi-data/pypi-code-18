import tensorflow as tf
import numpy as np
from caicloud.clever.tensorflow import dist_base
tf.logging.set_verbosity(tf.logging.INFO)
features = [tf.contrib.layers.real_valued_column("x", dimension=1)]
estimator = tf.contrib.learn.LinearRegressor(feature_columns=features)
x = np.array([1., 2., 3., 4.])
y = np.array([0., -1., -2., -3.])
input_fn = tf.contrib.learn.io.numpy_input_fn({"x":x}, y, batch_size=4,
                                              num_epochs=1000)
#estimator.fit(input_fn=input_fn, steps=1000)
#estimator.evaluate(input_fn=input_fn)
experiment = dist_base.Experiment(
    estimator = estimator,
    train_input_fn = input_fn,
    eval_input_fn = input_fn)
experiment.run()
