#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import tornado.web


class DefaultHandler(tornado.web.RequestHandler):
    def prepare(self):
        if "static_path" in self.settings:
            prefix = "/static/"
            if "static_url_prefix" in self.settings:
                prefix = self.settings["static_url_prefix"]

            path = os.path.abspath(os.path.join(self.settings["static_path"], self.request.path[1:]))
            if os.path.exists(path) and os.path.isfile(path):
                return self.redirect(prefix + self.request.path[1:])
        
        if self.request.path.endswith(".html") and "template_path" in self.settings:
            path = os.path.abspath(os.path.join(self.settings["template_path"], self.request.path[1:]))
            if os.path.exists(path):
                return self.render(self.request.path[1:])
        
        if "default_view_not_found" in self.settings:
            path = os.path.abspath(os.path.join(self.settings["template_path"], self.settings["default_view_not_found"]))
            if os.path.exists(path):
                return self.render(self.settings["default_view_not_found"])

        self.set_status(404)
        return self.finish()
