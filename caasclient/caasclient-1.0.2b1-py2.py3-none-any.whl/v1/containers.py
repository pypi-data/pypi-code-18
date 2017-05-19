# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-07 22:51:03
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-10 17:20:24

from caasclient.v1 import base

class Container(base.ApiObject):
    resource_name = 'container'

class ContainerManager(base.Manager):
    """Container Manager for CAAS Service API
        :method create: Create a container from a image
        :method start: Start a container
        :method stop: Stop a container
    	:method delete: Delete a container
    	:method list: List specified containers
    	:method inspect: Get an container object
        :method commit: 
        :method logs: show the log of a container
        To be added:[version related]
    """
    api_name = "containers"
    resource_class = Container

    def create(self, **kwargs):
        return self.api._post('/containers/create/', **kwargs)

    def start(self, c_id):
        return self.api._post('/container/%s/stop' % c_id)
        
    def stop(self, c_id):
        return self.api._post('/container/%s/start' % c_id)
    
    def delete(self, c_id):
        return self.api._delete('/containers/%s' % c_id)

    def list(self, filter=None, limit=None):
        return self.api._get('/containers')

    def inspect(self, c_id):
        return self.api._get('containers/%s' % c_id)

