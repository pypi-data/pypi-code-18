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
            logger.debug('  waiting')
            try:
                res = await coro
            except Exception as e:
                logger.error('encountered error while running coro')
                logger.error(e)
                res = e

            logger.debug('  result = {}'.format(res))
            future.set_result(res)
 
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

    async def close(self):
        logger.debug('CoroQueue close size={}'.format(self.__queue.qsize()))

        await self.cancel()

        while not self.__queue.empty():
            item = self.__queue.get_nowait()
            coro, future = item
            logger.debug('  coro: {}'.format(repr(coro)))
            
            task = self.loop.create_task(coro)

            ret = task.cancel()

            logger.debug('  cancel task: {}'.format(ret))

            continue

            res = await task

            logger.debug('  cancelled task: {}'.format(res))





