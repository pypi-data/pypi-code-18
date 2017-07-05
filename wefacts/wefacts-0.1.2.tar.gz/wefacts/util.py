"""
Utils.
"""

import logging
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('%s/raw' % base_dir):
    os.makedirs('%s/raw' % base_dir)

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(pathname)s %(lineno)d %(message)s')
file_handler = logging.FileHandler('%s/raw/wefacts.log' % base_dir)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

__version__ = "0.0.1"
