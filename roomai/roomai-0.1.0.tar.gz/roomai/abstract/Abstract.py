#!/bin/python
#coding=utf8

######################################################################### Basic Concepts #####################################################
class AbstractPublicState:
    turn            = None
    previous_id     = None
    previous_action = None

    is_terminal     = False
    scores          = None

class AbstractPrivateState:
    pass

class AbsractPersonState:
    id                = None
    available_actions = None

class AbstractInfo:
    public_state       = None
    person_state       = None

class AbstractAction:
    def __init__(self, key):
        raise NotImplementedError("The __init__ function hasn't been implemented")

    def get_key(self):
        '''
        :return:
            key: action's key 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The get_key function hasn't been implemented")

class AbstractPlayer:

    def receive_info(self, info):
        '''
        :param:
            info: the information produced by a game environments 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        '''
        :return: A Action produced by this player
        '''
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")


class AbstractEnv:

    def init(self):
        raise NotImplementedError("The init function hasn't been implemented")

    def forward(self, action):
        raise NotImplementedError("The receiveAction hasn't been implemented")

    @classmethod
    def compete(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")

############################################################### Some Utils ############################################################################

point_str_to_key  = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12, 'r':13, 'R':14}
point_key_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A', 13:'r', 14:'R'}
suit_key_to_str  = {0: 'Spade', 1: 'Heart', 2: 'Diamond', 3: 'Club'}
suit_str_to_key   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3}

class PokerCard:
    def __init__(self, point, suit = None):
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_key[kv[0]]
            suit1  = suit_str_to_key[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_key[point]
            suit1  = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_key[suit]

        self.point_str = point_key_to_str[point1]
        self.suit_str  = suit_key_to_str[suit1]
        self.String = "%s_%s"%(self.point_str, self.suit_str)

    def get_key(self):
        return self.String

    def get_point_rank(self):
        return point_str_to_key[self.point_str]

    def get_suit_rank(self):
        return suit_str_to_key[self.suit_str]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        pr1 = pokercard1.get_point_rank()
        pr2 = pokercard2.get_point_rank()

        if pr1 != pr2:
            return pr1 - pr2
        else:
            return pokercard1.get_suit_rank() - pokercard2.get_suit_rank()
    def __deepcopy__(self, memodict={}):
        copyinstance = PokerCard(self.point_str, self.suit_str)
        return copyinstance