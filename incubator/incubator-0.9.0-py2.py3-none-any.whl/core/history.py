"""
History of manipulation with containers -- create, change of state, or deletion.
"""

import logging
from collections import OrderedDict

from .constants import APP_NAME
from .output import CHAPTER

_logger = logging.getLogger(APP_NAME)


class ContainerHistory(object):
    """
    Saves the container manipulation history.
    """

    def __init__(self):
        self._hist = OrderedDict()

    def add_container_status(self, id, state, message=None):
        """
        Update the state of given container.

        * id: id of the container to save
        * state: new state of the container
        * message: message, that can be forwarded to the log
        """
        debug_text = "container {}\n- id: {}".format(state, id)
        if message:
            debug_text += "\n{}".format(message)
        _logger.debug(CHAPTER.format(debug_text))
        self._hist[id] = state

    def remove_container(self, id):
        """
        Remove container from the history.
        From now, the container is taken as deleted.
        * id: id of the container to remove
        """
        _logger.debug(CHAPTER.format("container removed\n- id: {}".format(id)))
        del self._hist[id]

    @property
    def containers(self):
        """
        * **return:** containers present in the history (containers that were not deleted)
        """
        return list(self._hist)
