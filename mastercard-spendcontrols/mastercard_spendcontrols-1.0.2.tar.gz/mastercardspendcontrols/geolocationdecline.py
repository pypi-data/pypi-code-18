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

class Geolocationdecline(BaseObject):
	"""
	
	"""

	__config = {
		
		"9b0a8aaa-c15f-4fb1-9eed-adbcd23ec509" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/geolocations", "delete", [], []),
		
		"5bbf4ed2-322d-4369-8eac-b7bbdb2f3659" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/geolocations", "query", [], []),
		
		"4cb10d5f-694e-48ba-9d99-a99b1a208482" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/geolocations", "create", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUI)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())





	@classmethod
	def deleteById(cls,id,map=None):
		"""
		Delete object of type Geolocationdecline by id

		@param str id
		@return Geolocationdecline of the response of the deleted instance.
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

		return BaseObject.execute("9b0a8aaa-c15f-4fb1-9eed-adbcd23ec509", Geolocationdecline(mapObj))

	def delete(self):
		"""
		Delete object of type Geolocationdecline

		@return Geolocationdecline of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("9b0a8aaa-c15f-4fb1-9eed-adbcd23ec509", self)








	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Geolocationdecline by id and optional criteria
		@param type criteria
		@return Geolocationdecline object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("5bbf4ed2-322d-4369-8eac-b7bbdb2f3659", Geolocationdecline(criteria))

	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Geolocationdecline

		@param Dict mapObj, containing the required parameters to create a new object
		@return Geolocationdecline of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("4cb10d5f-694e-48ba-9d99-a99b1a208482", Geolocationdecline(mapObj))







