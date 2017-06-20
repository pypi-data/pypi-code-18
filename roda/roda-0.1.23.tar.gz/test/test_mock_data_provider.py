import csv
from src.roda import *
from collections import namedtuple
import numpy as np


# def random_change():
#     return 1 + random.uniform(-0.4, 0.4)
#
# def random_decrease_change():
#     return 1 + random.uniform(-0.4, 0)
#
# def random_increase_change():
#     return 1 + random.uniform(0, 0.4)
#
# def generate_day_price(peer_price):
#     open_price = peer_price * random_change()
#     high_price = open_price * random_increase_change()
#     low_price = open_price * random_decrease_change()
#     close_price = open_price * random_change()
#
#     if close_price > high_price:
#         high_price = close_price
#     if close_price < low_price:
#         low_price = close_price
#
#     return (open_price, high_price, low_price, close_price)

# class RandomDataProvider(DataProvider):
#     def __init__(self):
#         pass
#     def load_price_by_date(self, code, one_date):
#         pass
#     def load_price_by_date_range(self, code, start_date, end_date):
#         pass
#

def read_data_from_csv(name):
    with open('test/data/' + name + '.csv') as file:
        spam_reader = csv.reader(file)

        date_arr = []
        open_arr = []
        high_arr = []
        low_arr = []
        close_arr = []
        volume_arr = []

        for row in spam_reader:
            date_arr.append(row[0])
            open_arr.append(float(row[2]))
            high_arr.append(float(row[3]))
            low_arr.append(float(row[4]))
            close_arr.append(float(row[5]))
            volume_arr.append(float(row[6]))

    return {
        'date': np.array(date_arr),
        'open': np.array(open_arr),
        'high': np.array(high_arr),
        'low': np.array(low_arr),
        'close': np.array(close_arr),
        'volume': np.array(volume_arr),
    }


Quote = namedtuple('quote', ['date', 'open', 'high', 'low', 'close', 'volume'])


class MockDataProvider(DataProvider):
    def __init__(self):
        self.data_dict = {
            'AMD': None,
            'NVDA': None
        }
        for code in self.data_dict:
            self.data_dict[code] = read_data_from_csv(code)

    def find_date_idx(self, code, date):
        code_data = self.data_dict[code]
        idx, = np.where(code_data['date'] == date)
        idx = idx[0]
        return idx

    def quote_range(self, code, idx_start, idx_end):
        data = self.data_dict[code]
        return Quote(data['date'][idx_start:idx_end],
                     data['open'][idx_start:idx_end],
                     data['high'][idx_start:idx_end],
                     data['low'][idx_start:idx_end],
                     data['close'][idx_start:idx_end],
                     data['volume'][idx_start:idx_end])

    def load_quote_by_date(self, code, one_date):
        idx = self.find_date_idx(code, one_date)
        return self.quote_range(code, idx, idx + 1)

    def load_quotes_by_range(self, code, start_date, end_date):
        idx_start = self.find_date_idx(code, start_date)
        idx_end = self.find_date_idx(code, end_date) + 1
        return self.quote_range(code, idx_start, idx_end)

    def load_previous_quotes(self, code, end_date, previous_num):
        idx_end = self.find_date_idx(code, end_date) + 1
        idx_start = idx_end - previous_num
        return self.quote_range(code, idx_start, idx_end)

    def load_next_quotes(self, code, start_date, next_num):
        idx_start = self.find_date_idx(code, start_date)
        idx_end = idx_start + next_num
        return self.quote_range(code, idx_start, idx_end)


#
#
# def test_init():
#     o, h, l, c = generate_day_price(10)
#     print(o, h, l, c)