from .Context import *
import pandas as pd

from matplotlib import pyplot as plt

def run(StrategyWillBeBackTest, data_provider, start_date, end_date):

    ctx = Context(None, data_provider)
    strategy = StrategyWillBeBackTest(ctx)

    benchmark_quotes = data_provider.load_quotes_by_range(ctx.benchmark, start_date, end_date)

    for idx, date in enumerate(benchmark_quotes.date):
        ctx.current_date = date
        strategy.handle_bar(ctx)

        ctx.statics()

    deals_df = pd.DataFrame(ctx.deals)

    print(deals_df)
    print('总收益率:', round((ctx.rate_daily[-1] - 1) * 100, 2), '%')

    plt.figure(figsize=(12, 6))
    plt.plot(ctx.rate_daily, label='rate')
    plt.plot(ctx.benchmark_rate_daily, label='benchmark')

    legend = plt.legend(loc='upper left')

    # frame = legend.get_frame()
    # frame.set_facecolor('0.90')

    plt.show()
