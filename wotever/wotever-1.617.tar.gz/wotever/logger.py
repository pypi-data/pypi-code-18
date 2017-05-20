import sys
import logging
import time

__version__ = '1.0'
class _AnsiColorizer(object):
    """
    A colorizer is an object that loosely wraps around a stream, allowing
    callers to write text to the stream in a particular color.

    Colorizer classes must implement C{supported()} and C{write(text, color)}.
    """
    _colors = dict(black=30, red=31, green=32, yellow=33,
                   blue=34, magenta=35, cyan=36, white=37)

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        """
        A class method that returns True if the current platform supports
        coloring terminal output using this method. Returns False otherwise.
        """
        if not stream.isatty():
            return False  # auto color only on TTYs
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                try:
                    return curses.tigetnum("colors") > 2
                except curses.error:
                    curses.setupterm()
                    return curses.tigetnum("colors") > 2
            except:
                raise
                # guess false in case of error
                return False

    def write(self, text, color):
        """
        Write the given text to the stream in the given color.

        @param text: Text to be written to the stream.

        @param color: A string label for a color. e.g. 'red', 'white'.
        """
        color = self._colors[color]
        self.stream.write('\x1b[%s;1m%s %s\x1b[0m' % (color,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),text))


class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stderr):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):
        msg_colors = {
            logging.DEBUG: "green",
            logging.INFO: "blue",
            logging.WARNING: "yellow",
            logging.ERROR: "red"
        }

        color = msg_colors.get(record.levelno, "blue")
        self.stream.write(record.msg + "\n", color)

globalLevelSet = False
handler = ColorHandler()
def setGlobalLevel(level="e"):
    globalLevelSet = True
    loggingLevel = logging.WARNING
    if level == 'd':
        loggingLevel = logging.DEBUG
    elif level == 'i':
        loggingLevel = logging.INFO
    elif level == 'w':
        loggingLevel = logging.WARNING
    elif level == 'e':
        loggingLevel = logging.ERROR
    logging.getLogger().setLevel(loggingLevel) 
    logging.getLogger().removeHandler(handler)
    logging.getLogger().addHandler(handler)
def unsetGlobalLevel():
    globalLevelSet = False


def d(str):
    if globalLevelSet:
        logging.debug(str)
    else:        
        logging.getLogger().setLevel(logging.DEBUG) 
        logging.getLogger().addHandler(handler)
        logging.debug(str)
        logging.getLogger().removeHandler(handler)
        logging.getLogger().setLevel(logging.WARNING) 
def i(str):
    if globalLevelSet:
        logging.info(str)
    else:        
        logging.getLogger().setLevel(logging.INFO) 
        logging.getLogger().addHandler(handler)
        logging.info(str)
        logging.getLogger().removeHandler(handler)
        logging.getLogger().setLevel(logging.WARNING) 
def w(str):
    if globalLevelSet:
        logging.warning(str)
    else:        
        logging.getLogger().setLevel(logging.WARNING) 
        logging.getLogger().addHandler(handler)
        logging.warning(str)
        logging.getLogger().removeHandler(handler)
        logging.getLogger().setLevel(logging.WARNING) 
def e(str):
    if globalLevelSet:
        logging.error(str)
    else:        
        logging.getLogger().setLevel(logging.ERROR) 
        logging.getLogger().addHandler(handler)
        logging.error(str)
        logging.getLogger().removeHandler(handler)
        logging.getLogger().setLevel(logging.WARNING) 
# setGlobalLevel('i')
# setGlobalLevel('w')

# e('sss')
# w('ddd')
# unsetGlobalLevel()
# i('iii')