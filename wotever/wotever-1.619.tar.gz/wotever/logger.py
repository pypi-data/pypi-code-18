import sys
import logging
import time

__version__ = '1.0'

# _colors = dict(black=30, red=31, green=32, yellow=33,blue=34, magenta=35, cyan=36, white=37)
def print_with_color(c, s):
    print "\x1b[%dm%s %s\x1b[0m" % (c,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), s)




def d(str):
    print_with_color(32,str)
def i(str):
    print_with_color(34,str)
def w(str):
    print_with_color(33,str)
def e(str):
    print_with_color(31,str)

