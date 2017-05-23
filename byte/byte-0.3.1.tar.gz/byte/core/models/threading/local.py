"""byte - local manager module."""
from __future__ import absolute_import, division, print_function

from threading import RLock

try:
    from thread import get_ident
except ImportError:
    from threading import get_ident


class LocalManager(object):
    """Local manager class."""

    def __init__(self):
        """Create local manager."""
        self._bindings = {}
        self._lock = RLock()

    def create(self, **kwargs):
        """Create item."""
        raise NotImplementedError

    def detach(self, item):
        """Detach item from thread.

        :param item: Item
        :type item: LocalItem
        """
        with self._lock:
            if not item._ident:
                return

            # Remove item from collection
            self._bindings.pop(item._ident)

            # Remove ident from item
            item._ident = None

            # Fire `on_detached` callback
            self.on_detached(item)

    def get(self, **kwargs):
        """Retrieve (or create) item for current thread."""
        ident = get_ident()

        try:
            return self._bindings[ident]
        except KeyError:
            return self._acquire(ident, **kwargs)

    def acquire(self, **kwargs):
        """Acquire item."""
        return True, self.create(**kwargs)

    def on_created(self, item):
        """Handle item creation event."""
        pass

    def on_detached(self, item):
        """Handle item detached event."""
        pass

    def _acquire(self, ident=None, **kwargs):
        if not ident:
            ident = get_ident()

        with self._lock:
            # Return existing item (if available)
            if ident in self._bindings:
                return self._bindings[ident]

            # Acquire item
            created, item = self.acquire(**kwargs)

            if not item:
                return None

            if created:
                if not isinstance(item, LocalItem):
                    raise ValueError('Invalid item (expected instance of LocalItem)')

                # Set item manager
                item._manager = self

                # Fire `on_created` callback
                self.on_created(item)

            # Bind item to ident
            return self._bind(item, ident)

    def _bind(self, item, ident):
        # Set item ident
        item._ident = ident

        # Store item in bindings
        self._bindings[ident] = item

        return item

    def __len__(self):
        return len(self._bindings)


class LocalItem(object):
    """Base local item class."""

    def __init__(self):
        """Create local item."""
        self._ident = None
        self._manager = None

    def detach(self):
        """Detach item from thread."""
        if not self._manager or not self._ident:
            return

        self._manager.detach(self)
