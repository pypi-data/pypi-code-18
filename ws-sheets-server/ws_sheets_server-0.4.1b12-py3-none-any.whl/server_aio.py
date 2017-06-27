import argparse
import asyncio
import concurrent.futures
import json
import numpy
import functools
import logging
import logging.config
import modconf
import pickle
import sys

import ws_storage
import ws_storage.coro_queue
import ws_storage.protocol
import ws_storage.impl.client

import ws_sheets
import ws_sheets_server.packet

logger = logging.getLogger(__name__)

class ServerClientProtocol(ws_storage.protocol.Protocol):
    def __init__(self, loop, app):
        super(ServerClientProtocol, self).__init__(loop)
        self.app = app
        self.app.protos.append(self)

class ScriptStringDescriptor(object):
    def __get__(self, obj, objtype):
        return obj.get_string()

    def __set__(self, obj, value):
        return obj.set_string(value)

class ScriptOutputDescriptor(object):
    def __get__(self, obj, objtype):
        return obj.get_output()

    def __set__(self, obj, value):
        raise RuntimeError('read only')

class Script(object):
    string = ScriptStringDescriptor()
    output = ScriptOutputDescriptor()

    def __init__(self, book, script):
        self.book = book
        self.__script = script

    def get_string(self):
        return self.book._put(self.__get_string)

    async def __get_string(self):
        return self.__script.get_string()

    def set_string(self, value):
        return self.book._put(self.__set_string, value)

    async def __set_string(self, s):
        self.__script.set_string(s)

    def get_output(self):
        return self.book._put(self.__get_output)

    async def __get_output(self):
        return self.__script.output

class Sheet(object):
    def __init__(self, book, sheet):
        self.book = book
        self.__sheet = sheet

    async def getitem(self, args):
        return (await self.book._put(functools.partial(self.__getitem, args)))

    async def __getitem(self, future, args):
        return self.__sheet.__getitem__(args)

    async def setitem(self, args, string):
        return self.book._put(functools.partial(self.__setitem, args, string))

    async def __setitem(self, args, string):
        return self.__sheet.__setitem__(args, string)

    async def add_row(self, i):
        return self.book._put(self.__add_row, i)

    async def __add_row(self, i):
        self.__sheet.add_row(i)

    async def add_column(self, i):
        return self.book._put(self.__add_column, i)

    async def __add_column(self, i):
        self.__sheet.add_column(i)

    async def convert_cells(self):
        return (await self.book._put(functools.partial(self.__convert_cells)))

    async def __convert_cells(self):
        def f(c):
            if c is None:
                return ws_sheets_server.Cell('','')
            
            if False:
                v = c.value
                if isinstance(v, str):
                    v = "\"" + v + "\""
                else:
                    v = str(v)
            else:
                v = c.value
            
            return ws_sheets_server.Cell(c.string, v)

        fv = numpy.vectorize(f, otypes=[ws_sheets_server.Cell])

        return fv(self.__sheet.cells.cells)

class Book(object):
    def __init__(self, app, loop, id_, book):
        self.app = app
        self.loop = loop
        self.id_ = id_
        self.__book = book

        self.__coro_queue = ws_storage.coro_queue.CoroQueue(loop)

        self.sheets = dict((i, Sheet(self, s)) for i, s in self.__book.sheets.items())

        self.script_pre = Script(self, self.__book.script_pre)
        self.script_post = Script(self, self.__book.script_post)

    def schedule_run_forever(self):
        self.__coro_queue.schedule_run_forever()

    def _put(self, f, *args):
        return self.__coro_queue.put_nowait(f, *args)

    async def calculate(self):
        return (await self._put(self.__calculate))

    async def __calculate(self):
        return (await self.loop.run_in_executor(
            None, functools.partial(self.__book.do_all)))

    async def write(self):
        return self._put(self.__write)

    async def __write(self):
        #self.app.storage.save_object(self.id_)
        #await self.app.write_book(self.id_)
        b = pickle.dumps(self.__book)
        await self.app.storage.write_binary(self.id_, b)

    async def set_docs(self, s):
        return (await self._put(self.__set_docs, s))
    
    async def __set_docs(self, s):
        self.__book.set_docs(s)

    @property
    def docs(self):
        return self.__book.docs

    async def close(self):
        logger.debug('book close')
        await self.__coro_queue.close()

class Application(object):
    def __init__(self, conf, loop, concurrent=False):
        self.loop = loop
        self.conf = conf
        self.concurrent = concurrent
        self.books = {}

        self.protos = []

    async def get_storage(self):
        host = self.conf.STORAGE_HOST
        port = self.conf.STORAGE_PORT
            
        self.storage = await ws_storage.impl.client.Storage.create(
                    self.loop,
                    host,
                    port)
        # TODO make sure the effect this deprecated line is performed elsewhere
        #self.storage.set_object_new_args((self.conf.conf_sheets.Settings,))

    async def read_book(self, id_):
        b = await self.storage.read_binary(id_)
        
        book = pickle.loads(b)
        
        bookc = Book(
                self,
                self.loop,
                id_,
                book)

        book.schedule_run_forever()

        self.books[id_] = bookc
        return bookc

    async def get_book(self, book_id):
        if book_id in self.books:
            return self.books[book_id]

        book = await self.read_book(book_id)
        return book

    async def book_new(self):
        id_ = await self.storage.next_id()

        bookc = Book(
                self,
                self.loop,
                id_,
                ws_sheets.Book(self.conf.conf_sheets.Settings))

        bookc.schedule_run_forever()

        self.books[id_] = bookc
       
        return id_, bookc


    async def close(self):
        logger.debug('open books')
        for book_id, book in self.books.items():
            logger.debug('  {}'.format(book_id))
            await book.close()

        logger.debug('protocols')
        for p in self.protos:
            logger.debug('  {}'.format(repr(p)))
            await p.close()

        await asyncio.sleep(5)

def test(loop, args):
   
    conf = modconf.import_class(args.conf_mod, 'Conf', ('DEVELOP' if args.d else 'DEPLOY',), folder=args.conf_dir)

    logging.config.dictConfig(conf.LOGGING)
    print('logging configured')

    # asyncio
    
    loop.set_debug(True)
    
    executor = concurrent.futures.ProcessPoolExecutor()
    #with concurrent.futures.ProcessPoolExecutor() as executor:
    if True:
        logger.debug('executor enter')
        
        #loop.set_default_executor(executor)
    
        app = Application(conf, loop)
        app.executor = executor
        
        loop.run_until_complete(app.get_storage())
    
        # Each client connection will create a new protocol instance
        coro = loop.create_server(
                functools.partial(ServerClientProtocol, loop, app),
                'localhost', 
                conf.PORT)
        
        logger.debug('start server')
        server = loop.run_until_complete(coro)
        
        # Serve requests until Ctrl+C is pressed
        logger.debug('Serving on {}'.format(server.sockets[0].getsockname()))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info('begin shutdown')
            loop.run_until_complete(app.close())
        
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())

def runserver(args):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_event_loop()
    try:
        test(loop, args)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception('exception occured\n{}'.format(e))
    loop.close()





