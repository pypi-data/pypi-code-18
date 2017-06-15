#Created by Yitong Song in May, 2017
from job import * 
from azkaban_util import *
import job
import azkaban_util
import os
import tempfile
import os.path
import zipfile
import shutil

#*****************************************************************************#
#Constructor                                                                  #
#@params:                                                                     #
#   - self: the Project class project                                         #
#	- host: azkaban web server host                                           #
#@return: None                                                                #
#*****************************************************************************#
def __init__(self, host, username, password):
	self.azkaban_host = host
	self.azkaban_username = username
	self.azkaban_password = password


#*****************************************************************************#
#Merge the key and the value to a string in a certain form                    #
#@params:                                                                     #
#   - k: a key in a dict                                                      #
#	- v: a value in a dict                                                    #
#@return: 																	  #
#	- serialized: a string made up with k and v in a certain form             #
#*****************************************************************************#
def process_property(k,v):
		serialized = ""
		serialized = serialized + str(k) + "="
		if callable(v):  
			delimited = False
			for v_part in v:
				if delimited: 
					serialized = serialized + ","
				serialized += v_part
				delimited = True
		else:
			serialized += str(v)
		serialized += "\n"
		return serialized


#*****************************************************************************#
#Created the zip file and upload it.                                          #
#@params:                                                                     #
#   - project : the project needed to be handled                              #
#@return: None                                                                #
#*****************************************************************************#
def deploy(project):
	stg = tempfile.mkdtemp()
	to_zip = []
	print "staging job to" + str(stg)
	prop_file = stg + "/" + project.name + ".properties"
	f = open(prop_file, "w")

	for k in project.property.keys():
		if project.property[k] is None:
			f.write(process_property(k,''))
		else:
			f.write(process_property(k,project.property[k]))
	
	to_zip.append(prop_file)
	basename = os.path.basename(prop_file) #get the basename of the file
	print "created " + basename
	f.close()

	
	
	for job in project.jobs:
		job_file = stg + "/" + job.name + ".job"
		file = open(job_file, 'w')
		string = job.serialize()
		#print "string in the job_file:"
		#print string
		file.write(string)
		to_zip.append(job_file)
		basename = os.path.basename(job_file)
		print "created " + basename
		file.close()

	zip_file = stg + "/" 
	file_name = project.name + ".zip"
	zip_files(zip_file, to_zip, project.name)
	zip_file = zip_file + project.name + ".zip"
	print "created " + os.path.basename(zip_file)
	print zip_file

	

	azkUtil = AzkabanUtil(project.host, project.user, project.password)
	azkUtil.upload_a_project_zip(project.name, zip_file)
	print "uploaded to project %s" % project.name

	#shutil.rmtree(stg) #remove the temp file

	print "clean up"
	print "done!"
	return


#*****************************************************************************#
#Schedule a workflow using helper function                                    #
#@params:                                                                     #
#   - project : the project needed to be handled                              #
#@return: None                                                                #
#*****************************************************************************#
def schedule(project):
	for sch in project.schedules:
		project_name = sch['project_name']
		flow_name = sch['flow_name']
		if 'cron_expression' not in sch.keys():
			print "Error: no schedule in *.yaml"
			exit(0)
		cron_expression = sch['cron_expression']
		azkUtil = AzkabanUtil(project.host, project.user, project.password)
		azkUtil.schedule_flow(project_name, flow_name, cron_expression)
		
		
		
		
def execute(project, params):
	for sch in project.schedules:
		project_name = sch['project_name']
		flow_name = sch['flow_name']
		azkUtil = AzkabanUtil(project.host, project.user, project.password)
		azkUtil.execute_a_flow(project_name, flow_name, params)


def kill(project, exec_id):
	for sch in project.schedules:
		project_name = sch['project_name']
		flow_name = sch['flow_name']
		azkUtil = AzkabanUtil(project.host, project.user, project.password)
		azkUtil.cancel_a_flow_execution(project_name, exec_id)


def info(project, exec_id):
	for sch in project.schedules:
		project_name = sch['project_name']
		flow_name = sch['flow_name']
		azkUtil = AzkabanUtil(project.host, project.user, project.password)
		azkUtil.fetch_a_flow_execution(project_name, exec_id)


def fetch(project, exec_id, num):
	for sch in project.schedules:
		project_name = sch['project_name']
		flow_name = sch['flow_name']
		azkUtil = AzkabanUtil(project.host, project.user, project.password)
		azkUtil.fetch_executions_of_a_flow(project_name, flow_name, num)




#*****************************************************************************#
#Generate a zip file with given sources                                       #
#@params:                                                                     #
#   - dest: the path where the new zip file will be created                   #
#	- sources: the given files needed to be compressed                        #
#	- name: the name of the newly-created zip file                            #
#@return: None                                                                #
#*****************************************************************************#
def zip_files(dest, sources, name):
	name += ".zip"
	os.chdir(dest)
	zipFile = zipfile.ZipFile(name,'w',)
	for tz in sources:
		zipFile.write(tz)

	zipFile.close()



	