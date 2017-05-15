#!/usr/bin/python3
# encoding: utf-8
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

class Kafka():
	def __init__(self, bootstrap_servers, kafkatopic):
		self.bootstrap_servers = bootstrap_servers
		self.kafkatopic = kafkatopic
		self.groupid = kafkatopic
		self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid, bootstrap_servers = self.bootstrap_servers)

	def consume_data(self):
		try:
			for message in self.consumer:
				# print json.loads(message.value)
				yield message
		except KeyboardInterrupt as e:
			print(e)

	def topics(self):
		try:
			for message in self.consumer:
				# print json.loads(message.value)
				yield message
		except KeyboardInterrupt as e:
			print(e)

	def sendjsondata(self, params):
		try:
			parmas_message = json.dumps(params)
			producer = self.producer
			producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
			producer.flush()
		except KafkaError as e:
			print(e)
