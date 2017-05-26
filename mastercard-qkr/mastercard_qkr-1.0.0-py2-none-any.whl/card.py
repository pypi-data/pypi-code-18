#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from resourceconfig import ResourceConfig

class Card(BaseObject):
	"""
	
	"""

	__config = {
		
		"cc220516-1929-41a0-aa64-fa822da6082e" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "create", ["X-Auth-Token"], []),
		
		"bc8e62ae-9c16-491d-a3f6-c8f9a886a567" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "delete", ["X-Auth-Token"], []),
		
		"38047ba3-2f9e-4cf1-a86c-48d1bae91dcc" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "query", ["X-Auth-Token"], []),
		
		"d61b1174-30cd-4965-a7df-b161c5606a60" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "update", ["X-Auth-Token"], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUI)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())


	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Card

		@param Dict mapObj, containing the required parameters to create a new object
		@return Card of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("cc220516-1929-41a0-aa64-fa822da6082e", Card(mapObj))









	@classmethod
	def deleteById(cls,id,map=None):
		"""
		Delete object of type Card by id

		@param str id
		@return Card of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""

		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if map:
			if (isinstance(map,RequestMap)):
				mapObj.setAll(map.getObject())
			else:
				mapObj.setAll(map)

		return BaseObject.execute("bc8e62ae-9c16-491d-a3f6-c8f9a886a567", Card(mapObj))

	def delete(self):
		"""
		Delete object of type Card

		@return Card of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("bc8e62ae-9c16-491d-a3f6-c8f9a886a567", self)








	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Card by id and optional criteria
		@param type criteria
		@return Card object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("38047ba3-2f9e-4cf1-a86c-48d1bae91dcc", Card(criteria))


	def update(self):
		"""
		Updates an object of type Card

		@return Card object representing the response.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("d61b1174-30cd-4965-a7df-b161c5606a60", self)






