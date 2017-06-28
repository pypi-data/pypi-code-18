# coding=utf-8

"""CNN scotopic mnist demo."""

import numpy as np
from snntoolbox.scotopic.cnn_scotopic import cnn_scotopic

from scripts.scotopic.config import update_settings_scotopic

# 4x learning rate in waldnet mode (adapt_layer == 'wb-first')
learning_rate = 4 * 0.001 * np.ones(80)

settings_scotopic = {'learning_rate': learning_rate,
                     'batch_size': 100,
                     'num_epochs': len(learning_rate)}

update_settings_scotopic(settings_scotopic)

cnn_scotopic()
