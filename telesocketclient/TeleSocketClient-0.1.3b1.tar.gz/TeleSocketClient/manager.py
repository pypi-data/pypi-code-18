from . import TeleSocket as ts, ADDRESS
from . import types


class TeleSocket(ts):
    def __init__(self, address=ADDRESS, daemonic=True, start=True):
        super(TeleSocket, self).__init__(address, daemonic, start)

    def generate_codes(self, count):
        payload = {'count': count}
        codes = self.request('generate_codes', payload).wait()
        return codes

    def clients_list(self):
        req = self.request('clients_list')
        clients = [types.Client.serialize(**raw_client) for raw_client in req.wait().get('clients')]
        return clients

    def get_client_bots(self, target):
        payload = {'target': target}
        result = self.request('get_client_bots', payload).wait()
        return types.WebHookLimits.serialize(**result)

    def find_user(self, username=None, user_id=None):
        payload = {}
        if username:
            payload['username'] = username
        if user_id:
            payload['user_id'] = user_id
        req = self.request('find_user', payload).wait()
        return [types.User.serialize(**raw_user) for raw_user in req.wait().get('result')]
