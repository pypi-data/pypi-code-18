from mdp import *
from tictac import Tictac

tictac = Tictac()
db = DB()
policy = Policy(gamma=0.9, tao=0.01, db=db, default_value = 0)
for i in range(100000):
    print i
    while tictac.ended != True:
        if tictac.color == 1:
            (action, value, move) = tictac.apply_policy(policy.pai, 'max')
        else:
            (action, value, move) = tictac.apply_policy(policy.pai, 'min')
        # print(action)
        db.update_value(tictac.board, value)
        tictac.play(action)
        # tictac.print_board()
    # tictac.print_board()
    tictac.reset()
