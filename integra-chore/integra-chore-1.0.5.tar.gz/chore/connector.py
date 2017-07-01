# Different Connectors for different vendors
# Author: Partha
import pandas as pd

from sqlalchemy import create_engine

class BaseConnector(object):

    connection = None

    def __init__(self, *args, **kwargs):
        super(BaseConnector, self).__init__()
        assert 'host' in kwargs, "Please provide host"
        assert 'db' in kwargs, "Please provide db"
        assert 'username' in kwargs, "Please provide username"
        assert 'password' in kwargs, "Please provide password"
        assert 'port' in kwargs, "Please provide port"
        
        self.host = kwargs['host']
        self.db = kwargs['db']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.port = kwargs['port']

    def connect(self, *args, **kwargs):
        """
        Need to override this method to connect with the db's
        """
        raise NotImplementedError

    def execute(self, *args, **kwargs):
        """
        Need to override this method to execute with the db's
        """
        raise NotImplementedError

    @property
    def as_table(self):
        if self.data is None:
            return None
        self.data = self.data.fillna('')
        return self.data.to_html(index = False)

    @property
    def as_csv(self):
        if self.data is None:
            return None
        self.data = self.data.fillna('')        
        return self.data.to_csv(index = False)

    @property
    def as_excel(self):
        if self.data is None:
            return None
        self.data = self.data.fillna('')        
        return self.data.to_excel("output.xlsx")

    @property
    def as_json(self):
        if self.data is None:
            return None
        self.data = self.data.fillna('')        
        return self.data.to_dict(orient = "records")

class PostgresConnector(BaseConnector):
    """
    Connector for the PostGres
    """
    def connect(self, *args, **kwargs):
        self.engine = create_engine('postgresql://%s:%s@%s:%s/%s'%(self.username, self.password, self.host, self.port, self.db))
        return True

    def execute(self, *args, **kwargs):
        assert "query" in kwargs, "Please provide the query name"
        self.data = pd.read_sql_query(kwargs['query'],con = self.engine)
        return self

class RedshiftConnector(BaseConnector):
    """
    Connector for the Redshift
    """
    def connect(self, *args, **kwargs):
        self.engine = create_engine('redshift+postgresql://%s:%s@%s:%s/%s'%(self.username, self.password, self.host, self.port, self.db))
        return True
    
    def execute(self, *args, **kwargs):
        assert "query" in kwargs, "Please provide the query name"
        self.data = pd.read_sql_query(kwargs['query'],con = self.engine)
        return self

class ElasticSearchConnector(BaseConnector):
    """
    Connector for the ElasticSearch
    """
    def connect(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        assert "query" in kwargs, "Please provide the query name"
        self.data = pd.read_sql_query(kwargs['query'],con = self.engine)
        return self

