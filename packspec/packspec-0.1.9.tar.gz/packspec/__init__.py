# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

# Version

import io
import os
__version__ = io.open(
    os.path.join(os.path.dirname(__file__), 'VERSION'),
    encoding='utf-8').read().strip()
