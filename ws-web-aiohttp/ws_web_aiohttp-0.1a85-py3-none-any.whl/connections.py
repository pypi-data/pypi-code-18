import asyncio
import functools
import json
import logging
import numpy

import ws_sheets_server
import ws_sheets_server.client_aio

import ws_web_aiohttp

logger = logging.getLogger(__name__)

def cells_array(cells):
    
    def f(c):
        v = c.value
        v = repr(v)
        #if isinstance(v, str): v = "\"" + v + "\""
        try:
            return json.dumps([c.string, v])
        except Exception as e:
            logger.error('error while json stringifying {}\n{}'.format(repr(v), e))
            raise

    return numpy.vectorize(f, otypes=[str])(cells).tolist()

class BookProtocol(ws_sheets_server.client_aio.BookProtocol):
    def __init__(self, loop, ws):
        super(BookProtocol, self).__init__(loop)
        self.ws = ws

    def packet_received(self, packet):
        super(BookProtocol, self).packet_received(packet)
        
        logger.debug('{} received {}'.format(self.__class__.__name__, packet.__class__.__name__))
        
        if isinstance(packet, ws_sheets_server.packet.ResponseSheetData):
            self.ws.send_json({
                'type':'response_sheet_data',
                'cells':cells_array(packet.cells),
                'script_pre':packet.script_pre,
                'script_pre_output':packet.script_pre_output,
                'script_post':packet.script_post,
                'script_post_output':packet.script_post_output,
                })

async def open_book_proto_web(app, ws):
    coro = app.loop.create_connection(
            functools.partial(BookProtocol, app.loop, ws),
            'localhost',
            app['conf'].ws_sheets_server.PORT)
    
    transport, proto = await coro

    return proto

async def open_book_proto(app):
    coro = app.loop.create_connection(
            functools.partial(ws_sheets_server.client_aio.BookProtocol, app.loop),
            'localhost',
            app['conf'].ws_sheets_server.PORT)
    
    transport, proto = await coro

    return proto

