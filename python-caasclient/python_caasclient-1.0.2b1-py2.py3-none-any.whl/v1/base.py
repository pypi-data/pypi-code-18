# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-07 22:29:31
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-10 17:19:37
"""
	Base Class for ApiObjects and Manager
	* Formatting the request and response data
	* Construct the request url
"""

class ApiObject(object):

	def __init__(self, manager, data):
		self.manager = manager
		self.data = data
		self.set_data(data)

	def set_data(data):
		pass

class Manager(object):
	
	def __init__(self,api):
		self.api = api

	def _path(self, url, version=None):
		return '/%s/%s' % {self.api_name, url}

	def _list(self, url ,limit=None):
		resp = self.api._get(url)
		self.api._raise_for_status(resp)
		return [self.resource_class(self, res)
				for res in resp.json()]

	def _get(self, url):
		resp = self.api._get(url)
		self.api._raise_for_status(resp)
		data = resp.json() #TODO: If cannot be decoded 
		return self.resource_class(self, data)
		# return a resource object

	def _post(self, url, data):
		resp = self.api._post(url, {'data': data}) #{'json': data}
		self.api._raise_for_status(resp)
		return resp.status_code

	def _update(self, url):
		resp = self.api._patch(url)
		self.api._raise_for_status(resp)
		return resp.status_code
		
	def _delete(self, url):
		resp = self.api._delete(url)
		if resp.status_code != 204:
			self.api._raise_for_status(resp)
		return resp.status_code


	
