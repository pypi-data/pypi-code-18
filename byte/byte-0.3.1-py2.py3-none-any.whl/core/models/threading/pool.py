"""byte - pool manager module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.threading.local import LocalItem, LocalManager


class PoolManager(LocalManager):
    """Pool manager class."""

    def __init__(self, maximum=None):
        """Create pool manager.

        :param maximum: Maximum number of items to create
        :type maximum: int or None
        """
        super(PoolManager, self).__init__()

        self.maximum = maximum

        self._all = []
        self._available = []

    @property
    def active(self):
        """Retrieve number of active items."""
        return len(self._all) - len(self._available)

    def acquire(self, blocking=False):
        """Acquire item from pool.

        :param blocking: Block until item is available.
        :type blocking: bool
        """
        # Use available item (if one exists)
        if self._available:
            return False, self._available.pop()

        # Create item (if below maximum)
        if self.maximum is None or len(self._all) < self.maximum:
            return True, self.create()

        # Blocking disabled, just return `None`
        if not blocking:
            return False, None

        # Wait for available item
        raise NotImplementedError

    def on_created(self, item):
        """Handle item creation event."""
        self._all.append(item)

    def on_detached(self, item):
        """Handle item detached event."""
        self._available.append(item)

    def __len__(self):
        return len(self._all)


class PoolItem(LocalItem):
    """Base pool item class."""

    pass
