"""
A Python logging handler that integrates with slack.
"""
from collections import OrderedDict
import json
import logging
from logging.handlers import BufferingHandler
import os

try: # pragma: no cover
    from urllib.parse import urlencode
except ImportError: # pragma: no cover
    from urllib import urlencode
try: # pragma: no cover
    from urllib.request import urlopen
except ImportError: # pragma: no cover
    from urllib2 import urlopen
try: # pragma: no cover
    from urllib.request import Request
except ImportError: # pragma: no cover
    from urllib2 import Request


class SlackHandler(BufferingHandler):
    """
    Buffers logs and finally flushes them to a slack hook.
    """
    def __init__(self, hook_url=None, token=None, env_token=None,
                 capacity=10000):
        """
        Initializes this object.
        """
        host = 'https://hooks.slack.com/services/'

        if hook_url is None and token is not None:
            hook_url = host + token
        elif hook_url is None and env_token is not None:
            hook_url = host + os.environ.get(env_token, None)

        # validate the hook url is set up correctly
        if hook_url is not None and host not in hook_url:
            raise ValueError('Hook url must start with %s' % host)

        self.host = host
        self.hook_url = hook_url
        self.capacity = capacity
        self._clear_buffer()
        super(SlackHandler, self).__init__(capacity=capacity)

    def parse_data(self):
        """
        Returns structured data about this group of records to be used in
        formatting.
        """
        msgs = []
        levels = []
        for r in self.buffer:
            #string = str(r.msg % r.args)
            string = self.format(r)
            msgs.append(string)
            levels.append(r.levelname)

        value = '\n'.join(msgs)
        max_level, color = color_picker(levels)
        title = self.buffer[0].name
        module = self.buffer[0].module

        return value, max_level, color, title, module

    def format_buffer(self):
        """
        Formats the logs nicely for slack display.
        """
        if not self.buffer: return []

        value, max_level, color, title, module = self.parse_data()
        rich_text = {
            'fallback': '%s Log [%s]' % (module, title),
            'pretext': '%s Log [%s]' % (module, title),
            'color': color,
            'fields': [{
                'title': max_level,
                'value': value,
                'short': False
                }]
            }

        self.json = json.dumps(rich_text)
        self.payload = {'payload': self.json}
        return self.buffer

    def _clear_buffer(self):
        """
        Clears the buffer and prevents a post to the slack hook.
        """
        self.buffer = []
        self.payload = {}
        self.json = ""

    def flush(self):
        """Sends the buffered logs out to slack hook."""
        response = None
        self.acquire()
        try:
            if self.format_buffer():
                response = self._post()
        finally:
            self.release()
        self._clear_buffer()
        return response

    def close(self):
        try:
            self.flush()
        finally:
            super(SlackHandler, self).close()

    def _post(self):
        """Sends the post request."""
        r = Request(self.hook_url, urlencode(self.payload).encode())
        return urlopen(r).read().decode()


def color_picker(levels):
    """
    Returns the color equivalent for the highest loglevel.
    """
    lookup = OrderedDict([
        ('CRITICAL', 'danger'),
        ('FATAL', 'danger'),
        ('ERROR', 'danger'),
        ('WARNING', 'warning'),
        ('WARN', 'warning'),
        ('INFO', 'good'),
        ('DEBUG', 'good')
    ])
    for key, val in lookup.items():
        if key in levels:
            return key, val
    return levels[0], 'good'

def build_logger(hook_url, level=logging.DEBUG,
                 fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """Builds a logger for you with a SlackHandler and sensible defaults."""
    logger = logging.getLogger(__name__)
    handler = SlackHandler(hook_url)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
