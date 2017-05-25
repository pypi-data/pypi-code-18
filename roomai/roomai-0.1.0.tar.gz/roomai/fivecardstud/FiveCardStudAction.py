#!/bin/python
#coding:utf-8
import roomai.abstract


class FiveCardStudAction(roomai.abstract.AbstractAction):

    # 弃牌
    Fold        = "Fold"
    # 过牌
    Check       = "Check"
    # 更注
    Call        = "Call"
    # 加注
    Raise       = "Raise"
    # 下注
    Bet         = "Bet"
    # all in
    Showhand    = "Showhand"

    def __init__(self,key):
        opt_price = key.strip().split("_")
        if  opt_price[0] != self.Fold    and opt_price[0] != self.Call  and \
            opt_price[0] != self.Check   and opt_price[0] != self.Raise and \
            opt_price[0] != self.Bet     and opt_price[0] != self.Showhand:
            raise  ValueError("%s is an invalid key. The Option must be in [Fold,Check,Call,Raise,Bet,Showhand]"%key)

        self.option = opt_price[0]
        self.price  = int(opt_price[1])
        self.String = "%s_%d"%(self.option, self.price)

    def get_key(self):
        return self.String


    def __deepcopy__(self, memodict={}):
        copyinstnce = FiveCardStudAction(self.String)
        return copyinstnce
