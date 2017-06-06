from gevent import pywsgi
import falcon
from .log import Log


class Application(object):
    def __init__(self, me):
        self.me = (me['host'], me['port'])
        self.name = me['name']
        self.desc = me['desc']
        self.mid = me['mid']
        self.res = me['res']
        self.log = Log()
        self.log.Info("%s ---> start" % self.desc)

    def Install(self):
        self.log.Info("%s ---> init" % self.desc)
        self.app = falcon.API(middleware=self.mid)
        list(map(lambda r: self.app.add_route(r[0], r[1]), self.res))
        return self

    def Forever(self):
        self.log.Info("%s ---> run %s:%d" % (self.desc,
                                             self.me[0],
                                             self.me[1]))
        pywsgi.WSGIServer(self.me, self.app).serve_forever()
