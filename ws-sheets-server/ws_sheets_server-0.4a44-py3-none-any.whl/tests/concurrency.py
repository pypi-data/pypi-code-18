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

class TestConcurrency(unittest.TestCase):

    def setUp(self):
        self.conf_mod = 'ws_sheets_server.tests.conf.simple'

        self.p = subprocess.Popen(('ws_sheets_server', self.conf_mod))

        time.sleep(3)
        
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.p.kill()

        print('close loop')
        self.loop.close()

    def test_concurrency(self):
    
        conf = modconf.import_conf(self.conf_mod)

        coro = self.loop.create_connection(
            functools.partial(ws_sheets_server.client_aio.BookProtocol, self.loop),
            'localhost', 
            conf.PORT)

        print('connecting')

        transport, proto = self.loop.run_until_complete(coro)
    
        print('connected')
        
        self.loop.run_until_complete(proto.request_new())

        res = self.loop.run_until_complete(proto.request_sheet_data('0'))

        futures = []

        for r in range(100):
            proto.set_cell('0', r, 0, 'sum(range(100))')
            
            fut = proto.request_sheet_data('0')

            futures.append(fut)
            #self.assertEqual(
            #        proto['0'][r, 0],

        print(futures)

        def func():
            done, pending = yield from asyncio.wait(futures)

            print('done =',done)
            print('pending =', pending)

            return None

        ret = asyncio.wait(futures)

        ret = self.loop.run_until_complete(ret)

        

        #ret = func()
        print('ret =', ret)

        print('complete')


