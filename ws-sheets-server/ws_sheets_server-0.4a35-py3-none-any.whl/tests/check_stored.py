import os
import sys
import json
import logging
import logging.config
import modconf
import unittest

import ws_storage.filesystem
import ws_sheets

class TestCheckStored(unittest.TestCase):
    def test(self):
        
        conf = modconf.import_class('ws_sheets_server.tests.conf.simple', 'Conf', ('DEVELOP',))

        #logging.config.dictConfig(settings_module.LOGGING)
    
        #port = settings_module.PORT
        
        stor = ws_storage.filesystem.Storage(ws_sheets.Book, conf.STORAGE_DIR)
    
        #server = sheets_backend.sockets.Server(stor, port)
    
        #return stor
        
        lst = os.listdir(stor.folder)
         
        print('{} files in {}'.format(len(lst), stor.folder))
        
        fail = False
        for f in lst:
            h, t = os.path.splitext(f)
            if t == '.bin':
                try:
                    o = stor.read(h)
                    #print(repr(o))
                    #print(dir(o))
                except Exception as e:
                    print(e)
                    fail = True

        self.assertFalse(fail)

    
