from .Context import *

def run(StrategyWillBeBackTest, data_provider, start_date, end_date):

    ctx = Context(None, data_provider)
    strategy = StrategyWillBeBackTest(ctx)

    pass