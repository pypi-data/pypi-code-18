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
    obj = backend.get_obj(str(model_class))
    if not obj:
        obj = db.query(model_class).get(_id)
        if obj:
            backend.set_obj(str(model_class), dumps(obj), expire=expire)
    else:
        obj = loads(obj)
        obj = db.merge(obj, load=False)
        #db.refresh(obj)

    if str(model_class) not in models:
        models[str(model_class)] = model_class

        @event.listens_for(model_class, 'after_update')
        def object_is_pending(mapper, connection, target):
            backend.clear(str(target.__class__))

    return obj   


def cached_by_condition(model_class, *criterion, **kwargs):
    """
    通过id读取缓存对象
    :param model_class: 
    :type model_class: 
    :param criterion: 
    :type criterion: model.id==1, model.name=='ddd'
    :param kwargs: 
    :type kwargs: set expire in here
    :return: 
    :rtype: 
    """
    obj = backend.get_obj(str(model_class))
    if not obj:
        obj = db.query(model_class).filter(*criterion).first()
        if obj:
            backend.set_obj(str(model_class), dumps(obj), expire=kwargs.get('expire', 3600))
    else:
        obj = loads(obj)
        obj = db.merge(obj, load=False)
        #db.refresh(obj)

    if str(model_class) not in models:
        models[str(model_class)] = model_class

        @event.listens_for(model_class, 'after_update')
        def object_is_pending(mapper, connection, target):
            backend.clear(str(target.__class__))

    return obj

