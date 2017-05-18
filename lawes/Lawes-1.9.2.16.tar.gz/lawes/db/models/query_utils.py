
from lawes.utils import tree
from lawes.utils import six
from bson.objectid import ObjectId

class Q(tree.Node):
    """
    Encapsulates filters as objects that can then be combined logically (using
    `&` and `|`).
    """
    AND = '$and'
    OR = '$or'

    def __init__(self, *args, **kwargs):
        if '_id' in kwargs :
            kwargs['_id'] = ObjectId(kwargs['_id'])
        super(Q, self).__init__(values=list(six.iteritems(kwargs)))

    def _combine(self, other, conn):
        if not isinstance(other, Q):
            raise TypeError(other)
        obj = type(self)()
        obj.add(self, other, conn)
        return obj

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)
