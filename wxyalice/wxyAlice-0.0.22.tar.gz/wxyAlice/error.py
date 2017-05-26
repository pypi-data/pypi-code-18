import falcon


class Http400(object):
    def __init__(self, msg):
        raise falcon.HTTPBadRequest('', msg)
