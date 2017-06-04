import math
from collections import namedtuple

StoreRecord = namedtuple('StoreRecord', ['price', 'volume', 'position'])
DealRecord = namedtuple('DealRecord', ['code', 'price', 'volume', 'date', 'op'])
RateRecord = namedtuple('RateRecord', ['date', 'value'])

class Context:

    def __init__(self, benchmark, data_provider, init_cash = 1000 * 1000):
        self.data_provider = data_provider
        self.current_date = None
        self.init_cash = init_cash
        self.cash = init_cash
        self.benchmark = benchmark
        self.benchmark_init_value = None
        self.deals = []
        self.store = {}
        self.rate_daily = []
        self.benchmark_rate_daily = []

    def order(self, code, position, price):
        # 有持仓取出持仓，无持仓设为空持仓
        if code in self.store:
            record = self.store[code]
        else:
            record = StoreRecord(code, 0, 0)

        diff_position = position - record.position
        # 当前仓位等于目标仓位，不操作
        if diff_position == 0:
            return

        # 仓位需要增加
        if diff_position > 0:
            self.__buy(code, record, position, price)
            return

        self.__sell(code, record, position, price)

    def __sell(self, record, code, position, price):
        diff_position = position - record.position

        # 清仓
        if position == 0:
            income = price * record.volume
            self.cash += income
            self.store.pop(code, None)
            op_volume = record.volume
        else:
            # 目标仓位小 -> 卖出
            # 如果是空持仓不会进行到这一步 所以不用担心record.position为0
            sell_volume = round(record.volume / record.position * diff_position, 0)
            income = price * sell_volume
            self.cash += income
            new_volume = record.volume - sell_volume
            real_position = new_volume * record.price / self.init_cash
            op_volume = new_volume
            self.store[code] = StoreRecord(record.price, new_volume, real_position)

        deal = DealRecord(code, price, op_volume, self.current_date, 'sell')
        self.deals.append(deal)


    def __buy(self, record, code, position, price):
        # 目标仓位大 ->
        # 当前可用仓位： 现金 / 原始资本
        valid_position = self.cash / self.init_cash
        # 可用仓位不够用 -> 跳出

        diff_position = position - record.position

        # 目标仓位大于可用仓位   退出
        if diff_position > valid_position:
            return

        # 仓位够用 -> 买入
        buy_volume = diff_position * self.init_cash / price

        # 如果可买不足1股 -> 退出
        if buy_volume < 1:
            return

        cost = price * buy_volume
        new_volume = record.volume + buy_volume

        self.cash -= cost
        avg_price = (record.price * record.volume + cost) / new_volume
        self.store[code] = StoreRecord(avg_price, new_volume, position)
        deal = (code, price, buy_volume, self.current_date, 'buy')
        self.deals.append(deal)


    def count_value(self):
        '''
        统计当前资本收益率
        :return: None
        '''
        value = self.cash
        for code in list(self.store.keys()):
            _, _, _, current_close = self.data_provider.load_price_by_date(code, self.current_date)
            value += current_close * self.store[code].volume
        self.rate_daily.append(RateRecord(self.current_date, value / self.init_cash))


    def count_benchmark_value(self):
        '''
        统计当前benchmark的收益率
        :return: None
        '''
        _, _, _, current_close = self.data_provider.load_price_by_date(self.benchmark, self.current_date)

        # 没有初始值的时候，以当前值初始化一下
        if self.benchmark_init_value is None:
            self.benchmark_rate_daily = current_close

        self.benchmark_rate_daily.append(RateRecord(self.current_date, current_close / self.benchmark_rate_daily))

