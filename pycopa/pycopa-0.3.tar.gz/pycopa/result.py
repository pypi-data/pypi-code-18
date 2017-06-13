
class ParserResult:
    def __init__(self, value):
        self.__value = value

    def get(self, name):
        return self.__value.get(name, None)

    def __getattr__(self, item):
        return self.__value.get(item, None)
