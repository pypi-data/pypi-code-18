import aiohttp
import functools
import json
import logging

import aiohttp_security

import ws_sheets.tests.functions

import ws_sheets_server
import ws_sheets_server.packet

import ws_web_aiohttp
import ws_web_aiohttp.db
import ws_web_aiohttp.connections
import ws_web_aiohttp.security
import ws_web_aiohttp.security.wrappers
import ws_web_aiohttp.security.db as db

logger = logging.getLogger(__name__)

async def subhandler_sheet(request, book_id, sheet_id):
    
    template = request.app['template_env'].get_template('sheet.html')
    
    ws_url = '{}://{}/ws'.format(request.app['SCHEME_WS'], request.host)
    
    logger.debug('ws_url = {}'.format(ws_url))

    text = template.render(
            ws_url=ws_url,
            book_id=book_id,
            sheet_id=sheet_id,)
    
    response = aiohttp.web.Response(body=text)
    response.content_type = 'text/html'
    return response

async def handler_index(request):
   
    userid = await aiohttp_security.authorized_userid(request)

    logger.info('index userid = {}'.format(userid))

    template = request.app['template_env'].get_template('index.html')
    
    text = template.render()
    
    response = aiohttp.web.Response(body=text)
    response.content_type = 'text/html'
    return response

@ws_web_aiohttp.security.wrappers.require()
async def handler(request):

    logger.debug('host={}'.format(request.host))
    
    book_id = request.match_info.get('book_id')

    return await subhandler_sheet(request, book_id, '0')


async def book_new(request):
    userid = await aiohttp_security.authorized_userid(request)
    user = await ws_web_aiohttp.db.get_user(request.app, userid)
    
    logger.debug('book new. user = {}'.format(repr(user)))
    
    proto = await ws_web_aiohttp.connections.open_book_proto(request.app)
    res = await proto.request_new()
 
    logger.debug('new book id = {}'.format(proto.book_id))

    async with request.app['db_engine'].acquire() as conn:
        await conn.execute(db.books.insert().values(user_id=user[0], bookid=proto.book_id))

    return proto

@ws_web_aiohttp.security.wrappers.require_login()
async def handler_book_new(request):
    name = request.match_info.get('name')

    proto = await book_new(request)

    response = await subhandler_sheet(request, proto.book_id, '0')

    return response

@ws_web_aiohttp.security.wrappers.require_login()
async def handler_demo(request):

    name = request.match_info.get('name')

    logger.info('demo {}'.format(name))

    cls = ws_sheets.tests.functions.DEMOS[name]
    o = cls()

    proto = await book_new(request)

    o.setup(proto)

    response = await subhandler_sheet(request, proto.book_id, '0')

    return response

async def process_json_message(app, data, proto):

    logger.debug('json message\n{}'.format(data))

    p = None

    async def f(p):
        await p.write_response_sheet_data(data['sheet_id'])

    if data['type'] == 'get_sheet_data':
        p = ws_sheets_server.packet.RequestSheetData(data['book_id'], data['sheet_id'])
    elif data['type'] == 'add_col':
        p = ws_sheets_server.packet.AddColumn(data['book_id'], data['sheet_id'], data['i'])
    elif data['type'] == 'add_row':
        p = ws_sheets_server.packet.AddColumn(data['book_id'], data['sheet_id'], data['i'])
    elif data['type'] == 'set_script_pre':
        p = ws_sheets_server.packet.SetScriptPre(data['book_id'], data['text'])
        p.callback_post.add_callback(functools.partial(p.write_response_sheet_data, data['sheet_id']))
    elif data['type'] == 'set_script_post':
        p = ws_sheets_server.packet.SetScriptPost(data['book_id'], data['text'])
        p.callback_post.add_callback(functools.partial(p.write_response_sheet_data, data['sheet_id']))
    elif data['type'] == 'set_cell':
        p = ws_sheets_server.packet.SetCell(data['book_id'], data['sheet_id'], data['r'], data['c'], data['s'])
    
    if p:
        proto.write(p)

async def handler_websocket(request):
    logger.debug('websocket handler')
    ws = aiohttp.web.WebSocketResponse()
    
    await ws.prepare(request)

    proto = await ws_web_aiohttp.connections.open_book_proto_web(request.app, ws)

    logger.debug('ws: wait for message')
    async for msg in ws:
        logger.debug('ws: msg = {}'.format(repr(msg)))
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                try:
                    data = json.loads(msg.data)
                except Exception as e:
                    logger.warning(e)
                else:
                    await process_json_message(request.app, data, proto)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error('ws connection closed with exception {}'.format(repr(ws.exception())))

    return ws

