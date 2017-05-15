#!/usr/bin/python3
# encoding: utf-8
import re
from datetime import datetime
from elasticsearch import Elasticsearch

class Es():
	def __init__(self, es_server):
		(self.host,self.port)=re.split(':',es_server)
		self.es = Elasticsearch([{'host': self.host, 'port': self.port}])

	def createIndex(self, index_name, auto_date=True, ignore=400):
		if(auto_date):
			now = datetime.utcnow()
			index_name=str(index_name)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)
		self.es.indices.create(index=index_name, ignore=ignore)

	def createData(self, index_name, body, doc_type='logs', auto_date=True):
		if(auto_date):
			now = datetime.utcnow()
			index_name=str(index_name)+"-"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)
		time_body={"@timestamp": datetime.utcnow()}
		self.es.index(index=index_name, doc_type=doc_type, body=dict(time_body, **body))
