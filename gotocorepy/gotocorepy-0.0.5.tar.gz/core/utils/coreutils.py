from sys import platform
import time

import datetime

from core.base.corebaseclass import CoreBaseClass


class CoreUtils(CoreBaseClass):
    @staticmethod
    def timeStamp():
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')

    @classmethod
    def isLinux(self):
        return bool(platform == "linux" or platform == "linux2")

    @classmethod
    def isWindows(self):
        return bool(platform == "win32")

    @classmethod
    def isOSX(self):
        return platform == "darwin"

