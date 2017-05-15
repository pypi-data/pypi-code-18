#!/usr/bin/python3
# encoding: utf-8
import uuid

class Alert():
	def __init__(self, atype):
		self.atype=atype
		self.alertId=uuid.uuid4()

	def getAlertId(self):
		return(self.alertId)

	def alertIt(self):
		print("ALERT: "+self.atype,self.alertId)
