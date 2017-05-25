#!/bin/python
#coding:utf-8

import roomai.abstract
import copy

class StageSpace:
    firstStage  = 1
    secondStage = 2
    thirdStage  = 3
    fourthStage = 4


class TexasHoldemAction(roomai.abstract.AbstractAction):
    # 弃牌
    Fold        = "fold"
    # 过牌
    Check       = "check"
    # 更注
    Call        = "call"
    # 加注
    Raise       = "raise"
    # all in
    AllIn       = "allin"
    def __init__(self, key):
        opt_price = key.strip().split("_")
        self.option = opt_price[0]
        self.price  = int(opt_price[1])
        self.String = "%s_%d"%(self.option, self.price)
    def get_key(self):
        return self.String

    def __deepcopy__(self, memodict={}):
        return TexasHoldemAction(self.String)

class TexasHoldemPublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.num_players        = None
        self.big_blind_bet      = None

        #state of players
        self.is_quit                        = None
        self.num_quit                       = None
        self.is_allin                       = None
        self.num_allin                      = None
        self.is_needed_to_action            = None
        self.num_needed_to_action           = None

        # who is expected to take a action
        self.turn               = None

        #chips is array which contains the chips of all players
        self.chips              = None

        #bets is array which contains the bets from all players
        self.bets               = None

        #max_bet = max(self.bets)
        self.max_bet_sofar      = None
        #the raise acount
        self.raise_account      = None

        self.previous_id        = None
        self.previous_action    = None

    def __deepcopy__(self, memodict={}):
            copyinstance = TexasHoldemPublicState()

            copyinstance.stage         = self.stage
            copyinstance.num_players   = self.num_players
            copyinstance.dealer_id     = self.dealer_id
            copyinstance.big_blind_bet = self.big_blind_bet

            if self.public_cards is None:
                copyinstance.public_cards = None
            else:
                copyinstance.public_cards = [self.public_cards[i].__deepcopy__() for i in xrange(len(self.public_cards))]


            ######## quit, allin , needed_to_action
            copy.num_quit = self.num_quit
            if self.is_quit is None:
                copyinstance.is_quit = None
            else:
                copyinstance.is_quit = [self.is_quit[i] for i in xrange(len(self.is_quit))]

            copyinstance.num_allin = self.num_allin
            if self.is_allin is None:
                copyinstance.is_allin = None
            else:
                copyinstance.is_allin = [self.is_allin[i] for i in xrange(len(self.is_allin))]

            copyinstance.num_needed_to_action = self.num_needed_to_action
            if self.is_needed_to_action is None:
                copyinstance.is_needed_to_action = None
            else:
                copyinstance.is_needed_to_action = [self.is_needed_to_action[i] for i in
                                                    xrange(len(self.is_needed_to_action))]

            # chips is array which contains the chips of all players
            if self.chips is None:
                copyinstance.chips = None
            else:
                copyinstance.chips = [self.chips[i] for i in xrange(len(self.chips))]

            # bets is array which contains the bets from all players
            if self.bets is None:
                copyinstance.bets = None
            else:
                copyinstance.bets = [self.bets[i] for i in xrange(len(self.bets))]

            copyinstance.max_bet_sofar = self.max_bet_sofar
            copyinstance.raise_account = self.raise_account
            copyinstance.turn = self.turn

            copyinstance.previous_id = self.previous_id
            if self.previous_action is None:
                copyinstance.previous_action = None
            else:
                copyinstance.previous_action = self.previous_action.__deepcopy__()

            ### isterminal, scores
            copyinstance.is_terminal = self.is_terminal
            if self.scores is None:
                copyinstance.scores = None
            else:
                copyinstance.scores = [self.scores[i] for i in xrange(len(self.scores))]

            return copyinstance


class TexasHoldemPrivateState(roomai.abstract.AbstractPrivateState):
    keep_cards = None
    hand_cards = None


class TexasHoldemPersonState(roomai.abstract.AbsractPersonState):
    id                =    None
    hand_cards        =    None
    available_actions =    None

    def __deepcopy__(self, memodict={}):
        copyinstance    = TexasHoldemPersonState()
        copyinstance.id = self.id
        if self.hand_cards is not None:
            copyinstance.hand_cards = [self.hand_cards[i].__deepcopy__() for i in xrange(len(self.hand_cards))]
        else:
            copyinstance.hand_cards = None

        if self.available_actions is not None:
            copyinstance.available_actions = dict()
            for key in self.available_actions:
                copyinstance.available_actions[key] = self.available_actions[key].__deepcopy__()
        else:
            copyinstance.available_actions = None
        return copyinstance

class TexasHoldemInfo(roomai.abstract.AbstractInfo):
    public_state            = None
    person_state            = None

    def __deepcopy__(self, memodict={}):
        info = TexasHoldemInfo()
        info.public_state = self.public_state.__deepcopy__()
        info.public_state = self.person_state.__deepcopy__()
        return info


AllCardsPattern = dict()
#0     1           2       3           4                                    5     6
#name, isStraight, isPair, isSameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [],        100, []]
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1],     98,  []]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2],     97,  []]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [],        96,  []]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [],        95,  []]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1],   94,  []]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1],   93,  []]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1], 92,  []]
AllCardsPattern["1_1_1_1_1"] = \
["1_1_1_1_1",           False, True,  False, [1,1,1,1,1],91, []]




