import jwt
import datetime


class Authorization(object):
    def __init__(self, secrete='kiss ever never teach'):
        self.secrete = secrete
        self.algorithm = 'HS256'

    def Exp(self, delta=7*86400):
        return datetime.datetime.utcnow() + datetime.timedelta(seconds=delta)

    def EnCode(self, _id):
        return jwt.encode({'exp': self.Exp(), '_id':_id},
                   self.secrete,
                   algorithm=self.algorithm).decode()

    def DeCode(self, token):
        return jwt.decode(token, self.secrete,algorithm=self.algorithm)


