class BaseAdapter(object):
    """
    PubSub adapter base class
    """

    def __init__(self):
        pass

    def publish(self, channel, message, **kwargs):
        raise NotImplementedError('Not implemented')

    def subscribe(self, channel, handler=lambda x: x, **kwargs):
        raise NotImplementedError('Not implemented')
