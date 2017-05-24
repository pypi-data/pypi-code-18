#!/usr/bin/env python
#-*- coding:utf-8 -*-

import routes
import tornado
import tornado.web
import defaulthandler


class Application(tornado.web.Application):
    @classmethod
    def start(cls, port = 8080, **kwargs):
        settings = {
            "handler_path": "handlers",
            "template_path": "views",
            "static_path": "static",
            "default_handler_class": defaulthandler.DefaultHandler,
            "default_view_error": "500.html",
            "default_view_not_found": "404.html",
        }
        settings.update(kwargs)

        handlers = routes.route.get_routes(settings["handler_path"])
        application = Application(handlers, **settings)
        application.listen(port)

        for domain, spec_list in application.handlers: 
            for spec in spec_list:
                print domain.pattern, spec.regex.pattern, spec.handler_class

        tornado.ioloop.IOLoop.current().start()
