"""
Module for caching of the build images.

Nowadays, only an empty implementation.
"""

import logging

from .constants import APP_NAME
from .output import SUBTITLE

_logger = logging.getLogger(APP_NAME)


class ImageCache:
    """
    Empty implementation of the caching class.
    """

    def add(self, image_id, parent_id, layer):
        """
        Save new image to the cache.

        * image_id: id of the current image
        * parent_id: id of the parent image
        * layer: current layer (with instructions executed on the parent image to get current image)
        """
        _logger.debug(SUBTITLE.format('CACHE - SAVE'))
        _logger.debug('id: {}\nparent: {}\n{}\n'.format(str(image_id), str(parent_id), str(layer)))

    def get_layer(self, parent, layer):
        """
        Try to find image in cache.

        * parent: id of the parent image
        * layer: current layer (instructions, that has to be executed on top of the parent image)
        * **return:** id of the image, or `None`
        """
        _logger.debug(SUBTITLE.format('CACHE - IMAGE NOT FOUND'))
        _logger.debug('parent: {}\n{}\n'.format(str(parent), str(layer)))
        return None
