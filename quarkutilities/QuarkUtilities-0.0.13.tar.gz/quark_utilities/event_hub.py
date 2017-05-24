import logging

logger = logging.getLogger("event_hub")
hub = None

def init_event_hub(app):
    global hub
    hub = EventHub(app)

class Event(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class EventHub(object):

    def __init__(self, app):
        self._app = app
        self._handlers = {}

    def subscribe(self, event_type):
        if event_type not in self._handlers:
            self._handlers[event_type] = set()

        def wrapper(f):
            self._handlers[event_type].add(f)
            return f

        return wrapper

    async def dispatch(self, event):
        logger.info("Event arrived <{}>".format(str(type(event))))

        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            await handler(event)


