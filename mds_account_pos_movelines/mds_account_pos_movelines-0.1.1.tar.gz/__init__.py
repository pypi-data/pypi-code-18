# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .account import AccountMoveLine

def register():
    Pool.register(
        AccountMoveLine,
        module='account_pos_movelines', type_='model')
