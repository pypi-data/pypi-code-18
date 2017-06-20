from src.roda import *

class StrategyKd(Strategy):
    def __init__(self, ctx):
        ctx.benchmark = 'FHN'
    def handle_bar(self, context):
        code = 'FHN'

#asap