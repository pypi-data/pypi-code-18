# To manage the data in cacahe
# Author: Partha
from django.core.cache import caches

cache = caches['default']


class BaseCache(object):

    def __init__(self, *args, **kwargs):
        super(BaseCache, self).__init__()

    def set(self, key = None, data = None):
        assert key is not None, "Please provide the key "
        try:
            cache.set(key, data)
            return True
        except Exception, e:
            print str(e)
            return False

    def get(self, key=None):
        assert key is not None, "Please provide a key"
        try:
            return cache.get(key)
        except Exception, e:
            print str(e)
            return None

class ResourceCache(BaseCache):

    cache_key = None

    def __init__(self, *args, **kwargs):
        super(ResourceCache, self).__init__()
        if 'UUID' in kwargs and kwargs['UUID'] != "":
            self.cache_key = kwargs['UUID']

    def cacheTableNames(self, tables = None):
        return self.set(self.cache_key + "_tables", tables)
        
    def cacheFieldNames(self, table_name = None, fields = None):
        return self.set(self.cache_key + "_" + table_name + "_fields", fields)

    def cacheTableData(self, table_name = None, data = None):
        return self.set(self.cache_key + "_" + table_name + "_data", data)

    def cacheQueryData(self, query_name = None, data = None):
        return self.set(self.cache_key + "_query_" + query_name + "_data", data)
    
    def getTableNames(self, _format = None):
        _data = self.get(self.cache_key + "_tables")
        if _data is None:
            return None
        if _format == 'json': 
            return _data.to_json(index = False)
        if _format == 'table': 
            return _data.to_html(index = False)
        if _format == 'csv': 
            return _data.to_csv(index = False)
        if _format == 'excel': 
            return _data.to_excel("output.xlsx")
        return _data

    def getFieldNames(self, table_name = None, _format = None):
        _data = self.get(self.cache_key + "_" + table_name + "_fields")
        if _format == 'json': 
            return _data.to_json(index = False)
        if _format == 'table': 
            return _data.to_html(index = False)
        if _format == 'csv': 
            return _data.to_csv(index = False)
        if _format == 'excel': 
            return _data.to_excel("output.xlsx")
        return _data

    def getTableData(self, table_name = None, _format = None):
        _data = self.get(self.cache_key + "_" + table_name + "_data")
        if _format == 'json': 
            return _data.to_json(index = False)
        if _format == 'table': 
            return _data.to_html(index = False)
        if _format == 'csv': 
            return _data.to_csv(index = False)
        if _format == 'excel': 
            return _data.to_excel("output.xlsx")
        return _data

    def getQueryData(self, query_name = None, _format = None):
        _data = self.get(self.cache_key + "_query_" + query_name + "_data")
        if _format == 'json': 
            return _data.to_json(index = False)
        if _format == 'table': 
            return _data.to_html(index = False)
        if _format == 'csv': 
            return _data.to_csv(index = False)
        if _format == 'excel': 
            return _data.to_excel("output.xlsx")
        return _data
        
        
