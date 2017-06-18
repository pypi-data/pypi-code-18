import asyncio
import functools
import pickle
import logging
import numpy

logger = logging.getLogger(__name__)

import ws_callbacks
import ws_sheets_server.client
import ws_sheets_server.packet
import ws_storage.protocol

class ClientProtocol(ws_storage.protocol.Protocol):

    def book_new(self):
        p = ws_sheets_server.packet.RequestBookNew()
        return self.write(p)

    def request_sheet_data(self, book_id, sheet_id):
        p = ws_sheets_server.packet.RequestSheetData(book_id, sheet_id)
        return self.write(p)

class BookProtocol(ws_storage.protocol.Protocol):
    """
    there was a queation of whether client Cell should contain stringized
    value or the actual value. if actual value, it will need to be pickleable
    or handle the error if not pickleable. This adds a security risk; the
    codemach security method only checks code when it is executed, and the user
    can write a __setstate__ function with malicious code. Solution?
    """
    def __init__(self, loop):
        super(BookProtocol, self).__init__(loop)
        
        self.book_id = None

        self.temp = ws_sheets_server.client.Book(self)

        self.callback_on_write = ws_callbacks.Callbacks()

    def __getitem__(self, sheet_id):
        return self.temp[sheet_id]

    def packet_received(self, packet):
        logger.debug('packet received: %s', repr(packet))
        try:
            self.loop.create_task(packet(self))
        except Exception as e:
            logger.error(e)

    async def request_new(self):
        """
        Send RequestBookNew.
        This object will then reference the new book.
        """
        p = ws_sheets_server.packet.RequestBookNew()
        
        fut = self.write(p)

        logger.debug('{} request new await response'.format(self.__class__.__name__))

        res = await fut

        self.book_id = res.book_id
   
        logger.debug('received new book {}'.format(self.book_id))

    def set_docs(self, s):
        """
        :param s: doc string in rst syntax
        """
        return self.write(ws_sheets_server.packet.SetDocs(self.book_id, s))

    def set_cell(self, sheet_id, r, c, s):
        """
        :param sheet_id: sheet id
        :param r: row
        :param c: column
        :param s: code string
        """
        logger.debug('set_cell{}'.format((sheet_id, r, c, s)))
        self.callback_on_write()
        return self.write(ws_sheets_server.packet.SetCell(self.book_id, sheet_id, r, c, s))
    
    def set_script_pre(self, s):
        """
        """
        return self.write(ws_sheets_server.packet.SetScriptPre(self.book_id, s))

    def set_script_post(self, s):
        """
        """
        return self.write(ws_sheets_server.packet.SetScriptPost(self.book_id, s))

    def request_sheet_data(self, sheet_id):
        """
        """
        return self.write(ws_sheets_server.packet.RequestSheetData(self.book_id, sheet_id))

    def get_script_post_output(self):
        """
        """
        return self.write(ws_sheets_server.packet.GetScriptPostOutput(self.book_id))
    
    def get_cell_data(self, sheet_id):
        """
        """
        return self.write(ws_sheets_server.packet.GetCellData(self.book_id, sheet_id))

    def add_column(self, sheet_id, i):
        """
        """
        return self.write(ws_sheets_server.packet.AddColumn(self.book_id, sheet_id, i))

    def add_row(self, sheet_id, i):
        """
        """
        return self.write(ws_sheets_server.packet.AddRow(self.book_id, sheet_id, i))

    

