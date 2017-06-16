import asyncio
import logging

logger = logging.getLogger(__name__)

class CoroQueue(object):
    def __init__(self, loop):
        self.loop = loop
        self.__queue = asyncio.Queue()

    def schedule_run_forever(self):
        logger.debug('schedule_run_forever')
        
        self.__task_run_forever = self.loop.create_task(self.run_forever())

    async def run_forever(self):
        logger.debug('run_forever')

        while True:
            #coro, future = await self.__coro_queue.get()
            item = await self.__queue.get()
            #logger.debug('Book coro queue get {}'.format((coro, future)))
            logger.debug('Book coro queue get {}'.format(item))
            coro, future = item
            logger.debug('  coro={}'.format(coro))
            logger.debug('  future={}'.format(future))
            future.set_result(await coro)
 
    def put_nowait(self, f, *args):
        logger.debug('put f={} args={}'.format(f, args))

        future = self.loop.create_future()
        coro = f(*args)
        
        if not asyncio.iscoroutine(coro):
            raise RuntimeError('{} is not a coroutine'.format(f))
        
        self.__queue.put_nowait((coro, future))

        logger.debug('coro={}'.format(coro))
        
        return future

    async def cancel(self):

        self.__task_run_forever.cancel()

