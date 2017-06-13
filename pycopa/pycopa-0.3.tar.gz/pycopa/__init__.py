from .lexer import Lexer
from .parser import Parser


def parse(line):
    l = Lexer()
    p = Parser()
    t = l.parse(line)
    return p.parse(t)
