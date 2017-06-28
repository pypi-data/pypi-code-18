# coding=utf-8

"""CNN scotopic CIFAR-10 demo."""

import numpy as np
from snntoolbox.scotopic.cnn_scotopic import cnn_scotopic

from scripts.scotopic.config import update_settings_scotopic

# 4x learning rate in waldnet mode (adapt_layer == 'wb-first')
learning_rate = 4 * np.hstack((0.05 * np.ones(30), 0.005 * np.ones(25),
                              0.0005 * np.ones(20)))

settings_scotopic = {'learning_rate': learning_rate,
                     'batch_size': 100,
                     'num_epochs': len(learning_rate),
                     'weight_decay': 0.0001}

update_settings_scotopic(settings_scotopic)

cnn_scotopic()
