#_MIT License
#_
#_Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)
#_
#_Permission is hereby granted, free of charge, to any person obtaining a copy
#_of this software and associated documentation files (the "Software"), to deal
#_in the Software without restriction, including without limitation the rights
#_to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#_copies of the Software, and to permit persons to whom the Software is
#_furnished to do so, subject to the following conditions:
#_
#_The above copyright notice and this permission notice shall be included in all
#_copies or substantial portions of the Software.
#_
#_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#_IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#_FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#_AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#_LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#_OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#_SOFTWARE.

# lightcli
# A lightweight terminal interaction library for Python.


import os
import time

__version__ = '1.0'



def choice_input(options=[], prompt='Press ENTER to continue.', 
        showopts=True, qopt=False):
    """Get input from a list of choices (q to quit)"""

    choice = None
    if showopts:
        prompt = prompt + ' ' + str(options)
    if qopt:
        prompt = prompt + ' (q to quit)'
    
    while not choice:
        try:
            choice = str(input(prompt + ' '))
        except SyntaxError:
            if options == []:
                pass
        if choice:
            if choice in options:
                return choice
            elif qopt == True and choice == 'q':
                choice = None
                is_sure = input('Are you sure you want to quit? ')
                if is_sure in ('Y', 'y', 'yes'):
                    exit('\nThanks for playing. Goodbye.\n')
            elif options == []:
                return 0
            else:
                print('Answer must be one of ' + str(options) +
                        '. Your answer?')
                if options:
                    choice = None
        elif options == []:
            return 0
        else:
            print('Answer must be one of ' + str(options) + 
                    '. Your answer?')



def long_input(prompt='Multi-line input\n' + \
        'Enter EOF on a blank line to end ' + \
        '(ctrl-D in *nix, ctrl-Z in windows)',
        maxlines = None, maxlength = None):
    """Get a multi-line string as input"""
    
    lines = []
    print(prompt)
    lnum = 1

    try:
        while True:
            
            if maxlines:
            
                if lnum > maxlines:
                    break
                
                else:
                    if maxlength:
                        lines.append(str(input(''))[:maxlength])
                    else:
                        lines.append(str(input('')))
                    lnum += 1
            
            else:
                if maxlength:
                    lines.append(str(input(''))[:maxlength])
                else:
                    lines.append(str(input('')))

    except EOFError:
        pass
    finally:
        return '\n'.join(lines)



def list_input(prompt='List input - enter each item on a seperate line\n' + \
        'Enter EOF on a blank line to end ' + \
        '(ctrl-D in *nix, ctrl-Z in windows)',
        maxitems=None, maxlength=None):
    """Get a list of strings as input"""
    
    lines = []
    print(prompt)
    inum = 1

    try:

        while True:
        
            if maxitems:
            
                if inum > maxitems:
                    break
                else:
                    if maxlength:
                        lines.append(str(input(''))[:maxlength])
                    else:
                        lines.append(str(input('')))
                    inum += 1
            
            else:
                if maxlength:
                    lines.append(str(input(''))[:maxlength])
                else:
                    lines.append(str(input('')))

    except EOFError:
        pass
    finally:
        return lines


def outfile_input(extension=None):
    """Get an output file name as input"""
    
    fileok = False
    
    while not fileok:
        filename = str(input('File name? '))
        if extension:
            if not filename.endswith(extension):
                if extension.startswith('.'):
                    filename = filename + extension
                else:
                    filename = filename + '.' + extension
        if os.path.isfile(filename):
            choice = choice_input(prompt=filename + \
                    ' already exists. Overwrite?',
                    options=['y', 'n'])
            if choice == 'y':
                try:
                    nowtime = time.time()
                    with open(filename, 'a') as f:
                        os.utime(filename, (nowtime, nowtime))
                    fileok = True
                except IOError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')
                except PermissionError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')
                except FileNotFoundError:
                    print(filename + ': directory not found. Try again.')

        else:
            choice = choice_input(
                    prompt=filename + ' does not exist. Create it?',
                    options=['y', 'n'])
            if choice == 'y':
                try:
                    nowtime = time.time()
                    with open(filename, 'w') as f:
                        os.utime(filename, (nowtime, nowtime))
                    fileok = True
                except IOError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')
                except PermissionError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')
                except FileNotFoundError:
                    print(filename + ': directory not found. Try again.')

    return filename
