# coding: utf-8
import threading
import traceback

from django.db import close_old_connections


class EventDispatcher(object):
    def __init__(self):
        self._events = {}

    def __del__(self):
        self._events = None

    def __listener_executor(self, listener, args, kwargs):
        try:
            listener(*args, **kwargs)
        except:
            print(traceback.format_exc())
        finally:
            close_old_connections()

    def has_listener(self, event_type, listener):
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def dispatch_event(self, event_type, *args, **kwargs):
        if event_type in self._events.keys():
            listeners = self._events[event_type]

            for listener in listeners:
                listener_thread = threading.Thread(target=self.__listener_executor, args=(listener, args, kwargs))
                listener_thread.setDaemon(True)
                listener_thread.start()

    def add_event_listener(self, event_type, listener):
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])
            listeners.append(listener)
            self._events[event_type] = listeners

    def remove_event_listener(self, event_type, listener):
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type]
            if len(listeners) == 1:
                del self._events[event_type]
            else:
                listeners.remove(listener)
                self._events[event_type] = listeners


EventDispatcher = EventDispatcher()
