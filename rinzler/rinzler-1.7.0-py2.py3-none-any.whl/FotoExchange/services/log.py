from datetime import datetime

from config.settings import BASE_DIR

class Log(object):

    __log_file = None

    __data = datetime.now().strftime("%Y-%m-%d")
    __hora = datetime.now().strftime("%H:%M:%S")

    def __int__(self):
        self.__log_file = BASE_DIR + "/log/" + self.__data + ".log"

    def register(self, data):
        log_file = self.get_log_file()
        log = "[{0}]: {1}\n".format(self.__hora, str(data))
        log_file.write(log)
        log_file.close()
        return True

    def get_log_file(self):
        file = BASE_DIR + "/log/" + self.__data + ".log"
        return open(file, "a+")
