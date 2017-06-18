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
        
        conf = modconf.import_conf('ws_sheets_server.tests.conf.simple')

        #logging.config.dictConfig(settings_module.LOGGING)
    
        #port = settings_module.PORT
        
        folder = conf.STORAGE_FOLDER
        
        stor = ws_storage.filesystem.Storage(ws_sheets.Book, folder)
    
        #server = sheets_backend.sockets.Server(stor, port)
    
        #return stor
        
        lst = os.listdir(stor.folder)
         
        print('files in {}:'.format(stor.folder),lst)
        
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

    
