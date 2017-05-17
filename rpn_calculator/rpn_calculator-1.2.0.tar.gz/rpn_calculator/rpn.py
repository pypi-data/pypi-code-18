# coding=utf-8

"""
RPN calculator for CLI
"""

import argparse

import six

__author__ = 'Masaya SUZUKI'

__version__ = '1.2.0'


class Stack(list):
    """
    Stack
    """

    def push(self, v):
        """
        push the value
        :param v:value
        """
        self.append(v)
        print(v)


def main():
    """
    main function
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog='RPN Calculator')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {0}'.format(__version__))
    args = parser.parse_args()

    # stack
    stack = Stack()

    try:
        while True:
            # get the input
            line = six.moves.input('> ').strip()

            # calculate when the operator was inputted
            if line.endswith('+') or line.endswith('-') \
                    or line.endswith('*') or line.endswith('/') or line.endswith('%') or line.endswith('^'):
                # push float to stack
                if 1 < len(line):
                    stack.push(float(line[:-1]))

                # temporary stack
                stack_tmp = [stack.pop() for i in range(2)]

                if line.endswith('+'):  # addition
                    stack.push(stack_tmp.pop() + stack_tmp.pop())
                elif line.endswith('-'):  # subtraction
                    stack.push(stack_tmp.pop() - stack_tmp.pop())
                elif line.endswith('*'):  # multiplication
                    stack.push(stack_tmp.pop() * stack_tmp.pop())
                elif line.endswith('/'):  # division
                    stack.push(stack_tmp.pop() / stack_tmp.pop())
                elif line.endswith('%'):  # residue
                    stack.push(stack_tmp.pop() % stack_tmp.pop())
                elif line.endswith('^'):  # power
                    stack.push(stack_tmp.pop() ** stack_tmp.pop())
            else:  # push float to stack when the float was inputted
                stack.push(float(line))
    except EOFError:  # exit a loop when the input ended
        pass


# main process
if __name__ == '__main__':
    main()
