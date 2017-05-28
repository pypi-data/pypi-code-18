"""A pure Python keyring backend using the Freedesktop secret service.
"""

__version__ = '0.1'

import os

from keyring.backend import KeyringBackend
from keyring.util import properties
from jeepney import new_method_call, DBusObject, Properties, DBusErrorResponse
from jeepney.integrate.blocking import connect_and_authenticate

secret_service = DBusObject('/org/freedesktop/secrets',
                            bus_name= 'org.freedesktop.secrets',
                            interface='org.freedesktop.Secret.Service')

class DBusMethods:
    """Wrappers for the subset of the secrets API we use.
    
    These methods will block while waiting for a reply.
    """
    def __init__(self, connection, collection):
        self.connection = connection
        self.session_path = self._open_session()
        self.collection = collection
        self.collection_obj = DBusObject(collection,
                                 bus_name='org.freedesktop.secrets',
                                 interface='org.freedesktop.Secret.Collection')

    def search(self, attribs):
        msg = new_method_call(self.collection_obj, 'SearchItems', 'a{ss}', (attribs,))
        return self.connection.send_and_get_reply(msg).body[0]

    def _open_session(self):
        msg = new_method_call(secret_service, 'OpenSession', 'sv',
                              ('plain', ('s', '')))
        return self.connection.send_and_get_reply(msg).body[1]

    # TODO: Handle unlocking. This will fail if the item is locked.
    def get_secret(self, item_path):
        item = DBusObject(item_path, bus_name='org.freedesktop.secrets',
                          interface='org.freedesktop.Secret.Item')
        msg = new_method_call(item, 'GetSecret', 'o',  (self.session_path,))
        return self.connection.send_and_get_reply(msg).body[0]

    def create_item(self, label, attributes, password, replace=True):
        secret = (self.session_path, b'', password.encode('utf-8'), 'text/plain; charset=utf8')
        properties = {
            'org.freedesktop.Secret.Item.Label': ('s', label),
            'org.freedesktop.Secret.Item.Attributes': ('a{ss}', attributes),
        }
        msg = new_method_call(self.collection_obj, 'CreateItem', 'a{sv}(oayays)b',
                              (properties, secret, replace))
        return self.connection.send_and_get_reply(msg).body[0]

    def delete(self, item_path):
        item = DBusObject(item_path, bus_name='org.freedesktop.secrets',
                          interface='org.freedesktop.Secret.Item')
        msg = new_method_call(item, 'Delete')
        prompt_path = self.connection.send_and_get_reply(msg).body[0]
        assert prompt_path == '/'

DEFAULT_COLLECTION = '/org/freedesktop/secrets/aliases/default'

class Keyring(KeyringBackend):
    """A keyring backend using the Freedesktop secret service."""
    def __init__(self, collection=DEFAULT_COLLECTION):
        self.conn = connect_and_authenticate(bus='SESSION')
        self.dbus_methods = DBusMethods(self.conn, collection)

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
            raise RuntimeError("Environment variable DBUS_SESSION_BUS_ADDRESS "
                               "not set")
        conn = connect_and_authenticate(bus='SESSION')
        try:
            conn.send_and_get_reply(Properties(secret_service).get('Collections'))
        except DBusErrorResponse:
            raise RuntimeError("Could not communicate with /org/freedesktop/secrets")
        # The well-tested Secret Service backend has priority 5. We'll defer
        # to that if it's available.
        return 4

    def _find(self, service, username):
        return self.dbus_methods.search({"username": username, "service": service})

    def get_password(self, service, username):
        for obj_path in self._find(service, username):
            secret = self.dbus_methods.get_secret(obj_path)
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
        self.dbus_methods.create_item(label, attributes, password, replace=True)

    def delete_password(self, service, username):
        for obj_path in self._find(service, username):
            return self.dbus_methods.delete(obj_path)

