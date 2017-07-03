import numpy as np
import keras.backend as b


class Inceptor(object):
    """
    An inceptor used to generate inceptions for a target in a neural network.

    Sample use:
        >>> from keras import applications
        >>> from netception.inceptor import Inceptor
        >>> model = applications.VGG16()
        >>> conv_layer = model.get_layer("block5_conv3")
        >>> filter_index = 42
        >>> target = conv_layer.output[:, :, :, filter_index]
        >>> inceptor = Inceptor(model, target)
        >>> inception, score = inceptor.incept()
    """

    def __init__(self, model, target, inception_rate=0.5, max_steps=20,
                 improvement_check_interval=5, improvement_threshold=0.05):
        """
        Constructs an Inceptor.

        :param model: The model to incept which contains the target.
        :param target: The target to incept within the model.
        :param inception_rate: The rate that guides the inception process.
        :param max_steps: The maximal number of inception steps.
        :param improvement_check_interval: Check interval for early stopping.
        :param improvement_threshold: Threshold for early stopping.

        :raises: ValueError
        """
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        if inception_rate <= 0.0:
            raise ValueError("inception_rate must be strictly positive")
        if improvement_check_interval < 1:
            raise ValueError("improvement_check_interval must be at least 1")
        if not 0.0 <= improvement_threshold <= 1.0:
            raise ValueError("improvement_threshold must be in [0.0; 1.0]")

        self._model = model
        self._target = target
        self._max_steps = max_steps
        self._inception_rate = inception_rate
        self._improvement_check_interval = improvement_check_interval
        self._improvement_threshold = improvement_threshold

    def incept(self):
        """
        Executes the inceptor's inception process.

        :return: inception, score
        """
        model_input = self._model.input
        model_input_shape = self._model.input_shape
        objective = b.mean(self._target)
        gradients = self._l2_normalize(b.gradients(objective, model_input))
        step_op = b.function([model_input], [objective, gradients])
        initial_inception = np.random.random((1, *model_input_shape[1:])) - 0.5
        inception, score = self._run_optimization(initial_inception, step_op)
        return inception[0], score

    @staticmethod
    def _l2_normalize(x):
        return x / (b.sqrt(b.mean(b.square(x))) + np.finfo(float).eps)

    def _run_optimization(self, inception, step_op):
        old_score = -np.inf
        score = -np.inf
        for step in range(self._max_steps):
            score, grads_value = step_op([inception])
            inception += grads_value[0] * self._inception_rate
            print("Inception    step: {}    score: {:.6f}".format(step, score))
            if step % self._improvement_check_interval == 0:
                if score <= (1 + self._improvement_threshold) * old_score:
                    print("Inception    step: {}    Early stopping because of "
                          "insufficient improvement".format(step))
                    break
                old_score = score
        return inception, score
