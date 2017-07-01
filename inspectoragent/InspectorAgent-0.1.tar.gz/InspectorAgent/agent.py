import __main__
import requests
import paramiko
import json

# Maybe required to install request and paramiko with:
# pip install requests
# pip install paramiko

hostInspector = ''
scriptName = ''
entity = []
envent = []

def fakeName(name):
    global scriptName
    scriptName = name

def startAssertion(host):
	if str(type(host))=="<type 'str'>":
	    global scriptName, envent, entity, hostInspector
	    if __main__.__file__[-4:] == '.pyc':
	        scriptName = __main__.__file__[:-4]
	    elif __main__.__file__[-3:] == '.py':
	        scriptName = __main__.__file__[:-3]
	    else:
	  	    scriptName = ''
	    entity = []
	    envent = []
	    hostInspector = host

def assertMetric(metric, result, addedInfo):
    if scriptName!= '' and str(type(metric))=="<type 'str'>"  and \
                           str(type(result))=="<type 'bool'>" and \
                           str(type(addedInfo))=="<type 'str'>":
    	global entity
    	assertedData = {}
    	assertedData['key'] = metric
    	assertedData['value'] = result
    	assertedData['info'] = addedInfo
    	entity.append(assertedData)

def envFreeMemory(envName, username, password, addedInfo):
    if scriptName!= '' and str(type(envName))=="<type 'str'>" and \
                           str(type(addedInfo))=="<type 'str'>":

        # will get env free memory here
        freeMemory = getEnvFreeMemory(envName, username, password)

        global envent
        envMemoryData = {}
        envMemoryData['free'] = freeMemory
        envMemoryData['env'] = envName
        envMemoryData['info'] = addedInfo
        envent.append(envMemoryData)

def finishAssertion():
    global scriptName, envent, entity, hostInspector
    if scriptName!= '':
	    _scriptName = scriptName
	    _envent = envent
	    _entity = entity
	    _hostInspector = hostInspector

	    hostInspector = ''
	    scriptName = ''
	    entity = []
	    envent = []

	    url = 'http://' + _hostInspector + '/submit'
	    values = {
	        "pyscript" : _scriptName,
	        "entity" : _entity,
	        "envent" : _envent}
	    r = requests.post(url, data=json.dumps(values), timeout=1)
	    print(r.status_code, r.reason)

def getEnvFreeMemory(server, username, password):
    freeMemory = 0
    cmd_to_execute = 'cat /proc/meminfo | grep MemFree'
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password, timeout=5)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    cmdOutput = ssh_stdout.readlines()[0].split(' ')
    ssh.close()
    strFree = cmdOutput[len(cmdOutput)-2]
    freeMemory = float(strFree)
    return freeMemory
