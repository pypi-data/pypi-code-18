# -*- coding: utf-8 -*-

from rqalpha.api import *
from rqalpha import run_func


def init(context):
    context.stock = "000300.XSHG"
    context.counter = 0


def handle_bar(context, bar_dict):
    context.counter += 1
    if context.counter == 1:
        print(111)
        order_target_percent(context.stock, 1)
    elif context.counter == 2:
        print(222)
        order_target_percent(context.stock, 0)


config = {
  "base": {
    "start_date": "2015-12-07",
    "end_date": "2015-12-15",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_accounts": {
      "stock_t1": False
    },
    "sys_analyser": {
      "enabled": True,
      # "plot": True
    },
    "sys_simulation": {
      "matching_type": "next_bar"
    }
  }
}


# 如果你的函数命名是按照 API 规范来，则可以直接按照以下方式来运行
run_func(**globals())
