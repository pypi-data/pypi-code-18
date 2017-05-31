#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2017 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from argparse import ArgumentParser
import quizlight.quiz
import quizlight.review
import quizlight.edit
from quizlight import __version__
import lightcli



def parse_args():
    """set config options"""
    
    parser = ArgumentParser()

    parser.add_argument('--version', action='version',
            version='%(prog)s ' + str(__version__))
    parser.add_argument('-d', action='store',
            default='/usr/share/doc/lightcli/modules', dest='directory',
            help=('set the module import directory'))
    parser.add_argument('--learn', action='store_true', dest='learning',
            help=('turn on learning mode (immediate answer feedback)'))
    parser.add_argument('file', nargs='?',
            help=('set the module import file'))

    args = parser.parse_args()

    return args


def run_quiz(args):
    """Manage quiz taking"""

    filename = quizlight.review.check_save()
    material, total, correct = quizlight.quiz.run_quiz(args)
    quizlight.review.do_review(material, total, correct,
            resultfile=filename)
    


def edit_quiz(args):
    """Manage quiz creation"""

    quizlight.edit.run_edit(args)


def select_mode():
    """Select a mode: quiz/edit"""
    
    args = parse_args()

    print('\n')
    try:
        if args.file:
            run_quiz(args)
        else:
            mode = lightcli.choice_input(prompt='Select a mode (Test/Edit)',
                    options=['t', 'e'], qopt=True)
            if mode == 'e':
                edit_quiz(args)
            else:
                run_quiz(args)
    
    except KeyboardInterrupt:
        print('\n\nSorry, something went wrong.' + \
                '\nThe developer responsible has been sacked.')
    except EOFError:
        print('\n\nSorry, something went wrong.' + \
                '\nThe developer responsible has been sacked.')




def main():
    select_mode()

if __name__ == "__main__":
    select_mode()
