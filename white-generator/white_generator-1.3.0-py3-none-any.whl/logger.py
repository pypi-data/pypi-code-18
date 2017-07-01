import logging

import termcolor

class Formatter(logging.Formatter):
    _LEVELS_COLORS = {
        '[INFO]': 'green',
        '[WARNING]': 'yellow',
        '[ERROR]': 'red',
    }

    def format(self, record):
        message = super().format(record)
        for level, color in self._LEVELS_COLORS.items():
            message = message.replace(level, termcolor.colored(level, color))

        return message

def get_logger():
    return logging.getLogger(__package__)

def init_logger():
    handler = logging.StreamHandler()
    handler.setFormatter(Formatter(
        fmt=termcolor.colored('%(asctime)s', 'grey') \
            + ' [%(levelname)s] %(message)s',
    ))

    get_logger().addHandler(handler)
    get_logger().setLevel(logging.INFO)
