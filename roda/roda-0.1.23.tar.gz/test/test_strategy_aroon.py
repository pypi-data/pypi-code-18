import talib


# current_date为收盘状态
class StrategyAroon:
    def __init__(self, context):
        context.benchmark = 'NVDA'

    def handle_bar(self, context):
        code = 'AMD'
        period = 14
        data = context.data_provider.load_previous_quotes(code,
                                                          end_date=context.current_date,
                                                          previous_num=100)

        if len(data.date) == 0:
            return

        # 根据昨天的数据 判断今天如何操作
        downs, ups = talib.AROON(data.high[0:-1], data.low[0:-1], period)

        # 以今日开盘价格买入
        current_price = data.open[-1]

        the_last_up = ups[-1]
        the_last_down = downs[-1]

        if the_last_up > the_last_down:
            context.order(code, 0.99, current_price)
        if the_last_up < the_last_down:
            context.order(code, 0, current_price)


