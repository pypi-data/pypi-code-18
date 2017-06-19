import re

def patternReplace(string, replacement, *pats):
    '''
    matches and replaces multiple patters in a string

      [string] <str> : a string with substrings to replaces
      [replacement] <str> : a string to replace the patterns
      [pats] <str> : patterns in the string to have replaced

      returns : string with patterns replaced
    '''

    for pattern in pats:
        string = re.sub(pattern,replacement,string)
    return string
