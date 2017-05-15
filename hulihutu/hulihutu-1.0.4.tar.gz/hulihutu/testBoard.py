#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
from main import Tictac
a = Tictac()
a.play(0, 0)
a.printBoard()
a.play(0, 1)
a.play(0, 2)
a.printBoard()
a.play(1, 0)
a.play(1, 1)
a.play(1, 2)
a.printBoard()
a.play(2, 0)
a.play(2, 1)
winner = a.play(2, 2)
a.printBoard()
print winner

# reset game
a.reset()

#
