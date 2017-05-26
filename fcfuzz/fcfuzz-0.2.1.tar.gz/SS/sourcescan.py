#!/usr/bin/env python3

# @author: Ian Guibas
# This library does a simple quick scan of C source code
# and looks for potentially dangerous snippets. Due to certain
# aspects of computing, there is non-deterministic behaviour in
# identifying particular program features. I have opted to simply
# ensure some simple mistakes are avoided here.

import re
import os
import sys

# Used for short circuit logic
class ShortCircuit(Exception):
    pass

INSECURE = {'gets':0,
            'scanf':1,
            'sprintf':2,
            'strcpy':3,
            'strcat':4,
            'tmpfile':5,
            'mktemp':5
            }

ALTERNATIVES = {0:'fgets using standard input as the file stream',
                1:'fgets for input then sscanf for parsing',
                2:'snprintf',
                3:'strncpy or strndup',
                4:'strncat',
                5:'mkstemp',
               }

REASONS = { 0:'gets is deprecated and completely unbounded. It will ALWAYS' +
              'lead to a buffer overflow and instability.',
            1:'scanf does no bounds checking and can lead to a buffer ' +
              'overflow.',
            2:'sprintf does no bounds checking on the destination buffer ' +
              'which can lead to buffer overflows and instability.',
            3:'strcpy does not check that the source string fits into the ' +
              'destination buffer which can lead to buffer overflows. ' +
              'As an aside, strncpy may not provide the most efficient ' +
              'behavior, depending upon the size of the source and ' +
              'destination buffers.',
            4:'strcat does not check that the total length does not exceed ' +
              'the buffer size of the destination leading to buffer overflows.',
            5:'tmpfile and mktemp often do not set the correct permissions ' +
              'on the temporary files they create leading to potential ' +
              'information leaks and/or undefined behaviour based upon ' +
              'how the files get used.'}

              
def color(text, color, BOLD=False):
    """ANSI Sequence wrapper for text, colorizes output"""
    ANSI_PREFIX = '\x1b['
    ANSI_ENDS = '\x1b[0m'
    ANSI_COLORS_FOREGROUND = {
        'black'   : ANSI_PREFIX + '90m',
        'red'     : ANSI_PREFIX + '91m',
        'green'   : ANSI_PREFIX + '92m',
        'yellow'  : ANSI_PREFIX + '93m',
        'blue'    : ANSI_PREFIX + '94m',
        'magenta' : ANSI_PREFIX + '95m',
        'cyan'    : ANSI_PREFIX + '96m',
        'white'   : ANSI_PREFIX + '97m'
    }

    if color.lower() in ANSI_COLORS_FOREGROUND.keys():
        colored = ANSI_COLORS_FOREGROUND[color] + text + ANSI_ENDS
        if BOLD:
            colored = '\x1b[1m' + colored
        return colored
    
    else: return text

class scanner:
    """Scan source code for bad calls.
    Requires path to source file to scan""" 

    def __init__(self, src):
        with open(src,'r') as f:
            self.source = f.readlines()
    
    def scan(self):
        
        # REGULAR EXPRESSIONS
        r_gets = re.compile(r'\s*gets\(.*\);')
        r_scanf = re.compile(r'\s*scanf\(.*\);')
        r_sprintf = re.compile(r'\s*sprintf\(.*\);')
        r_strcpy = re.compile(r'\s*strcpy\(.*\);')
        r_strcat = re.compile(r'\s*strcat\(.*\);')
        r_tmpfile = re.compile(r'\s*tmpfile\(.*\);')
        r_mktemp = re.compile(r'\s*mktemp\(.*\);')
        r_badprintf = re.compile(r'\s*printf\([a-zA-Z].*')
        
        print('Scanning...')
        print()

        DANGER = '\x1b[41m\x1b[1mDANGER\x1b[0m '
        WARN   = '\x1b[45m\x1b[1mwarning\x1b[0m '

        lineno = 0
        for line in self.source:
            lineno += 1
            try:
                if r_gets.match(line):
                    code = INSECURE['gets']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(DANGER, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('gets()','red'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_scanf.match(line): 
                    code = INSECURE['scanf']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('scanf()','green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_sprintf.match(line): 
                    code = INSECURE['sprintf']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('sprintf()', 'green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_strcpy.match(line):
                    code = INSECURE['strcpy']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('strcpy()','green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit
                
                if r_strcat.match(line):
                    code = INSECURE['strcat']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('strcat()','green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_tmpfile.match(line):
                    code = INSECURE['tmpfile']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('tmpfile()','green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_mktemp.match(line):
                    code = INSECURE['mktemp']
                    alternative = ALTERNATIVES[code]
                    reason = REASONS[code]
                    print(WARN, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('mktemp()','green'))
                    print('Possible replacement: {0}'.format(alternative))
                    print('Reason: {0}'.format(reason))
                    raise ShortCircuit

                if r_badprintf.match(line):
                    print(DANGER, end='')
                    print(color('Line {}: '.format(lineno),'red',True),end=' ')
                    print('Found ' + color('printf(var)','red',True))
                    print('Possible replacement: puts(var)')
                    print('Reason: User input should never be passed directly '+
                          'to a format string function as printf makes ' +
                          'no distinction between a user string and format ' +
                          'string. This allows a user to specify formats to ' +
                          'both leak and modify the program memory as well ' +
                          'as hijack control flow and undermine various ' +
                          'security methods such as ASLR and Canary.')
                    # No need to short circuit at end

            # No need to evaluate line for all RE's, stop on first match
            except ShortCircuit:
                print()
                pass

    def view_source(self):
        '''Attempts to view the source code in a human readable manner'''

        lineno = 1
        for line in self.source:
            line = line.replace('\n','')
            print(str(lineno) + '\t' + line)
            lineno += 1

