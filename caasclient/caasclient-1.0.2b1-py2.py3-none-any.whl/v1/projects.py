# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-07 22:50:49
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-10 17:20:21

from caasclient.v1 import base

class Project(base.ApiObject):
	resource_name = 'project'

class ProjectManager(base.Manager):
    """Project Manager for CAAS Service API
        :method create: Create a project based on template
    	:method delete: Delete a project
        :method scale: Scale a project
        :method start: Run a project
        :method stop: Stop a project
    	:method list: List specified projects
    	:method inspect: Get a project info
		To be added [template_related_method]
    """

    api_name = "projects"
    resource_class = Project

    def create(self, **kwargs):
        return self.api._post('/projects', **kwargs)

   	def delete(self, p_id):
   		return self.api._delete('/projects/%s' % p_id)

    def scale(self, p_id):
        return self.api._patch('/projects/%s' % p_id)

    def start(self, p_id):
        return self.api._post('/projects/%s/start' % p_id)

    def stop(self, p_id):
        return self.api._post('/projects/%s/stop' % p_id)

    def list(self, p_id, filter=None, limit=None):
        return self.api._get('/projects')

    def inspect(self, p_id):
        return self.api._get('/projects/%s' % p_id)