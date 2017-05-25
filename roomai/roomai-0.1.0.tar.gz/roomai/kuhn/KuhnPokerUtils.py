#!/bin/python
import random
import math
import roomai.abstract
import copy


class KuhnPokerAction(roomai.abstract.AbstractAction):
    bet   = 0;
    check = 1;
    def __init__(self, key):
        self.action = ""
        if key == "bet": self.action = KuhnPokerAction.bet
        elif key == "check":self.action = KuhnPokerAction.check
        else:
            raise KeyError("%s is invalid key for Kuhn Action"%(key))

    def get_key(self):
        if self.action == KuhnPokerAction.bet:
            return "bet"
        else:
            return "check"


class KuhnPokerPublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.turn                       = 0
        self.first                      = 0
        self.epoch                      = 0
        self.action_list                = []

class KuhnPokerPrivateState(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.hand_cards = []

class KuhnPokerPersonState(roomai.abstract.AbsractPersonState):
    def __init__(self):
        self.available_actions  = None
        self.id                 = None
        self.card               = None

class KuhnPokerInfo(roomai.abstract.AbstractInfo):
    public_state       = None
    person_state       = None

    def __deepcopy__(self, memodict={}):
        info = KuhnPokerInfo()
        info.public_state = copy.deepcopy(self.public_state)
        info.public_state = copy.deepcopy(self.person_state)
        return info