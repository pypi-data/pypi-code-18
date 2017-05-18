import os
import time
from logging.handlers import TimedRotatingFileHandler


class ResultItem(dict):
    @staticmethod
    def from_dict(d):
        ret = ResultItem(**d)
        return ret

    @staticmethod
    def _parse_item(x):
        if isinstance(x, dict):
            return ResultItem.from_dict(x)
        elif isinstance(x, (set, list, tuple)) and len(x) > 0:
            return [ResultItem._parse_item(y) for y in x]
        else:
            return x

    def __setattr__(self, key, value):
        if isinstance(value, (set, list, tuple)) and len(value) > 0:
            super().__setitem__(key, ResultItem._parse_item(value))
        elif not isinstance(value, ResultItem) and isinstance(value, dict):
            self[key] = ResultItem()
            for k, v in value.items():
                self[key].__setattr__(k, v)
        else:
            self[key] = value

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        if not isinstance(value, ResultItem) and isinstance(value, (dict, list, set, tuple)) and len(value) > 0:
            self.__setattr__(key, value)
        else:
            super().__setitem__(key, value)

    def __init__(self, **kwargs):
        super().__init__()
        for argk, argv in kwargs.items():
            self[argk] = argv


class ApiResult(ResultItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ApiException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


PLATFORM_IOS = 'ios'
PLATFORM_ANDROID = 'android'
PLATFORM_WEB = 'web'
PLATFORM_WX = 'wx'
PLATFORM_WX_CYCLE = 'wxcycle'
PLATFORM_TRD = 'trd'


class SafeRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)

    """
    Override doRollover
    lines commanded by "##" is changed by cc
    """

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
   
        Override,   1. if dfn not exist then do rename
                    2. _open with "a" model
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        ##        if os.path.exists(dfn):
        ##            os.remove(dfn)

        # Issue 18940: A file may not have been created if delay is True.
        ##        if os.path.exists(self.baseFilename):
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
