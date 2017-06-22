# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os

logging.basicConfig(
    level=logging.ERROR,
    filename=os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'pypackt.log'
    ),
    filemode='w',
)
