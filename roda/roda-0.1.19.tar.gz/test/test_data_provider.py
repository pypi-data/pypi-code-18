from src import *
import random


def random_change():
    return 1 + random.uniform(-0.4, 0.4)

def random_decrease_change():
    return 1 + random.uniform(-0.4, 0)

def random_increase_change():
    return 1 + random.uniform(0, 0.4)

def generate_day_price(peer_price):
    open_price = peer_price * random_change()
    high_price = open_price * random_increase_change()
    low_price = open_price * random_decrease_change()
    close_price = open_price * random_change()

    if close_price > high_price:
        high_price = close_price
    if close_price < low_price:
        low_price = close_price

    return (open_price, high_price, low_price, close_price)

class RandomDataProvider(DataProvider):
    def __init__(self):
        pass
    def load_price_by_date(self, code, one_date):
        pass
    def load_price_by_date_range(self, code, start_date, end_date):
        pass

class MockDataProvider(DataProvider):
    def __init__(self):
        pass
    def load_price_by_date(self, code, one_date):
        pass
    def load_price_by_date_range(self, code, start_date, end_date):
        pass


def test_init():
    o, h, l, c = generate_day_price(10)
    print(o, h, l, c)