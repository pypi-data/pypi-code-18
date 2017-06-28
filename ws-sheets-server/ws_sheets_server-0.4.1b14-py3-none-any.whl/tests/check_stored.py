import asyncio
import pickle
import time
import os
import sys
import json
import logging
import logging.config
import modconf
import subprocess
import traceback

import ws_storage.impl.filesystem
import ws_sheets

class TestCheckStored():

    conf_mod = 'ws_sheets_server.tests.conf.simple'
    conf_dir = None
    d = True
    
    def setUp(self):

        self.conf_dir = self.conf_dir or os.path.join(os.environ['HOME'], 'config')

        self.p1 = subprocess.Popen((
            'pipenv', 'run',
            'ws_storage', 
            'runserver', 
            'ws_storage.tests.conf.simple', 
            '-d',
            '--conf_dir', 
            self.conf_dir,
            ))

        time.sleep(2)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.p1.kill()

        print('close loop')
        self.loop.close()

    def test(self):
        try:
            self.setUp()
            self.loop.run_until_complete(self.go())
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise
        finally:
            self.tearDown()

    async def go(self):
        
        conf = modconf.import_class(self.conf_mod, 'Conf', ('DEVELOP' if self.d else 'DEPLOY',), folder=self.conf_dir)
        conf.log_console()
        logging.config.dictConfig(conf.LOGGING)

        stor = await ws_storage.impl.client.Storage.create(self.loop, conf.STORAGE_HOST, conf.STORAGE_PORT)
       
        print('storage={}'.format(stor))

        lst = await stor.list_files()
        
        print('files =',lst)

        fail = False
        for f in lst:
            if f == '_counter':
                print('skip', repr(f))
                continue
            try:
                print('f=',f)
                b = await stor.read_binary(f)

                o = pickle.loads(b)

                print(repr(o))
                #print(dir(o))
            except Exception as e:
                print(e)
                fail = True

        assert (not fail)

    
