from abc import ABCMeta, abstractmethod

class DataProvider(metaclass=ABCMeta):
    '''
    统一不同类型的数据源
    '''
    @abstractmethod
    def load_price_by_date(self, code, one_date):
        '''
        获取某天的输入
        :param code:
        :param one_date:
        :return: (open, high, low, close)
        '''
        pass
    @abstractmethod
    def load_price_by_date_range(self, code, start_date, end_date):
        '''
        获取一段时间范围里的数据
        :param code: str, 股票代码
        :param start_date: str, 开始时间
        :param end_date: str, 结束时间
        :return: (open:list, high:list, low:list, close:list)
        '''
        pass


class Strategy(metaclass=ABCMeta):
    '''
    策略基类
    '''
    @abstractmethod
    def handle_bar(self, context):
        pass