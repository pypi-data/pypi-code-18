from src.roda import *

import talib

class StrategyDmi(Strategy):
    def __init__(self, ctx):
        ctx.benchmark = 'FHN'

    def handle_bar(self, ctx):

        code = 'FHN'

        adx_period = 14
        short_ma_num = 5
        long_ma_num = 20
        data = ctx.data_provider.load_previous_quotes(code,
                                                      end_date=ctx.current_date,
                                                      previous_num=100)

        if len(data.date) == 0:
            return

        data_high = data.high[:-1]
        data_low = data.low[:-1]
        data_close = data.close[:-1]
        adx = talib.ADX(data_high, data_low, data_close, adx_period)
        plus_di = talib.PLUS_DI(data_high, data_low, data_close, adx_period)
        minus_di = talib.MINUS_DI(data_high, data_low, data_close, adx_period)
        short_ma = talib.SMA(data_close, short_ma_num)
        long_ma = talib.SMA(data_close, long_ma_num)

        current_price = data.close[-1]

        ma_up_cross = short_ma[-1] > long_ma[-1] and short_ma[-2] < long_ma[-2]
        ma_down_cross = short_ma[-1] < long_ma[-1] and short_ma[-2] > long_ma[-2]
        adx_up = adx[-1] > adx[-2]
        di_up = plus_di[-1] > minus_di[-1]

        if ma_up_cross and adx_up and di_up:
            ctx.order(code, 0.99, current_price)
        if ma_down_cross and not adx_up and not di_up:
            ctx.order(code, 0, current_price)

