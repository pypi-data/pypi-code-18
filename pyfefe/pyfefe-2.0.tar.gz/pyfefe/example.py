from io import StringIO

from pyfefe import covfefe


def say(text):   #Example function
    return text

f = StringIO()  #Create a stream

with covfefe.stdout_translator(f):  #All stout is translated here
    print('There are tons of fake media')
    print(say('I hate media coverage'))

covfefe.read_translation(f) #Reads off translations