#!/usr/local/bin/python3
"""
All commands go through this script
Purpose: Collecting user data
"""


import os

import json
from sys import argv
import requests

# Asciinema things
import asciinema
import asciinema.config as config
from asciinema.api import Api
from asciinema.commands.record import RecordCommand


def main():

    # Load default asciinema configuration
    cfg = config.load()
    # args = {}
    print("xxx3 initing Api")
    api = Api(cfg.api_url, os.environ.get("USER"), cfg.api_token)
    # args.command = None,
    # args.filename = 'roa',
    # args.max_wait = None,
    # args.quiet = False,
    # args.title = None,
    # args.yes = False
    RecordCommand(api, 'roa', None, None, False, False, None).execute()

    """
    Get command, args, exit code
    Send those data to server for business logic
    Returns:
        Not return anything, print result on terminal
    Raises:
        all: do nothing
    """

    # exit_code = argv[1]
    # command = argv[2]
    # arguments_list = argv[3:]

    # print "-------debug------------"
    # print ( command )
    # print ( exit_code )
    # print ( ' '.join(arguments_list) )
    # asciinema.recorder.exe

    # args = ' '.join(arguments_list)

    # Terminal tracking
    # url = "http://localhost:5000"
    # data = {
    #     'command': command,
    #     'exit_code': exit_code,
    #     'args': args
    # }
    # headers = {'content-type': 'application/json'}
    # try:
    #     r = requests.post(url=url, data=json.dumps(data), headers=headers)
    #     r_stat = r.text
    #     # print r.status_code
    #     print (r_stat)
    # except:
    #     # do nothing
    #     pass

print("xxx4 we are here!")
if __name__ == "__main__":
    main()
