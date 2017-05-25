#!/bin/python
#coding:utf-8
import roomai.abstract
import copy
import logging
import random


from FiveCardStudUtils  import FiveCardStudPokerCard
from FiveCardStudInfo   import FiveCardStudPublicState
from FiveCardStudInfo   import FiveCardStudPersonState
from FiveCardStudInfo   import FiveCardStudPrivateState
from FiveCardStudInfo   import FiveCardStudInfo
from FiveCardStudAction import FiveCardStudAction

class FiveCardStudEnv(roomai.abstract.AbstractEnv):
    def __init__(self):
        self.logger         = roomai.get_logger()
        self.num_players    = 3
        self.chips          = [500 for i in xrange(self.num_players)]
        self.floor_bet      = 10

    def gen_infos(self):
        infos = [FiveCardStudInfo() for i in xrange(self.public_state.num_players)]
        for i in xrange(self.public_state.num_players):
            infos[i].person_state = self.person_states[i].__deepcopy__()
            infos[i].public_state = self.public_state.__deepcopy__()

        return infos

    #@override
    def init(self):
        if FiveCardStudEnv.is_valid_initialization(self) == False:
            pass

        self.public_state   = FiveCardStudPublicState()
        self.private_state  = FiveCardStudPrivateState()
        self.person_states  = [FiveCardStudPersonState() for i in xrange(self.num_players)]


        ## initialize the cards
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(FiveCardStudPokerCard(i, j))
        random.shuffle(allcards)

        ## private_state
        self.private_state.all_hand_cards      = allcards[0: 5 * self.num_players]

        ## public_state
        self.public_state.num_players          = self.num_players
        self.public_state.chips                = self.chips
        self.public_state.second_hand_cards    = self.private_state.all_hand_cards[1*self.num_players:  2 * self.num_players]
        self.public_state.floor_bet            = self.floor_bet
        self.public_state.upper_bet            = min(self.public_state.chips)

        self.public_state.bets                 = [self.public_state.floor_bet for i in xrange(self.num_players)]
        self.public_state.chips                = [self.public_state.chips[i] - self.public_state.floor_bet for i in xrange(self.num_players)]
        self.public_state.max_bet_sofar        = self.public_state.floor_bet
        self.public_state.is_quit              = [False for i in xrange(self.num_players)]
        self.public_state.num_quit             = 0
        self.public_state.is_needed_to_action  = [True for i in xrange(self.num_players)]
        self.public_state.num_needed_to_action = self.num_players
        self.public_state.is_raise             = [False for i in xrange(self.num_players)]
        self.public_state.num_raise            = 0

        self.public_state.round                = 1
        self.public_state.turn                 = FiveCardStudEnv.choose_player_at_begining_of_round(self.public_state)
        self.public_state.is_terminal          = False
        self.public_state.scores               = None

        ## person_state
        for i in xrange(self.num_players):
            self.person_states[i].id = i
            self.person_states[i].first_hand_card  = self.private_state.all_hand_cards[i]
            self.person_states[i].second_hand_card = self.private_state.all_hand_cards[self.num_players+i]
        turn = self.public_state.turn
        self.person_states[turn].available_actions = FiveCardStudEnv.available_actions(self.public_state)

        return self.gen_infos(), self.public_state, self.person_states, self.private_state


    #@override
    def forward(self, action):
        '''
        :param action: 
        :except: throw ValueError when the action is invalid at this time 
        '''
        turn = self.public_state.turn
        if not FiveCardStudEnv.is_action_valid(self.public_state, self.person_states[turn], action):
            self.logger.critical("action=%s is invalid" % (action.get_key()))
            raise ValueError("action=%s is invalid" % (action.get_key()))

        pu = self.public_state
        pe = self.person_states
        pr = self.private_state

        if action.option == FiveCardStudAction.Fold:
            self.action_fold(action)
        elif action.option == FiveCardStudAction.Check:
            self.action_check(action)
        elif action.option == FiveCardStudAction.Call:
            self.action_call(action)
        elif action.option == FiveCardStudAction.Raise:
            self.action_raise(action)
        elif action.option == FiveCardStudAction.Showhand:
            self.action_showhand(action)
        elif action.option == FiveCardStudAction.Bet:
            self.action_bet(action)
        else:
            raise Exception("action.option(%s) not in [Fold, Check_, Call, Raise, Showhand, Bet]" % (action.option))
        pu.previous_id     = pu.turn
        pu.previous_action = action
        pu.previous_round  = pu.round

        # computing_score
        if FiveCardStudEnv.is_compute_scores(self.public_state):
            num_players          = pu.num_players
            pu.first_hand_cards  = pr.all_hand_cards[0:                1 * num_players]
            pu.second_hand_cards = pr.all_hand_cards[1 * num_players:  2 * num_players]
            pu.third_hand_cards  = pr.all_hand_cards[2 * num_players:  3 * num_players]
            pu.fourth_hand_cards = pr.all_hand_cards[3 * num_players:  4 * num_players]
            pu.fifth_hand_cards  = pr.all_hand_cards[4 * num_players:  5 * num_players]
            pu.round             = 4

            pu.is_terminal = True
            pu.scores      = self.compute_scores(pu)

            for i in xrange(num_players):
                pu.chips[i] += pu.bets[i] + pu.scores[i]

            for i in xrange(num_players):
                pe[i].first_hand_card  = pr.all_hand_cards[0 * num_players + i]
                pe[i].second_hand_card = pr.all_hand_cards[1 * num_players + i]
                pe[i].third_hand_card  = pr.all_hand_cards[2 * num_players + i]
                pe[i].fourth_hand_card = pr.all_hand_cards[3 * num_players + i]
                pe[i].fifth_hand_card  = pr.all_hand_cards[4 * num_players + i]

            pu.turn                              = None
            pe[pu.previous_id].available_actions = None

        # enter into the next stage
        elif FiveCardStudEnv.is_nextround(self.public_state):
            num_players = self.public_state.num_players
            add_cards   = []
            if pu.round == 1:
                pu.third_hand_cards        = pr.all_hand_cards[2 * num_players:  3 * num_players]
                for i in xrange(num_players):
                    pe[i].third_hand_card  = pr.all_hand_cards[2 * num_players + i]
            if pu.round == 2:
                pu.fourth_hand_cards       = pr.all_hand_cards[3 * num_players:  4 * num_players]
                for i in xrange(num_players):
                    pe[i].fourth_hand_card = pr.all_hand_cards[3 * num_players + i]
            if pu.round == 3:
                pu.fifth_hand_cards        = pr.all_hand_cards[4 * num_players:  5 * num_players]
                for i in xrange(num_players):
                    pe[i].fifth_hand_card  = pr.all_hand_cards[4 * num_players + i]


            pu.round                = pu.round + 1
            pu.turn                 = FiveCardStudEnv.choose_player_at_begining_of_round(pu)
            pu.is_needed_to_action  = [True for i in xrange(pu.num_players)]
            pu.num_needed_to_action = self.public_state.num_players
            pu.is_raise             = [False for i in xrange(pu.num_players)]
            pu.num_raise            = 0

            pe[pu.previous_id].available_actions = None
            pe[pu.turn].available_actions        = self.available_actions(pu)

        else:
            pu.turn                              = self.next_player(pu)
            pe[pu.previous_id].available_actions = None
            pe[pu.turn].available_actions        = self.available_actions(pu)


        infos                                = self.gen_infos()


        return infos, self.public_state, self.person_states, self.private_state

    #@override
    @classmethod
    def compete(cls, env, players):
        total_scores = [0 for i in xrange(len(players))]
        total_count    = 1000

        for count in xrange(total_count):
            env.chips       = [(100 +random.random()*500) for i in xrange(len(players))]
            env.num_players = len(players)
            env.floor_bet   = 10
            infos, public, persons, private = env.init()
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

            while public.is_terminal == False:
                turn = public.turn
                action = players[turn].take_action()
                infos, public, persons, private = env.forward(action)
                for i in xrange(len(players)):
                    players[i].receive_info(infos[i])

            for i in xrange(len(players)):
                players[i].reset()
                total_scores[i] += public.scores[i]


            if (count + 1)%500 == 0:
                tmp_scores = [0 for i in xrange(len(total_scores))]
                for i in xrange(len(total_scores)):
                    tmp_scores[i] = total_scores[i] / (count+1)
                roomai.get_logger().info("FiveCardStud completes %d competitions, scores=%s"%(count+1, ",".join([str(i) for i in tmp_scores])))

        for i in xrange(len(players)):
            total_scores[i]   /= total_count * 1.0

        return total_scores;


    def action_fold(self, action):
        pu = self.public_state
        pu.is_quit[pu.turn] = True
        pu.num_quit        += 1

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_check(self, action):
        pu = self.public_state
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_call(self, action):
        pu = self.public_state
        pu.chips[pu.turn]               -= action.price
        pu.bets[pu.turn]                += action.price
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1


    def action_bet(self, action):
        pu = self.public_state

        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet_sofar   = pu.bets[pu.turn]

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        p = (pu.turn + 1)%pu.num_players
        while p != pu.turn:
            if  pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                pu.num_needed_to_action   += 1
                pu.is_needed_to_action[p]  = True
            p = (p + 1) % pu.num_players

    def action_raise(self, action):
        pu = self.public_state

        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet_sofar   = pu.bets[pu.turn]

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        pu.is_raise[pu.turn]            = True
        pu.num_raise                   +=1
        p = (pu.turn + 1)%pu.num_players
        while p != pu.turn:
            if pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                pu.num_needed_to_action   += 1
                pu.is_needed_to_action[p]  = True
            p = (p + 1) % pu.num_players


    def action_showhand(self, action):
        pu = self.public_state

        pu.bets[pu.turn]               += action.price
        pu.chips[pu.turn]               = 0

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        if pu.bets[pu.turn] > pu.max_bet_sofar:
            p = (pu.turn + 1) % pu.num_players
            while p != pu.turn:
                if pu.is_quit[p] == False and pu.is_needed_to_action[p] == False and pu.bets[p] < pu.upper_bet:
                    pu.num_needed_to_action  += 1
                    pu.is_needed_to_action[p] = True
                p = (p + 1) % pu.num_players

            pu.is_raise[pu.turn] = True
            pu.max_bet_sofar     = pu.bets[pu.turn]
            pu.num_raise         = False

############################################# Utils Function ######################################################
    @classmethod
    def is_valid_initialization(cls, env):
        if len(env.chips) != env.num_players:
            raise ValueError("len(env.chips)%d != env.num_players%d"%(len(env.chips), env.num_players))

        if env.num_players * 5 > 52:
            raise ValueError("env.num_players * 5 must be less than 51, now env.num_players = %d"%(env.num_players))

        return True

    @classmethod
    def is_compute_scores(cls, public_state):
        pu = public_state
        if pu.round == 4 and pu.num_needed_to_action == 0:
            return True
        if pu.num_needed_to_action == 0 and pu.max_bet_sofar == pu.upper_bet:
            return True

        return False

    @classmethod
    def compute_scores(cls, public_state):
        max_cards = [public_state.first_hand_cards[0],\
                     public_state.second_hand_cards[0], public_state.third_hand_cards[0],\
                     public_state.fourth_hand_cards[0], public_state.fifth_hand_cards[0]]
        max_id    = 0
        for i in xrange(1, public_state.num_players):
            tmp = [public_state.first_hand_cards[i],\
                   public_state.second_hand_cards[i], public_state.third_hand_cards[i],\
                   public_state.fourth_hand_cards[i], public_state.fifth_hand_cards[i]]
            if FiveCardStudEnv.compare_cards(max_cards, tmp) < 0:
                max_cards = tmp
                max_id    = i
     
        scores = [0 for i in xrange(public_state.num_players)]
        for i in xrange(public_state.num_players):
            if i == max_id:
                scores[i] = sum(public_state.bets) - public_state.bets[i]
            else:
                scores[i] = -public_state.bets[i]
        for i in xrange(public_state.num_players):
            scores[i]    /= public_state.floor_bet * 1.0

        return scores

    @classmethod
    def choose_player_at_begining_of_round(cls, public_state):

        round = public_state.round
        if round in [1,2,3]:
            public_cards = None
            if   round == 1: public_cards = public_state.second_hand_cards
            elif round == 2: public_cards = public_state.third_hand_cards
            elif round == 3: public_cards = public_state.fourth_hand_cards
            max_card = public_cards[0]
            max_id   = 0
            for i in xrange(1, public_state.num_players):
                if FiveCardStudPokerCard.compare(max_card, public_cards[i]) < 0:
                    max_card = public_cards[i]
                    max_id   = i
            return max_id

        elif round == 4:
            max_cards = [public_state.second_hand_cards[0], public_state.third_hand_cards[0],\
                         public_state.fourth_hand_cards[0], public_state.fifth_hand_cards[0]]
            max_id    = 0
            for i in xrange(1, public_state.num_players):
                tmp = [public_state.second_hand_cards[i], public_state.third_hand_cards[i], \
                       public_state.fourth_hand_cards[i], public_state.fifth_hand_cards[i]]
                if FiveCardStudEnv.compare_cards(max_cards, tmp) < 0:
                    max_cards = tmp
                    max_id    = i
            return max_id

        else:
            raise ValueError("pulic_state.round(%d) not in [1,2,3,4]"%(public_state.turn))

    @classmethod
    def next_player(self, pu):
        i = pu.turn
        if pu.num_needed_to_action == 0:
            return -1

        p = (i+1)%pu.num_players
        while pu.is_needed_to_action[p] == False:
            p = (p+1)%pu.num_players
        return p

    @classmethod
    def is_action_valid(cls, public_state, person_state, action):
        if action.get_key() not in person_state.available_actions:
            return False
        return True

    @classmethod
    def available_actions(cls, public_state):
        pu             = public_state
        round          = pu.round
        turn           = pu.turn
        Showhandcount = pu.upper_bet - pu.bets[turn]
        Call_count     = pu.max_bet_sofar - pu.bets[turn]

        actions = dict()
        if round  == 1 or round == 2 or round == 3:
            if pu.previous_round is None or pu.previous_round == round -1:
                ## bet
                for i in xrange(int(pu.bets[turn]+1), int(pu.upper_bet-pu.bets[turn])):
                    actions["Bet_%d"%i]                 = FiveCardStudAction("Bet_%d"%i)
                ## fold
                actions["Fold_0"]                       = FiveCardStudAction("Fold_0")
                ## showhand
                actions["Showhand_%d"%(Showhandcount)] = FiveCardStudAction("Showhand_%d"%Showhandcount)
                ## Check_
                actions["Check_0"]                      = FiveCardStudAction("Check_0")
            else:
                ## fold
                actions["Fold_0"]                       = FiveCardStudAction("Fold_0")
                ## showhand
                actions["Showhand_%d"%Showhandcount]   = FiveCardStudAction("Showhand_%d"%(Showhandcount))
                ## Call
                if Call_count  < Showhandcount:
                    if Call_count == 0:
                        actions["Check_0"]                 = FiveCardStudAction("Check_0")
                    else:
                        actions["Call_%d"%(Call_count )]   = FiveCardStudAction("Call_%d"%(Call_count))
                ## "raise"
                if pu.is_raise[turn] == False:
                    for i in xrange(int(Call_count + 1),int(Showhandcount)):
                        actions["Raise_%d"%(i)] = FiveCardStudAction("Raise_%d"%i)


        elif round == 4:
            if pu.previous_round == round - 1:
                ## showhand
                actions["Showhand_%d"%(Showhandcount)] = FiveCardStudAction("Showhand_%d"%(Showhandcount))
                ## bet
                for i in xrange(1, int(pu.upper_bet) - int(pu.bets[turn])):
                    actions["Bet_%d"%i] = FiveCardStudAction("Bet_%d"%i)
                ## fold
                actions["Fold_0"]     = FiveCardStudAction("Fold_0")

            else:
                ## fold
                actions["Fold_0"]     = FiveCardStudAction("Fold_0")
                ## Call
                if Call_count  == Showhandcount:
                    actions["Showhand_%d"%(Call_count)]       = FiveCardStudAction("Showhand_%d"%(Call_count))
                elif Call_count == 0:
                    actions["Check_0"]                        = FiveCardStudAction("Check_0")
                else:
                    actions["Call_%d"%(Call_count )]          = FiveCardStudAction("Call_%d"%(Call_count))

        else:
            raise ValueError("pulic_state.round(%d) not in [1,2,3,4]" % (public_state.turn))

        return actions

    @classmethod
    def is_nextround(self, public_state):
        '''
        :return: 
        A boolean variable indicates whether is it time to enter the next stage
        '''
        return public_state.num_needed_to_action == 0

    @classmethod
    def compare_cards(cls, cards1, cards2):
        if len(cards1) == len(cards2) and len(cards1) == 4:
            pattern1 = cls.fourcards2pattern(cards1)
            pattern2 = cls.fourcards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(FiveCardStudPokerCard.compare)
                cards2.sort(FiveCardStudPokerCard.compare)
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        elif len(cards1) == len(cards2) and len(cards1) == 5:
            pattern1 = cls.cards2pattern(cards1)
            pattern2 = cls.cards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(FiveCardStudPokerCard.compare)
                cards2.sort(FiveCardStudPokerCard.compare)
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        else:
            raise  ValueError("len(cards1)%d, and len(cards2)%d are same and are 4 or 5 "%(len(cards1),len(cards2)))

    @classmethod
    def cards2pattern(cls, cards):
        pointrank2cards = dict()
        for c in cards:
            if c.get_point_rank() in pointrank2cards:
                pointrank2cards[c.get_point_rank()].append(c)
            else:
                pointrank2cards[c.get_point_rank()] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(FiveCardStudPokerCard.compare)

        suitrank2cards = dict()
        for c in cards:
            if c.get_suit_rank() in suitrank2cards:
                suitrank2cards[c.get_suit_rank()].append(c)
            else:
                suitrank2cards[c.get_suit_rank()] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(FiveCardStudPokerCard.compare)

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in xrange(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].get_point_rank() == suitrank2cards[s][i + 1].get_point_rank() - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) ==1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["4_1"]
            return pattern

        ##3_2
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_pointrank[p]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.FiveCardStudAllCardsPattern["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return  roomai.fivecardstud.FiveCardStudAllCardsPattern["1_1_1_1_1"]

    @classmethod
    def fourcards2pattern(cls, cards):
        pointrank2cards = dict()
        for c in cards:
            if c.get_point_rank() in pointrank2cards:
                pointrank2cards[c.get_point_rank()].append(c)
            else:
                pointrank2cards[c.get_point_rank()] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(FiveCardStudPokerCard.compare)

        suitrank2cards = dict()
        for c in cards:
            if c.get_suit_rank() in suitrank2cards:
                suitrank2cards[c.get_suit_rank()].append(c)
            else:
                suitrank2cards[c.get_suit_rank()] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(FiveCardStudPokerCard.compare)

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in xrange(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##candidate straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 4:
                numStraight = 1
                for i in xrange(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].get_point_rank() == suitrank2cards[s][i + 1].get_point_rank()  - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 4:
                        pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["4_1"]
            return pattern

        ##3_2 impossible
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 4:
                pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 4:
                pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["Straight_DiffSuit"]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.FiveCardStudAllCardsPattern["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return roomai.fivecardstud.FiveCardStudAllCardsPattern["1_1_1_1_1"]
