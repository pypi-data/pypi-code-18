import falcon


class Http400(object):
    def __init__(self, msg):
        raise falcon.HTTPBadRequest('', msg)

class Http401(object):
    def __init__(self, msg):
        raise falcon.HTTPUnauthorized('', msg)


class Http406(object):
    def __init__(self, msg):
        raise falcon.HTTPNotAcceptable(msg)

class Http415(object):
    def __init__(self, msg):
        raise falcon.HTTPUnsupportedMediaType(msg)

class Http500(object):
    def __init__(self, msg):
        raise falcon.HTTPInternalServerError('',msg)
class Http500(object):
    def __init__(self, msg):
        raise falcon.HTTPInternalServerError('',msg)
