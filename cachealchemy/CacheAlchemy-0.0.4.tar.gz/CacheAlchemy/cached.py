# coding=utf8
from sqlalchemy import event
try:
    from cPickle import loads, dumps
except:
    from pickle import loads, dumps

db = None
models = {}
backend = None

def init_cached(db_session, backend_obj):
    """
    初始化缓存
    :param db_session: 
    :type db_session: 
    :param backend_obj: 
    :type backend_obj: 
    :return: 
    :rtype: 
    """
    global db, backend
    db = db_session
    backend = backend_obj


def cached_by_id(model_class, _id, expire=3600):
    """
    通过id读取缓存对象
    :param model_class: 
    :type model_class: 
    :param _id: 
    :type _id: 
    :param expire: 
    :type expire: 
    :return: 
    :rtype: 
    """

    keys = '{}:{}'.format(str(model_class), _id)
    obj = backend.get_obj(keys)
    if not obj:
        obj = db.query(model_class).get(_id)
        if obj:
            backend.set_obj(keys, dumps(obj), expire=expire)
    else:
        obj = loads(obj)
        obj = db.merge(obj, load=False)

    if str(model_class) not in models:
        models[str(model_class)] = model_class

        @event.listens_for(model_class, 'after_update')
        def object_is_pending(mapper, connection, target):
            backend.clear('{}:{}'.format(str(target.__class__), target.id))

    return obj


class CachedQuery(object):
    def __init__(self, model_class):
        self.model = model_class
        self.query = db.query(model_class.id)

    def filter(self, *conditions):
        self.query = self.query.filter(*conditions)
        return self

    def order_by(self, *orders):
        self.query = self.query.order_by(*orders)
        return self

    def __getitem__(self, item):
        if type(item) == slice:
            self.query = self.query[item.start: item.stop]
        return self

    def all(self, expire=3600):
         for obj_id in self.query:
             yield cached_by_id(self.model, obj_id, expire=expire)