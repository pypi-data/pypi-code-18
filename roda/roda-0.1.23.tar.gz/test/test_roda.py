from nose.tools import assert_equal

from .test_mock_data_provider import MockDataProvider
from .test_strategy_aroon import StrategyAroon
from .test_strategy_dmi import StrategyDmi

from src.roda import *
from conf import *

def test_run():

    start_date = '2014-12-17'
    end_date = '2017-05-30'
    # data_provider = MockDataProvider()
    data_provider = MongoDataProvider(conf['mongo'])
    data_provider.preload(['FHN'], start_date, end_date)
    run(StrategyDmi, data_provider, start_date, end_date)



def test_context_order():

    benchmark = 'NVDA'
    code = 'AMD'

    ctx = Context(benchmark, None)

    result = ctx.order(code, 0.99, 1.1)
    assert_equal(result.success, True, 'buy')

    result = ctx.order(code, 0, 1.1)
    assert_equal(result.success, True, '清仓')

    result = ctx.order(code, 0.5, 1.1)
    assert_equal(result.success, True, 'buy')

    result = ctx.order(code, 0.9, 1.1)
    assert_equal(result.success, True, 'buy')

    result = ctx.order(code, 1.25, 1.1)
    assert_equal(result.success, False, '仓位超出100%')

    result = ctx.order(code, 0.9, 1.1)
    assert_equal(result.success, False, '上一个操作没成功，仓位应该没变化，所以这一次操作也不应该成功')

    ctx.order(code, 0, 1.1)
    assert_equal(ctx.init_cash, ctx.cash, '以买入价清仓，现金应该保持不变')




