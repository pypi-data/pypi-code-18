# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-11 16:03:31
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-12 17:13:25

import requests

class APIException(requests.exceptions.HTTPError):

	def __init__(self, message, response):
		super(APIException, self).__init__(message)
		self.code = response.status_code
		self.response = response

class NotFoundException(APIException):
	pass