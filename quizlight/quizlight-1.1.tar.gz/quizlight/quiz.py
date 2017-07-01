#!/usr/bin/env python3

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


import os
import json
import lightcli
import quizlight.review



def ask_question(chapt, qnum, question, answer, options, reason, 
        learning=False):
    """Asks a multiple choice question"""

    status = None
    printed_qnum = '======== Question # ' + str(qnum) + ' ========'
    printed_qpr = 'Your answer?'
    printed_q = '\n\n' + printed_qnum + '\n\n' + question + '\n' + \
            printed_qpr
    
    x = lightcli.choice_input(options, prompt=printed_q, qopt=True)
    
    if question.startswith('What is the air speed velocity of an ' + \
            'unladen swallow?') and x == 'd':
        exit('\n' * 10 + 'A'+ 'aaaaaaaaaa' * 20 + 'hh.' + '\n' * 10)
    if x == answer:
        if learning:
            print('Correct!')
            lightcli.choice_input(showopts=False, qopt=True)
        status = 1
    else:
        if learning:
            print('Incorrect! The answer was '+ a + '.')
            if r: print(r)
            lightcli.choice_input(showopts=False, qopt=True)
    
    info = [qnum, question, answer, options, x, reason]
    return status, info


def quiz_chapter(chapt, questions, args):
    
    total = len(questions)
    correct = 0
    qnum = 0
    material = []
    
    print('\n\n' + str(total) + ' questions for this chapter.')
    lightcli.choice_input(showopts=False, qopt=True)
    
    for q, a, op, r in questions:
        qnum = qnum + 1
        status, info = ask_question(chapt, qnum, q, a, op, r,
                learning=args.learning)
        if status: correct = correct + 1
        material.append([status, info])
    
    return material, total, correct


def load_chapter(material):
    """Ask questions for a given chapter"""
    chapt = None
    while not chapt:
        chapt = lightcli.choice_input(list(map(str, range(1, len(material) + 1))),
                prompt='\nFor which chapter are we testing?', qopt=True)
    
    questions = material[int(chapt)-1]

    return chapt, questions


def choose_module(directory, fileext='.json'):
    """Choose a quiz module"""
    
    if not os.path.isdir(directory):
        directory = '.'

    jsonfiles = [f for f in os.listdir(directory) \
            if os.path.isfile(directory + '/' + f) and f.endswith(fileext)]
    

    choices = {}
    for f in jsonfiles:
        shortname = f[:-5]
        choices[shortname] = directory + '/' + f

    modprompt = '==== Modules: ====\n'
    for m in choices:
        modprompt = modprompt + m + '\n'
    modprompt = modprompt + '\nYour choice?'

    choice = lightcli.choice_input(prompt=modprompt, options=list(choices.keys()),
            showopts=False, qopt=True)
    
    with open(choices[choice]) as f:
        material = json.loads(f.read())

    return choices[choice]


def load_module(filename):
    """Read a module from a specified file"""
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            material = json.loads(f.read())

    return material


def run_quiz(args):
    if not args.file: module = choose_module(args.directory)
    else: module = args.file
    material = load_module(module)

    chapt, questions = load_chapter(material)
    material, total, correct = \
            quiz_chapter(chapt, questions, args)

    return material, total, correct
