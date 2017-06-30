'''
    legos.ctftime, A plugin for Legobot to interact with CTFtime API
    Copyright (C) 2017 Bren Briggs

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Portions of CTFtime API interaction are borrowed from
    https://github.com/spiperac/ctftime-ircbot, released under GPLv3
'''


import logging
import requests
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)


class CTFtime(Lego):
    @staticmethod
    def listening_for(message):
        if message['text'] is not None:
            return message['text'].startswith('!ctftime ')

    def handle(self, message):
        try:
            cmd = message['text'].split()[1]
        except IndexError as e:
            logger.warn('Lego called without arguments')
            return False

        dispatcher = {'upcoming': self._get_upcoming}

        if cmd in dispatcher:
            logger.debug('Dispatching command {}'.format(cmd))
            dispatcher[cmd](message)
        return

    @staticmethod
    def get_name():
        return 'ctftime'

    @staticmethod
    def get_help():
        return 'Get info from the CTFtime API. Usage: !ctftime upcoming'

    # Internal methods (the actual work)

    @staticmethod
    def _handle_opts(message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
            return opts
        except IndexError:
            return None

    def _get_upcoming(self, message):

        baseurl = 'https://ctftime.org/api/v1'
        r = requests.get('{}/events/'.format(baseurl))
        opts = self._handle_opts(message)
        if opts is None:
            return False
        if r.status_code == requests.codes.ok:
            for event in r.json():
                reply = 'Name: {}, Format: {}, Date {} - {}'.format(
                    event['title'],
                    event['format'],
                    event['start'],
                    event['finish'])
                logger.info('Reply: {}'.format(reply))
                self.reply(message, reply, opts)
            return True
        else:
            return False
