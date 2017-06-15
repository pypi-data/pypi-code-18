

class Storage(object):
    """
    An abstaction for reading and writing sheets from
    and to long term storage.
    """
    def get_object(self, object_id):
        raise NotImplementedError()

    def save_object(self, object_id, object_):
        raise NotImplementedError()

class StorageProxy(object):
    """
    This class is an abstraction for indirect access to a Storage object.
    """
    def get_object(self, object_id):
        raise NotImplementedError()

    def save_object(self, object_id, object_):
        raise NotImplementedError()



