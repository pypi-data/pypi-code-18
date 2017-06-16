
import asyncio
import functools
import logging
import logging.config

logger = logging.getLogger(__name__)

import modconf
import ws_storage.filesystem
import ws_storage.protocol
import ws_storage.coro_queue

class ServerClientProtocol(ws_storage.protocol.Protocol):
    def __init__(self, loop, app):
        logger.debug('{} created'.format(self.__class__.__name__))
        super(ServerClientProtocol, self).__init__(loop)
        logger.debug('super initialized')
        self.app = app

class Application(object):
    def __init__(self, loop, conf):
        self.loop = loop
        self.conf = conf
        self.storage = ws_storage.filesystem.Storage(self.conf.STORAGE_DIR)
        self.coro_queue = ws_storage.coro_queue.CoroQueue(loop)
        self.coro_queue.schedule_run_forever()

    def write_object(self, id_, o):
        return self.coro_queue.put_nowait(self.__write_object, id_, o)

    def read_object(self, id_):
        return self.coro_queue.put_nowait(self.__read_object, id_)

    async def __write_object(self, id_, o):
        self.storage.write_object(id_, o)

    async def __read_object(self, id_):
        return self.storage.read_object(id_)

    def write_binary(self, id_, o):
        return self.coro_queue.put_nowait(self.__write_binary, id_, o)

    def read_binary(self, id_):
        return self.coro_queue.put_nowait(self.__read_binary, id_)

    async def __write_binary(self, id_, o):
        self.storage.write_binary(id_, o)

    async def __read_binary(self, id_):
        return self.storage.read_binary(id_)

def runserver(args):
    conf = modconf.import_class(
            args.conf_mod, 
            'Conf', 
            ('DEVELOP' if args.d else 'DEPLOY',), 
            folder=args.conf_dir[0])

    logging.config.dictConfig(conf.LOGGING)

    loop = asyncio.get_event_loop()

    app = Application(loop, conf)

    coro = loop.create_server(
            functools.partial(ServerClientProtocol, loop, app),
            'localhost', 
            conf.PORT)
    
    logger.debug('start server')
    server = loop.run_until_complete(coro)
    
    # Serve requests until Ctrl+C is pressed
    logger.debug('serving on {}'.format(server.sockets[0].getsockname()))
    logger.debug('server = {}'.format(server))
    logger.debug('ws_storage version = {}'.format(ws_storage.__version__))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('got keyboard interrupt')
    except Exception as e:
        logger.error(e)

    logger.debug('closing')    
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())


