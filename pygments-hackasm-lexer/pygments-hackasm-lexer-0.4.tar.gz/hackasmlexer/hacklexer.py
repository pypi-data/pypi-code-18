import re
from pygments.lexer import RegexLexer, include
from pygments.token import *

class HackAsmLexer(RegexLexer):
    name = 'Hack Assembler'
    aliases = ['hack_asm']
    filenames = ['*.asm']

    identifier = r'[a-zA-Z$._?][a-zA-Z0-9$._?]*'

    flags = re.IGNORECASE | re.MULTILINE
    tokens = {
        'root': [
            include('whitespace'),
            (r'\(' + identifier + '\)', Name.Label),
            (r'[+-=;&|!]+', Operator),
            (r'\/\/.+$', Comment),
            (r'[\r\n]+', Text),
            (r'@[A-Za-z][A-Za-z0-9]+', Name.Variable),
            (r'\b(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)\b', Keyword),
            (r'null', Keyword.Pseudo),
            (r'\b(D|M|MD|A|AM|AD|AMD)\b', Name.Builtin),
            (r'@[0-9]+', Name.Constant)
        ],
        'whitespace': [
            (r'\n', Text),
            (r'\s+', Text),
            (r'#.*?\n', Comment)
        ]
    }
