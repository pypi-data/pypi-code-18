# -*- coding: utf-8 -*-

import xerox

from jsonapp.utils.cli_util import cli_print, do_copy_to_clipboard
from jsonapp.utils.print_util import print_with_separators_and_space
from jsonapp.utils.result_util import result_failure, result_success
from jsonapp.utils.string_util import String

script_output = 'script'
user_output = 'user'


class JSONApp(object):

    def __init__(self):
        pass

    def run(self, clipboard=None, json_string=None, copy_to_clipboard=None, output=None, pager=False):

        if clipboard:
            json_string = xerox.paste()
            self.format(json_string=json_string, copy_to_clipboard=True, output=output, pager=pager)

        elif json_string:
            self.format(json_string=json_string, copy_to_clipboard=copy_to_clipboard, output=output, pager=pager)

        else:
            return result_failure()

        return result_success()

    def format(self, json_string, copy_to_clipboard, output, pager):

        if not json_string:
            cli_print('No JSON string.')
            return

        formatted_json_string = String(json_string).to_pretty_json_string()
        result = formatted_json_string

        if output == user_output:
            print_with_separators_and_space(result, pager=pager)
        elif output == script_output:
            print(result)
        else:
            raise NotImplementedError

        if copy_to_clipboard:
            do_copy_to_clipboard(result)


json_app = JSONApp()
