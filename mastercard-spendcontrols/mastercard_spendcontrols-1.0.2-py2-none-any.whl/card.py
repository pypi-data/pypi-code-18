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
		
		"e816c724-d1bf-4be5-b8a2-b5f819324431" : OperationConfig("/issuer/spendcontrols/v1/card", "create", [], []),
		
		"b5781aee-13fc-46a9-b8c3-265bb53ea2c6" : OperationConfig("/issuer/spendcontrols/v1/card/uuid", "create", [], []),
		
		"d18e32b0-557a-440b-af7f-cdca63a1557b" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}", "delete", [], []),
		
		"e8af20fa-8d2e-4415-bda1-f90e79d75642" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}", "create", [], []),
		
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
		return BaseObject.execute("e816c724-d1bf-4be5-b8a2-b5f819324431", Card(mapObj))






	@classmethod
	def read(cls,mapObj):
		"""
		Creates object of type Card

		@param Dict mapObj, containing the required parameters to create a new object
		@return Card of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("b5781aee-13fc-46a9-b8c3-265bb53ea2c6", Card(mapObj))









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

		return BaseObject.execute("d18e32b0-557a-440b-af7f-cdca63a1557b", Card(mapObj))

	def delete(self):
		"""
		Delete object of type Card

		@return Card of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("d18e32b0-557a-440b-af7f-cdca63a1557b", self)



	@classmethod
	def update(cls,mapObj):
		"""
		Creates object of type Card

		@param Dict mapObj, containing the required parameters to create a new object
		@return Card of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("e8af20fa-8d2e-4415-bda1-f90e79d75642", Card(mapObj))







