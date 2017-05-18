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
__version__ = '1.2.1'


class Stack(list):
    """
    Stack
    """

    def __init__(self):
        super(Stack, self).__init__()
        self._str_value = ''

    def add_str_value(self, s):
        """
        add the str of value
        :param s: str of value
        """
        self._str_value += s

    def push(self, value=None):
        """
        push the value
        :param value: value
        """
        if value and self._str_value:  # duplicate
            raise ValueError('Duplicate value')
        elif value or self._str_value:
            if self._str_value:
                try:
                    value = decimal.Decimal(self._str_value)
                except decimal.InvalidOperation:
                    raise ValueError(self._str_value)

                self._str_value = ''

            self.append(value)

    def top(self):
        """
        get the top value
        :return: top value
        """
        return self[-1]


class RPNCalculator:
    """
    RPN Calculator
    """

    def __init__(self):
        self._stack = Stack()
        self._operators = {
            ' ': lambda: self._stack.push(),
            '+': lambda: self._calculate(lambda x, y: x + y),
            '-': lambda: self._calculate(lambda x, y: x - y),
            '*': lambda: self._calculate(lambda x, y: x * y),
            '/': lambda: self._calculate(lambda x, y: x / y),
            '%': lambda: self._calculate(lambda x, y: x % y),
            '^': lambda: self._calculate(lambda x, y: x ** y)
        }

    def _calculate(self, method):
        """
        calculate
        :param method: calculate method
        """
        self._stack.push()
        y = self._stack.pop()
        x = self._stack.pop()
        try:
            self._stack.push(method(x, y))
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
                self._stack.add_str_value(s)

        print(self._stack.top())


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
