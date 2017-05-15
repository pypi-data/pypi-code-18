#!/usr/bin/python3
# encoding: utf-8
import re
from .Alert import Alert
from ..Tools.Es import Es
from ..Tools.Kafka import Kafka
from .Monitor import Monitor

class LogMonitor(Monitor):
	def __init__(self, conf_data):
		self.conf_data= conf_data
		self.kafka_server=conf_data['kafka_server']
		self.es_server=conf_data['es_server']
		self.topic=conf_data['topic']
		self.log_regex=conf_data['log_regex']
		self.host_regex=conf_data['host_regex']
		self.file_regex=conf_data['file_regex']
		self.max_count=int(conf_data['max_count'])
		self.output=conf_data['output']
		self.atype=conf_data['atype']
		self.message=[]

		self.es=Es(self.es_server)
		consumer = Kafka(self.kafka_server, self.topic)
		self.message = consumer.consume_data()

	def runMonitor(self):
		regex = re.compile(self.host_regex+'.*'+self.file_regex+'.*'+self.log_regex)
		array=[]
		j=0
	
		for i in self.message:
			data=i.value.decode("utf-8")
			if(regex.search(data) != None):
				j+=1
				tmpdata=re.split(' ',data)
				array.append([tmpdata[0],tmpdata[1],data])
				if(j==self.max_count):
					alert_inst=Alert(atype=self.atype)
					alert_id=alert_inst.getAlertId()
					alert_inst.alertIt()
					index_name='alert-'+self.atype
					for xxx in array:
						self.es.createData(index_name=index_name,body={'ip':xxx[0], 'file-source':xxx[1], 'alert_id':alert_id, 'message':xxx[2]})
	
					alert_id=''
					array=[]
					j=0
	
	
