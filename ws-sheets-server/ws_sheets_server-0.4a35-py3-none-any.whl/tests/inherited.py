import logging
import logging.config
import sys
import functools
import asyncio
import json
import argparse
import modconf
import ws_sheets
import ws_sheets.tests.functions
import ws_sheets_server.client_aio
import ws_storage.protocol
import subprocess
import unittest
import time

logger = logging.getLogger(__name__)

class TestBase(unittest.TestCase):
    def setUp(self):
        self.conf_mod = 'ws_sheets_server.tests.conf.simple'

        self.p = subprocess.Popen(('ws_sheets_server', 'runserver', self.conf_mod))

        time.sleep(3)

        conf = modconf.import_class(self.conf_mod, 'Conf', ('DEVELOP',))

        for l in conf.LOGGING['loggers'].values():
            l['handlers'] = ['console']

        logging.config.dictConfig(conf.LOGGING)

        #self.loop = asyncio.get_event_loop()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)

        #print('is closed 1', self.loop.is_closed())

        try:
            coro = self.loop.create_connection(
                functools.partial(ws_sheets_server.client_aio.BookProtocol, self.loop),
                'localhost', 
                conf.PORT)
        
            #print('is closed 2', self.loop.is_closed())

            transport, self.protocol = self.loop.run_until_complete(coro)
        
        except:
            #self.loop.close()
            raise

    def tearDown(self):
        self.p.kill()
        #self.loop.close()

class TestDemos(TestBase):
    def test(self):
        for cls in ws_sheets.tests.functions.DEMOS.values():
            o = cls()
            
            print('------------------\n{}\n-----------------'.format(cls))

            self.loop.run_until_complete(self.protocol.request_new())

            #fut = self.protocol.request_sheet_data('0')

            #res = self.loop.run_until_complete(fut)

            o.book = self.protocol

            o.test()
    
        #self.loop.close() 


def suite():
    class Test2(TestBase):
        def test(self):
            o = self.cls()
            self.loop.run_until_complete(self.protocol.request_new())
            o.book = self.protocol
            o.test()

    suite = unittest.TestSuite()
    for cls in ws_sheets.tests.functions.DEMOS.values():
        t = Test2()
        t.cls = cls
        suite.addTest(t)
    return suite




