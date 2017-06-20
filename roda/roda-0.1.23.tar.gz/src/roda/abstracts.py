from abc import ABCMeta, abstractmethod

class DataProvider(metaclass=ABCMeta):
    '''
    统一不同类型的数据源
    '''
    @abstractmethod
    def load_quote_by_date(self, code, date):
        '''
        获取某天的输入
        :param code:
        :param one_date:
        :return: namedtuple(open, high, low, close, volume)
        '''
        pass
    @abstractmethod
    def load_quotes_by_range(self, code, start_date, end_date):
        '''
        获取一段时间范围里的数据
        :param code: str, 股票代码
        :param start_date: str, 开始时间
        :param end_date: str, 结束时间
        :return: namedtuple(open, high, low, close, volume, dates)
        '''
        pass

    def load_previous_quotes(self, code, end_date, previous_num):
        '''
        获取end_date之前previous_num个数据点(包括end_date)
        :param code:
        :param end_date:
        :param previous_num:
        :return: namedtuple(open, high, low, close, volume, dates)
        '''
        pass

    def load_next_quotes(self, code, start_date, next_num):
        '''
        获取start_date及以后的next_num个数据点
        :param code:
        :param start_date:
        :param next_num:
        :return:
        '''




class Strategy(metaclass=ABCMeta):
    '''
    策略基类
    '''
    @abstractmethod
    def handle_bar(self, context):
        pass