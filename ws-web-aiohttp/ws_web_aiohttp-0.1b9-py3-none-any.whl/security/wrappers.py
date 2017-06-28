import asyncio
import functools
import aiohttp.web
import aiohttp_security
import logging

logger = logging.getLogger(__name__)

def require():
    def wrapper(f):
        @functools.wraps(f)
        async def wrapped(request): #async def wrapped(self, request):
            logger.debug('require wrapper')
            logger.debug('rel_url = {}'.format(request.rel_url))

            book_id = request.match_info.get('book_id')

            logger.debug('book_id = {}'.format(book_id))
            
            has_perm = await aiohttp_security.permits(request, book_id)
            if not has_perm:
                message = 'User has no permission {}'.format(book_id)
                logger.info(message)

                return aiohttp.web.HTTPFound(request.app['LOGIN_URL']+'?next='+request.rel_url.path)

            #return (await f(self, request))
            return (await f(request))
        return wrapped
    return wrapper

def require_login():
    def wrapper(f):
        @functools.wraps(f)
        async def wrapped(request): #async def wrapped(self, request):
            logger.debug('require_login wrapper')
            logger.debug('rel_url = {}'.format(request.rel_url))
            
            userid = await aiohttp_security.authorized_userid(request)

            logger.debug('userid = {}'.format(userid))
            
            if not userid:
                message = 'Not signed in'
                logger.info(message)

                return aiohttp.web.HTTPFound(request.app['LOGIN_URL']+'?next='+request.rel_url.path)

            #return (await f(self, request))
            return (await f(request))
        return wrapped
    return wrapper


