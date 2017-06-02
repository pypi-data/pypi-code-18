"""
Author: Trieu Pham (trieu@codelynx.io)

A private property of #codelynx company
"""

import json
import sys
from asciinema.commands.command import Command

import requests


class Api(Command):
    """
    This class manages talking with api server
    """

    def __init__(self):
        with open('conf') as f:
            self.url = f.readline().strip()
        # self.url = "http://localhost:5000"
        Command.__init__(self)  # color

    def handle_data(self, collection, quiet=True, method='POST', **kwargs):
        """
            Send char/output to server
            @params:
                collection: insert into this collection <str>
                quiet: display result on screen or not <bool>
                **kwargs: tuple of data <str>
            @returns: text
            @raises: exit program
        """
        data = {'collection': collection, 'kwargs': kwargs}
        headers = {'content-type': 'application/json'}
        try:
            if method == 'POST':
                result = requests.post(
                    url=self.url,
                    data=json.dumps(data),
                    headers=headers)
            if method == 'GET':
                result = requests.get(
                    url=self.url + '/lookup/get',
                    params={"question": kwargs['question']}
                )
            # print(lookups.url)
            # print(result.text)
            if not quiet:  # Print return info if required
                if result.status_code == 404:
                    self.print_warning(result.text)
                elif result.status_code == 500:
                    self.print_error(result.text)
                else:
                    self.print_info(result.text)
                # if 'Success' in result.text:
                #     self.print_info(result.text)
                # if 'False' in result.text:
                #     self.print_warning(result.text)
            # return r.status_code
            # return r.text
            return result
        except requests.exceptions.ConnectionError as e:
            # Print info in red and exit whole program
            sys.exit('\x1b[31m\n~ Cannot connect server, exit now...\x1b[0m')
