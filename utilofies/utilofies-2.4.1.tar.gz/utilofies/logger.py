# -*- encoding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import logging

# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
logger = logging.getLogger('utilofies')
logger.addHandler(logging.NullHandler())
