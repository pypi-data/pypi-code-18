import os

from hurry.filesize import alternative
from hurry.filesize import filesize
from hurry.filesize import size

from core.logger.base.corebaselogger import CoreBaseLogger


class CoreLoggerFile(CoreBaseLogger):

    def __init__(self, file_path, max_file_size="10", max_file_size_unit="MB"):
        super(CoreLoggerFile, self).__init__()
        self.file_path = file_path
        self.max_file_size = max_file_size
        self.max_file_size_unit = max_file_size_unit

    def addLogEntry(self, message):

        try:
            size_num = size(os.path.getsize(self.file_path), system=alternative).split(" ")[0]
            size_unit = size(os.path.getsize(self.file_path), system=alternative).split(" ")[1]

            if size_unit == self.max_file_size_unit:
                print "unit:"+size_unit
                if size_num >= self.max_file_size:
                    print "num:"+size_num
                    os.remove(self.file_path)
        except OSError as error:
            print error

        self.file = open(self.file_path, 'a')
        self.file.write(self.createEntryFrom(message) + str("\n"))
        self.file.close()
