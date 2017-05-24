#!/usr/bin/python
import re

regex_check = ['host_name', 'service_name', 'hostgroup_name', 'servicegroup_name', 'varname' 'hostgroup_name', 'servicegroup_name', 'contactgroup_name', 'varname', 'event_handler_command', 'checkcommand', 'timeperiod', 'checktimeperiod', 'plugin_output', 'file_name', 'notification_tp', 'delete', 'notification_number', 'status_code', 'return_code', 'options', 'start_time','end_time', 'notification_time', 'varvalue', 'checktime', 'fixed', 'checkattempts', 'checkinterval', 'value', 'sticky', 'notify', 'persistent', 'duration', 'trigger_id', 'downtime_id', 'comment_id', 'author', 'comment', 'event_handler_command', 'checkcommand', 'timeperiod', 'checktimeperiod', 'plugin_output', 'file_name', 'notification_tp', 'delete', 'notification_number', 'status_code', 'return_code', 'options', 'start_time', 'end_time', 'notification_time', 'varvalue', 'checktime', 'fixed', 'checkattempts', 'checkinterval', 'value', 'sticky', 'notify', 'persistent', 'duration', 'trigger_id', 'downtime_id', 'comment_id', 'author', 'comment']
email_check = ['contactgroup_name','contact_name']
end_time_check = ['end_time']

def check_regex(template_arg, input_arg):
    """
    validates the input arguments against those of template file through regex check
    """
    ReturnValue = ""
    if (template_arg in email_check):
        match = re.match(r'[\w.-]+@[\w.-]+\.\w+', input_arg)
        if not match:
            return False
    if (template_arg in regex_check):
        datatype_Dict = {'timeperiod' : 1, 'checktimeperiod' : 1, 'notification_tp' : 1, 'delete' : 1, 'notification_number' : 1, 'status_code' : 1, 'return_code' : 1, 'options' : 1, 'start_time' : 1, 'end_time' : 1, 'notification_time' : 1, 'varvalue' : 1, 'checktime' : 1, 'fixed' : 1, 'checkattempts' : 1, 'checkinterval' : 1, 'value' : 1, 'sticky' : 1, 'notify' : 1, 'persistent' : 1, 'duration' : 1, 'host_name' : 'string', 'service_name' : 'string', 'contact_name' : 'string', 'hostgroup_name' : 'string', 'servicegroup_name' : 'string', 'contactgroup_name' : 'string', 'varname' : 'string', 'event_handler_command' : 'string', 'checkcommand' : 'string', 'plugin_output' : 'string', 'file_name' : 'string', 'trigger_id' : 'string', 'downtime_id' : 'string', 'comment_id' : 'string', 'author' : 'string', 'comment' : 'string'}    
        if type(datatype_Dict[template_arg]) == type(1):
            match = re.match(r'\d{1,20}', input_arg)
            if not match:
               return False
        if type(datatype_Dict[template_arg]) == type('string'):
            match = re.match(r'\w{1,30}', input_arg)
            if not match:
               return False
    return True

def validate_endtime(template_arg,start_time, input_arg):
    """
    checks if end_time is greater than start_time
    """
    regex_endtime = check_regex(template_arg, input_arg)
    if regex_endtime == False:
        return False
    regex_starttime = check_regex("start_time", start_time)
    if regex_starttime == False:
        return False
    if int(input_arg) < int(start_time):
        return False
    return True
