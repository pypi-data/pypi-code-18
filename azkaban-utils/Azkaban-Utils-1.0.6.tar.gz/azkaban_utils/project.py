
#Created by Yitong Song in May, 2017
#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import yaml
import sys
import os
import job
from project_deployer import deploy
from azkaban_util import *
from project import *
from jobs_checker import *


class Project:
	#*************************************************************************#
    #Constructor for Project Class                                            #
    #@params:                                                                 #
    #   - self: the Project class project                                     #
    #	- file: the .yaml file with data needed                               #
    #@return: None                                                            #
    #*************************************************************************#
	def __init__(self, file):
		f = open(file)
		conf = yaml.load(f)
		self.host = conf['azkaban']['host']
		self.user = conf['azkaban']['user']
		self.password = conf['azkaban']['password']
		f.close()

	#getters
	def getName(self):
		return self.name

	def getProperty(self):
		return self.property

	def getHost(self):
		return self.host

	def getUser(self):
		return self.user

	def getPassword(self):
		return self.password

	def getJobs(self):
		return self.jobs

	def getSchedules(self):
		return self.schedules 

	#*************************************************************************#
    #Split jobs based on their azkaban flows.                                 #
    #The first job is always the flow's name (last job of the flow).          #
    #@params:                                                                 #
    #   - self: the Project class project                                     #
    #	- file: the .yaml file with data needed                               #
    #@return: None                                                            #
    #*************************************************************************#
	def load_jobs_from_file(self, file):
		f = open(file)
		conf = yaml.load(f)
		self.name = conf['project']['name']
		self.property = {"azkaban.user.home" : ""}
		if 'user_home' in conf['project']:
			self.property["azkaban.user.home"] = conf['project']['user_home']
		
		self.working_dir = conf['project']['azkaban_working_dir']
		self.job_working_dir = conf['project']['job_working_dir']
		self.user_to_proxy = conf['project']['user_to_proxy']
		self.jobs = []
		self.schedules = []
		

		for workflow in conf['workflows']:
			schedule_conf = workflow['schedule']
			flow_name = None
			for job in workflow['jobs']:
				params = {
					"working.dir" : self.working_dir, 
					"user.to.proxy": self.user_to_proxy,
					"failure.emails": "" if schedule_conf == None else schedule_conf['failure_emails'],
					"success.emails": "" if schedule_conf == None else schedule_conf['success_emails'],
					'command' : "bash -c 'cd " + self.job_working_dir + " && " + job['command'] + "'",
					'dependencies' : None if job['dependencies'] == None else job['dependencies'],
				}
				flow_name = job['name']
				# initialize a new job and add it to the "jobs" list
				self.jobs.append(Job(job['name'], params)) 
			if schedule_conf:
				#initialize a new schedule coresponding to the new job and add it to the "schedules" list
				new_schedule = {
					'project_name' : conf['project']['name'],
					'flow_name' : flow_name,
					'cron_expression' : schedule_conf['cron_expression']
				}
				self.schedules.append(new_schedule)
		
		f.close()
		return

	
	#*************************************************************************#
    #Check whether the files in jobs are valid.                               #
    #@params:                                                                 #
    #   - home_dir: the home directory                                        #
    #@return: None                                                            #
    #*************************************************************************#
	def is_valid(self, home_dir):
		if home_dir:
			params = {'home_dir' : home_dir}
		flow_valid(self.jobs)
		return

def usage():
	print "Wrong Usage! Please see https://xiaohongshu.quip.com/HsImAChwIa8z for usage."

def main():
	index = len(sys.argv)
	if sys.argv[index-1] == "-c":
		print "Establishing new project"
		new_project = Project(sys.argv[1])
		new_project.load_jobs_from_file(sys.argv[1])
		print "Checking new project directory valid or not..."
		new_project.is_valid(os.environ["HOME"])
		exit(0)	

	file = ""
	for arg in sys.argv:
		if "yaml" in arg:
			file = arg


	project = Project(file)
	project.load_jobs_from_file(file)
	if sys.argv[1] == "upload":
		deploy(project)
	elif sys.argv[1] == "schedule":
		schedule(project)
	elif sys.argv[1] == "execute":
		execute(project, {})
	elif sys.argv[1] == "kill":
		exec_id = sys.argv[2]
		kill(project, exec_id)
	elif sys.argv[1] == "info":
		exec_id = sys.argv[2]
		info(project, exec_id)
	elif sys.argv[1] == "fetch":
		exec_id = sys.argv[2]
		num = sys.argv[3]
		fetch(project, exec_id, num)
	else:
		usage()

	
	





