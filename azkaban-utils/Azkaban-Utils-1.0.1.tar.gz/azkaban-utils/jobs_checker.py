#Created by Yitong Song in May, 2017
from job import *
from project_deployer import *
import sys
import os.path

#*****************************************************************************#
#Check if files all exist 									                  #
#@params:                                                                     #
#   - jobs: the jobs in the Project object                                    #
#@return: 																	  #
#	- ok: whether the files all exist		              					  #
#*****************************************************************************#
def files_all_exist(jobs):
	ok = 1
	handle_missing_file = lambda file, name : sys.stderr.write("Missing " + file + " in job " + name + " .\n")
		
	for job in jobs:
		working_dir = job.options['working.dir']
		llist = ["command", "command.1", "command.2", "command.3", "command.4"]
		cmds = {}
		for cmd in llist:
			if cmd in job.options.keys():
				cmds[cmd] = job.options[cmd]
				fields = cmds[cmd].split(" ")
				
				if len(fields) < 2:
					break
				if fields[0] == 'python':
					have_python_file = 0
					for field in fields:
						if field.endswith('py'):
							have_python_file = 1
							break
					if not have_python_file:
						handle_missing_file("python file", job.name) 
						ok = 0

				elif fields[0] == 'ruby':
					have_ruby_file = 0
					for field in fields:
						if field.endswith('rb'):
							have_ruby_file = 1
							break
					if not have_ruby_file:
						handle_missing_file('ruby file', job.name)
						ok = 0

				for field in fields:
					if field.endswith('.py') or field.endswith('.rb') or field.endswith('.sql'):
						file = working_dir + "/" + field
						if os.path.isfile(file):
							handle_missing_file(file, job.name)
							ok = 0
	if ok:
		print "Files all exist"
	return ok
				

#*****************************************************************************#
#Check if denpendencies exist 								                  #
#@params:                                                                     #
#   - jobs: the jobs in the Project object                                    #
#@return: 																	  #
#	- ok: whether the dependencies all exist                                  #
#*****************************************************************************#
def dependencies_all_exist(jobs):
	ok = 1
	handle_missing_file = lambda job, missed_job : sys.stderr.write("Missing dept[" + missed_job + "] in job " + job + " .\n")
	job_names = []
	
	
	for j in jobs:
		job_names.append(j.name)
	
	for job in jobs:
		if job.options["dependencies"] is None:
			break
		depends = job.options[dependencies]
		if not depends:
			continue
		else:
			break
		if not isinstance(depends, list):
			depends = [depends]
		for missed in (depends - job_names):
			handle_missing_file(job.name, missed)
			ok = 0
	if ok:
		print "Dependencies all exist"
	return ok
	


#*****************************************************************************#
#The wrapper function checking the file existence and dependencies	          #
#@params:                                                                     #
#   - jobs: the jobs in the Project object                                    #
#@return: None																  #
#*****************************************************************************#	
def flow_valid(jobs):
	if files_all_exist(jobs) and dependencies_all_exist(jobs):
		print "OK"
	else: 
		print "Error"
