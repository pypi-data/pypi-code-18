"""A pure Python keyring backend using the Freedesktop secret service.
"""

__version__ = '0.2'

import os

from keyring.backend import KeyringBackend
from keyring.util.properties import ClassProperty
from jeepney import new_method_call, MessageGenerator, Properties, DBusErrorResponse
from jeepney.integrate.blocking import connect_and_authenticate, Proxy


# ---- Generated bindings from jeepney.bindgen ----
class Service(MessageGenerator):
    interface = 'org.freedesktop.Secret.Service'

    def __init__(self, object_path='/org/freedesktop/secrets',
                 bus_name='org.freedesktop.secrets'):
        super().__init__(object_path=object_path, bus_name=bus_name)

    def OpenSession(self, algorithm, input):
        return new_method_call(self, 'OpenSession', 'sv', (algorithm, input))

    def CreateCollection(self, properties, alias):
        return new_method_call(self, 'CreateCollection', 'a{sv}s',
                               (properties, alias))

    def SearchItems(self, attributes):
        return new_method_call(self, 'SearchItems', 'a{ss}', (attributes,))

    def Unlock(self, objects):
        return new_method_call(self, 'Unlock', 'ao', (objects,))

    def Lock(self, objects):
        return new_method_call(self, 'Lock', 'ao', (objects,))

    def LockService(self):
        return new_method_call(self, 'LockService')

    def ChangeLock(self, collection):
        return new_method_call(self, 'ChangeLock', 'o', (collection,))

    def GetSecrets(self, items, session):
        return new_method_call(self, 'GetSecrets', 'aoo', (items, session))

    def ReadAlias(self, name):
        return new_method_call(self, 'ReadAlias', 's', (name,))

    def SetAlias(self, name, collection):
        return new_method_call(self, 'SetAlias', 'so', (name, collection))


class Collection(MessageGenerator):
    interface = 'org.freedesktop.Secret.Collection'

    def __init__(self, object_path, bus_name='org.freedesktop.secrets'):
        super().__init__(object_path=object_path, bus_name=bus_name)

    def Delete(self):
        return new_method_call(self, 'Delete')

    def SearchItems(self, attributes):
        return new_method_call(self, 'SearchItems', 'a{ss}', (attributes,))

    def CreateItem(self, properties, secret, replace):
        return new_method_call(self, 'CreateItem', 'a{sv}(oayays)b',
                               (properties, secret, replace))


class Item(MessageGenerator):
    interface = 'org.freedesktop.Secret.Item'

    def __init__(self, object_path, bus_name='org.freedesktop.secrets'):
        super().__init__(object_path=object_path, bus_name=bus_name)

    def Delete(self):
        return new_method_call(self, 'Delete')

    def GetSecret(self, session):
        return new_method_call(self, 'GetSecret', 'o', (session,))

    def SetSecret(self, secret):
        return new_method_call(self, 'SetSecret', '(oayays)', (secret,))
# ---- End of generated bindings ----


DEFAULT_COLLECTION = '/org/freedesktop/secrets/aliases/default'

class Keyring(KeyringBackend):
    """A keyring backend using the Freedesktop secret service."""
    def __init__(self, collection=DEFAULT_COLLECTION):
        self.conn = connect_and_authenticate(bus='SESSION')
        self.service = Proxy(Service(), self.conn)
        self.session_path = self.service.OpenSession('plain', ('s', ''))[1]
        self.collection_name = collection
        self.collection = Proxy(Collection(self.collection_name), self.conn)

    @ClassProperty
    @classmethod
    def priority(cls):
        if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
            raise RuntimeError("Environment variable DBUS_SESSION_BUS_ADDRESS "
                               "not set")
        conn = connect_and_authenticate(bus='SESSION')
        try:
            conn.send_and_get_reply(Properties(Service()).get('Collections'))
        except DBusErrorResponse:
            raise RuntimeError("Could not communicate with /org/freedesktop/secrets")
        # The well-tested Secret Service backend has priority 5. We'll defer
        # to that if it's available.
        return 4

    def _find(self, service, username):
        return self.collection.SearchItems(
            {"username": username, "service": service})[0]

    def _proxy_item(self, obj_path):
        return Proxy(Item(obj_path), self.conn)

    def get_password(self, service, username):
        for obj_path in self._find(service, username):
            secret = self._proxy_item(obj_path).GetSecret(self.session_path)[0]
            session, enc_params, value, content_type = secret
            # TODO: check encoding with content_type
            return bytes(value).decode('utf-8')

    def set_password(self, service, username, password):
        attributes = {
            "application": "python-keyring",
            "service": service,
            "username": username
        }
        label = "Password for '%s' on '%s'" % (username, service)
        secret = (self.session_path, b'', password.encode('utf-8'),
                  'text/plain; charset=utf8')
        properties = {
            'org.freedesktop.Secret.Item.Label': ('s', label),
            'org.freedesktop.Secret.Item.Attributes': ('a{ss}', attributes),
        }
        self.collection.CreateItem(properties, secret, replace=True)

    def delete_password(self, service, username):
        for obj_path in self._find(service, username):
            prompt_path = self._proxy_item(obj_path).Delete()[0]
            assert prompt_path == '/'
            return
