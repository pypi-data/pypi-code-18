"""
Author: Trieu Pham (trieu@codelynx.io)

A private property of #codelynx company
"""

import sys
from codelynx.api import Api
from asciinema.commands.command import Command


class Ask(Command):
    """
    This class manages asking xirion a question
    Expected command: xirion ask <question>
    Response: print xirion answer
    @args:
        question: ask xirion this question
    @returns:
        0 if everything 's good, 1 otherwise
    @raises:
        unknown
    """

    def __init__(self, question):
        # self.cmd = cmd
        # self.correction = correction
        self.api = Api()
        self.question = question
        Command.__init__(self)  # color

    def execute(self):
        """
        Execute asking
        """
        try:
             # Debug
            # print(self.question)
            # lookup quetions here
            # self.api.handle_data('lookup', quiet=False, orig=self.question)
            answer = self.api.handle_data('lookup', quiet=False, method='GET', question=self.question)
        except Exception as ex:
            print(ex)
            return 1
        return 0
