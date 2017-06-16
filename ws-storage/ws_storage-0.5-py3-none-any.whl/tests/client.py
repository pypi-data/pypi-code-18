import sys
import functools
import asyncio
import json
import argparse
import modconf
import subprocess
import unittest
import time
import pickle
import logging.config

import ws_storage.client

class Foo(object): pass

class TestClient(unittest.TestCase):

    def setUp(self):
        self.conf_mod = 'ws_storage.tests.conf.simple'

        self.p = subprocess.Popen(('ws_storage', 'runserver', self.conf_mod, '-d'))

        time.sleep(3)
        
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.p.kill()

        print('close loop')
        self.loop.close()

    def test(self):
    
        conf = modconf.import_class(self.conf_mod, 'Conf', ('DEVELOP',))

        #client = ws_sheets_server.sockets.Client(port)
        
        #print(client.book_new())
        
        L = conf.LOGGING
        for l in L['loggers'].values():
            l['handlers'] = ['console']
        logging.config.dictConfig(L)
        
        logger = logging.getLogger(__name__)

        logger.debug('ws_stroage version = {}'.format(ws_storage.__version__))

        coro = self.loop.create_connection(
            functools.partial(ws_storage.client.ClientProtocol, self.loop),
            'localhost', 
            conf.PORT)
    
        transport, protocol = self.loop.run_until_complete(coro)
    
        print(transport)
        print(protocol)
        
        if transport.is_closing():
            self.fail()

        o = Foo()
        
        print('write')
        
        b = pickle.dumps(o)

        future = protocol.write_binary('0', b)
        print(future)
        #res = self.loop.run_until_complete(future)
        
        #print(res)

        print('read')
        future = protocol.read_binary('0')
        print(future)
        res = self.loop.run_until_complete(future)
 
        print(res)

        o = pickle.loads(res.b)

        print(o)
   
        self.assertTrue(isinstance(o, Foo))

    
    
    
    
