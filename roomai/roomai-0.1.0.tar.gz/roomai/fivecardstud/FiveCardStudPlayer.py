#!/bin/python
import roomai.abstract
import random

class FiveCardStudRandomPlayer(roomai.abstract.AbstractPlayer):

    available_actions = None
    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        actions = self.available_actions.values()
        idx     = int(random.random() * len(actions))
        return actions[idx]

    def reset(self):
        pass
