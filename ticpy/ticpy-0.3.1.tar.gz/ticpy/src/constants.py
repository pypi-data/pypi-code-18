"""
This module stores all the constants used in the Game libraries
Bunch library is used to access dictionary key-value as an object's attribute.
"""
from bunch import Bunch

GAME_STATE = Bunch({'PLAYING': 0,
                    'DRAW': 1,
                    'CROSS_WON': 2,
                    'NOUGHT_WON': 3
                    })

current_state = GAME_STATE.PLAYING

SEED = Bunch({
    'EMPTY': 0,
    'CROSS': 1,
    'NOUGHT': 2
})

# String representation for seed types
SEED_REPR = [' ', 'X', 'O']


def get_player_name(seed):
    """
    :param seed: (int) Seed attribute  
    :return: (string) string representation of seed attribute
    """
    return SEED_REPR[seed]
