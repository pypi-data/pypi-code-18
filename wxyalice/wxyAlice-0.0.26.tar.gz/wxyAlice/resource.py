import falcon
from jsonschema import validate
from .error import Http400


def OK(func):
    def wrapper(self, ids, req, res):
        req.context['ret'] = func(self, ids, req, res)
        res.status = falcon.HTTP_OK

    return wrapper


class Resource(object):
    def __init__(self):
        pass

    def Doc(self, req):
        return req.context['doc']

    def Qry(self, req):
        return req.params

    def Chk(self, doc):
        try:
            if self.schema:
                validate(doc, self.schema)
        except Exception as e:
            Http400(e.message)

    @OK
    def C(self, ids, req, res):
        doc = self.Doc(req)
        self.Chk(doc)
        return self.mod.C(ids, doc)

    @OK
    def Q(self, ids, req, res):
        return self.mod.Q(ids, self.Qry(req))

    @OK
    def R(self, ids, req, res):
        return self.mod.R(ids)

    @OK
    def U(self, ids, req, res):
        return self.mod.U(ids, self.Doc(req))

    @OK
    def D(self, ids, req, res):
        return self.mod.D(ids)
