import sys
import functools
import asyncio
import json
import argparse
import modconf
import ws_sheets
import ws_sheets_server.client_aio
import ws_sheets_server.protocol
import subprocess
import unittest
import time

class TestClient(unittest.TestCase):

    def setUp(self):
        self.conf_mod = 'ws_sheets_server.tests.conf.simple'

        self.p = subprocess.Popen(('ws_sheets_server', self.conf_mod))

        time.sleep(3)
        
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.p.kill()

        print('close loop')
        self.loop.close()

    def test(self):
    
        conf = modconf.import_conf(self.conf_mod)

        #client = ws_sheets_server.sockets.Client(port)
        
        #print(client.book_new())
    
        coro = self.loop.create_connection(
            functools.partial(ws_sheets_server.client_aio.BookProtocol, self.loop),
            'localhost', 
            conf.PORT)
    
        transport, protocol = self.loop.run_until_complete(coro)
    
        print(transport)
        print(protocol)
        
        self.loop.run_until_complete(protocol.request_new())

        res = self.loop.run_until_complete(protocol.request_sheet_data('0'))
    
        print('future result')
        print(repr(res))
    

    
    
    
    
