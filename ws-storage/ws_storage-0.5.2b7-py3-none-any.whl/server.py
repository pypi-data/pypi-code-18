
import asyncio
import functools
import logging
import logging.config

logger = logging.getLogger(__name__)

import modconf
import ws_storage.impl.as3
import ws_storage.impl.filesystem
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
        
        factory = {
                'FILESYSTEM': ws_storage.impl.filesystem.Storage,
                'AS3': ws_storage.impl.as3.Storage,
                }

        logger.debug('impl={}'.format(repr(self.conf.IMPL)))

        self.storage = factory[self.conf.IMPL](self.conf, self.loop)
        
        self.coro_queue = ws_storage.coro_queue.CoroQueue(loop)
        self.coro_queue.schedule_run_forever()

    def write_binary(self, id_, b):
        return self.coro_queue.put_nowait(self.__write_binary, id_, b)

    async def __write_binary(self, id_, b):
        await self.storage.write_binary(id_, b)

    async def read_binary(self, id_):
        res = await self.coro_queue.put_nowait(self.__read_binary, id_)
        logger.debug('read_binary res={}'.format(repr(res)))
        
        if isinstance(res, Exception):
            raise res

        return res

    async def __read_binary(self, id_):
        logger.debug('{} __read_binary'.format(self.__class__.__module__, self.__class__.__name__))
        logger.debug('storage type = {}'.format(type(self.storage)))#self.__class__.__module__, self.__class__.__name__))

        coro = self.storage.read_binary(id_)
        logger.debug('coro = {}'.format(coro))
        logger.debug('waiting')
        res = await coro
        logger.debug('res = {}'.format(res))
        return res

    def list_files(self):
        return self.coro_queue.put_nowait(self.__list_files)

    async def __list_files(self):
        return (await self.storage.list_files())

def runserver(args):
    conf = modconf.import_class(
            args.conf_mod, 
            'Conf', 
            ('DEVELOP' if args.d else 'DEPLOY', args.conf_dir, args.impl), 
            folder=args.conf_dir)

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


