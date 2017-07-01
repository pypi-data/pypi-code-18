# To Integrate the data with the cache and expose the data
# Author: Partha
import json

from .connector import BaseConnector, PostgresConnector, RedshiftConnector, ElasticSearchConnector
from .cache_mixin import BaseCache, ResourceCache

class ChoreAPI(object):
    """
    Base API for the interacting with the Remote DataBase 
    """
    creds = {}
    connector_klass = None
    connector = None
    UUID = None
    cache_manager = None

    def __init__(self, *args, **kwargs):
        super(ChoreAPI, self).__init__()
        assert 'app_type' in kwargs, "Please provide app_type"
        assert 'cred_type' in kwargs, "Please provide cred_type"        
        assert 'host' in kwargs, "Please provide host"
        assert 'db' in kwargs, "Please provide db"
        assert 'username' in kwargs, "Please provide username"
        assert 'password' in kwargs, "Please provide password"
        assert 'port' in kwargs, "Please provide port"
        assert 'UUID' in kwargs, "Please provide a UUID"

        self.creds['host'] = kwargs['host']
        self.creds['db'] = kwargs['db']
        self.creds['username'] = kwargs['username']
        self.creds['password'] = kwargs['password']
        self.creds['port'] = kwargs['port']
        self.creds['app_type'] = kwargs['app_type']
        self.creds['cred_type'] = kwargs['cred_type']
        self.UUID = kwargs['UUID']

        self._get_connector_class()
        self._connect()

    def _get_connector_class(self):
        """
        Used to Find the connector class
        """
        if self.creds['app_type'] == "RDBMS":
            if self.creds['cred_type'] == "POSTGRES":
                self.connector_klass = PostgresConnector
                return True

            if self.creds['cred_type'] == "REDSHIFT":
                self.connector_klass = RedshiftConnector
                return True
        raise NotImplementedError

    def _connect(self):
        """
        Used to connect with the multiple Database or File Vendor
        """
        self.connector = self.connector_klass(**self.creds)
        self.connector.connect()

    def _format(self, data, _format):
        """
        Used to convert the data to given format
        """
        data = data.fillna('')

        if _format == "csv":
            data = data.to_csv(index = False)
        
        if _format == "excel":
            data = data.to_excel("output.xlsx")
        
        if _format == "html":
            data = data.to_html(index = False)
        
        if _format == "json":
            data = data.to_dict(orient = "records")
        return data

    def getTablesList(self, _format = 'json', reset = False):
        """
        Used to retrieve the tables List
        """
        #1. Look in the cache with the UUID
        _cache_flag = False
        self.cache_manager = ResourceCache(UUID = self.UUID)
        if reset is False:
            data = self.cache_manager.getTableNames()
            if data is None:
                _cache_flag = True
        else:
            #2. Get data from connector
            _cache_flag = True
        
        if _cache_flag is True:
            query = """
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public';
            """
            self.connector.execute(query = query)
            data = self.connector.data
            self.cache_manager.cacheTableNames(tables = self.connector.data)
        
        # Format the data
        return self._format(data, _format)        

    def getTableFieldsList(self, table_name = None, reset = False, _format = "json"):
        """
        Used to retrieve the fields in the table along with the data type
        """
        _cache_flag = False
        self.cache_manager = ResourceCache(UUID = self.UUID)
        if reset is False:
            data = self.cache_manager.getFieldNames(table_name = table_name)
            if data is None:
                _cache_flag = True
        else:
            #2. Get data from connector
            _cache_flag = True
        
        if _cache_flag is True:
            query = """
                SELECT table_name, column_name, data_type, is_nullable, column_default, character_maximum_length
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name   = '"""+ table_name + """';"""
            self.connector.execute(query = query)
            data = self.connector.data
            self.cache_manager.cacheFieldNames(table_name = table_name, fields = self.connector.data)            

        return self._format(data, _format)        

    #TODO: Need to include pagination details
    def getTableData(self, table_name = None, reset = False, _format = None, page = 1, page_size = 100):
        """
        Used to retrieve the table data
        """
        _cache_flag = False
        self.cache_manager = ResourceCache(UUID = self.UUID)
        if reset is False:
            data = self.cache_manager.getTableData(table_name = table_name)
            if data is None:
                _cache_flag = True                
        else:
            #2. Get data from connector
            _cache_flag = True
        
        if _cache_flag is True:
            query = """
                SELECT * from %s;
            """%table_name
            self.connector.execute(query = query)
            data = self.connector.data
            self.cache_manager.cacheTableData(table_name = table_name, data = data)            

        # Slice the data
        _from = ((page - 1) * page_size)
        _to = page * page_size
        data = data[_from : _to]
        # Debug
        print "TableData", _cache_flag
        # Format the data
        return self._format(data, _format)

    def getTableFieldsData(self, *args, **kwargs):
        """
        Used to retrieve the table specific fields data
        """
        raise NotImplementedError 

    #TODO: Need to include pagination(fixed pagination)
    def getQueryData(self, query_name = None, query = None, _format = None, reset = True, page = 1, page_size = 100):
        """ 
        Used to execute the custom query 
        """
        _cache_flag = False
        self.cache_manager = ResourceCache(UUID = self.UUID)
        if reset is False:
            data = self.cache_manager.getQueryData(query_name = query_name)
            if data is None:
                _cache_flag = True
        else:
            #2. Get data from connector
            _cache_flag = True
        
        if _cache_flag is True:
            self.connector.execute(query = query)
            data = self.connector.data
            self.cache_manager.cacheQueryData(query_name = query_name, data = data)            

        # Slice the result
        _from = ((page - 1) * page_size)
        _to = page * page_size
        data = data[ _from : _to ]
        # Debug
        print "QueryData", _cache_flag
        # Format the data
        return self._format(data, _format)


"""
Example:
creds = {
    'app_type':'RDBMS',
    'cred_type':'POSTGRES',
    'host':'localhost',
    'db':'sunrisebilling',
    'username':'integra',
    'password':'integra',
    'port':5432,
    'UUID':'test'
}
from chore.chore_api import ChoreAPI
sd = ChoreAPI(**creds)

# Getting Tables List
sd.getTablesList()

# Getting Table Columns/Fields List
sd.getTableFieldsList(table_name = "gbl_process")

# Getting Specific table data
sd.getTableData(table_name = "gbl_process")
## Specifying the page_size
sd.getTableData(table_name = "gbl_process", page_size = 20)
## Specifying the page 
sd.getTableData(table_name = "gbl_process", page_size = 20, page = 2)
## Resetting the data
sd.getTableData(table_name = "gbl_process", reset = True)

# Getting query data
sd.getQueryData(query_name = "test", query = "select * from gbl_process")

"""
