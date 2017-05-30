import json
import logging

from tornado.web import RequestHandler

from ppg_common.errors import (
    BubblesHttpError,
    ButterCupHTTPException,
    BlossomHTTPError,
    PpgHTTPError
)


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-session')
        self.set_header('Access-Control-Allow-Methods',
                        'GET,PUT,PATCH,POST,DELETE,OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(204)

    def write_error(self, status_code, **kwargs):
        exc_class, exc_obj, traceback = kwargs.get('exc_info')
        if any([exc_class is err for err in [
            BubblesHttpError,
            BlossomHTTPError,
            ButterCupHTTPException,
            PpgHTTPError
        ]]):
            self.finish({
                'message': exc_obj.log_message,
                'code': exc_obj.custom_code
            })
        else:
            self.finish({
                'message': traceback.format_exc(),
                'code': 500
            })

    def finish(self, chunk=None):
        logger = logging.getLogger()
        if isinstance(chunk, dict):
            logger.debug('response finish= ' + json.dumps(chunk))
        super(BaseHandler, self).finish(chunk)

    def write(self, chunk):
        logger = logging.getLogger()
        if isinstance(chunk, dict):
            logger.debug('response write= ' + json.dumps(chunk))
        super(BaseHandler, self).write(chunk)

    def initialize(self):
        logger = logging.getLogger()
        logger.debug(
            'request headers= ' + json.dumps(self.request.headers._dict))
        try:
            logger.debug(
                'request body= ' +
                json.dumps(self.request.body.decode("utf-8"))
            )
        except TypeError:
            pass
