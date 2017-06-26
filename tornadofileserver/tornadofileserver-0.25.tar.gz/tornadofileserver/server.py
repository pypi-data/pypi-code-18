#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient
import gridfs
import os
import logging

import tornado.options
from tornado.options import define, options

import file_util as fu

define("port", default=8999, help="run on the given port", type=int)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", IndexHandler),
            (r"\/*.*", IndexHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass
class IndexHandler(BaseHandler):
    def get(self):
        path = fu.translate_path(self)
        if os.path.isfile(path):
            # file_name = uri.split('/')[-1]
            ctype = fu.guess_type(self,path)
            with open(path, 'rb') as f:
                data = f.read()
                # application/octet-stream
                self.set_header ('Content-Type', ctype)
                self.write(data)

        if os.path.isdir(path):
            print path
            files = [item for item in os.listdir(path)]
            print files
            self.render('index.html',files=files,path=path)
    def post(self):
        # TODO 上传文件
        pass




class ErrorHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.redirect('/')


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.info('Serving HTTP on 0.0.0.0 port %d ...' % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()


