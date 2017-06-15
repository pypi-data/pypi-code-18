#Created by Yitong Song in May, 2017
#coding:utf-8
#!/usr/bin/python

import json
import time
import urllib2
import urllib
import requests
import cookielib
import os.path
import commands
#import datetime
import logging

class AzkabanUtil:
    #*************************************************************************#
    #Constructor for Class AzkabanUtil                                        #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - host: azkaban web serverhost                                        #
    #   - username: azkaban login azkaban_username                            #
    #   - password: azkaban login azkaban_password                            #
    #@return: None                                                            #
    #*************************************************************************#
    def __init__(self, host, username, password):
        self.azkaban_host = host
        self.azkaban_username = username
        self.azkaban_password = password


    #*************************************************************************#
    #Login to Azkaban web app and upload a project zip file                   #
    #more details on official documentation                                   #
    #http://azkaban.github.io/azkaban/docs/latest/#api-upload-a-project-zip   #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of azkaban project                           #
    #   - file: the zip file created to be uploaded, more requirements about  #
    #the zip file please see http://azkaban.github.io/docs/2.5/#upload-project#
    #@return: None                                                            #
    #*************************************************************************#
    def upload_a_project_zip(self, project_name, file):
        session_id = self.get_session_id(self.azkaban_username, 
        								 self.azkaban_password)
        url = "%s/manager"%(self.azkaban_host)
        command = '''curl -k -i -H "Content-Type: multipart/mixed" -X POST --form 'session.id=%s' --form 'ajax=upload' --form 'file=@%s;type=application/zip' --form 'project=%s' %s''' % (session_id,file,project_name,url)
        print '>>>>',command
        status,result = commands.getstatusoutput(command) #used for debugging
       	print ""
        return


    #*************************************************************************#
    #This API call schedules a flow by a cron Expression.                     #
    #more details on official documentation                                   #
    #http://azkaban.github.io/azkaban/docs/latest/#api-flexible-schedule      #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of the project.                              #
    #   - flow_name: the name of the flow   								  #
    #	- cron_expression: A CRON expression is a string comprising 6 or 7    #
    #fields separated by white space that represents a set of times.In azkaban#
    #we use Quartz Cron Format.                                               #
    #@return: None                                                            #
    #*************************************************************************#
    def schedule_flow(self, project_name, flow_name, cron_expression):
        session = self.get_session(project_name)
        url = "%s/schedule"%(self.azkaban_host)
        payload = {
            "ajax"                  : "scheduleCronFlow",
            "projectName"           : project_name,
            "flow"                  : flow_name,
            "cronExpression"        : cron_expression
        }        
        resp = session.post(url, data = payload)
        print(resp.text)
        return
        

    #*************************************************************************#
    #This API executes a flow via an ajax call, supporting a rich selection of#
    #different options. Running an individual job can also be achieved via    #
    #this API by disabling all other jobs in the same flow.                   #
    #More details on official documentation                                   #
    #http://azkaban.github.io/azkaban/docs/latest/#api-execute-a-flow         #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of the project.                              #
    #   - flow_name: the name of the flow   								  #
    #   - params: customized params, will replace the existed payload         #
    #@return: None                                                            #
    #*************************************************************************#
    def execute_a_flow(self, project_name, flow_name, params):
        session = self.get_session(project_name)
        url = "%s/executor"%(self.azkaban_host)
        payload = {
            "ajax"                  : "executeFlow",
            "project"               : project_name,
            "flow"                  : flow_name,
            "disabled"              : "[]",
            "failureEmailsOverride" : "false",
            "successEmailsOverride" : "false",
            "failureAction"         : "finishPossible",
            "notifyFailureFirst"    : "false",
            "notifyFailureLast"     : "false",
            "concurrentOption"      : "ignore"   
        }

        for k,v in params:
            payload[k] = v

        resp = session.post(url, data = payload)
        print(resp.text)
        return

    #*************************************************************************#
    #Given an execution id, this API call cancels a running flow. If the flow #
    #is not running, it will return an error message.                         #
    #More details on official documentation                                   #
    #http://azkaban.github.io/azkaban/docs/latest/#api-cancel-a-flow-execution#
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of the project.                              #     #
    #   - execid: the execution id                                            #
    #@return: None                                                            #
    #*************************************************************************#
    def cancel_a_flow_execution(self, project_name, exec_id):
        session = self.get_session(project_name)
        url = "%s/executor"%(self.azkaban_host)
        payload = {
            "ajax"      : "cancelFlow",
            "execid"    : exec_id
        }
        resp = session.post(url, data = payload)
        print(resp.text)
        return


    #*************************************************************************#
    #Given an execution id, this API call fetches all the detailed information#
    #of that execution, including a list of all the job executions.           #
    #More details on official documentation                                   #
    #http://azkaban.github.io/azkaban/docs/latest/#api-fetch-a-flow-execution #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - execid: the execution id                                            #
    #@return: None                                                            #
    #*************************************************************************#
    def fetch_a_flow_execution(self, project_name, exec_id):
        session = self.get_session(project_name)
        url = "%s/executor"%(self.azkaban_host)
        payload = {
            "ajax"      : "fetchexecflow",
            "execid"    : exec_id
        }
        resp = session.post(url, data = payload)
        print(resp.text)
        return


    #*************************************************************************#
    #Given a project name, and a certain flow, this API call provides a list  #
    #of corresponding executions. Those executions are sorted in descendent   #
    #submit time order. Also parameters are expected to specify the start     #
    #index and the length of the list. This is originally used to handle      #
    #pagination.															  #
    #More details on official documentation: http://azkaban.github.io/azkaban/#
    #docs/latest/#api-fetch-executions-of-a-flow  							  #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of the project.                              #
    #   - flow_name: the name of the flow                                     #
    # 	- num: the max length of the returned list		                      #
    #@return: None                                                            #
    #*************************************************************************#
    def fetch_executions_of_a_flow(self, project_name,flow_name, num): # latest
        session = self.get_session(project_name)
        url = "%s/manager"%(self.azkaban_host)
        payload = {
            "ajax"      : "fetchFlowExecutions",
            "flow"      : flow_name,
            "start"     : 0, 
            "length"    : num,
            "project"   : project_name,
        }
        resp = session.post(url, data = payload)
        print(resp.text)
        return


    #helper
    #*************************************************************************#
    #Build up a session and log in                                            #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - username: azkaban login azkaban_username                            #
    #   - password: azkaban login azkaban_password                            #
    #@return:   															  #
    #	- the newly-created session id                                        #
    #*************************************************************************#
    def get_session_id(self, username, password):
        url = self.azkaban_host
        params = {}
        params['action'] = 'login'
        params['username']= username
        params['password']= password
        data = urllib.urlencode(params) 
        req = urllib2.Request(url,data)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        obj = json.loads(res)

        return  obj['session.id']

    #*************************************************************************#
    #Build up a session and log in                                            #
    #@params:                                                                 #
    #   - self: AzkabanUtil object                                            #
    #   - project_name: the name of the project.                              #
    #@return:                                                                 #
    #   - the newly-created session                                           #
    #*************************************************************************#
    def get_session(self, project_name):
        s = requests.Session()
        data = {
            'action' : 'login',
            'username' : self.azkaban_username,
            'password' : self.azkaban_password
        }
        url = self.azkaban_host
        s.get(url)
        res = s.post(url, data=data, json=None,)
        return s
        






