# coding=utf-8

"""
RPN calculator for CLI
"""

import argparse
import decimal
import sys

import six
import zenhan

__author__ = 'Masaya SUZUKI'
__version__ = '1.2.1.1'


class RPNCalculator:
    """
    RPN Calculator
    """

    def __init__(self):
        self._stack = list()
        self._buffer = ''
        self._operators = {
            ' ': lambda: self._push(),
            '+': lambda: self._calculate(lambda x, y: x + y),
            '-': lambda: self._calculate(lambda x, y: x - y),
            '*': lambda: self._calculate(lambda x, y: x * y),
            '/': lambda: self._calculate(lambda x, y: x / y),
            '%': lambda: self._calculate(lambda x, y: x % y),
            '^': lambda: self._calculate(lambda x, y: x ** y)
        }

    def _push(self, value=None):
        """
        push the stack
        :param value: value
        """
        if self._buffer and value:
            raise AttributeError('Duplicate Value')
        elif self._buffer or value:
            if self._buffer:
                try:
                    value = decimal.Decimal(self._buffer)
                except decimal.InvalidOperation:
                    raise AttributeError(str(self._buffer))

            self._stack.append(value)

    def _calculate(self, method):
        """
        calculate
        :param method: calculate method
        """
        self._push()
        y = self._stack.pop()
        x = self._stack.pop()
        try:
            self._push(method(x, y))
        except decimal.DivisionByZero:
            raise ZeroDivisionError()

    def execute(self, line):
        """
        execute a line
        :param line: line
        """
        for s in zenhan.z2h(line).strip() + ' ':
            if s in self._operators:
                self._operators[s]()
            else:
                self._buffer += s

        print(self._stack[-1])


def s2u_2(s):
    """
    str to unicode when Python 2.x
    :param s: str
    :return: unicode
    """
    if six.PY2:
        s = s.decode(sys.getfilesystemencoding())

    return s


def main():
    """
    main function
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog='RPN Calculator')
    parser.add_argument('-e', '--execute', type=str, help='calculation formula')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {0}'.format(__version__))
    args = parser.parse_args()

    # calculator
    calculator = RPNCalculator()

    if args.execute:  # given formula by the command line argument
        calculator.execute(s2u_2(args.execute))
    else:  # given formula by standard input
        try:
            while True:
                calculator.execute(s2u_2(six.moves.input('> ')))
        except EOFError:  # exit when the input ended
            exit(0)


# main process
if __name__ == '__main__':
    main()
