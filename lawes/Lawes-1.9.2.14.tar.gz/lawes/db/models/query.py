# -*- coding:utf-8 -*-

from pymongo import MongoClient
from lawes.core.exceptions import MultipleObjectsReturned
from lawes.core.exceptions import DoesNotExist
from lawes.core.exceptions import UniqueError
from lawes.core.exceptions import MongoClientError
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId
from lawes.db.models.query_utils import Q
from lawes.db.models import sql
from lawes.db.models.fields import AutoField
import copy

CONF_RAESE = """
The correct formal is:
from lawes.db import models
models.setup(conf={'mongo_uri': 'mongodb://127.0.0.1:27017/test', 'db_name': 'testindex'})
self._mongo: %s , self._db: %s
"""

class ConfigQuerySet(object):

    def __init__(self):
        self.mongo = None
        self.db_name = ''

    def _setup(self, conf):
        """ 设置mongodb的连接方式
        """
        if self.mongo:
            return
        if self.db_name:
            return
        if not 'db_name' in conf:
            raise MongoClientError(CONF_RAESE % ('', ''))
        if not 'mongo_uri' in conf:
            raise MongoClientError(CONF_RAESE % ('', ''))
        self.mongo = MongoClient(conf['mongo_uri'])
        self.db_name = conf['db_name'].lower()

# init the MongoClient
configqueryset = ConfigQuerySet()

class QuerySet(object):

    def __init__(self, model=None, query=None):

        self.query_flag = False                    # set the query_flag to True after filer, order_by , that the methon only return QuerySet
        self.model = model
        self._mongo = configqueryset.mongo
        self._db = configqueryset.db_name           # the name of the db
        self.db_table = model._meta.db_table        # the name of the collection
        if not self._mongo or not self._db:
            raise MongoClientError(CONF_RAESE % (str(self._mongo), str(self._db)))
        self._collection = getattr(self._mongo[self._db], self.db_table)
        self.query = query or sql.Query(model)

    def __iter__(self):
        for data in self._fetch_all():
            yield data

    def __getitem__(self, item):
        if isinstance(item, int):
            self.query.limit = item
            self.query.skip = item
        elif isinstance(item, slice):
            self.query.skip = item.start
            self.query.limit = item.stop - item.start
        if isinstance(item, int):
            for iter_item in self.__iter__():
                return iter_item
        else:
            return self.__iter__()

    def __bool__(self):
        return bool(self.count())

    def count(self):
        return self._exec_sql().count()

    def _clone(self):
        if self.query_flag is False:
            obj = QuerySet(model=self.model)
        else:
            obj = self
        return obj

    def filter(self, *args, **kwargs):
        return self._filter_or_exclude(False, *args, **kwargs)

    def exclude(self, *args, **kwargs):
        return self._filter_or_exclude(True, *args, **kwargs)

    def _filter_or_exclude(self, negate, *args, **kwargs):
        if args and kwargs:
            return self
        clone = self._clone()
        clone.query_flag = True
        if negate:
            query = ~Q(*args, **kwargs) # TODO This has not QAed yet
        else:
            query = Q(*args, **kwargs)
        for arg in args:
            query = arg & query
        clone.query.add_q(query)
        return clone

    def _fetch_all(self, originally=False):
        """ run the sql actually
        :return:
        """
        multi_data = self.query.execute_sql(collection=self._collection)
        if originally is True:
            for data in multi_data:
                yield data
        else:
            for data in multi_data:
                obj = self.model()
                obj = obj.to_obj(data=data)
                yield obj

    def _insert(self, data):
        """
        Inserts a new record for the given model. This provides an interface to
        the InsertQuery class and is how Model.save() is implemented.
        """
        return self._collection.insert_one(data)

    def _update(self, data):
        """
        Inserts a new record for the given model. This provides an interface to
        the InsertQuery class and is how Model.save() is implemented.
        """
        mongodb_id = data.pop('_id')
        return self._collection.update({'_id': mongodb_id}, {'$set': data}, upsert=True)

    def init_index(self):
        """  create the index_1
        :param db_indexs: {'name': {'unique': False}}
        :return:
        """
        db_indexs = self.model._meta.db_indexs
        try:
            old_index = self._collection.index_information()
        except OperationFailure:
            old_index = {}

        for attr in db_indexs:
            unique = db_indexs[attr].get('unique', False)
            if not attr + '_1' in old_index:
                if unique is True:
                    self._collection.ensure_index(attr, unique=True)
                else:
                    self._collection.ensure_index(attr)
            elif unique is True:
                if not 'unique' in old_index[attr + '_1']:
                    self._collection.drop_index(attr + '_1')
                    self._collection.ensure_index(attr, unique=True)

    def get(self, *args, **kwargs):
        """
        Performs the query and returns a single object matching the given
        keyword arguments.
        """
        # self.filter_query.update(kwargs)
        # data = self._collection.find(self.filter_query)
        self = self._filter_or_exclude(False, *args, **kwargs)
        data = self.query.execute_sql(collection=self._collection)
        num = data.count()
        if num == 1:
            obj = self.model()
            obj = obj.to_obj(data=data[0])
            return obj
        if not num:
            raise DoesNotExist(
                "%s matching query does not exist." %
                self.query.as_sql()
            )
        raise MultipleObjectsReturned(
            "findone  %s returned more than one -- it returned %s!" %
            (self.query.as_sql(), num)
        )

    def get_or_create(self, **kwargs):
        """
        :param kwargs:  name='x'
        :return:  a tuple of (object, created), where created is a boolean
        specifying whether an object was created.
        """
        created = False
        try:
            index_information = self._collection.index_information()
        except OperationFailure:
            index_information = {}

        kwargs_keys = set(kwargs.keys())
        index_keys = [ filed for filed in index_information if index_information[filed].get('unique', False)]
        index_keys = [ index_key.replace('_1', '').replace('_-1', '') for index_key in index_keys ]
        need_index_set = kwargs_keys - set(index_keys)
        if need_index_set:
            raise UniqueError('UNIQUE constraint failed: %s: %s, please do collection.ensure_index: Model.objects.init_index()' % (
            self.db_table, str(need_index_set)))
        # self.filter_query.update(kwargs)
        # data = self._collection.find(self.filter_query)
        self = self._filter_or_exclude(False, **kwargs)
        data = self.query.execute_sql(collection=self._collection)
        num = data.count()
        if num == 1:
            to_obj_data = data[0]
        elif not num:
            to_obj_data = kwargs
            created = True
        else:
            raise MultipleObjectsReturned(
                "findone  %s returned more than one -- it returned %s!" %
                (self.query.as_sql(), num)
            )

        obj = self.model()
        obj = obj.to_obj(data=to_obj_data)
        if not num:
            obj.save()
        return obj, created

    def order_by(self, *field_names):
        field_names = field_names[0]
        if '-' in field_names:
            field_names = field_names.replace('-', '')
            order_index = -1
        else:
            order_index = 1
        self.query.order_by_query = (field_names, order_index)
        return self

    def delete(self):
        """
        Deletes the records in the current QuerySet.
        """
        for data in self._fetch_all(originally=True):
            self._remove(_id=str(data['_id']))

    def _remove(self, _id):
        remove_dict = {'_id': ObjectId(_id)}
        self._collection.delete_many(remove_dict)

    def get_auto_collection(self, field_name):
        auto_collection = getattr(self._mongo[self._db], self.db_table + '_auto_%s' % (field_name))
        return auto_collection

    def save_auto_field(self, local_fields=[]):
        data = {}
        local_fields = copy.deepcopy(local_fields)
        for field_name in local_fields:
            if isinstance(local_fields[field_name], AutoField):
                auto_collection = self.get_auto_collection(field_name=field_name)
                auto_infos = auto_collection.find_one_and_update(filter={'key': field_name}, update={'$inc': {'autoid': 1}},new=True, upsert=True)
                data[field_name] = auto_infos['autoid']
        return data

    def clean_auto_field(self, local_fields=[]):
        local_fields = copy.deepcopy(local_fields)
        for field_name in local_fields:
            if isinstance(local_fields[field_name], AutoField):
                auto_collection = self.get_auto_collection(field_name=field_name)
                auto_collection.delete_many({})