from opfront.client import OpfrontClient
from opfront.order import OrderResource
from opfront.product import ProductResource
from opfront.resource import OpfrontResource


class OpfrontSession(object):

    """
    OpfrontSession defines the set of resources available from the Opfront API.
    Can be used as a standard object as and as a context manager.

    Args:
        email (str): Email with which to login
        password (str): Password associated with the email
    """

    def __init__(self, email, password):
        client = OpfrontClient(email, password)

        # Resource definition
        self.spectacle = OpfrontResource('/spectacles', client)
        self.store = OpfrontResource('/stores', client)
        self.product = ProductResource('/products', client)
        self.order = OrderResource('/orders', client)

        # TODO: Test this once the user resource is accessible by admin users
        self.user = OpfrontResource('/users', client)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
