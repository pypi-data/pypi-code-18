#!/usr/bin/env python3
import functools
import logging
import os
import jinja2

import aiohttp
import aiohttp.web
import aiohttp_security
import aiohttp_session.redis_storage
import aioredis
import aiopg
import aiopg.sa
import sys
import json
import requests_oauthlib
import ssl
import modconf
import argparse
import asyncio
import pickle

import ws_sheets.tests.functions
import ws_sheets_server
import ws_sheets_server.packet

import ws_web_aiohttp.handlers
import ws_web_aiohttp.security.handlers
import ws_web_aiohttp.security.db_auth
import ws_web_aiohttp.security.db

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)

SCHEME = 'http'
SCHEME_WS = 'ws'

async def setup_db(db_engine):

    logger.info('setup_db')

    async with db_engine.acquire() as conn:
        with open(os.path.join(BASE_DIR, 'sql', 'init.sql')) as f:
            ret = (await conn.execute(f.read()))
        #ret = ws_web_aiohttp.security.db.metadata.create_all(bind=conn)
    
async def on_startup(app):
    
    db_engine = await aiopg.sa.create_engine(
            user=app['conf'].PG.user,
            password=app['conf'].PG.password,
            database=app['conf'].PG.db,
            host=app['conf'].PG.host)
   
    #aiohttp_session.setup(app, 
    #        aiohttp_session.redis_storage.RedisStorage(redis_pool))

    await setup_db(db_engine)

    aiohttp_security.setup(app,
            aiohttp_security.SessionIdentityPolicy(),
            ws_web_aiohttp.security.db_auth.DBAuthorizationPolicy(db_engine))

    app['db_engine'] = db_engine


async def setup_app(conf_mod, conf_dir, d, port=None):

    #redis_pool = await aioredis.create_pool(('localhost', 6379))
    conf = modconf.import_class(conf_mod, 'Conf', ('DEVELOP' if d else 'DEPLOY', port, conf_dir), folder=conf_dir)

    logging.config.dictConfig(conf.LOGGING)

    redis_pool = await aioredis.create_pool(('localhost', 6379))
   
    app = aiohttp.web.Application(middlewares=[
        aiohttp_session.session_middleware(aiohttp_session.redis_storage.RedisStorage(redis_pool))])
 
    app['conf'] = conf
   
    app.on_startup.append(on_startup)

    app['oauth'] = {}

    app['conf'] = modconf.import_class(conf_mod, 'Conf', ('DEVELOP' if d else 'DEPLOY', port))

    logging.config.dictConfig(app['conf'].LOGGING)

    app['template_env'] = jinja2.Environment(
            loader=jinja2.PackageLoader('ws_web_aiohttp', 'templates'))

    app['SCHEME'] = app['conf'].SCHEME
    app['SCHEME_WS'] = app['conf'].SCHEME_WS

    # routes
    app.router.add_get('/', ws_web_aiohttp.handlers.handler_index)
    app.router.add_get('/user/', ws_web_aiohttp.handlers.handler_user_index)
    app.router.add_get('/{book_id}/', ws_web_aiohttp.handlers.handler)
    app.router.add_get('/book_new/{name}/', ws_web_aiohttp.handlers.handler_book_new)
    app.router.add_get('/demo/{name}/', ws_web_aiohttp.handlers.handler_demo)
    app.router.add_get('/ws', ws_web_aiohttp.handlers.handler_websocket)
    
    app.router.add_get('/google_oauth2_login', ws_web_aiohttp.security.handlers.handler_google_oauth2_login)
    app.router.add_get('/google_oauth2_response', ws_web_aiohttp.security.handlers.handler_google_oauth2_response)

    app['LOGIN_URL'] = '/google_oauth2_login'

    # static routes
    if app['conf'].MODE == app['conf'].Mode.DEVELOP:
        app.router.add_static('/static/other/handsontable',
                path=os.path.join(os.environ['HOME'], 'web_sheets/handsontable/dist'),
                name='static_hot')
     
        app.router.add_static('/static/other/google',
                path=os.path.join(os.environ['HOME'], 'static/google'),
                name='static_google')
   
        app.router.add_static('/static/',
                path=os.path.join(BASE_DIR, 'static'),
                name='static')

    elif app['conf'].MODE == app['conf'].Mode.DEPLOY:
        app.router.add_static('/static/other',
                path=app['conf'].STATIC_DIR,
                name='static_other')

        app.router.add_static('/static/',
                path=os.path.join(BASE_DIR, 'static'),
                name='static')
    else:
        raise Exception('invalid mode')

    logger.debug('starting web app')

    return app

def runserver(args):
    loop = asyncio.get_event_loop()
    
    app = loop.run_until_complete(setup_app(args.conf_mod, args.conf_dir, args.d, args.p))

    aiohttp.web.run_app(
            app, 
            port=app['conf'].PORT, 
            ssl_context=app['conf'].SSL_CONTEXT)



