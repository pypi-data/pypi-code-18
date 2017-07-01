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


import lightcli
import os
import time
import json



def create_question():
    """Edit a question"""
    
    allfinished = False
    while not allfinished:

        # Set the question prompt:
        finished = False
        while not finished:
            print('\n\nEnter your question')
            question = lightcli.long_input()

            print('\n\n==== Your Question: ====\n')
            print(question)

            choice = lightcli.choice_input(options=['k', 'r'],
                    prompt = 'Keep/Rewrite', qopt=True)
            if choice == 'k':
                finished = True

        # Set the answer options:
        finished = False
        while not finished:
            print('Enter the list of answers (short name, e.g. a, b, c, d)')
            aoptions = lightcli.list_input()

            print('\n\n==== Your Options: ====\n')
            print(aoptions)
            
            choice = lightcli.choice_input(options=['k', 'r'],
                    prompt = 'Keep/Rewrite', qopt=True)
            if choice == 'k':
                finished = True

        # Set the correct answer:
        finished = False
        while not finished:
            print('Enter the correct answer (must be in the answer list)')
            answer = lightcli.choice_input(prompt='Correct answer:',
                    options=aoptions, qopt=True)
            
            print('\n\n==== Your Answer: ====\n')
            print(answer)
            
            choice = lightcli.choice_input(options=['k', 'r'],
                    prompt = 'Keep/Rewrite', qopt=True)
            if choice == 'k':
                finished = True

        # Set the reason:
        finished = False
        while not finished:
            print('Enter the reason (Blank for none)')
            reason = str(input('Reason (blank for None):'))
            if reason == '':
                reason = None
            
            print('\n\n==== Your Reason: ====\n')
            print(reason)
            
            choice = lightcli.choice_input(options=['k', 'r'],
                    prompt = 'Keep/Rewrite', qopt=True)
            if choice == 'k':
                finished = True

        # Verify everything:
        print('\n\n==== Your Question: ====\n')
        print(question)
        x = lightcli.choice_input(showopts=False, )

        print('\n\n==== Your Options: ====\n')
        print(aoptions)

        print('\n\n==== Your Answer: ====\n')
        print(answer)
        x = lightcli.choice_input(showopts=False, )
        
        print('\n\n==== Your Reason: ====\n')
        print(reason)
        x = lightcli.choice_input(showopts=False, )
        
        choice = lightcli.choice_input(options=['k', 'r', 'a'],
                prompt = 'Keep/Rewrite/Abort', qopt=True)
        if choice == 'k':
            allfinished = True
        elif choice == 'a':
            return None

    return [question, answer, aoptions, reason]



def create_chapter(filename):
    """Create a chapter of questions"""
    
    chapter = []

    finished = False
    while not finished:
        question = create_question()
        if question: chapter.append(question)
        
        choice = lightcli.choice_input(prompt='\n\nAdd another question?',
                options=['y', 'n'], qopt=True)

        if choice == 'n': finished = True

    
    with open(filename, 'r') as f:
        try:
            module = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            module = []
        # module = json.loads(f.read())
    
    # print module
    module.append(chapter)
    modulejson = json.dumps(module, indent=2)

    with open(filename, 'w') as f:
        f.write(modulejson)



def extend_chapter(filename, cnum):
    """Extend an existing chapter"""
    
    with open(filename, 'r') as f:
        module = json.loads(f.read())
        
    chapter = module[int(cnum)-1]

    finished = False
    while not finished:
        question = create_question()
        if question: chapter.append(question)
        
        choice = lightcli.choice_input(prompt='Add another question?',
                options=['y', 'n'], qopt=True)

        if choice == 'n': finished = True

    module[int(cnum)-1] = chapter
    modulejson = json.dumps(module, indent=2)

    with open(filename, 'w') as f:
        f.write(modulejson)


def load_module():
    """Load a module to edit"""
    
    fileok = False
    while not fileok:
        filename = str(input('File name? '))
        if not filename.endswith('.json'):
            filename = filename + '.json'
        if os.path.isfile(filename):
            choice = lightcli.choice_input(prompt=filename + \
                    ' already exists. Edit it?',
                    options=['y', 'n'], qopt=True)
            if choice == 'y':
                try:
                    nowtime = time.time()
                    with open(filename, 'a') as f:
                        os.utime(filename, (nowtime, nowtime))
                    fileok = True
                except IOError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')
            
                with open(filename, 'r') as f:
                    try:
                        module = json.loads(f.read())
                    except json.decoder.JSONDecodeError:
                        module = []
                
                if module != []:
                    print('\n' + filename + ' contains ' + \
                            str(len(module)) + ' chapter(s)')
                    choice = lightcli.choice_input(
                            prompt='Add new chapter, or Extend existing?',
                            options=['a', 'e'], qopt=True)
                
                    if choice == 'e':
                        clist = [str(x + 1) for x in range(0, len(module))]
                        cnum = lightcli.choice_input(prompt='Extend ' + \
                                'which chapter?',
                                options=clist, qopt=True)
                    else:
                        cnum = None
                else:
                    cnum = None

        else:
            fprompt = filename + ' does not exist. Create it?'
            choice = lightcli.choice_input(prompt=fprompt,
                    options=['y', 'n'], qopt=True)
            if choice == 'y':
                try:
                    newlist = []
                    newmodule = json.dumps(newlist)
                    with open(filename, 'w') as f:
                        f.write(newmodule)
                    fileok = True
                    cnum = None
                except IOError:
                    print('Write permission denied on ' + filename + \
                            '. Try again.')

    return filename, cnum



def run_edit(args):
    """Start quiz module creation or editing"""

    keepcreating = True
    while keepcreating:
        filename, cnum = load_module()
        if not cnum:
            create_chapter(filename)
        else:
            extend_chapter(filename, cnum)

        choice = lightcli.choice_input(prompt='Add/edit more?',
                options=['y', 'n'], qopt=True)
        if choice == 'n': keepcreating = False

