from multiprocessing import Process


class ThreadService(object):

    __target = None
    __kwargs = dict()

    def __init__(self, callback, **keywargs):
        self.__target = callback
        self.__kwargs = keywargs

    def start(self):
        Process(target=self.__target, kwargs=self.__kwargs).start()
