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

import ws_storage.filesystem
import ws_sheets
import ws_sheets_server.packet
import ws_sheets_server.protocol

logger = logging.getLogger(__name__)

class StorageClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('client connection made')

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')

class ServerClientProtocol(ws_sheets_server.protocol.Protocol):
    def __init__(self, loop, app):
        ws_sheets_server.protocol.Protocol.__init__(self, loop)
        self.app = app

    def packet_received(self, packet):
        logger.debug('{}: packet received: {}'.format(self.__class__.__name__, packet.__class__.__name__))
        try:
            self.loop.create_task(packet(self))
        except Exception as e:
            logger.error('{} {}'.format(packet, e))

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

        self.__coro_queue = asyncio.Queue()

        self.sheets = dict((i, Sheet(self, s)) for i, s in self.__book.sheets.items())

        self.script_pre = Script(self, self.__book.script_pre)
        self.script_post = Script(self, self.__book.script_post)

    def schedule_run_forever(self):
        logger.debug('Book schedule_run_forever')
        self.__task_run_forever = self.loop.create_task(self.run_forever())

    async def run_forever(self):
        logger.debug('Book run_forever')
        while True:
            #coro, future = await self.__coro_queue.get()
            item = await self.__coro_queue.get()
            #logger.debug('Book coro queue get {}'.format((coro, future)))
            logger.debug('Book coro queue get {}'.format(item))
            coro, future = item
            logger.debug('  coro={}'.format(coro))
            logger.debug('  future={}'.format(future))
            future.set_result(await coro)
            
    def _put(self, f, *args):
        logger.debug('Book put f={}'.format(f))
        future = self.loop.create_future()
        coro = f(*args)
        if not asyncio.iscoroutine(coro):
            raise RuntimeError('{} is not a coroutine'.format(f))
        self.__coro_queue.put_nowait((coro, future))
        logger.debug('  coro={}'.format(coro))
        return future

    async def calculate(self):
        return (await self._put(self.__calculate))

    async def __calculate(self):
        return (await self.loop.run_in_executor(
            None, functools.partial(self.__book.do_all)))

    async def write(self):
        return self._put(self.__write)

    async def __write(self):
        self.app.storage.save_object(self.id_)

    async def set_docs(self, s):
        return (await self._put(self.__set_docs, s))
    
    async def __set_docs(self, s):
        self.__book.set_docs(s)

    @property
    def docs(self):
        return self.__book.docs

class Application(object):
    def __init__(self, conf, loop, concurrent=False):
        self.loop = loop
        self.conf = conf
        self.concurrent = concurrent
        self.books = {}

    async def get_storage(self):
        try:
            addr = conf.STORAGE_ADDRESS
        except:
            self.storage = ws_storage.filesystem.Storage(
                    ws_sheets.Book, 
                    self.conf.STORAGE_FOLDER)
        else:
            coro = self.loop.create_connection(
                    functools.partial(StorageClientProtocol),
                    *addr)
            transport, proto = await coro
            self.storage = proto
    
        self.storage.set_object_new_args((self.conf.conf_sheets.Settings,))

    def cache_book(self, book_id):
        book = Book(
                self,
                self.loop,
                book_id,
                self.storage.get_object(book_id))
        book.schedule_run_forever()
        return book

    def get_book(self, book_id):
        if book_id in self.books:
            return self.books[book_id]

        book = self.cache_book(book_id)
        self.books[book_id] = book
        return book

def test(loop, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--conf_dir',
            nargs=1,
            default=(None,),
            help='modconf module directory')
    parser.add_argument(
            'conf_mod',
            help='modconf module name')

    args = parser.parse_args(argv[1:])
    
    conf = modconf.import_conf(args.conf_mod, args.conf_dir[0])

    logging.config.dictConfig(conf.LOGGING)

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
            pass
        
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())

def main(argv):
    logger = logging.getLogger(__name__)
    loop = asyncio.get_event_loop()
    try:
        test(loop, argv)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception('exception occured\n{}'.format(e))
    loop.close()





