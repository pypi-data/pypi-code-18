#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import textwrap
import math


level = 0
has_header = False
line_length = 70

def header(str):
    global has_header
    if has_header:
        return subheader(str)
    has_header = True
    side = '-' * (int((line_length - 8) / 2) - math.ceil(len(str) / 2))
    print('\033[93m\033[3m%s=<] %s [>=%s\033[0m' % (side, str, side + ('-' if len(str) % 2 == 1 else '')))

def subheader(str):
    side = ' ' * (int((line_length - 8) / 2) - math.ceil(len(str) / 2))
    print('\033[93m\033[3m%s  [ %s ]\033[0m' % (side, str))

def splitter():
    print('\033[90m\033[3m%s\033[0m' % '-' * line_length)

def output(prefix, str, color='\033[0m'):
    lines = textwrap.wrap(prefix + ' ' + ('| ' * level) + str, line_length)
    print(color + lines[0] + (' ' * (line_length - len(lines[0]))) + '\033[0m')

    for i in range(1, len(lines)):
        print(color + (' ' * (line_length - len(lines[i]))) + lines[i] + '\033[0m')

def info(str):
    output('[i]', str, color='\033[093m')

def cmd(str):
    output('[$]', str, color='')

def doing(str):
    output('[.]', str, color='\033[33m')

def action(str):
    output('[*]', str, color='\033[92m')

def fail(str):
    output('[!]', str, color='\033[41m')

def die(str):
    output('[X]', str, color='\033[41m')
    exit()
