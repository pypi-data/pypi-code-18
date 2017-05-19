# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-06 23:10:19
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-12 17:14:15
import requests

from exceptions import APIException
from six.moves.urllib.parse import urlparse

class HTTPClient(requests.Session):
	def __init__(self, base_url, **kwargs):
		super(HTTPClient, self).__init__()

		self.base_url = base_url
		# Authentication self.auth_token = kwargs.get('auth_token')
		self.api_version = kwargs.get('api_version')
		# self.connection_params = kwargs.get('connection_params')

	def _get(self, url, **kwargs):
		return self.get(self._url(url), **kwargs)
		
	def _post(self, url, **kwargs):
		return self.post(self._url(url), **kwargs)

	def _put(self, url, **kwargs):
		return self.put(self._url(url), **kwargs)

	def _patch(self, url, **kwargs):
		return self.patch(self._url(url), **kwargs)

	def _delete(self, url, **kwargs):
		return self.delete(self._url(url), **kwargs)

	def _raise_for_status(self, response):
		'''
			To be completed: Error and Exception Class
		'''
		try:
			response.raise_for_status()
		except request.exceptions.HTTPError as e:
			# if e.response.status_code == 404:
			# 	raise NotFoundError(e, response)
			raise APIException(e, response)

	def get_kwargs(self, **kwargs):
		'''
			Create a full URL to request based on arguments.
		'''
		pass

	def _url(self, url, version=None):
		if version:
			return '{0}/v{1}{2}'.format(
				self.base_url, version, url
			)
		else:
			return '{0}{1}'.format(self.base_url, url)

	def api_version(self):
		return self.api_version
