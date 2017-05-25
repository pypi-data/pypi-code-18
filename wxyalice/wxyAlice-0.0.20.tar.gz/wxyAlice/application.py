from gevent import pywsgi
import falcon


class Application(object):
    def __init__(self, me):
        self.me = (me['host'], me['port'])
        self.mid = me['mid']
        self.res = me['res']

    def Install(self):
        self.app = falcon.API(middleware=self.mid)
        map(lambda r: self.app.add_route(r[0], r[1]), self.res)

    def Forever(self):
        pywsgi.WSGIServer(self.me, self.app).serve_forever()
