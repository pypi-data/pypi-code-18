from gevent import pywsgi
import falcon


class Application(object):
    def __init__(self, me, log):
        self.me = (me['host'], me['port'])
        self.name = me['name']
        self.desc = me['desc']
        self.mid = me['mid']
        self.res = me['res']
        self.log = log
        self.log.info("%s ---> start" % self.desc)

    def Install(self):
        self.log.info("%s ---> init" % self.desc)
        self.app = falcon.API(middleware=self.mid)
        list(map(lambda r: self.app.add_route(r[0], r[1]), self.res))
        return self

    def Forever(self):
        self.log.info("%s ---> run %s:%d" % (self.desc,
                                             self.me[0],
                                             self.me[1]))
        pywsgi.WSGIServer(self.me, self.app).serve_forever()
