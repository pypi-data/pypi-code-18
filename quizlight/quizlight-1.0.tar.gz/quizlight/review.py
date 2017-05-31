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


from datetime import datetime
import lightcli



def check_save():
    """Check if results will be saved"""

    choice = lightcli.choice_input(['y', 'n'], prompt='\nSave results?',
            qopt=True)

    if choice == 'y':
        filename = lightcli.outfile_input(extension='.txt', quitopt=True)
        return filename
    else:
        return None



def do_review(material, total, correct, resultfile=None):
    """Reviews test questions"""

    resultstring = '\n\n======== Finished! ========\n\n' + \
    'Score: ' + str(int(correct / total * 100)) + '%\n' + \
    'Correct: ' + str(correct) + ' out of ' + str(total) + '\n' + \
    'Missed questions: ' + str(int(total - correct))
    
    if resultfile:
        tstamp = 'Completed ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(resultfile, 'w') as f:
            f.write('\n' + tstamp + resultstring + '\n')

    print(resultstring)
    
    
    # print('\n\n======== Finished! ========\n')
    # print('Score:', str(int(correct / total * 100)) + '%')
    # print('Correct:', correct, 'out of', total)
    # print('Missed questions:', int(total - correct))

    mode = lightcli.choice_input(['y', 'n'], prompt='\nReview questions?',
            qopt=True)
    if mode == 'y':
        reviewtype = lightcli.choice_input(['a', 'i'],
                prompt='Review all questions or incorrect questions?',
                qopt=True)
        if reviewtype == 'a': review_all = 1
        else: review_all = 0

        anything_there = None
        for status, info in material:
            if status and not review_all:
                continue
            else:
                if not anything_there: anything_there = 1
                rn, rq, ra, ro, rx, rr = info
                print('\n\n======== Question #' + str(rn) + ' ========\n')
                print(rq)
                print('Your answer:', rx)
                print('Correct answer:', ra)
                if rr: print(rr)
                lightcli.choice_input(qopt=True)
        
        if not anything_there:
            print('\nAll answers correct! No need for review.')
            print('Score: 100%')
            lightcli.choice_input(qopt=True)
