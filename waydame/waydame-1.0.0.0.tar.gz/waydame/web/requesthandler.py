#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import traceback
import tornado.web
from tornado.util import ObjectDict


class RequestHandler(tornado.web.RequestHandler):
    """
        示例：
            @url("/index")
            class HandlerUrl(RequestHandler):
                def get(self):
                    return self.content("这是一个自定义Handler匹配URL的例子")
    """
    @property
    def context(self):
        """
            请求上下文
            在上下文里的数据，在模板文件可以直接通过key访问
            当context里的数据和调用template函数时传的参数冲突时，以context里的数据优先。
            e.g.:
            index.py
                self.context["page_title"] = "网易"
            index.html
                <title>{{ page_title }}</title>
        """
        if not hasattr(self, "_context"):
            self._context = ObjectDict()

        return self._context


    def prepare(self):
        """
            处理前执行代码
        """
        if "debug" in self.settings and self.settings["debug"]:
            print "{0} {1} {2}".format(self.request.method, self.request.path, self)
    
    
    def get_current_user(self):
        """
            用户验证函数
        """
        return self.get_secure_cookie("u")


    def content(self, content, content_type="text/plain; charset=utf-8"):
        """
            输出文本到页面
        """
        self.set_header("Content-Type", content_type)
        self.write(content)


    def json(self, obj, content_type="text/json; charset=utf-8", cls=None):
        """
            输出json结果
        """
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls))


    def file(self, path, filename="", content_type="application/x-octet-stream"):
        """
            输出文件
        """
        if path and os.path.isfile(path) and os.path.exists(path):
            if not filename:
                filename = os.path.basename(path)

            with open(path) as f:
                self.set_header("Content-Type", content_type)
                self.set_header("Content-Disposition", "filename=%s" % filename)
                self.write(f.read())

            self.finish()

        return self.set_status(404)


    def render(self, name, **kwargs):
        """
            返回页面模板
        """
        kwargs.update(self.context)
        return super(RequestHandler, self).render(name, **kwargs)


    def view(self, name, **kwargs):
        """
            返回页面模板
        """
        return self.render(name, **kwargs)


    def write_error(self, status_code, **kwargs):
        """
            处理页面错误
        """
        if "default_view_error" in self.settings:
            self.context.reason = self._reason
            if "exc_info" in kwargs:
                self.context.traceback = ""
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    self.context.reason = line
                    self.context.traceback += line

            path = os.path.abspath(os.path.join(self.settings["template_path"], self.settings["default_view_error"]))
            if os.path.exists(path):
                return self.render(self.settings["default_view_error"])

        return super(RequestHandler, self).write_error(status_code, **kwargs)
